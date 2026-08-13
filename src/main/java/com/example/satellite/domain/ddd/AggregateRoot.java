package com.example.satellite.domain.ddd;

import java.lang.annotation.*;

/**
 * Identifies an Aggregate Root in DDD.
 * Aggregate Roots control consistency boundaries and manage their internal entities.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface AggregateRoot {
    String value() default "";
}
