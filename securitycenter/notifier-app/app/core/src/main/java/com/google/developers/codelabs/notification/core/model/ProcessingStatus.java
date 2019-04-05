package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.MoreObjects;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class ProcessingStatus.
 */
@Entity
public class ProcessingStatus {

  /** The Constant KEY_VALUE. */
  public static final String KEY_VALUE = "processing_status_key";

  /** The entity key. */
  @Id
  public String entityKey;

  /** The status. */
  public ProcessingStatusOptions status;

  /**
   * Instantiates a new processing status.
   */
  public ProcessingStatus() {}

  /**
   * Instantiates a new processing status.
   *
   * @param status the status
   */
  public ProcessingStatus(ProcessingStatusOptions status) {
    this.entityKey = KEY_VALUE;
    this.status = status;
  }

  /**
   * Instantiates a new processing status.
   *
   * @param entityKey the entity key
   * @param status the status
   */
  public ProcessingStatus(String entityKey, ProcessingStatusOptions status) {
    this.entityKey = entityKey;
    this.status = status;
  }

  /**
   * Gets the status.
   *
   * @return the status
   */
  public ProcessingStatusOptions getStatus() {
    return status;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("status", status)
        .toString();
  }

  /**
   * Gets the entity key.
   *
   * @return the entity key
   */
  public String getEntityKey() {
    return entityKey;
  }

}
