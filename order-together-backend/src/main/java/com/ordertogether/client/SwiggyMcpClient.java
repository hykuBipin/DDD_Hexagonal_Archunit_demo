package com.ordertogether.client;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.ordertogether.config.SwiggyProperties;
import com.ordertogether.model.Address;
import com.ordertogether.model.Restaurant;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Thin client over the Swiggy Builders Club MCP "food" server.
 *
 * <p>Speaks JSON-RPC 2.0 over HTTP (MCP Streamable HTTP transport). The server may answer
 * with either a single {@code application/json} body or a {@code text/event-stream} (SSE)
 * frame, so the response is read as raw text and parsed defensively.
 */
@Component
public class SwiggyMcpClient {

	private static final Logger log = LoggerFactory.getLogger(SwiggyMcpClient.class);

	private final WebClient webClient;
	private final SwiggyProperties props;
	private final ObjectMapper mapper;
	private final AtomicLong requestIds = new AtomicLong(1);

	/** Key: {@code restaurantId:page} — menus don't vary by delivery address. */
	private final Cache<String, MenuPage> menuPageCache = Caffeine.newBuilder()
			.expireAfterWrite(Duration.ofHours(3))
			.maximumSize(2000)
			.build();

	/** Key: {@code query:resolvedAddr:offset} — search results are location-sensitive. */
	private final Cache<String, List<Restaurant>> searchResultCache = Caffeine.newBuilder()
			.expireAfterWrite(Duration.ofMinutes(30))
			.maximumSize(500)
			.build();

	public SwiggyMcpClient(WebClient swiggyWebClient, SwiggyProperties props, ObjectMapper mapper) {
		this.webClient = swiggyWebClient;
		this.props = props;
		this.mapper = mapper;
	}

	static final int MENU_PAGE_SIZE = 8;
	static final int MENU_MAX_PAGES = 5;

	/**
	 * Fetches menu item text for a restaurant, paginating lazily until all
	 * {@code preferences} are found or there are no more pages (max {@value MENU_MAX_PAGES}).
	 *
	 * <p>Each page uses {@code pageSize=}{@value MENU_PAGE_SIZE}. Pages are fetched
	 * sequentially; fetching stops as soon as every preference has a match, so most
	 * restaurants only need 1–2 pages.
	 *
	 * @param restaurantId Swiggy restaurant id
	 * @param addressId    delivery address id (required by the tool)
	 * @param bearer       OAuth access token
	 * @param preferences  dish terms to match; used for early-exit only
	 * @return flat list of {@code "name description"} strings across fetched pages
	 */
	public Mono<List<String>> getMenuItemNames(
			String restaurantId, String addressId, String bearer, List<String> preferences) {
		String addr = (addressId == null || addressId.isBlank()) ? props.defaultAddressId() : addressId;
		return fetchMenuPages(restaurantId, addr, resolveToken(bearer), preferences, 1, new ArrayList<>());
	}

	private Mono<List<String>> fetchMenuPages(
			String restaurantId, String addr, String token,
			List<String> preferences, int page, List<String> accumulated) {

		return fetchSingleMenuPage(restaurantId, addr, token, page)
				.flatMap(result -> {
					accumulated.addAll(result.items());
					boolean allFound = allPreferencesFound(preferences, accumulated);
					if (allFound || !result.hasMore() || page >= MENU_MAX_PAGES) {
						log.debug("Menu fetch done for {} after {} page(s), allFound={}", restaurantId, page, allFound);
						return Mono.just(accumulated);
					}
					return fetchMenuPages(restaurantId, addr, token, preferences, page + 1, accumulated);
				});
	}

	private Mono<MenuPage> fetchSingleMenuPage(String restaurantId, String addr, String token, int page) {
		String cacheKey = restaurantId + ":" + page;
		MenuPage hit = menuPageCache.getIfPresent(cacheKey);
		if (hit != null) {
			log.debug("Menu cache hit: key={}", cacheKey);
			return Mono.just(hit);
		}

		Map<String, Object> body = Map.of(
				"jsonrpc", "2.0",
				"method", "tools/call",
				"params", Map.of(
						"name", "get_restaurant_menu",
						"arguments", Map.of(
								"restaurantId", restaurantId,
								"addressId", addr == null ? "" : addr,
								"page", page,
								"pageSize", MENU_PAGE_SIZE)),
				"id", requestIds.getAndIncrement());

		return webClient.post()
				.uri(props.foodPath())
				.headers(h -> {
					if (token != null && !token.isBlank()) {
						h.setBearerAuth(token);
					}
				})
				.contentType(MediaType.APPLICATION_JSON)
				.accept(MediaType.APPLICATION_JSON, MediaType.TEXT_EVENT_STREAM)
				.bodyValue(body)
				.retrieve()
				.bodyToMono(String.class)
				.map(raw -> parseMenuPage(raw, restaurantId, page))
				.doOnNext(result -> {
					if (!result.items().isEmpty()) {
						menuPageCache.put(cacheKey, result);
					}
				})
				.onErrorResume(e -> {
					log.warn("MCP get_restaurant_menu failed for id='{}' page={}: {}", restaurantId, page, e.toString());
					return Mono.just(MenuPage.EMPTY);
				});
	}

