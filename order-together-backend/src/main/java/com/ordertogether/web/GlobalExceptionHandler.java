package com.ordertogether.web;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.bind.support.WebExchangeBindException;

import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

	/** Turn bean-validation failures on the request body into a 400 ProblemDetail. */
	@ExceptionHandler(WebExchangeBindException.class)
	ProblemDetail handleValidation(WebExchangeBindException ex) {
		String detail = ex.getFieldErrors().stream()
				.map(e -> e.getField() + ": " + e.getDefaultMessage())
				.collect(Collectors.joining("; "));
		ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,
				detail.isBlank() ? "Invalid request" : detail);
		pd.setTitle("Validation failed");
		return pd;
	}

	@ExceptionHandler(Exception.class)
	ProblemDetail handleGeneric(Exception ex) {
		ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_GATEWAY,
				"Failed to query Swiggy: " + ex.getMessage());
		pd.setTitle("Upstream error");
		return pd;
	}
}
