package com.google.developers.codelabs.notification.guice;

import static org.junit.Assert.assertNotNull;

import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.binder.Appengine;
import com.google.developers.codelabs.notification.binder.Sendgrid;
import com.google.developers.codelabs.notification.service.PubsubCommunication;
import com.google.developers.codelabs.notification.servlet.ReceiveMessageServlet;
import com.google.developers.codelabs.notification.servlet.contextlistener.NotifyModule;
import com.google.developers.codelabs.notification.servlet.contextlistener.NotifyServletModule;
import com.google.inject.AbstractModule;
import com.google.inject.Guice;
import com.google.inject.Inject;
import com.google.inject.Injector;
import com.google.inject.servlet.ServletModule;

import org.junit.Before;
import org.junit.Test;

/**
 * The Class GuiceIntegration.
 */
@SuppressWarnings("javadoc")
public class GuiceIntegration {
  private Injector injector;

  /** The appengine email adapter. */
  @Inject
  @Appengine
  NotificationAdapter appengineEmailAdapter;

  /** The send grid email adapter. */
  @Inject
  @Sendgrid
  NotificationAdapter sendGridEmailAdapter;

  /** The receive message servlet. */
  @Inject
  ReceiveMessageServlet receiveMessageServlet;

  /** The pubsub communication. */
  @Inject
  PubsubCommunication pubsubCommunication;

  @Before
  public void setup() {
    ServletModule servletModule = new NotifyServletModule();
    AbstractModule applicationModule = new NotifyModule();
    this.injector = Guice.createInjector(servletModule, applicationModule);
    this.injector.injectMembers(this);
  }

  @Test
  public void validateGuiceInjector() {
    assertNotNull(sendGridEmailAdapter);
    assertNotNull(appengineEmailAdapter);
    assertNotNull(receiveMessageServlet);
    assertNotNull(pubsubCommunication);
  }

}
