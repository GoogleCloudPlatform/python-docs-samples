package com.google.developers.codelabs.notification.service;

import com.google.developers.codelabs.notification.core.model.FlatRule;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.service.rules.Action;
import com.google.developers.codelabs.notification.service.rules.Rule;

/**
 * The Class RuleConverter.
 */
public class RuleConverter {

  /**
   * Convert flat rule.
   *
   * @param flatRule the flat rule
   * @return the rule
   */
  public Rule convertFlatRule(FlatRule flatRule) {

    Action allAction = convertAllAction(flatRule);
    Action anyDeleted = convertAnyDeletedAction(flatRule);
    Action anyCreated = convertAnyCreatedAction(flatRule);
    Action anyModified = convertAnyModifiedAction(flatRule);
    Action anyActive = convertAnyActiveAction(flatRule);
    Action anyOpened = convertAnyOpenedAction(flatRule);
    Action anyResolved = convertAnyResolvedAction(flatRule);

    Rule rule = new Rule(NotificationType.formNotification(flatRule.getType()),
        allAction, anyDeleted, anyCreated, anyModified, anyActive, anyOpened, anyResolved);

    return rule;
  }


  private Action convertAnyResolvedAction(FlatRule flatRule) {
    Action anyResolved = null;
    if (flatRule.getResolvedAction() != null) {
      anyResolved = new Action(flatRule.getResolvedAction());
    }
    return anyResolved;
  }
  
  private Action convertAnyOpenedAction(FlatRule flatRule) {
    Action anyOpened = null;
    if (flatRule.getOpenedAction() != null) {
    	anyOpened = new Action(flatRule.getOpenedAction());
    }
    return anyOpened;
  }
  
  private Action convertAnyActiveAction(FlatRule flatRule) {
    Action anyActive = null;
    if (flatRule.getActiveAction() != null) {
      anyActive = new Action(flatRule.getActiveAction());
    }
    return anyActive;
  }
  
  private Action convertAnyModifiedAction(FlatRule flatRule) {
    Action anyModified = null;
    if (flatRule.getModifiedAction() != null) {
      anyModified = new Action(flatRule.getModifiedAction());
    }
    return anyModified;
  }

  private Action convertAnyCreatedAction(FlatRule flatRule) {
    Action anyCreated = null;
    if (flatRule.getCreatedAction() != null) {
      anyCreated = new Action(flatRule.getCreatedAction());
    }
    return anyCreated;
  }

  private Action convertAnyDeletedAction(FlatRule flatRule) {
    Action anyDeleted = null;
    if (flatRule.getDeletedAction() != null) {
      anyDeleted = new Action(flatRule.getDeletedAction());
    }
    return anyDeleted;
  }

  private Action convertAllAction(FlatRule flatRule) {
    Action allAction = null;
    if (flatRule.getAllAction() != null) {
      allAction = new Action(flatRule.getAllAction());
    }
    return allAction;
  }
}
