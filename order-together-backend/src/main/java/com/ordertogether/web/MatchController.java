package com.ordertogether.web;

import com.ordertogether.dto.MatchRequest;
import com.ordertogether.dto.MatchResponse;
import com.ordertogether.service.RestaurantMatchService;

import jakarta.validation.Valid;

import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api")
public class MatchController {

	private final RestaurantMatchService matchService;

	public MatchController(RestaurantMatchService matchService) {
		this.matchService = matchService;
	}

	/**
	 * Find restaurants serving every diner's dish preference at once.
	 *
	 * <p>The caller's OAuth bearer token (if present) is forwarded to the Swiggy MCP
	 * server; otherwise the server-configured dev token is used.
	 */
	@PostMapping("/match")
	public Mono<MatchResponse> match(
			@Valid @RequestBody MatchRequest request,
			@RequestHeader(value = HttpHeaders.AUTHORIZATION, required = false) String authorization) {

		String bearer = stripBearer(authorization);
		return matchService.match(request, bearer);
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
