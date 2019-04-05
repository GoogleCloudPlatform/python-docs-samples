package com.google.developers.codelabs.notification.service.rules;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.FlatRule;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.service.*;

import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.HashMap;

/**
 * The Class RulesTest.
 */
@SuppressWarnings("javadoc")
public class RulesTest {

  @Test
  public void executeAllAssetsRuleWithSucesses() {

    NotificationService mock = Mockito.mock(NotificationService.class);

    HashMap<String, Rule> rules = buildSingelRuleMap(NotificationType.ASSETS, ActionType.ALL);

    EventContext context = buildContext("ASSETS", "CREATED", "{\"properties\" : {}}");

    RuleEngine ruleEngine = new RuleEngine(mock);
    ruleEngine.check(rules, context);

    Mockito.verify(mock).callAdapters(Mockito.any(OutputMessage.class), Mockito.anyBoolean());
  }

  @Test
  public void executeAnyCreatedAssetsRuleWithSucesses() {

    NotificationService mock = Mockito.mock(NotificationService.class);

    HashMap<String, Rule> rules =
        buildSingelRuleMap(NotificationType.ASSETS, ActionType.ANY_CREATED);

    EventContext context = buildContext("ASSETS", "CREATED", "{\"properties\" : {}}");

    RuleEngine ruleEngine = new RuleEngine(mock);
    ruleEngine.check(rules, context);

    Mockito.verify(mock).callAdapters(Mockito.any(OutputMessage.class), Mockito.anyBoolean());
  }

  @Test
  public void executeAnyDeletedAssetsRuleWithSucesses() {

    NotificationService mock = Mockito.mock(NotificationService.class);

    HashMap<String, Rule> rules =
        buildSingelRuleMap(NotificationType.ASSETS, ActionType.ANY_DELETED);

    EventContext context = buildContext("ASSETS", "DELETED", "{\"properties\" : {}}");

    RuleEngine ruleEngine = new RuleEngine(mock);
    ruleEngine.check(rules, context);

    Mockito.verify(mock).callAdapters(Mockito.any(OutputMessage.class), Mockito.anyBoolean());
  }

  @Test
  public void executeAnyModifiedAssetsRuleWithSucesses() {

    NotificationService mock = Mockito.mock(NotificationService.class);

    HashMap<String, Rule> rules =
        buildSingelRuleMap(NotificationType.ASSETS, ActionType.ANY_MODIFIED);

    EventContext context = buildContext("ASSETS", "MODIFIED", "{\"properties\" : {}}");

    RuleEngine ruleEngine = new RuleEngine(mock);
    ruleEngine.check(rules, context);

    Mockito.verify(mock).callAdapters(Mockito.any(OutputMessage.class), Mockito.anyBoolean());
  }

  @Test
  public void ruleExecuteAllAction() {
    OutputMessage ouputMessage = executeRule(ActionType.ALL, "MODIFIED");
    Assert.assertEquals(ActionType.ALL, ouputMessage.getActionType());
  }

  @Test
  public void ruleExecuteAllAndCreatedAction() {
    Rule rule = buildRule(NotificationType.ASSETS,
        buildAction(ActionType.ALL),
        buildAction(ActionType.ANY_CREATED));

    EventContext context = buildContext("ASSETS", "CREATED", "{\"properties\" : {}}");

    OutputMessage ouputMessage = rule.execute(context);
    Assert.assertEquals(ActionType.ANY_CREATED, ouputMessage.getActionType());
  }

  @Test
  public void ruleExecuteAnyCreatedAction() {
    OutputMessage ouputMessage = executeRule(ActionType.ANY_CREATED, "CREATED");
    Assert.assertEquals(ActionType.ANY_CREATED, ouputMessage.getActionType());
  }
  
  @Test
  public void ruleExecuteAnyActiveAction() {
    OutputMessage ouputMessage = executeRule(ActionType.ANY_ACTIVE, "ACTIVE");
    Assert.assertEquals(ActionType.ANY_ACTIVE, ouputMessage.getActionType());
  }

  @Test
  public void ruleExecuteAnyDeletedAction() {
    OutputMessage ouputMessage = executeRule(ActionType.ANY_DELETED, "DELETED");
    Assert.assertEquals(ActionType.ANY_DELETED, ouputMessage.getActionType());
  }

