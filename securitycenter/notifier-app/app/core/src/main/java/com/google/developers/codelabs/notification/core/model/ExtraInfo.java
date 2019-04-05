package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class ExtraInfo.
 */
@Entity
public class ExtraInfo {

  /** The Constant KEY_VALUE. */
  public static final String KEY_VALUE = "extra_info_key";

  /** The entity key. */
  @Id
  public String entityKey;

  /** The type. */
  public NotificationType type;

  /** The info. */
  public String info;

  /**
   * Instantiates a new extra info.
   */
  public ExtraInfo() {}

  /**
   * Instantiates a new extra info.
   *
   * @param type the type
   * @param info the info
   */
  public ExtraInfo(NotificationType type, String info) {
    this.type = type;
    this.entityKey = KEY_VALUE + "_" + type.name();
    this.info = info;
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
   * Gets the type.
   *
   * @return the type
   */
  public NotificationType getType() {
    return type;
  }

  /**
   * Gets the key by type.
   *
   * @param type the type
   * @return the key by type
   */
  public static String getKeyByType(NotificationType type) {
    return KEY_VALUE + "_" + type.name();
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
