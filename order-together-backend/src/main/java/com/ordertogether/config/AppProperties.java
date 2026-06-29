package com.ordertogether.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app")
public record AppProperties(
		String publicUrl,
		OAuth oauth) {

	public record OAuth(
			String clientId,
			String authEndpoint,
			String tokenEndpoint,
			String scope,
			String deepLinkScheme) {
	}

	/** The redirect_uri sent to Swiggy and used in the token exchange. */
	public String callbackUri() {
		return publicUrl + "/api/auth/callback";
	}
}
