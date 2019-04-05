package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class MessageId.
 */
@Entity
public class MessageId {

  /** The message id. */
  @Id
  public String messageId;

  /**
   * Gets the message id.
   *
   * @return the message id
   */
  public String getMessageId() {
    return messageId;
  }

  /**
   * Instantiates a new message id.
   */
  public MessageId() {}

  /**
   * Instantiates a new message id.
   *
   * @param messageId the message id
   */
  public MessageId(String messageId) {
    super();
    this.messageId = messageId;
  }

}
