package com.google.developers.codelabs.notification.service.rules;

import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.NotificationService;
import com.google.developers.codelabs.notification.service.OutputMessage;

import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class RuleEngine.
 */
public class RuleEngine {

  private static final Logger LOG = Logger.getLogger(RuleEngine.class.getName());

  private NotificationService service;

  /**
   * Instantiates a new rule engine.
   *
   * @param service the service
   */
  public RuleEngine(NotificationService service) {
    this.service = service;
  }

  /**
   * Check if an eventContext satisfies one of the rules.
   *
   * @param rules   the rules
   * @param context the eventContext
   */
  public void check(Map<String, Rule> rules, EventContext context) {

    Rule rule = findMatchingRule(rules, context);
    if (rule != null) {
      OutputMessage ouputMessage = rule.execute(context);
      if (ouputMessage != null) {
        service.callAdapters(ouputMessage, cloudFunctionActive(rules));
      } else {
        LOG.log(Level.WARNING, "No matching action found for message {0}", context.getMessage());
      }
    } else {
      LOG.log(Level.WARNING, "No matching rule found for message {0}", context.getMessage());
    }
  }

  private boolean cloudFunctionActive(Map<String, Rule> rules) {
    return rules.containsKey(NotificationType.CLOUD_FUNCTION.name());
  }

  private Rule findMatchingRule(Map<String, Rule> rules, EventContext context) {
    return rules.get(NotificationType.formNotification(context.getNotificationType()).name());
  }
}
