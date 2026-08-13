package com.example.satellite.infrastructure.hexagonal;

import java.lang.annotation.*;

/**
 * Identifies an Output (Driven) Adapter in Hexagonal Architecture (e.g. database client, broker wrapper).
 * Output adapters realize the contracts (ports) defined by the core.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface OutputAdapter {
    String value() default "";
}
