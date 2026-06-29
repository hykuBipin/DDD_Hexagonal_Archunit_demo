package com.ordertogether.service;

import com.ordertogether.client.SwiggyMcpClient;
import com.ordertogether.dto.MatchRequest;
import com.ordertogether.dto.MatchResponse;
import com.ordertogether.dto.MatchedRestaurant;
import com.ordertogether.model.Restaurant;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Finds restaurants that simultaneously satisfy every diner's dish preference.
 *
 * <p><b>Algorithm</b>
 * <ol>
 *   <li>Fan out one {@code search_restaurants} call per preference in parallel → build a
 *       <em>union</em> pool of all returned restaurants (deduped by id).</li>
 *   <li>For every restaurant in the pool, call {@code get_restaurant_menu} in parallel
 *       (up to {@value #MENU_CONCURRENCY} concurrent requests).</li>
 *   <li>Keep only restaurants whose menu contains <em>all</em> preferences
 *       (case-insensitive substring match on item name + description).</li>
 *   <li>Rank: open restaurants first; closed ones kept but sorted to the bottom.
 *       Within each group, restaurants that appeared in more original search results first
 *       (higher search-hit count = stronger relevance signal), then {@code avgRating}
 *       descending, then {@code deliveryTimeMinutes} ascending.</li>
 * </ol>
 */
@Service
public class RestaurantMatchService {

	private static final Logger log = LoggerFactory.getLogger(RestaurantMatchService.class);

	/** Max parallel menu-fetch calls. Keeps request rate reasonable. */
	private static final int MENU_CONCURRENCY = 15;

	/** Results per search page (Swiggy default). */
	private static final int SEARCH_PAGE_SIZE = 10;
	/** Max pages to fetch per preference — gives up to 30 candidates per dish. */
	private static final int SEARCH_MAX_PAGES = 3;

	private final SwiggyMcpClient mcpClient;

	public RestaurantMatchService(SwiggyMcpClient mcpClient) {
		this.mcpClient = mcpClient;
	}

	public Mono<MatchResponse> match(MatchRequest request, String bearer) {
		List<String> preferences = dedupe(request.preferences());
		if (preferences.isEmpty()) {
			return Mono.just(new MatchResponse(List.of(), 0, List.of()));
		}

		// Step 1 — fan out searches in parallel; each preference fetches up to SEARCH_MAX_PAGES.
		return Flux.fromIterable(preferences)
				.flatMap(pref -> fetchSearchPages(pref, request.addressId(), bearer, 0, new ArrayList<>())
						.map(list -> new PreferenceResult(pref, list)))
				.collectList()
				.flatMap(perPreference -> verifyByMenu(preferences, perPreference, request.addressId(), bearer));
	}

	/**
	 * Fetches search results for {@code pref} across pages until a page returns fewer than
	 * {@value #SEARCH_PAGE_SIZE} results (last page) or {@value #SEARCH_MAX_PAGES} pages
	 * have been fetched (cap = 30 candidates per preference).
	 */
	private Mono<List<Restaurant>> fetchSearchPages(
			String pref, String addressId, String bearer, int pageNum, List<Restaurant> acc) {
		int offset = pageNum * SEARCH_PAGE_SIZE;
		return mcpClient.searchRestaurants(pref, addressId, bearer, offset)
				.flatMap(page -> {
					acc.addAll(page);
					boolean lastPage = page.size() < SEARCH_PAGE_SIZE || pageNum + 1 >= SEARCH_MAX_PAGES;
					log.debug("Search page {} for '{}': {} results (lastPage={})",
							pageNum + 1, pref, page.size(), lastPage);
					if (lastPage) {
						return Mono.just(new ArrayList<>(acc));
					}
					return fetchSearchPages(pref, addressId, bearer, pageNum + 1, acc);
				});
	}

	private Mono<MatchResponse> verifyByMenu(
			List<String> preferences,
			List<PreferenceResult> perPreference,
			String addressId,
			String bearer) {

		// Build the union pool. Track how many preferences each restaurant appeared in.
		Map<String, Restaurant> pool = new LinkedHashMap<>();
		Map<String, Integer> searchHitCount = new LinkedHashMap<>();

		for (PreferenceResult pr : perPreference) {
			for (Restaurant r : pr.restaurants()) {
				if (r.id() == null) {
					continue;
				}
				pool.merge(r.id(), r, RestaurantMatchService::mergePreferRicher);
				searchHitCount.merge(r.id(), 1, Integer::sum);
			}
		}

		log.info("Union pool size: {} restaurants for preferences {}", pool.size(), preferences);

		// Step 2 — parallel menu checks.
		return Flux.fromIterable(pool.entrySet())
				.flatMap(entry -> {
					String id = entry.getKey();
					Restaurant r = entry.getValue();
					return mcpClient.getMenuItemNames(id, addressId, bearer, preferences)
							.map(menuItems -> new MenuCheckResult(
									r,
									menuItems,
									searchHitCount.getOrDefault(id, 0)));
				}, MENU_CONCURRENCY)
				// Step 3 — keep only restaurants where every preference is found in the menu.
				.filter(result -> allPreferencesInMenu(preferences, result.menuItems()))
				// Step 4 — rank: open restaurants first, then by relevance.
				.sort(RANKING)
				.map(result -> MatchedRestaurant.from(result.restaurant(), preferences))
				.collectList()
				.map(matched -> {
					log.info("Matched {} restaurant(s) (incl. closed) after menu verification for {}",
							matched.size(), preferences);
					return new MatchResponse(preferences, matched.size(), matched);
				});
	}

	// --- matching helpers ---------------------------------------------------

	/** True when every preference has a case-insensitive substring match in the menu. */
	public static boolean allPreferencesInMenu(List<String> preferences, List<String> menuItems) {
		for (String pref : preferences) {
			String prefLower = pref.toLowerCase();
			boolean found = menuItems.stream()
					.anyMatch(item -> item.toLowerCase().contains(prefLower));
			if (!found) {
				return false;
			}
		}
		return true;
	}

	// Relevance within open/closed groups: searchHitCount desc → rating desc → ETA asc.
	private static final Comparator<MenuCheckResult> BY_RELEVANCE =
			Comparator.comparingInt(MenuCheckResult::searchHitCount).reversed()
					.thenComparing(
							r -> r.restaurant().avgRating(),
							Comparator.nullsLast(Comparator.reverseOrder()))
					.thenComparing(
							r -> r.restaurant().deliveryTimeMinutes(),
							Comparator.nullsLast(Comparator.naturalOrder()));

	// Open restaurants first, then BY_RELEVANCE within each group.
	private static final Comparator<MenuCheckResult> RANKING =
			Comparator.<MenuCheckResult>comparingInt(r -> r.restaurant().isOpen() ? 0 : 1)
					.thenComparing(BY_RELEVANCE);

	// --- shared helpers -----------------------------------------------------

	/** When the same restaurant appears in multiple searches, keep the more complete record. */
	private static Restaurant mergePreferRicher(Restaurant a, Restaurant b) {
		return nonNullCount(b) > nonNullCount(a) ? b : a;
	}

	private static int nonNullCount(Restaurant r) {
		int n = 0;
		if (r.name() != null) n++;
		if (r.avgRating() != null) n++;
		if (r.deliveryTimeMinutes() != null) n++;
		if (r.costForTwo() != null) n++;
		if (r.availabilityStatus() != null) n++;
		if (r.imageUrl() != null) n++;
		if (r.cuisines() != null && !r.cuisines().isEmpty()) n++;
		return n;
	}

	static List<String> dedupe(List<String> raw) {
		if (raw == null) {
			return List.of();
		}
		Map<String, String> seen = new LinkedHashMap<>();
		for (String p : raw) {
			if (p != null && !p.isBlank()) {
				seen.putIfAbsent(p.trim().toLowerCase(), p.trim());
			}
		}
		return new ArrayList<>(seen.values());
	}

	// --- internal records ---------------------------------------------------

	private record PreferenceResult(String preference, List<Restaurant> restaurants) {
	}

	record MenuCheckResult(Restaurant restaurant, List<String> menuItems, int searchHitCount) {
	}
}
