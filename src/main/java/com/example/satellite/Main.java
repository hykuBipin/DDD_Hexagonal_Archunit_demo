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

        // ---------------------------------------------------------------------
        // STEP 1: CHOOSE DATABASE ADAPTER (TOGGLE COMMENTS FOR MIGRATION DEMO)
        // ---------------------------------------------------------------------

        // [DATABASE ADAPTER OPTION A] Java In-Memory Database (Default)
        System.out.println("\n>>> RUNNING WITH IN-MEMORY DATABASE ADAPTER <<<");
        SatelliteRepository repository = new InMemorySatelliteRepository();

        // [DATABASE ADAPTER OPTION B] Oracle Enterprise SQL Database
        // (To show Oracle DB demo: Comment Option A and uncomment Option B lines below!)
        // System.out.println("\n>>> RUNNING WITH ORACLE DATABASE ADAPTER <<<");
        // SatelliteRepository repository = new OracleSatelliteRepository();

        // ---------------------------------------------------------------------
        // STEP 2: BOOTSTRAP APPSERVICE (INPUT PORT) WITH CHOSEN ADAPTER
        // ---------------------------------------------------------------------
        SatelliteApplicationService appService = new SatelliteApplicationService(repository);

        // ---------------------------------------------------------------------
        // STEP 3: RUN DRIVING CONSOLE ADAPTER
        // ---------------------------------------------------------------------
        SatelliteConsoleAdapter adapter = new SatelliteConsoleAdapter(appService, repository);
        adapter.runSimulation();

        System.out.println("\n========================================================================");
        System.out.println("DEMO SUMMARY:");
        System.out.println("- Wired to: " + repository.getClass().getSimpleName());
        System.out.println("- Swapping the database requires zero modifications to Domain core!");
        System.out.println("========================================================================");
    }
}
