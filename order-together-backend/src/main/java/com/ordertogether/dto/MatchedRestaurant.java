package com.ordertogether.dto;

import com.ordertogether.model.Restaurant;

import java.util.List;

/**
 * A restaurant that satisfies all diners' preferences, enriched with the dishes it
 * matched and deep links to complete the order in Swiggy (MVP is discovery-only).
 */
public record MatchedRestaurant(
		String id,
		String name,
		Double avgRating,
		String totalRatings,
		Integer deliveryTimeMinutes,
		String deliveryTimeRange,
		String costForTwo,
		String availabilityStatus,
		String nextOpenTime,
		String imageUrl,
		List<String> cuisines,
		String areaName,
		Double distanceKm,
		List<String> matchedPreferences,
		String appDeepLink,
		String webUrl) {

	public static MatchedRestaurant from(Restaurant r, List<String> matchedPreferences) {
		return new MatchedRestaurant(
				r.id(),
				r.name(),
				r.avgRating(),
				r.totalRatings(),
				r.deliveryTimeMinutes(),
				r.deliveryTimeRange(),
				r.costForTwo(),
				r.availabilityStatus(),
				r.nextOpenTime(),
				r.imageUrl(),
				r.cuisines(),
				r.areaName(),
				r.distanceKm(),
				matchedPreferences,
				"swiggy://menu?restaurant_id=" + r.id(),
				"https://www.swiggy.com/restaurants/" + r.id());
	}
}
