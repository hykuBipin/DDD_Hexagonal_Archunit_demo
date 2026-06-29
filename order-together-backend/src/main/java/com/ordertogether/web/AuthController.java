package com.ordertogether.web;

import com.ordertogether.config.AppProperties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.time.Duration;
import java.util.Base64;
import java.util.Map;
import java.util.UUID;

/**
 * Server-side OAuth 2.1 PKCE broker.
 *
 * <p>Keeps PKCE state in-memory (fine for MVP / single-instance). Abandoned flows are
 * cleaned up automatically after 5 minutes via Caffeine TTL.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

	private static final Logger log = LoggerFactory.getLogger(AuthController.class);

	/** state → code_verifier; auto-expires after 5 min to clean up abandoned auth flows. */
	private final Cache<String, String> pkceStore = Caffeine.newBuilder()
			.expireAfterWrite(Duration.ofMinutes(5))
			.maximumSize(1000)
			.build();

	private final AppProperties props;
	private final WebClient webClient;

	public AuthController(AppProperties props, WebClient.Builder builder) {
		this.props = props;
		// Separate WebClient for the auth/token endpoint (not the MCP food path).
		this.webClient = builder
				.baseUrl("https://mcp.swiggy.com")
				.codecs(c -> c.defaultCodecs().maxInMemorySize(1024 * 1024))
				.build();
	}

	/**
	 * Step 1 — initiate login.
	 * Generates PKCE, stores the verifier, and redirects the browser to Swiggy's
	 * authorization endpoint.
	 *
	 * <p>Open this URL in a browser (or from the Flutter app via url_launcher):
	 * {@code GET /api/auth/login}
	 */
	@GetMapping("/login")
	public ResponseEntity<Void> login() {
		String state = UUID.randomUUID().toString();
		String codeVerifier = generateCodeVerifier();
		String codeChallenge = generateCodeChallenge(codeVerifier);

		pkceStore.put(state, codeVerifier);

		String authUrl = props.oauth().authEndpoint()
				+ "?response_type=code"
				+ "&client_id=" + props.oauth().clientId()
				+ "&redirect_uri=" + encode(props.callbackUri())
				+ "&scope=" + encode(props.oauth().scope())
				+ "&state=" + state
				+ "&code_challenge=" + codeChallenge
				+ "&code_challenge_method=S256";

		log.info("Initiating OAuth login, state={}", state);
		return redirect(authUrl);
	}

	/**
	 * Step 2 — Swiggy posts back here with the authorization code.
	 * Exchanges the code for an access token, then deep-links back to the Flutter app.
	 */
	@GetMapping("/callback")
	public Mono<ResponseEntity<Void>> callback(
			@RequestParam String code,
			@RequestParam String state) {

		String codeVerifier = pkceStore.getIfPresent(state);
		if (codeVerifier != null) pkceStore.invalidate(state);
		if (codeVerifier == null) {
			log.warn("OAuth callback received unknown state={}", state);
			return Mono.just(ResponseEntity.badRequest().<Void>build());
		}

		MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
		form.add("grant_type", "authorization_code");
		form.add("code", code);
		form.add("redirect_uri", props.callbackUri());
		form.add("client_id", props.oauth().clientId());
		form.add("code_verifier", codeVerifier);

		return webClient.post()
				.uri("/auth/token")
				.contentType(MediaType.APPLICATION_FORM_URLENCODED)
				.body(BodyInserters.fromFormData(form))
				.retrieve()
				.bodyToMono(Map.class)
				.map(tokenResponse -> {
					String accessToken = (String) tokenResponse.get("access_token");
					if (accessToken == null) {
						log.error("Token exchange succeeded but no access_token in response: {}", tokenResponse);
						return ResponseEntity.status(HttpStatus.BAD_GATEWAY).<Void>build();
					}
					log.info("OAuth token exchange successful, redirecting to Flutter app");
					return redirect(props.oauth().deepLinkScheme() + "?token=" + encode(accessToken));
				})
				.onErrorResume(e -> {
					log.error("Token exchange failed: {}", e.toString());
					return Mono.just(ResponseEntity.status(HttpStatus.BAD_GATEWAY).<Void>build());
				});
	}

	// ---- PKCE helpers -------------------------------------------------------

	private static String generateCodeVerifier() {
		byte[] bytes = new byte[32];
		new SecureRandom().nextBytes(bytes);
		return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
	}

	private static String generateCodeChallenge(String verifier) {
		try {
			MessageDigest digest = MessageDigest.getInstance("SHA-256");
			byte[] hash = digest.digest(verifier.getBytes(StandardCharsets.US_ASCII));
			return Base64.getUrlEncoder().withoutPadding().encodeToString(hash);
		}
		catch (Exception e) {
			throw new IllegalStateException("SHA-256 not available", e);
		}
	}

	private static ResponseEntity<Void> redirect(String location) {
		return ResponseEntity.status(HttpStatus.FOUND)
				.header(HttpHeaders.LOCATION, location)
				.build();
	}

	private static String encode(String value) {
		return java.net.URLEncoder.encode(value, StandardCharsets.UTF_8);
	}
}
