package com.example.satellite.domain.ddd;

import java.lang.annotation.*;

/**
 * Identifies a Value Object in DDD.
 * Value Objects are immutable, self-validating, and compared by property equality.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface ValueObject {
    String value() default "";
}
