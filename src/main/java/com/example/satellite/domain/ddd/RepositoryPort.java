package com.example.satellite.domain.ddd;

import java.lang.annotation.*;

/**
 * Identifies a Repository Port interface in DDD / Hexagonal Architecture.
 * This represents the abstract contract (Output Port) for data access.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RepositoryPort {
    String value() default "";
}
