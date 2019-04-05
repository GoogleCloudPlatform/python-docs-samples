package com.google.developers.codelabs.notification.api.entities;

import com.google.api.server.spi.config.AnnotationBoolean;
import com.google.api.server.spi.config.ApiResourceProperty;

import java.util.Map;

/**
 * The Class ConfigurationRequestBody.
 */
public class ConfigurationRequestBody {

  private Map<String, String> configuration;

  /**
   * Gets the configuration.
   *
   * @return the configuration
   */
  public Map<String, String> getConfiguration() {
    return configuration;
  }

  /**
   * Sets the configuration.
   *
   * @param configuration the configuration
   */
  public void setConfiguration(Map<String, String> configuration) {
    this.configuration = configuration;
  }

  /**
   * Checks if is empty.
   *
   * @return true, if is empty
   */
  @ApiResourceProperty(ignored = AnnotationBoolean.TRUE)
  public boolean isEmpty() {
    return configuration == null || configuration.isEmpty();
  }
}
