package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

import java.util.Map;

/**
 * The Class ChannelConfiguration.
 */
@Entity
public class Configuration {

  /** The Constant KEY_VALUE. */
  public static final String KEY_VALUE = "configuration_key";

  /** The entity key. */
  @Id
  public String entityKey;

  /** The configuration. */
  public Map<String, String> configuration;

  /**
   * Instantiates a new configuration.
   */
  public Configuration() {}

  /**
   * Instantiates a new configuration.
   *
   * @param configuration the configuration
   */
  public Configuration(Map<String, String> configuration) {
    this.entityKey = KEY_VALUE;
    this.configuration = configuration;
  }

  /**
   * Gets the configuration.
   *
   * @return the configuration
   */
  public Map<String, String> getConfiguration() {
    return configuration;
  }


}
