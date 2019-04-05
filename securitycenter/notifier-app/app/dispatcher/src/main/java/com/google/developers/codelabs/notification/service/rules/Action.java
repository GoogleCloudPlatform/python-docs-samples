package com.google.developers.codelabs.notification.service.rules;

import com.google.developers.codelabs.notification.core.model.ActionType;

/**
 * The Class Action.
 */
public class Action {

  private ActionType type;

  /**
   * Instantiates a new action.
   *
   * @param type the type
   */
  public Action(ActionType type) {
    this.type = type;
  }

  /**
   * Gets the type.
   *
   * @return the type
   */
  public ActionType getType() {
    return type;
  }

}
