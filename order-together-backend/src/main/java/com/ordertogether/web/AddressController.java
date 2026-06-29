package com.ordertogether.web;

import com.ordertogether.client.SwiggyMcpClient;
import com.ordertogether.model.Address;

import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Mono;

import java.util.List;

@RestController
@RequestMapping("/api")
public class AddressController {

	private final SwiggyMcpClient mcpClient;

	public AddressController(SwiggyMcpClient mcpClient) {
		this.mcpClient = mcpClient;
	}

	/**
	 * Returns all delivery addresses saved in the user's Swiggy account.
	 * The Flutter app uses this list for the location-selection screen.
	 */
	@GetMapping("/addresses")
	public Mono<List<Address>> getAddresses(
			@RequestHeader(value = HttpHeaders.AUTHORIZATION, required = false) String authorization) {

		String bearer = stripBearer(authorization);
		return mcpClient.getAddresses(bearer);
	}

	private String stripBearer(String authorization) {
		if (authorization == null) {
			return null;
		}
		String trimmed = authorization.trim();
		if (trimmed.regionMatches(true, 0, "Bearer ", 0, 7)) {
			return trimmed.substring(7).trim();
		}
		return trimmed;
	}
}
