package com.ordertogether.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.util.List;

/**
 * Request to find restaurants that satisfy every diner's dish preference at once.
 *
 * @param preferences one dish/search term per person (e.g. ["shawarma", "dal tadka"])
 * @param addressId   Swiggy address id to search around; optional (server default used if blank)
 */
public record MatchRequest(
		@NotEmpty(message = "at least one preference is required")
		@Size(max = 10, message = "at most 10 preferences are supported")
		List<@NotBlank(message = "preference must not be blank") String> preferences,

		String addressId) {
}
