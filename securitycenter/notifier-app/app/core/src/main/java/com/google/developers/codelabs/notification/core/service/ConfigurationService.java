package com.google.developers.codelabs.notification.core.service;

import com.google.developers.codelabs.notification.core.model.Configuration;
import com.google.inject.Inject;

/**
 * The Class ConfigurationService.
 */
public class ConfigurationService {

  private DataStoreService service;

  /**
   * Constructor.
   * @param service
   */
  @Inject
  public ConfigurationService(DataStoreService service) {
    this.service = service;
  }

  /**
   * Gets the configuration value.
   *
   * @param key the key
   * @return the configuration value
   */
  public String getConfig(String key) {
    Configuration channelConfiguration = service.getConfiguration();
    if (channelConfiguration != null && channelConfiguration.getConfiguration() != null) {
      return channelConfiguration.getConfiguration().get(key);
    }
    return null;
  }


}
