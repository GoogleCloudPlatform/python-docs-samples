package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.Strings;

/**
 * The Enum ActionType.
 */
public enum ActionType {

  /** The all. */
  ALL,
  /** The any created. */
  ANY_CREATED,
  /** The any deleted. */
  ANY_DELETED,
  /** The any modified. */
  ANY_MODIFIED,
  /** The any active. */
  ANY_ACTIVE,
  /** The any opened. */
  ANY_OPENED,
  /** The any resolved. */
  ANY_RESOLVED,
  /** The unknown. */
  UNKNOWN;

  /** The Constant MODIFIED_EVENT_TEXT. */
  public static final String MODIFIED_EVENT_TEXT = "MODIFIED";

  /** The Constant DELETED_EVENT_TEXT. */
  public static final String DELETED_EVENT_TEXT = "DELETED";

  /** The Constant CREATED_EVENT_TEXT. */
  public static final String CREATED_EVENT_TEXT = "CREATED";
  
  public static final String ACTIVE_EVENT_TEXT = "ACTIVE";
  
  public static final String OPENED_EVENT_TEXT = "OPENED";
  
  public static final String RESOLVED_EVENT_TEXT = "RESOLVED";

  /**
   * Create an ActionType from an event type.
   *
   * @param text the text
   * @return the action type
   */
  public static ActionType fromEventType(String text) {

    switch (Strings.nullToEmpty(text).trim().toUpperCase()) {
      case CREATED_EVENT_TEXT:
        return ANY_CREATED;
      case DELETED_EVENT_TEXT:
        return ANY_DELETED;
      case MODIFIED_EVENT_TEXT:
        return ANY_MODIFIED;
      case ACTIVE_EVENT_TEXT:
          return ANY_ACTIVE;
      case OPENED_EVENT_TEXT:
          return ANY_OPENED;
      case RESOLVED_EVENT_TEXT:
          return ANY_RESOLVED;
      default:
        return UNKNOWN;
    }
  }

  /**
   * Create an ActionType from a rule action.
   *
   * @param ruleAction the rule action
   * @return the action type
   */
  public static ActionType fromRuleAction(String ruleAction) {

    switch (Strings.nullToEmpty(ruleAction).trim().toUpperCase()) {
      case "ALL":
        return ALL;
      case "ANY-CREATED":
        return ANY_CREATED;
      case "ANY-DELETED":
        return ANY_DELETED;
      case "ANY-MODIFIED":
        return ANY_MODIFIED;
      case "ANY-ACTIVE":
          return ANY_ACTIVE;
      case "ANY-OPENED":
          return ANY_OPENED;
      case "ANY-RESOLVED":
          return ANY_RESOLVED;
      default:
        return UNKNOWN;
    }
  }
}

