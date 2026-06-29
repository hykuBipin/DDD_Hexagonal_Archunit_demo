package com.ordertogether.dto;

import java.util.List;

/**
 * Result of an OrderTogether match.
 *
 * @param preferences the dish terms that were searched
 * @param matchCount  number of restaurants serving all preferences and currently open
 * @param restaurants matched restaurants, ranked best-first (rating desc, then ETA asc)
 */
public record MatchResponse(
		List<String> preferences,
		int matchCount,
		List<MatchedRestaurant> restaurants) {
}
