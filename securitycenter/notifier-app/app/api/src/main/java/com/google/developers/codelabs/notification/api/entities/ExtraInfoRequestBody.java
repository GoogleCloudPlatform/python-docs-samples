package com.google.developers.codelabs.notification.api.entities;

import com.google.common.base.MoreObjects;

/**
 * The Class ExtraInfoRequestBody.
 */
public class ExtraInfoRequestBody {

  private String notificationType;
  private String info;

  /**
   * Gets the notification type.
   *
   * @return the notification type
   */
  public String getNotificationType() {
    return notificationType;
  }

  /**
   * Sets the notification type.
   *
   * @param notificationType the new notification type
   */
  public void setNotificationType(String notificationType) {
    this.notificationType = notificationType;
  }

  /**
   * Gets the info.
   *
   * @return the info
   */
  public String getInfo() {
    return info;
  }

  /**
   * Sets the info.
   *
   * @param info the new info
   */
  public void setInfo(String info) {
    this.info = info;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("info", info)
        .add("notificationType", notificationType)
        .toString();
  }
}
