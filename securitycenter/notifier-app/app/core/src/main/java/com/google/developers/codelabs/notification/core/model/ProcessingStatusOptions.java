package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.Strings;

/**
 * The Enum ProcessingStatusOptions.
 */
public enum ProcessingStatusOptions {

  /** The start. */
  START,
  /** The stop. */
  STOP,
  /** The unknown. */
  UNKNOWN;

  /**
   * From status.
   *
   * @param status the status
   * @return the processing status options
   */
  public static ProcessingStatusOptions fromStatus(String status) {

    switch (Strings.nullToEmpty(status).trim().toUpperCase()) {
      case "START":
        return START;
      case "STOP":
        return STOP;
      default:
        return UNKNOWN;
    }
  }
}
