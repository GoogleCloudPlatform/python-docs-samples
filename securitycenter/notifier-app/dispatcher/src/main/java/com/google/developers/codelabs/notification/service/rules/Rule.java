package com.google.developers.codelabs.notification.service.rules;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.service.*;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class Rule.
 */
public class Rule {

  private static final Logger LOG = Logger.getLogger(Rule.class.getName());

  private NotificationType type;
  private Action allAction;
  private Action anyDeleted;
  private Action anyCreated;
  private Action anyModified;
  private Action anyActive;
  private Action anyOpened;
  private Action anyResolved;

  /**
   * Instantiates a new rule.
   *
   * @param type        the type
   * @param allAction   the all action
   * @param anyDeleted  the any deleted
   * @param anyCreated  the any created
   * @param anyModified the any modified
   */
  public Rule(NotificationType type,
              Action allAction,
              Action anyDeleted,
              Action anyCreated,
              Action anyModified,
              Action anyActive,
              Action anyOpened,
              Action anyResolved) {

    this.type = type;
    this.allAction = allAction;
    this.anyDeleted = anyDeleted;
    this.anyCreated = anyCreated;
    this.anyModified = anyModified;
    this.anyActive = anyActive;
    this.anyOpened = anyOpened;
    this.anyResolved = anyResolved;

  }

  /**
   * Execute.
   *
   * @param context the context
   * @return the ouput message
   */
  public OutputMessage execute(EventContext context) {

    Action action = findMatchingAction(context);
    if (action != null) {
      return new OutputMessage(type, action.getType(), context);
    }
    return null;
  }

  private Action findMatchingAction(EventContext context) {
    Action selectAction;
    switch (ActionType.fromEventType(context.getEventType())) {
      case ANY_CREATED:
        selectAction = anyCreated;
        break;
      case ANY_DELETED:
        selectAction = anyDeleted;
        break;
      case ANY_MODIFIED:
        selectAction = anyModified;
        break;
      case ANY_ACTIVE:
        selectAction = anyActive;
        break;
      case ANY_OPENED:
        selectAction = anyOpened;
        break;
      case ANY_RESOLVED:
        selectAction = anyResolved;
        break;
      default:
        LOG.log(Level.WARNING, String.format("No Event-Type found for: %s. Resolving to default Action (ALL)", context.getEventType()));
        selectAction = null;
    }

    return (selectAction != null) ? selectAction : allAction;
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
   * Gets the all action.
   *
   * @return the all action
   */
  public Action getAllAction() {
    return allAction;
  }

  /**
   * Gets the any deleted.
   *
   * @return the any deleted
   */
  public Action getAnyDeleted() {
    return anyDeleted;
  }

  /**
   * Gets the any created.
   *
   * @return the any created
   */
  public Action getAnyCreated() {
    return anyCreated;
  }

  /**
   * Gets the any modified.
   *
   * @return the any modified
   */
  public Action getAnyModified() {
    return anyModified;
  }

  public Action getAnyActive() {
    return anyActive;
  }

  public Action getAnyOpened() {
    return anyOpened;
  }

  public Action getAnyResolved() {
    return anyResolved;
  }

}
