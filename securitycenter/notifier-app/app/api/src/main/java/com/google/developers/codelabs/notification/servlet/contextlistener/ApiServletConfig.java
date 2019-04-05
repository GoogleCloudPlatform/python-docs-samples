package com.google.developers.codelabs.notification.servlet.contextlistener;

import javax.servlet.annotation.WebListener;

import com.google.inject.AbstractModule;
import com.google.inject.Guice;
import com.google.inject.Injector;
import com.google.inject.servlet.GuiceServletContextListener;
import com.google.inject.servlet.ServletModule;

/**
 * The Class ApiServletConfig.
 */
@WebListener
public class ApiServletConfig extends GuiceServletContextListener {

  @Override
  protected Injector getInjector() {
    ServletModule servletModule = new ApiEndpointsServletModule();
    AbstractModule applicationModule = new ApiModule();
    return Guice.createInjector(servletModule, applicationModule);
  }

}
