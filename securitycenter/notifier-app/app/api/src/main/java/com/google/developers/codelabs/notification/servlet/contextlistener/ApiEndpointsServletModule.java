package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.api.control.ServiceManagementConfigFilter;
import com.google.api.control.extensions.appengine.GoogleAppEngineControlFilter;
import com.google.api.server.spi.guice.EndpointsModule;
import com.google.common.collect.ImmutableList;
import com.google.developers.codelabs.notification.api.Notification;
import com.google.developers.codelabs.notification.filter.NamespaceFilter;

import com.googlecode.objectify.ObjectifyFilter;

import java.util.HashMap;
import java.util.Map;

/**
 * The Class ApiEndpointsServletModule.
 */
public class ApiEndpointsServletModule extends EndpointsModule {
  @Override
  protected void configureServlets() {

    Map<String, String> params = new HashMap<>();
    params.put("endpoints.projectId", System.getenv("ENDPOINTS_PROJECT_ID"));
    params.put("endpoints.serviceName", System.getenv("ENDPOINTS_SERVICE_NAME"));

    filter("/_ah/api/*").through(GoogleAppEngineControlFilter.class, params);

    filter("/_ah/api/*").through(ServiceManagementConfigFilter.class);

    configureEndpoints("/_ah/api/*", ImmutableList.of(Notification.class));

    filter("/*").through(ObjectifyFilter.class);
    filter("/*").through(NamespaceFilter.class);
  }

}
