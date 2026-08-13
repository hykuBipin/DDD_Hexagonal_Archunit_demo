package com.example.satellite;

import com.example.satellite.application.SatelliteApplicationService;
import com.example.satellite.domain.SatelliteRepository;
import com.example.satellite.infrastructure.adapters.input.SatelliteConsoleAdapter;
import com.example.satellite.infrastructure.adapters.output.persistence.InMemorySatelliteRepository;
import com.example.satellite.infrastructure.adapters.output.persistence.OracleSatelliteRepository;

/**
 * Main application bootstrap composer.
 * In Hexagonal Architecture, this root composer configures the adapters,
 * binds them to ports, and kicks off the system.
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("========================================================================");
        System.out.println("   DEMO: Domain-Driven Design & Hexagonal Architecture DB Migration");
        System.out.println("========================================================================");
        System.out.println("This demo showcases that the Core Domain & Use Cases are fully decoupled");
        System.out.println("from database technologies. We will run the tracking system use cases");
        System.out.println("first with an In-Memory (Java default) database adapter, and then swap to");
        System.out.println("an Oracle Database adapter by changing ONLY the repository wiring.");
        System.out.println("No domain logic or application services are modified!");
        System.out.println("========================================================================");

        // --- PART 1: DEFAULT JAVA IN-MEMORY STORAGE ---
        System.out.println("\n>>> SCENARIO 1: RUNNING WITH IN-MEMORY DATABASE ADAPTER <<<");
        SatelliteRepository inMemoryRepo = new InMemorySatelliteRepository();
        SatelliteApplicationService inMemoryAppService = new SatelliteApplicationService(inMemoryRepo);
        
        // We inject the In-memory repository port implementation
        SatelliteConsoleAdapter inMemoryAdapter = new SatelliteConsoleAdapter(inMemoryAppService, inMemoryRepo);
        inMemoryAdapter.runSimulation();

        // --- PART 2: ORACLE DATABASE STORAGE (THE SWAP) ---
        System.out.println("\n>>> SCENARIO 2: RUNNING WITH ORACLE DATABASE ADAPTER <<<");
        System.out.println("[MIGRATION STAGE] Swapping In-Memory Repository with Oracle Repository...");
        SatelliteRepository oracleRepo = new OracleSatelliteRepository();
        SatelliteApplicationService oracleAppService = new SatelliteApplicationService(oracleRepo);
        
        // We inject the Oracle repository port implementation
        SatelliteConsoleAdapter oracleAdapter = new SatelliteConsoleAdapter(oracleAppService, oracleRepo);
        oracleAdapter.runSimulation();
        
        System.out.println("\n========================================================================");
        System.out.println("DEMO SUMMARY:");
        System.out.println("- Swapped database from In-Memory to Oracle database successfully.");
        System.out.println("- No changes were made to Satellite.java, SatelliteRepository.java, or");
        System.out.println("  SatelliteApplicationService.java.");
        System.out.println("- Domain invariants (like decommissioning validation) were fully preserved.");
        System.out.println("========================================================================");
    }
}
