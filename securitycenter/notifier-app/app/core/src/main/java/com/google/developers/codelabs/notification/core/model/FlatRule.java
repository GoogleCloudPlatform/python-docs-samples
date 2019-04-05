package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class FlatRule.
 */
@Entity
public class FlatRule {

  /** The type. */
  @Id
  public String type;

  /** The all action. */
  public ActionType allAction;

  /** The created action. */
  public ActionType createdAction;

  /** The deleted action. */
  public ActionType deletedAction;

  /** The modified action. */
  public ActionType modifiedAction;
  
  public ActionType activeAction;
  
  public ActionType openedAction;
  
  public ActionType resolvedAction;

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
   * Gets the all action.
   *
   * @return the all action
   */
  public ActionType getAllAction() {
    return allAction;
  }

  /**
   * Sets the all action.
   *
   * @param allAction the new all action
   */
  public void setAllAction(ActionType allAction) {
    this.allAction = allAction;
  }

  /**
   * Gets the created action.
   *
   * @return the created action
   */
  public ActionType getCreatedAction() {
    return createdAction;
  }

  /**
   * Sets the created action.
   *
   * @param createdAction the new created action
   */
  public void setCreatedAction(ActionType createdAction) {
    this.createdAction = createdAction;
  }

  /**
   * Gets the deleted action.
   *
   * @return the deleted action
   */
  public ActionType getDeletedAction() {
    return deletedAction;
  }

  /**
   * Sets the deleted action.
   *
   * @param deletedAction the new deleted action
   */
  public void setDeletedAction(ActionType deletedAction) {
    this.deletedAction = deletedAction;
  }

  /**
   * Gets the modified action.
   *
   * @return the modified action
   */
  public ActionType getModifiedAction() {
    return modifiedAction;
  }

  /**
   * Sets the modified action.
   *
   * @param modifiedAction the new modified action
   */
  public void setModifiedAction(ActionType modifiedAction) {
    this.modifiedAction = modifiedAction;
  }

public ActionType getActiveAction() {
	return activeAction;
}

public void setActiveAction(ActionType activeAction) {
	this.activeAction = activeAction;
}

public ActionType getOpenedAction() {
	return openedAction;
}

public void setOpenedAction(ActionType openedAction) {
	this.openedAction = openedAction;
}

public ActionType getResolvedAction() {
	return resolvedAction;
}

public void setResolvedAction(ActionType resolvedAction) {
	this.resolvedAction = resolvedAction;
}

}
