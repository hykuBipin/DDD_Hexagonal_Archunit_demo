package com.example.satellite.infrastructure.adapters.input;

import com.example.satellite.application.RegisterSatelliteCommand;
import com.example.satellite.application.SatelliteApplicationService;
import com.example.satellite.domain.*;

import com.example.satellite.infrastructure.hexagonal.InputAdapter;

import java.util.List;

/**
 * Driving (Input) Adapter simulating a delivery mechanism (such as a CLI or Web Controller).
 * In Hexagonal Architecture, a driving adapter depends ONLY on input ports (application use cases)
 * and the domain layer. It has ZERO dependencies on concrete output adapters (databases)!
 */
@InputAdapter("Console CLI Driving Input Adapter")
public class SatelliteConsoleAdapter {

    private final SatelliteApplicationService appUseCase;
    private final SatelliteRepository repositoryPort;

    public SatelliteConsoleAdapter(SatelliteApplicationService appUseCase, SatelliteRepository repositoryPort) {
        this.appUseCase = appUseCase;
        this.repositoryPort = repositoryPort;
    }

    /**
     * Executes business simulation use cases.
     * Operates purely on Domain entities and Application services (Hexagon core).
     * Decoupled from database implementations by accepting the Port interface.
     */
    public void runSimulation() {
        // Use Case 1: Register Satellite
        System.out.println("\n[UseCase] Registering Satellite...");
        SatelliteId issId = appUseCase.registerSatellite(
                new RegisterSatelliteCommand("International Space Station", 418.0, 51.64, 92.9)
        );

        // Use Case 2: Update Telemetry
        System.out.println("[UseCase] Receiving Telemetry update...");
        appUseCase.updateTelemetry(issId, 45.51, -122.68, 7.66, 95);

        // Query state
        System.out.println("[UseCase] Querying satellite data...");
        List<Satellite> satellites = repositoryPort.findAll();
        for (Satellite sat : satellites) {
            System.out.printf("  Loaded: %s (ID: %s) | Orbit: %.1f km | Battery: %d%%\n",
                    sat.getName(),
                    sat.getId(),
                    sat.getOrbit().altitudeKm(),
                    sat.getLatestTelemetry().batteryPercentage()
            );
        }

        // Use Case 3: Decommissioning
        System.out.println("[UseCase] Decommissioning satellite...");
        appUseCase.decommissionSatellite(issId);

        // Enforce state invariants
        try {
            System.out.println("[UseCase] Attempting telemetry update on decommissioned satellite...");
            appUseCase.updateTelemetry(issId, 46.0, -123.0, 7.66, 90);
        } catch (IllegalStateException e) {
            System.out.println("  Caught expected invariant guard violation: " + e.getMessage());
        }
    }
}
