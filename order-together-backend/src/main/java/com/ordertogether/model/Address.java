package com.ordertogether.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * A saved delivery address from the user's Swiggy account, as returned by the
 * {@code get_addresses} MCP tool.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public record Address(
		String id,
		String addressLine,
		String phoneNumber,
		String addressCategory,
		String addressTag) {
}
