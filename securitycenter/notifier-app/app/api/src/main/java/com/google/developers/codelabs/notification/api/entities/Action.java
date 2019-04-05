package com.google.developers.codelabs.notification.api.entities;

import com.google.common.base.MoreObjects;

/**
 * The Class Actions.
 */
public class Action {

  private String type;

  /**
   * Gets the type.
   *
   * @return the type
   */
  public String getType() {
    return type;
  }

  /**
   * Sets the type.
   *
   * @param type the new type
   */
  public void setType(String type) {
    this.type = type;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("type", type)
        .toString();
  }
}
