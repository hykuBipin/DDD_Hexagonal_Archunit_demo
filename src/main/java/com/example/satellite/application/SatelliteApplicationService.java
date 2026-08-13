package com.example.satellite.application;

import com.example.satellite.domain.*;
import com.example.satellite.infrastructure.adapters.output.persistence.OracleSatelliteRepository;

import org.springframework.beans.factory.annotation.Autowired;

import java.time.Instant;
import java.util.Objects;

/**
 * Application Service coordinating use cases for the Satellites domain.
 * In DDD, the Application Layer orchestrates the workflow. It loads aggregates, 
 * delegates business decisions to the Domain Layer (e.g. entities or domain services), 
 * and persists the changes. It does not make core business decisions itself.
 */
public class SatelliteApplicationService {

    private final SatelliteRepository repository;

    @Autowired
    private Satellite dummySatellite; // DEMO VIOLATION: Field injection via @Autowired is forbidden in the core!

    public SatelliteApplicationService(SatelliteRepository repository) {
        this.repository = Objects.requireNonNull(repository, "Repository cannot be null");
    }

    //private OracleSatelliteRepository oracleDb; // VIOLATION: Application layer accessing Output Adapter directly

    /**
     * Registers a new satellite.
     */
    public SatelliteId registerSatellite(RegisterSatelliteCommand command) {
        Orbit orbit = new Orbit(
                command.altitudeKm(),
                command.inclinationDegrees(),
                command.periodMinutes()
        );
        SatelliteId id = SatelliteId.generate();
        Satellite satellite = new Satellite(id, command.name(), orbit);
        
        repository.save(satellite);
        return id;
    }

    /**
     * Updates telemetry readings for a specific satellite.
     */
    public void updateTelemetry(
            SatelliteId id,
            double latitude,
            double longitude,
            double speedKms,
            int batteryPercentage
    ) {
        Satellite satellite = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Satellite not found with ID: " + id));

        Telemetry telemetry = new Telemetry(
                latitude,
                longitude,
                speedKms,
                batteryPercentage,
                Instant.now()
        );

        // Aggregate root enforces safety invariant rules (e.g., cannot update if decommissioned)
        satellite.updateTelemetry(telemetry);
        
        repository.save(satellite);
    }

    /**
     * Decommissions a satellite.
     */
    public void decommissionSatellite(SatelliteId id) {
        Satellite satellite = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Satellite not found with ID: " + id));

        // State changes occur on the aggregate root itself
        satellite.decommission();
        
        repository.save(satellite);
    }
}