	MenuPage parseMenuPage(String rawBody, String restaurantId, int page) {
		try {
			JsonNode envelope = readJsonRpcEnvelope(rawBody);
			if (envelope.has("error") && !envelope.get("error").isNull()) {
				log.warn("MCP returned error for get_restaurant_menu id='{}' page={}: {}",
						restaurantId, page, envelope.get("error"));
				return MenuPage.EMPTY;
			}
			JsonNode structured = envelope.path("result").path("structuredContent");
			boolean hasMore = structured.path("hasMore").asBoolean(false);
			JsonNode categories = structured.path("categories");

			List<String> items = new ArrayList<>();
			if (categories.isArray()) {
				for (JsonNode category : categories) {
					JsonNode categoryItems = category.path("items");
					if (!categoryItems.isArray()) continue;
					for (JsonNode item : categoryItems) {
						String name = item.path("name").asText("").trim();
						String desc = item.path("description").asText("").trim();
						if (!name.isEmpty()) {
							items.add(desc.isEmpty() ? name : name + " " + desc);
						}
					}
				}
			}
			return new MenuPage(items, hasMore);
		}
		catch (Exception e) {
			log.warn("Failed to parse menu page for id='{}' page={}: {}", restaurantId, page, e.toString());
			return MenuPage.EMPTY;
		}
	}

	private static boolean allPreferencesFound(List<String> preferences, List<String> menuItems) {
		return preferences.stream().allMatch(pref -> {
			String lower = pref.toLowerCase();
			return menuItems.stream().anyMatch(item -> item.toLowerCase().contains(lower));
		});
	}

	record MenuPage(List<String> items, boolean hasMore) {
		static final MenuPage EMPTY = new MenuPage(List.of(), false);
	}

	/**
	 * Fetches all saved delivery addresses from the user's Swiggy account via the
	 * {@code get_addresses} MCP tool.
	 *
	 * @param bearer OAuth access token; falls back to the configured dev token when blank
	 */
	public Mono<List<Address>> getAddresses(String bearer) {
		String token = resolveToken(bearer);

		Map<String, Object> body = Map.of(
				"jsonrpc", "2.0",
				"method", "tools/call",
				"params", Map.of(
						"name", "get_addresses",
						"arguments", Map.of()),
				"id", requestIds.getAndIncrement());

		return webClient.post()
				.uri(props.foodPath())
				.headers(h -> {
					if (token != null && !token.isBlank()) {
						h.setBearerAuth(token);
					}
				})
				.contentType(MediaType.APPLICATION_JSON)
				.accept(MediaType.APPLICATION_JSON, MediaType.TEXT_EVENT_STREAM)
				.bodyValue(body)
				.retrieve()
				.bodyToMono(String.class)
				.map(this::parseAddresses)
				.doOnError(e -> log.warn("MCP get_addresses failed: {}", e.toString()));
	}

	/**
	 * Calls the {@code search_restaurants} MCP tool for a single dish query.
	 *
	 * @param query     the dish / search term (e.g. "shawarma")
	 * @param addressId Swiggy address id; falls back to the configured default when blank
	 * @param bearer    OAuth access token; falls back to the configured dev token when blank
	 * @param offset    0-based item offset for pagination (0 = first page of ~10 results)
	 */
	public Mono<List<Restaurant>> searchRestaurants(String query, String addressId, String bearer, int offset) {
		String addr = (addressId == null || addressId.isBlank()) ? props.defaultAddressId() : addressId;
		String token = resolveToken(bearer);
		String cacheKey = query + ":" + addr + ":" + offset;

		List<Restaurant> hit = searchResultCache.getIfPresent(cacheKey);
		if (hit != null) {
			log.debug("Search cache hit: key={}", cacheKey);
			return Mono.just(hit);
		}

		Map<String, Object> body = Map.of(
				"jsonrpc", "2.0",
				"method", "tools/call",
				"params", Map.of(
						"name", "search_restaurants",
						"arguments", Map.of(
								"query", query,
								"addressId", addr == null ? "" : addr,
								"offset", offset)),
				"id", requestIds.getAndIncrement());

		return webClient.post()
				.uri(props.foodPath())
				.headers(h -> {
					if (token != null && !token.isBlank()) {
						h.setBearerAuth(token);
					}
				})
				.contentType(MediaType.APPLICATION_JSON)
				.accept(MediaType.APPLICATION_JSON, MediaType.TEXT_EVENT_STREAM)
				.bodyValue(body)
				.retrieve()
				.bodyToMono(String.class)
				.map(raw -> parseRestaurants(raw, query))
				.doOnNext(result -> {
					if (!result.isEmpty()) {
						searchResultCache.put(cacheKey, result);
					}
				})
				.doOnError(e -> log.warn("MCP search_restaurants failed for query='{}': {}", query, e.toString()));
	}

	// --- response parsing -------------------------------------------------------------

