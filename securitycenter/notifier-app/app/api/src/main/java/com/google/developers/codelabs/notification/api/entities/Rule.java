package com.google.developers.codelabs.notification.api.entities;

import com.google.common.base.MoreObjects;

import java.util.List;

/**
 * The Class Rule.
 */
public class Rule {

  private String type;
  private List<Action> actions;

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

  /**
   * Gets the actions.
   *
   * @return the actions
   */
  public List<Action> getActions() {
    return actions;
  }

  /**
   * Sets the actions.
   *
   * @param actions the new actions
   */
  public void setActions(List<Action> actions) {
    this.actions = actions;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("type", type)
        .add("actions", actions)
        .toString();
  }
}
