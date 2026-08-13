package com.example.satellite.domain;

import com.example.satellite.domain.ddd.ValueObject;

import java.time.Instant;
import java.util.Objects;

/**
 * Value Object representing the telemetry reading of a satellite at a specific point in time.
 * Value Objects are immutable. Any modification results in a new instance.
 */
@ValueObject("Telemetry Reading Value Object")
public record Telemetry(
        double latitude,
        double longitude,
        double speedKms,
        int batteryPercentage,
        Instant timestamp
) {
    public Telemetry {
        if (latitude < -90.0 || latitude > 90.0) {
            throw new IllegalArgumentException("Latitude must be between -90 and 90 degrees");
        }
        if (longitude < -180.0 || longitude > 180.0) {
            throw new IllegalArgumentException("Longitude must be between -180 and 180 degrees");
        }
        if (speedKms < 0.0) {
            throw new IllegalArgumentException("Speed cannot be negative");
        }
        if (batteryPercentage < 0 || batteryPercentage > 100) {
            throw new IllegalArgumentException("Battery percentage must be between 0 and 100");
        }
        Objects.requireNonNull(timestamp, "Timestamp cannot be null");
    }
}
