package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.api.services.pubsub.Pubsub;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.mailer.gae.AppengineMailSender;
import com.google.developers.codelabs.notification.binder.Appengine;
import com.google.developers.codelabs.notification.binder.Jira;
import com.google.developers.codelabs.notification.binder.Sendgrid;
import com.google.developers.codelabs.notification.binder.Twilio;
import com.google.developers.codelabs.notification.cloudfunction.CloudFunctionExecutor;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.core.service.DataStoreService;
import com.google.developers.codelabs.notification.filter.NamespaceFilter;
import com.google.developers.codelabs.notification.helper.QueueHelper;
import com.google.developers.codelabs.notification.service.NotificationService;
import com.google.developers.codelabs.notification.service.PubsubCommunication;
import com.google.developers.codelabs.notification.service.PubsubPuller;
import com.google.developers.codelabs.notification.servlet.SecurityHeaderVerifier;
import com.google.developers.codelabs.util.PropertyManager;
import com.google.developers.codelabs.util.PropertyReader;
import com.google.developers.codelabs.util.SystemPropertyReader;
import com.google.inject.AbstractModule;
import com.google.inject.Singleton;

import com.googlecode.objectify.ObjectifyFilter;

/**
 * The Class NotifyModule.
 */
public class NotifyModule extends AbstractModule {

  @Override
  protected void configure() {
    bind(NotificationAdapter.class)
        .annotatedWith(Sendgrid.class)
        .toProvider(SendgridEmailAdapterProvider.class);

    bind(NotificationAdapter.class)
        .annotatedWith(Appengine.class)
        .toProvider(AppEngineEmailAdapterProvider.class);
    bind(AppengineMailSender.class);

    bind(NotificationAdapter.class)
        .annotatedWith(Twilio.class)
        .toProvider(TwilioSmsAdapterProvider.class);

    bind(NotificationAdapter.class)
        .annotatedWith(Jira.class)
        .toProvider(JiraAdapterProvider.class);

    bind(PropertyReader.class).to(SystemPropertyReader.class);
    bind(Pubsub.class).toProvider(PubsubProvider.class);

    bind(DataStoreService.class);
    bind(NotificationService.class);
    bind(PropertyManager.class);
    bind(PubsubCommunication.class);
    bind(PubsubPuller.class);
    bind(QueueHelper.class);
    bind(SecurityHeaderVerifier.class);
    bind(ConfigurationService.class);
    bind(CloudFunctionExecutor.class);

    bind(ObjectifyFilter.class).in(Singleton.class);
    bind(NamespaceFilter.class).in(Singleton.class);
  }

}
