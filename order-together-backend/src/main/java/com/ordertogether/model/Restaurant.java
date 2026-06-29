package com.ordertogether.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

/**
 * A restaurant as returned by the Swiggy MCP {@code search_restaurants} tool.
 *
 * <p>{@code costForTwo} is kept as a {@link String} because Swiggy returns it formatted
 * (e.g. {@code "₹300 for two"}). Unknown fields are ignored so the model stays
 * forward-compatible with the MCP payload.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public record Restaurant(
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
		Double distanceKm) {

	/** True unless the restaurant explicitly reports any CLOSED availability status. */
	public boolean isOpen() {
		return availabilityStatus == null
				|| !availabilityStatus.trim().toUpperCase().contains("CLOSED");
	}
}
