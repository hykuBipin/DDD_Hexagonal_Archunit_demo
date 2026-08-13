package com.example.satellite.infrastructure.adapters.output.persistence;

import com.example.satellite.domain.Satellite;
import com.example.satellite.domain.SatelliteId;
import com.example.satellite.domain.SatelliteRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Driven Output Adapter for In-Memory / Java Default Storage.
 * Implements the SatelliteRepository output port interface.
 */
public class InMemorySatelliteRepository implements SatelliteRepository {

    private final Map<SatelliteId, Satellite> storage = new ConcurrentHashMap<>();

    @Override
    public void save(Satellite satellite) {
        System.out.println("[IN-MEMORY DB] Saving satellite: " + satellite.getName() + " (ID: " + satellite.getId() + ")");
        storage.put(satellite.getId(), satellite);
    }

    @Override
    public Optional<Satellite> findById(SatelliteId id) {
        System.out.println("[IN-MEMORY DB] Finding satellite by ID: " + id);
        return Optional.ofNullable(storage.get(id));
    }

    @Override
    public List<Satellite> findAll() {
        System.out.println("[IN-MEMORY DB] Retrieving all satellites");
        return new ArrayList<>(storage.values());
    }
}
