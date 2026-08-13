package com.example.satellite.infrastructure.adapters.output.persistence;

import com.example.satellite.domain.Orbit;
import com.example.satellite.domain.Satellite;
import com.example.satellite.domain.SatelliteId;
import com.example.satellite.domain.SatelliteRepository;
import com.example.satellite.domain.Telemetry;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Driven Output Adapter for Oracle Database.
 * Implements the SatelliteRepository output port interface.
 * Simulates SQL generation, connection logging, and transactional behavior of an Oracle Database driver.
 */
public class OracleSatelliteRepository implements SatelliteRepository {

    private final Map<SatelliteId, Satellite> mockOracleTables = new ConcurrentHashMap<>();

    @Override
    public void save(Satellite satellite) {
        System.out.println("[ORACLE DB] Connecting to Oracle Database Instance (SID: XE, Port: 1521)...");
        System.out.println("[ORACLE DB] EXECUTING SQL MERGE STATEMENT:");
        
        String mergeSql = """
            MERGE INTO SATELLITES target
            USING (SELECT '%s' AS id, '%s' AS name, %f AS altitude, %f AS inclination, %f AS period FROM dual) source
            ON (target.id = source.id)
            WHEN MATCHED THEN
              UPDATE SET target.decommissioned = %d
            WHEN NOT MATCHED THEN
              INSERT (id, name, altitude, inclination, period, decommissioned)
              VALUES (source.id, source.name, source.altitude, source.inclination, source.period, 0);
            """;
        
        System.out.printf(mergeSql, 
                satellite.getId(), 
                satellite.getName(), 
                satellite.getOrbit().altitudeKm(), 
                satellite.getOrbit().inclinationDegrees(), 
                satellite.getOrbit().periodMinutes(),
                satellite.isDecommissioned() ? 1 : 0
        );

        if (satellite.getLatestTelemetry() != null) {
            System.out.println("[ORACLE DB] EXECUTING TELEMETRY INSERT STATEMENT:");
            String telemetrySql = """
                INSERT INTO SATELLITE_TELEMETRY (id, latitude, longitude, speed, battery, logged_at)
                VALUES ('%s', %f, %f, %f, %d, TO_TIMESTAMP('%s', 'YYYY-MM-DD"T"HH24:MI:SS.FF3"Z"'));
                """;
            System.out.printf(telemetrySql,
                    satellite.getId(),
                    satellite.getLatestTelemetry().latitude(),
                    satellite.getLatestTelemetry().longitude(),
                    satellite.getLatestTelemetry().speedKms(),
                    satellite.getLatestTelemetry().batteryPercentage(),
                    satellite.getLatestTelemetry().timestamp()
            );
        }
        
        System.out.println("[ORACLE DB] Transaction committed.");
        mockOracleTables.put(satellite.getId(), satellite);
    }

    @Override
    public Optional<Satellite> findById(SatelliteId id) {
        System.out.println("[ORACLE DB] Connecting to Oracle Database...");
        System.out.println("[ORACLE DB] EXECUTING SQL QUERY:");
        System.out.printf("SELECT * FROM SATELLITES WHERE id = '%s';\n", id);
        return Optional.ofNullable(mockOracleTables.get(id));
    }

    @Override
    public List<Satellite> findAll() {
        System.out.println("[ORACLE DB] Connecting to Oracle Database...");
        System.out.println("[ORACLE DB] EXECUTING SQL QUERY:");
        System.out.println("SELECT * FROM SATELLITES;");
        return new ArrayList<>(mockOracleTables.values());
    }
}
