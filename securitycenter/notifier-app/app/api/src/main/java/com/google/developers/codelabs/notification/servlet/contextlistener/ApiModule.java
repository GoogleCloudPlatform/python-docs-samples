package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.api.control.ServiceManagementConfigFilter;
import com.google.api.control.extensions.appengine.GoogleAppEngineControlFilter;
import com.google.developers.codelabs.notification.core.service.DataStoreService;
import com.google.developers.codelabs.notification.filter.NamespaceFilter;
import com.google.inject.AbstractModule;
import com.google.inject.Singleton;

import com.googlecode.objectify.ObjectifyFilter;

/**
 * The Class ApiModule.
 */
public class ApiModule extends AbstractModule {

  @Override
  protected void configure() {
    bind(DataStoreService.class);
    bind(ObjectifyFilter.class).in(Singleton.class);
    bind(NamespaceFilter.class).in(Singleton.class);
    bind(GoogleAppEngineControlFilter.class).in(Singleton.class);
    bind(ServiceManagementConfigFilter.class).in(Singleton.class);
  }

}
