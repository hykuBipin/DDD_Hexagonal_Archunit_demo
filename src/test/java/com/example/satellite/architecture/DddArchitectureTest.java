package com.example.satellite.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.core.importer.Location;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.library.Architectures.layeredArchitecture;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.slices;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

/**
 * Architecture tests using ArchUnit.
 * These tests automatically verify and enforce Hexagonal Architecture package boundaries.
 * We exclude the Main.java composer class from analysis, as it is the bootstrap root that wires the dependencies together.
 */
@AnalyzeClasses(
        packages = "com.example.satellite",
        importOptions = {ImportOption.DoNotIncludeTests.class, DddArchitectureTest.ExcludeMainComposer.class}
)
public class DddArchitectureTest {

    /**
     * Excludes the Main class composer from architectural rules checks,
     * since the bootstrap composer must instantiate all ports and adapters to wire them.
     */
    public static class ExcludeMainComposer implements ImportOption {
        @Override
        public boolean includes(Location location) {
            return !location.contains("com/example/satellite/Main.class");
        }
    }

    /**
     * Enforces Hexagonal Architecture boundaries:
     * - Domain Layer has zero dependencies.
     * - Application Layer (Input Ports) depends only on Domain.
     * - Adapters (Input & Output) depend only on Core layers (Domain & Application).
     */
    @ArchTest
    public static final ArchRule hexagonal_layers_should_be_respected = layeredArchitecture()
            .consideringAllDependencies()
            .layer("Domain").definedBy("com.example.satellite.domain..")
            .layer("Application").definedBy("com.example.satellite.application..")
            .layer("InputAdapters").definedBy("com.example.satellite.infrastructure.adapters.input..")
            .layer("OutputAdapters").definedBy("com.example.satellite.infrastructure.adapters.output..")

            .whereLayer("Domain").mayOnlyBeAccessedByLayers("Application", "InputAdapters", "OutputAdapters")
            .whereLayer("Application").mayOnlyBeAccessedByLayers("InputAdapters", "OutputAdapters")
            .whereLayer("InputAdapters").mayNotBeAccessedByAnyLayer()
            .whereLayer("OutputAdapters").mayNotBeAccessedByAnyLayer();

    /**
     * Enforces the boundary that Input Adapters (Driving) must NOT depend on Output Adapters (Driven).
     * Input adapters must only interact via Ports (interfaces).
     */
    @ArchTest
    public static final ArchRule input_adapters_should_not_depend_on_output_adapters = noClasses()
            .that().resideInAPackage("com.example.satellite.infrastructure.adapters.input..")
            .should().dependOnClassesThat().resideInAPackage("com.example.satellite.infrastructure.adapters.output..");

    /**
     * Prevent cyclic dependencies between subpackages.
     */
    @ArchTest
    public static final ArchRule no_cycles_between_slices = slices()
            .matching("com.example.satellite.(*)..")
            .should().beFreeOfCycles();
}
