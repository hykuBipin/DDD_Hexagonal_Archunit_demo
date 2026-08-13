package com.example.satellite.application;

/**
 * Command DTO for registering a new satellite.
 * In DDD, the Application Layer uses simple Data Transfer Objects (DTOs) 
 * to pass data across boundaries without exposing internal domain objects.
 */
public record RegisterSatelliteCommand(
        String name,
        double altitudeKm,
        double inclinationDegrees,
        double periodMinutes
) {}
