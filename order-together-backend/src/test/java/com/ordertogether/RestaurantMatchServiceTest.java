package com.ordertogether;

import com.ordertogether.client.SwiggyMcpClient;
import com.ordertogether.dto.MatchRequest;
import com.ordertogether.dto.MatchResponse;
import com.ordertogether.model.Restaurant;
import com.ordertogether.service.RestaurantMatchService;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import reactor.core.publisher.Mono;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;

class RestaurantMatchServiceTest {

	private Restaurant r(String id, String name, Double rating, Integer eta, String status) {
		return new Restaurant(
				id, name, rating, null,
				eta, null,
				"₹300", status, null,
				null, List.of("North Indian"),
				null, null, null);
	}

	@Test
	void menuVerificationFiltersRestaurantsMissingADish() {
		SwiggyMcpClient client = Mockito.mock(SwiggyMcpClient.class);

		// Both searches return A, B, C → union pool = {A, B, C}
		Mockito.when(client.searchRestaurants(eq("shawarma"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(
						r("A", "Al Faham", 4.5, 30, "CLOSED - FOR NOW"),
						r("B", "Kebab House", 4.2, 40, "OPEN"),
						r("C", "Grill Inn", 4.8, 25, "OPEN"))));
		Mockito.when(client.searchRestaurants(eq("dal tadka"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(
						r("A", "Al Faham", 4.5, 30, "CLOSED - FOR NOW"),
						r("B", "Kebab House", 4.2, 40, "OPEN"),
						r("C", "Grill Inn", 4.8, 25, "OPEN"))));

		// C has both dishes in menu → matches
		Mockito.when(client.getMenuItemNames(eq("C"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Chicken Shawarma Roll", "Dal Tadka Special")));
		// B has shawarma but NOT dal tadka → filtered out
		Mockito.when(client.getMenuItemNames(eq("B"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Shawarma Wrap", "Kebab Platter")));
		// A is CLOSED but its menu has both dishes → included, sorted last
		Mockito.when(client.getMenuItemNames(eq("A"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Shawarma", "Dal Tadka")));

		RestaurantMatchService service = new RestaurantMatchService(client);
		MatchResponse resp = service.match(
				new MatchRequest(List.of("shawarma", "dal tadka"), null), null).block();

		assertThat(resp).isNotNull();
		// B is dropped (no dal tadka in menu). C (open) and A (closed) both match.
		// Open restaurants rank first, so C comes before A.
		assertThat(resp.matchCount()).isEqualTo(2);
		assertThat(resp.restaurants().get(0).id()).isEqualTo("C");
		assertThat(resp.restaurants().get(1).id()).isEqualTo("A");
		assertThat(resp.restaurants().get(0).appDeepLink()).isEqualTo("swiggy://menu?restaurant_id=C");
	}

	@Test
	void restaurantsOnlyInOneSearchResultCanStillMatchViaMenu() {
		SwiggyMcpClient client = Mockito.mock(SwiggyMcpClient.class);

		// D appears only in shawarma results (not in dal tadka results)
		// but D's menu has both → should still match (union approach)
		Mockito.when(client.searchRestaurants(eq("shawarma"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("D", "Dubai Kitchen", 4.6, 30, "OPEN"))));
		Mockito.when(client.searchRestaurants(eq("dal tadka"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("E", "Punjabi Dhaba", 4.0, 35, "OPEN"))));

		// D has both dishes
		Mockito.when(client.getMenuItemNames(eq("D"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Shawarma Plate", "Dal Tadka", "Butter Naan")));
		// E only has dal tadka, not shawarma
		Mockito.when(client.getMenuItemNames(eq("E"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Dal Tadka", "Paneer Tikka")));

		RestaurantMatchService service = new RestaurantMatchService(client);
		MatchResponse resp = service.match(
				new MatchRequest(List.of("shawarma", "dal tadka"), null), null).block();

		assertThat(resp).isNotNull();
		assertThat(resp.matchCount()).isEqualTo(1);
		assertThat(resp.restaurants().get(0).id()).isEqualTo("D");
	}

	@Test
	void searchHitCountDrivesRankingBeforeRating() {
		SwiggyMcpClient client = Mockito.mock(SwiggyMcpClient.class);

		// F appears in BOTH search results (hit count = 2), rating 4.0
		// G appears in only ONE search result (hit count = 1), rating 4.9
		Mockito.when(client.searchRestaurants(eq("pizza"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(
						r("F", "Pizza Palace", 4.0, 30, "OPEN"),
						r("G", "Gourmet Spot", 4.9, 25, "OPEN"))));
		Mockito.when(client.searchRestaurants(eq("pasta"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("F", "Pizza Palace", 4.0, 30, "OPEN"))));

		Mockito.when(client.getMenuItemNames(eq("F"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Margherita Pizza", "Spaghetti Pasta")));
		Mockito.when(client.getMenuItemNames(eq("G"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Wood-fired Pizza", "Penne Pasta")));

		RestaurantMatchService service = new RestaurantMatchService(client);
		MatchResponse resp = service.match(
				new MatchRequest(List.of("pizza", "pasta"), null), null).block();

		assertThat(resp).isNotNull();
		assertThat(resp.matchCount()).isEqualTo(2);
		// F (hit count 2) ranks above G (hit count 1) despite lower rating
		assertThat(resp.restaurants()).extracting("id").containsExactly("F", "G");
	}

	@Test
	void noOverlapYieldsNoMatches() {
		SwiggyMcpClient client = Mockito.mock(SwiggyMcpClient.class);

		Mockito.when(client.searchRestaurants(eq("sushi"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("X", "Edo", 4.6, 35, "OPEN"))));
		Mockito.when(client.searchRestaurants(eq("biryani"), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("Y", "Paradise", 4.4, 45, "OPEN"))));

		// X menu has no biryani; Y menu has no sushi
		Mockito.when(client.getMenuItemNames(eq("X"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Salmon Sushi", "Tuna Roll")));
		Mockito.when(client.getMenuItemNames(eq("Y"), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of("Hyderabadi Biryani", "Raita")));

		RestaurantMatchService service = new RestaurantMatchService(client);
		MatchResponse resp = service.match(
				new MatchRequest(List.of("sushi", "biryani"), null), null).block();

		assertThat(resp).isNotNull();
		assertThat(resp.matchCount()).isZero();
	}

	@Test
	void menuMatchIsCaseInsensitive() {
		assertThat(RestaurantMatchService.allPreferencesInMenu(
				List.of("Shawarma", "DAL TADKA"),
				List.of("chicken shawarma roll", "dal tadka special"))).isTrue();

		assertThat(RestaurantMatchService.allPreferencesInMenu(
				List.of("shawarma"),
				List.of("Pasta", "Pizza"))).isFalse();
	}

	@Test
	void menuCheckFailureDropsRestaurantGracefully() {
		SwiggyMcpClient client = Mockito.mock(SwiggyMcpClient.class);

		Mockito.when(client.searchRestaurants(any(), isNull(), isNull(), anyInt()))
				.thenReturn(Mono.just(List.of(r("Z", "Broken Place", 4.5, 20, "OPEN"))));
		// Simulate empty menu (could be a parse failure or API error)
		Mockito.when(client.getMenuItemNames(any(), isNull(), isNull(), any()))
				.thenReturn(Mono.just(List.of()));

		RestaurantMatchService service = new RestaurantMatchService(client);
		MatchResponse resp = service.match(
				new MatchRequest(List.of("biryani"), null), null).block();

		assertThat(resp).isNotNull();
		assertThat(resp.matchCount()).isZero();
	}
}