	List<Address> parseAddresses(String rawBody) {
		try {
			JsonNode envelope = readJsonRpcEnvelope(rawBody);
			if (envelope.has("error") && !envelope.get("error").isNull()) {
				log.warn("MCP returned JSON-RPC error for get_addresses: {}", envelope.get("error"));
				return List.of();
			}
			JsonNode result = envelope.path("result");
			List<Address> found = new ArrayList<>();
			findAddresses(result, found);
			return found;
		}
		catch (Exception e) {
			log.warn("Failed to parse MCP get_addresses response: {}", e.toString());
			return List.of();
		}
	}

	List<Restaurant> parseRestaurants(String rawBody, String query) {
		try {
			JsonNode envelope = readJsonRpcEnvelope(rawBody);
			if (envelope.has("error") && !envelope.get("error").isNull()) {
				log.warn("MCP returned JSON-RPC error for query='{}': {}", query, envelope.get("error"));
				return List.of();
			}
			JsonNode result = envelope.path("result");
			List<Restaurant> found = new ArrayList<>();
			findRestaurants(result, found);
			return found;
		}
		catch (Exception e) {
			log.warn("Failed to parse MCP response for query='{}': {}", query, e.toString());
			return List.of();
		}
	}

	/**
	 * Extracts the JSON-RPC envelope from a response body that may be plain JSON or an SSE
	 * stream of {@code data:} lines.
	 */
	private JsonNode readJsonRpcEnvelope(String rawBody) throws Exception {
		String trimmed = rawBody == null ? "" : rawBody.trim();
		if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
			return mapper.readTree(trimmed);
		}
		// SSE framing: concatenate the payload of all `data:` lines and parse the result.
		StringBuilder data = new StringBuilder();
		for (String line : trimmed.split("\\r?\\n")) {
			if (line.startsWith("data:")) {
				data.append(line.substring("data:".length()).trim());
			}
		}
		String json = data.toString();
		if (json.isEmpty()) {
			throw new IllegalStateException("No JSON found in MCP response body");
		}
		return mapper.readTree(json);
	}

	/**
	 * Recursively walks the MCP result looking for the {@code structuredContent.addresses}
	 * array from {@code get_addresses}.
	 */
	private void findAddresses(JsonNode node, List<Address> out) {
		if (node == null || node.isMissingNode() || node.isNull() || !out.isEmpty()) {
			return;
		}
		if (node.isObject()) {
			// structuredContent.addresses is the canonical location.
			if (node.has("addresses") && node.get("addresses").isArray()) {
				node.get("addresses").forEach(el -> {
					Address a = mapper.convertValue(el, Address.class);
					if (a != null && a.id() != null) {
						out.add(a);
					}
				});
				if (!out.isEmpty()) {
					return;
				}
			}
			for (JsonNode child : node) {
				findAddresses(child, out);
			}
		}
		else if (node.isArray()) {
			for (JsonNode child : node) {
				findAddresses(child, out);
			}
		}
	}

	/**
	 * Recursively walks the MCP result looking for the first array of restaurant-shaped
	 * objects. Handles {@code structuredContent}, {@code content[].text} (which embeds a
	 * JSON string), and other nesting variants the tool might use.
	 */
	private void findRestaurants(JsonNode node, List<Restaurant> out) {
		if (node == null || node.isMissingNode() || node.isNull() || !out.isEmpty()) {
			return;
		}
		if (node.isArray()) {
			if (looksLikeRestaurantArray(node)) {
				node.forEach(el -> {
					Restaurant r = mapper.convertValue(el, Restaurant.class);
					if (r != null && r.id() != null) {
						out.add(r);
					}
				});
				if (!out.isEmpty()) {
					return;
				}
			}
			for (JsonNode child : node) {
				findRestaurants(child, out);
			}
			return;
		}
		if (node.isObject()) {
			for (JsonNode child : node) {
				if (child.isTextual()) {
					maybeParseEmbeddedJson(child.asText(), out);
				}
				else {
					findRestaurants(child, out);
				}
			}
			return;
		}
		if (node.isTextual()) {
			maybeParseEmbeddedJson(node.asText(), out);
		}
	}

	private void maybeParseEmbeddedJson(String text, List<Restaurant> out) {
		String t = text == null ? "" : text.trim();
		if (t.startsWith("{") || t.startsWith("[")) {
			try {
				findRestaurants(mapper.readTree(t), out);
			}
			catch (Exception ignored) {
				// not JSON, ignore
			}
		}
	}

	private boolean looksLikeRestaurantArray(JsonNode array) {
		if (array.isEmpty()) {
			return false;
		}
		JsonNode first = array.get(0);
		return first.isObject() && first.has("name") && (first.has("id") || first.has("avgRating"));
	}

	private String resolveToken(String bearer) {
		return (bearer == null || bearer.isBlank()) ? props.token() : bearer;
	}

	// Retained for potential generic tool calls / tests.
	@SuppressWarnings("unused")
	private List<Map<String, Object>> asMaps(JsonNode node) {
		return mapper.convertValue(node, new TypeReference<>() {});
	}
}
