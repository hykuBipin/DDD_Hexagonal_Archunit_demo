package com.ordertogether.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.netty.http.client.HttpClient;

import java.time.Duration;

@Configuration
public class WebClientConfig {

	/** WebClient pointed at the Swiggy MCP base URL, used by {@code SwiggyMcpClient}. */
	@Bean
	WebClient swiggyWebClient(WebClient.Builder builder, SwiggyProperties props) {
		HttpClient httpClient = HttpClient.create()
				.responseTimeout(Duration.ofSeconds(props.timeoutSeconds()));

		return builder
				.baseUrl(props.baseUrl())
				.clientConnector(new ReactorClientHttpConnector(httpClient))
				// MCP tool responses can be sizeable; raise the in-memory buffer limit.
				.codecs(c -> c.defaultCodecs().maxInMemorySize(8 * 1024 * 1024))
				.build();
	}
}
