package com.example.satellite.domain;

import java.util.List;
import java.util.Optional;

/**
 * Repository interface for managing Satellites.
 * In DDD, the repository interface belongs to the Domain Layer. 
 * This keeps the Domain Layer independent of storage/database technologies (Infrastructure).
 */
public interface SatelliteRepository {
    
    /**
     * Saves a satellite aggregate.
     */
    void save(Satellite satellite);

    /**
     * Finds a satellite by its unique ID.
     */
    Optional<Satellite> findById(SatelliteId id);

    /**
     * Retrieves all registered satellites.
     */
    List<Satellite> findAll();
}
