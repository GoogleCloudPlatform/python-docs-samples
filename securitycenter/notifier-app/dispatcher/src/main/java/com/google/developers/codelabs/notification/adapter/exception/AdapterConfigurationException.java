package com.google.developers.codelabs.notification.adapter.exception;

/**
 * Exception to represent adapter configuration exceptions.
 *
 * @author dandrade
 *
 */
public class AdapterConfigurationException extends RuntimeException {

  /**
   *
   */
  private static final long serialVersionUID = 1L;

  /**
   * Base Constructor.
   *
   * @param message Exception message
   * @param cause Original Exception
   */
  public AdapterConfigurationException(String message, Throwable cause) {
    super(message, cause);
  }

}
