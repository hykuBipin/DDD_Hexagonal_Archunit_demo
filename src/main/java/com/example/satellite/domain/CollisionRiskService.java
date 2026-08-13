package com.example.satellite.domain;

import com.example.satellite.domain.ddd.DomainService;

/**
 * Domain Service to detect collision risks between satellites.
 * In DDD, Domain Services contain business logic that doesn't naturally belong to a single Entity or Value Object,
 * often because it coordinates operations across multiple aggregates.
 */
@DomainService("Collision Risk Domain Service")
public class CollisionRiskService {

    private static final double MIN_SAFE_ALTITUDE_DIFF_KM = 10.0;
    private static final double MIN_SAFE_INCLINATION_DIFF_DEG = 1.0;

    /**
     * Calculates if there is a collision risk between two active satellites based on their orbits.
     */
    public boolean isCollisionRisk(Satellite first, Satellite second) {
        // Decommissioned satellites or the same satellite are not checked for collision
        if (first.equals(second) || first.isDecommissioned() || second.isDecommissioned()) {
            return false;
        }

        return first.getOrbit().isCloseTo(
                second.getOrbit(),
                MIN_SAFE_ALTITUDE_DIFF_KM,
                MIN_SAFE_INCLINATION_DIFF_DEG
        );
    }
}
