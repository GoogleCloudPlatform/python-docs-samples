package com.google.developers.codelabs.util;

/**
 * The Class SystemPropertyReader.
 */
public class SystemPropertyReader implements PropertyReader {
  @Override
  public String getProperty(String propertyName) {
    return System.getenv(propertyName);
  }
}
