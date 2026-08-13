package com.example.satellite.domain;

/**
 * Value Object representing the orbital parameters of a satellite.
 * In DDD, Value Objects enforce their own invariants upon creation.
 */
public record Orbit(double altitudeKm, double inclinationDegrees, double periodMinutes) {
    
    public Orbit {
        if (altitudeKm < 0) {
            throw new IllegalArgumentException("Altitude cannot be negative");
        }
        if (inclinationDegrees < 0 || inclinationDegrees > 180) {
            throw new IllegalArgumentException("Inclination must be between 0 and 180 degrees");
        }
        if (periodMinutes <= 0) {
            throw new IllegalArgumentException("Orbital period must be positive");
        }
    }

    /**
     * Checks if this orbit is in close proximity to another orbit, which represents collision risk.
     */
    public boolean isCloseTo(Orbit other, double altitudeThresholdKm, double inclinationThresholdDegrees) {
        double altitudeDiff = Math.abs(this.altitudeKm - other.altitudeKm);
        double inclinationDiff = Math.abs(this.inclinationDegrees - other.inclinationDegrees);
        return altitudeDiff < altitudeThresholdKm && inclinationDiff < inclinationThresholdDegrees;
    }
}
