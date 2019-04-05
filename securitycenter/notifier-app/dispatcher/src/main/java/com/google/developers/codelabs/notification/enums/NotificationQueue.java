package com.google.developers.codelabs.notification.enums;

/**
 * The Enum NotificationQueue.
 */
public enum NotificationQueue {

  /** The entry. */
  ENTRY("/queue/pubsub/entry", "entry");

  private String url;
  private String queueName;

  private NotificationQueue(String url, String queueName) {
    this.url = url;
    this.queueName = queueName;
  }

  /**
   * Gets the url.
   *
   * @return the url
   */
  public String getUrl() {
    return url;
  }

  /**
   * Gets the queue name.
   *
   * @return the queue name
   */
  public String getQueueName() {
    return queueName;
  }
}
