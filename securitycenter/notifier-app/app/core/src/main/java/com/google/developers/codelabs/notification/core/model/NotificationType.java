package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.Strings;

/**
 * The Enum NotificationType.
 */
public enum NotificationType {

  /** The assets. */
  ASSETS,
  /** The findings. */
  FINDINGS,
  /** The scan configurations. */
  SCAN_CONFIGURATIONS,
  /** The scan findings. */
  SCAN_FINDINGS,
  /** The cloud function. */
  CLOUD_FUNCTION,
  /** The unknown. */
  UNKNOWN;

  /**
   * Form notification.
   *
   * @param notificationType the notification type
   * @return the notification type. UNKNOWN if none matches
   */
  public static NotificationType formNotification(String notificationType) {

    switch (Strings.nullToEmpty(notificationType).trim().toUpperCase()) {
      case "ASSETS":
        return ASSETS;
      case "FINDINGS":
        return FINDINGS;
      case "SCAN_CONFIGURATIONS":
      case "SCAN-CONFIGURATIONS":
        return SCAN_CONFIGURATIONS;
      case "SCAN_FINDINGS":
      case "SCAN-FINDINGS":
        return SCAN_FINDINGS;
      case "CLOUD-FUNCTION":
      case "CLOUD_FUNCTION":
        return CLOUD_FUNCTION;
      default:
        return UNKNOWN;
    }
  }
}
