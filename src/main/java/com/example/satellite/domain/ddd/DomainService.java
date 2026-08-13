package com.example.satellite.domain.ddd;

import java.lang.annotation.*;

/**
 * Identifies a Domain Service in DDD.
 * Domain Services hold business calculations or behaviors that operate across multiple aggregates.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface DomainService {
    String value() default "";
}
