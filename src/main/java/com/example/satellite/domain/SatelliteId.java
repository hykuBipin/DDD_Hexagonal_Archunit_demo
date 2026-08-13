package com.example.satellite.domain;

import com.example.satellite.domain.ddd.ValueObject;

import java.util.Objects;
import java.util.UUID;

/**
 * Value Object representing a unique identifier for a Satellite.
 * In DDD, Value Objects are immutable and defined by their attributes rather than a thread of continuity.
 */
@ValueObject("Satellite Identity Value Object")
public record SatelliteId(UUID value) {
    public SatelliteId {
        Objects.requireNonNull(value, "Satellite ID value cannot be null");
    }

    public static SatelliteId generate() {
        return new SatelliteId(UUID.randomUUID());
    }

    public static SatelliteId fromString(String uuidString) {
        return new SatelliteId(UUID.fromString(uuidString));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
