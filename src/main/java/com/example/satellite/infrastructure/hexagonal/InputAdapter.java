package com.example.satellite.infrastructure.hexagonal;

import java.lang.annotation.*;

/**
 * Identifies an Input (Driving) Adapter in Hexagonal Architecture (e.g. Controller, CLI).
 * Input adapters translate external triggers (HTTP, console, timers) into core commands.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface InputAdapter {
    String value() default "";
}
