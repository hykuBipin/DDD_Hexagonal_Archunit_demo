# Satellite Tracking System - DDD & Hexagonal Architecture Demo

This repository is a clean, simple demonstration of **Domain-Driven Design (DDD)** and **Hexagonal Architecture (Ports and Adapters)** in Java 17, with boundaries verified by **ArchUnit** tests.

It simulates a satellite tracking system, highlighting how core business logic is isolated from database technologies (swapping between a standard Java In-Memory database and an Oracle Database).

## Key Features

1. **Domain-Driven Design (DDD)**:
   - **Aggregate Root**: `Satellite` guards invariants (e.g. decommissioned satellites can't receive telemetry).
   - **Value Objects**: `SatelliteId`, `Orbit`, and `Telemetry` enforce validation rules.
   - **Domain Service**: `CollisionRiskService` checks orbits for collision risks.
   - **Domain Repository Interface**: `SatelliteRepository` is pure and agnostic of database technologies.

2. **Hexagonal Architecture**:
   - **Hexagon Core**: Encompasses the Domain and Application layers (`SatelliteApplicationService` input port).
   - **Driving Input Adapter**: `SatelliteConsoleAdapter` drives the simulation.
   - **Driven Output Adapters**: `InMemorySatelliteRepository` and `OracleSatelliteRepository` implement the repository port.
   - We demonstrate database migration by changing a **single dependency instantiation line** at the application bootstrap composer (`Main.java`).

3. **ArchUnit Boundary Enforcement**:
   - Automated tests enforce architecture rules: core packages cannot access adapters, and input adapters cannot depend on output adapters directly.

---

## Getting Started

### Prerequisites
* Java 17
* Maven 3+

### Run Architecture & Unit Tests
```bash
mvn clean test
```

### Run DB Migration Simulation
```bash
mvn compile exec:java -Dexec.mainClass="com.example.satellite.Main"
```

---

## Project Structure
```text
src/
├── main/java/com/example/satellite/
│   ├── Main.java (Bootstrap Composer)
│   ├── application/
│   │   ├── RegisterSatelliteCommand.java (DTO)
│   │   └── SatelliteApplicationService.java (Input Port)
│   ├── domain/
│   │   ├── Satellite.java (Aggregate Root)
│   │   ├── Orbit.java (Value Object)
│   │   ├── Telemetry.java (Value Object)
│   │   ├── CollisionRiskService.java (Domain Service)
│   │   └── SatelliteRepository.java (Output Port Interface)
│   └── infrastructure/adapters/
│       ├── input/
│       │   └── SatelliteConsoleAdapter.java (Driving Adapter)
│       └── output/persistence/
│           ├── InMemorySatelliteRepository.java (Driven Adapter)
│           └── OracleSatelliteRepository.java (Driven Adapter)
└── test/java/com/example/satellite/
    ├── architecture/
    │   └── DddArchitectureTest.java (ArchUnit Rules)
    └── domain/
        └── SatelliteDomainTest.java (Domain Unit Tests)
```
