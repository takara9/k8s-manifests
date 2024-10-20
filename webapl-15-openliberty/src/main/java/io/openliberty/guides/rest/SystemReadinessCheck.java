//package io.openliberty.sample.system;
package io.openliberty.guides.rest;

import javax.enterprise.context.ApplicationScoped;

import javax.inject.Inject;
import javax.inject.Provider;

import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.health.Readiness;
import org.eclipse.microprofile.health.HealthCheck;
import org.eclipse.microprofile.health.HealthCheckResponse;

@Readiness
@ApplicationScoped
public class SystemReadinessCheck implements HealthCheck {

    //private static final String READINESS_CHECK = SystemResource.class.getSimpleName()
    //                                             + " Readiness Check";

    private static final String READINESS_CHECK = " Readiness Check";
    @Inject
    @ConfigProperty(name = "io_openliberty_guides_system_inMaintenance")
    Provider<String> inMaintenance;

    @Override
    public HealthCheckResponse call() {

	UpTime uptime = new UpTime();
	System.out.println("up time = " + uptime.getUpTime());

        //if (inMaintenance != null && inMaintenance.get().equalsIgnoreCase("true")) {
	if ( uptime.getUpTime() < 30 ) {
            return HealthCheckResponse.down(READINESS_CHECK);
	}
        return HealthCheckResponse.up(READINESS_CHECK);
    }

}
