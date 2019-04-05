package com.google.developers.codelabs.notification.api.entities;

/**
 * The Class StatusRequest.
 */
public class StatusRequest {

  private String status;

  /**
   * Gets the status.
   *
   * @return the status
   */
  public String getStatus() {
    return status;
  }

  /**
   * Sets the status.
   *
   * @param status the new status
   */
  public void setStatus(String status) {
    this.status = status;
  }

  @Override
  public String toString() {
    return "StatusRequest [status=" + status + "]";
  }
}
