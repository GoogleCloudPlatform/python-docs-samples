package com.google.developers.codelabs.notification.adapter.exception;

/**
 * Exception to represent adapter execution exceptions.
 *
 * @author dandrade
 *
 */
public class AdapterExecutionException extends RuntimeException {

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
  public AdapterExecutionException(String message, Throwable cause) {
    super(message, cause);
  }

  /**
   * Instantiates a new adapter execution exception.
   *
   * @param message the message
   */
  public AdapterExecutionException(String message) {
    super(message);
  }

}
