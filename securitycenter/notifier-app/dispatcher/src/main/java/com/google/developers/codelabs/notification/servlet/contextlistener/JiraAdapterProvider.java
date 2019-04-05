package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.jira.JiraNotificationAdapter;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.inject.Inject;
import com.google.inject.Provider;

/**
 * The Class JiraAdapterProvider.
 */
public class JiraAdapterProvider implements Provider<NotificationAdapter> {
  private final ConfigurationService configurationService;

  /**
   * Instantiates a new sendgrid email adapter provider.
   * @param configurationService configuration service.
   */
  @Inject
  public JiraAdapterProvider(ConfigurationService configurationService) {
    this.configurationService = configurationService;
  }

  @Override
  public NotificationAdapter get() {
    return new JiraNotificationAdapter(configurationService);
  }

}
