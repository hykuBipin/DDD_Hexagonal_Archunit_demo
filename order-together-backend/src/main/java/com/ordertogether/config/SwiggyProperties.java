package com.ordertogether.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Configuration for the Swiggy Builders Club MCP server.
 *
 * <p>The {@code token} here is only a convenience fallback for local/dev use. In
 * production the OAuth 2.1 (PKCE) access token is obtained by the Flutter client and
 * forwarded to this backend in the {@code Authorization} header per request.
 */
@ConfigurationProperties(prefix = "swiggy.mcp")
public record SwiggyProperties(
		String baseUrl,
		String foodPath,
		String token,
		String defaultAddressId,
		int timeoutSeconds) {

	public SwiggyProperties {
		if (baseUrl == null || baseUrl.isBlank()) {
			baseUrl = "https://mcp.swiggy.com";
		}
		if (foodPath == null || foodPath.isBlank()) {
			foodPath = "/food";
		}
		if (timeoutSeconds <= 0) {
			timeoutSeconds = 20;
		}
	}
}
