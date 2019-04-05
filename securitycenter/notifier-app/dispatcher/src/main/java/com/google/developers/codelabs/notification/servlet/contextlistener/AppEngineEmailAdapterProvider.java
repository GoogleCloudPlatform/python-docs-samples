package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.mailer.gae.AppengineMailAdapter;
import com.google.developers.codelabs.notification.adapter.mailer.gae.AppengineMailSender;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.inject.Inject;
import com.google.inject.Provider;

/**
 * The Class AppEngineEmailAdapterProvider.
 */
public class AppEngineEmailAdapterProvider implements Provider<NotificationAdapter> {
  private final AppengineMailSender sender;
  private final ConfigurationService configurationService;

  /**
   * Instantiates a new app engine email adapter provider.
   * @param sender
   * @param configurationService
   */
  @Inject
  public AppEngineEmailAdapterProvider(
      AppengineMailSender sender,
      ConfigurationService configurationService) {
    super();
    this.sender = sender;
    this.configurationService = configurationService;
  }

  @Override
  public NotificationAdapter get() {
    return new AppengineMailAdapter(sender, configurationService);
  }

}
