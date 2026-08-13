package com.example.satellite.domain;

import org.junit.jupiter.api.Test;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests verifying business invariants of the Domain Layer (Entities, Value Objects, and Services).
 */
public class SatelliteDomainTest {

    @Test
    void shouldCreateSatelliteSuccessfully() {
        SatelliteId id = SatelliteId.generate();
        Orbit orbit = new Orbit(400.0, 51.6, 92.0);
        Satellite satellite = new Satellite(id, "ISS", orbit);

        assertEquals(id, satellite.getId());
        assertEquals("ISS", satellite.getName());
        assertEquals(orbit, satellite.getOrbit());
        assertNull(satellite.getLatestTelemetry());
        assertFalse(satellite.isDecommissioned());
    }

    @Test
    void shouldFailToCreateSatelliteWithEmptyName() {
        Orbit orbit = new Orbit(400.0, 51.6, 92.0);
        assertThrows(IllegalArgumentException.class, () ->
                new Satellite(SatelliteId.generate(), "   ", orbit)
        );
    }

    @Test
    void shouldFailToCreateOrbitWithNegativeAltitude() {
        assertThrows(IllegalArgumentException.class, () ->
                new Orbit(-10.0, 51.6, 92.0)
        );
    }

    @Test
    void shouldFailToCreateTelemetryWithInvalidBattery() {
        assertThrows(IllegalArgumentException.class, () ->
                new Telemetry(0.0, 0.0, 7.5, 105, Instant.now())
        );
    }

    @Test
    void shouldUpdateTelemetryOnActiveSatellite() {
        Satellite satellite = new Satellite(SatelliteId.generate(), "ISS", new Orbit(400.0, 51.6, 92.0));
        Telemetry telemetry = new Telemetry(45.0, 90.0, 7.6, 99, Instant.now());

        satellite.updateTelemetry(telemetry);

        assertEquals(telemetry, satellite.getLatestTelemetry());
    }

    @Test
    void shouldFailToUpdateTelemetryOnDecommissionedSatellite() {
        Satellite satellite = new Satellite(SatelliteId.generate(), "ISS", new Orbit(400.0, 51.6, 92.0));
        satellite.decommission();

        Telemetry telemetry = new Telemetry(45.0, 90.0, 7.6, 99, Instant.now());

        assertThrows(IllegalStateException.class, () -> satellite.updateTelemetry(telemetry));
    }

    @Test
    void shouldDetectCollisionRisk() {
        CollisionRiskService riskService = new CollisionRiskService();

        Satellite sat1 = new Satellite(SatelliteId.generate(), "Sat A", new Orbit(400.0, 50.0, 90.0));
        Satellite sat2 = new Satellite(SatelliteId.generate(), "Sat B", new Orbit(405.0, 50.5, 90.0)); // Close orbits
        Satellite sat3 = new Satellite(SatelliteId.generate(), "Sat C", new Orbit(500.0, 50.0, 90.0)); // Far orbit

        assertTrue(riskService.isCollisionRisk(sat1, sat2));
        assertFalse(riskService.isCollisionRisk(sat1, sat3));
    }
}