  @Test
  public void ruleExecuteAnyModifiedAction() {
    OutputMessage ouputMessage = executeRule(ActionType.ANY_MODIFIED, "MODIFIED");
    Assert.assertEquals(ActionType.ANY_MODIFIED, ouputMessage.getActionType());
  }

  @Test
  public void ruleExecuteNoAction() {

    Rule rule = buildRule(NotificationType.ASSETS, buildAction(ActionType.ANY_CREATED));
    EventContext context = buildContext("ASSETS", "MODIFIED", "{\"properties\" : {}}");

    OutputMessage ouputMessage = rule.execute(context);

    Assert.assertNull(ouputMessage);

  }

  @Test
  public void flatRuleConverterAllAction() {

    FlatRule flatRule = new FlatRule();
    flatRule.setType(NotificationType.ASSETS.name());
    flatRule.setAllAction(ActionType.ALL);

    Rule convertedRule = new RuleConverter().convertFlatRule(flatRule);

    Assert.assertEquals(NotificationType.ASSETS, convertedRule.getType());
    Assert.assertEquals(ActionType.ALL, convertedRule.getAllAction().getType());
  }

  @Test
  public void flatRuleConverterAnyDeletedAction() {

    FlatRule flatRule = new FlatRule();
    flatRule.setType(NotificationType.ASSETS.name());
    flatRule.setDeletedAction(ActionType.ANY_DELETED);

    Rule convertedRule = new RuleConverter().convertFlatRule(flatRule);

    Assert.assertEquals(NotificationType.ASSETS, convertedRule.getType());
    Assert.assertEquals(ActionType.ANY_DELETED, convertedRule.getAnyDeleted().getType());
  }

  @Test
  public void flatRuleConverterAnyActiveAction() {

    FlatRule flatRule = new FlatRule();
    flatRule.setType(NotificationType.ASSETS.name());
    flatRule.setActiveAction(ActionType.ANY_ACTIVE);

    Rule convertedRule = new RuleConverter().convertFlatRule(flatRule);

    Assert.assertEquals(NotificationType.ASSETS, convertedRule.getType());
    Assert.assertEquals(ActionType.ANY_ACTIVE, convertedRule.getAnyActive().getType());
  }

  private Action buildAction(ActionType actionType) {
    return new Action(actionType);
  }

  private OutputMessage executeRule(ActionType actionType, String actionTypeName) {
    Rule rule = buildRule(NotificationType.ASSETS, buildAction(actionType));
    EventContext context = buildContext("ASSETS", actionTypeName, "{\"properties\" : {}}");
    OutputMessage ouputMessage = rule.execute(context);
    return ouputMessage;
  }

  private HashMap<String, Rule> buildSingelRuleMap(
      NotificationType notificatioType,
      ActionType actionType) {

    HashMap<String, Rule> rules = new HashMap<String, Rule>();
    Rule buildRule = buildRule(notificatioType, buildAction(actionType));
    rules.put(notificatioType.name(), buildRule);

    return rules;
  }

  private Rule buildRule(NotificationType notificatioType, Action... action) {

    Action allAction = null;
    Action anyDeleted = null;
    Action anyCreated = null;
    Action anyModified = null;
    Action anyActive = null;
    Action anyOpened = null;
    Action anyResolved = null;

    for (int i = 0; i < action.length; i++) {
      switch (action[i].getType()) {
        case ALL:
          allAction = action[i];
          break;
        case ANY_DELETED:
          anyDeleted = action[i];
          break;
        case ANY_CREATED:
          anyCreated = action[i];
          break;
        case ANY_MODIFIED:
          anyModified = action[i];
          break;
        case ANY_ACTIVE:
          anyActive = action[i];
          break;
        case ANY_OPENED:
          anyOpened = action[i];
          break;
        case ANY_RESOLVED:
          anyResolved = action[i];
          break;
        default:
          break;
      }
    }

    Rule assetsRule = new Rule(notificatioType,
        allAction,
        anyDeleted,
        anyCreated,
        anyModified,
        anyActive,
        anyOpened,
        anyResolved);

    return assetsRule;
  }

  private EventContext buildContext(String notificationType, String eventtype, String message) {
    HashMap<String, String> attributes = new HashMap<String, String>();
    attributes.put("Notification-Type", notificationType);
    attributes.put("Event-Type", eventtype);
    EventContext context = new EventContext(message, attributes);
    return context;
  }
}

