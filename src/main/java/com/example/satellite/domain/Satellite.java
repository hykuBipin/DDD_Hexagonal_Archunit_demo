package com.example.satellite.domain;

import com.example.satellite.domain.ddd.AggregateRoot;

import java.util.Objects;

/**
 * Aggregate Root representing a Satellite.
 * In DDD, the Aggregate Root ensures consistency within its boundary. All mutations 
 * to its state must go through methods on this class to satisfy domain rules (invariants).
 */
@AggregateRoot("Satellite Aggregate Root")
public class Satellite {
    private final SatelliteId id;
    private final String name;
    private final Orbit orbit;
    private Telemetry latestTelemetry;
    private boolean decommissioned;

    public Satellite(SatelliteId id, String name, Orbit orbit) {
        this.id = Objects.requireNonNull(id, "Satellite ID cannot be null");
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Satellite name cannot be empty");
        }
        this.name = name;
        this.orbit = Objects.requireNonNull(orbit, "Orbit cannot be null");
        this.decommissioned = false;
    }

    /**
     * Updates the satellite's latest telemetry reading.
     * Enforces the business rule that decommissioned satellites cannot receive telemetry updates.
     */
    public void updateTelemetry(Telemetry telemetry) {
        if (decommissioned) {
            throw new IllegalStateException("Cannot update telemetry: Satellite is already decommissioned");
        }
        this.latestTelemetry = Objects.requireNonNull(telemetry, "Telemetry cannot be null");
    }

    /**
     * Decommissions the satellite.
     */
    public void decommission() {
        if (decommissioned) {
            throw new IllegalStateException("Satellite is already decommissioned");
        }
        this.decommissioned = true;
    }

    // Getters

    public SatelliteId getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Orbit getOrbit() {
        return orbit;
    }

    public Telemetry getLatestTelemetry() {
        return latestTelemetry;
    }

    public boolean isDecommissioned() {
        return decommissioned;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Satellite satellite = (Satellite) o;
        return id.equals(satellite.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
