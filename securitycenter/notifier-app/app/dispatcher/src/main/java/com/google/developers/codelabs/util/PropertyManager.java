package com.google.developers.codelabs.util;

import com.google.common.base.Preconditions;
import com.google.common.base.Strings;
import com.google.inject.Inject;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class PropertyManager.
 */
public class PropertyManager {
  private static final Logger LOG = Logger.getLogger(PropertyManager.class.getName());
  private static final String NOT_CONFIGURED = "[%s] is not configured";
  private PropertyReader reader;

  /**
   * Constructor with dependencies.
   *
   * @param reader the reader
   */
  @Inject
  public PropertyManager(PropertyReader reader) {
    super();
    this.reader = reader;
  }

  /**
   * Read a environment variable that must be configured.
   *
   * @param environmentVariable the environment variable
   * @return the required property
   * @throws IllegalStateException if the environmentvariable is not null
   */
  public String getRequiredProperty(String environmentVariable) {
    String value = reader.getProperty(environmentVariable);
    boolean nullOrEmpty = Strings.isNullOrEmpty(value);
    if (nullOrEmpty) {
      String message = String.format(NOT_CONFIGURED, environmentVariable);
      Preconditions.checkState(!nullOrEmpty, message);
    }
    return value;
  }

  /**
   * Reads a environment variable.
   *
   * @param propertyName the environment variable
   * @return the property
   */
  public String getProperty(String propertyName) {
    String value = reader.getProperty(propertyName);
    LOG.log(Level.FINEST, String.format("Property READ - %s=[%s]", propertyName, value));
    return value;
  }

}
