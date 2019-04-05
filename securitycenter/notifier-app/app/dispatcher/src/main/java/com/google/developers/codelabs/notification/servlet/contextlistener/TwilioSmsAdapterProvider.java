package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.sms.TwilioSmsAdapter;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.inject.Inject;
import com.google.inject.Provider;

/**
 * The Class TwilioSmsAdapterProvider.
 */
public class TwilioSmsAdapterProvider implements Provider<NotificationAdapter> {
  private final ConfigurationService configurationService;

  /**
   * Instantiates a new twilio sms adapter provider.
   * @param configurationService configuration service.
   */
  @Inject
  public TwilioSmsAdapterProvider(ConfigurationService configurationService) {
    this.configurationService = configurationService;
  }

  @Override
  public NotificationAdapter get() {
    return new TwilioSmsAdapter(configurationService);
  }

}
