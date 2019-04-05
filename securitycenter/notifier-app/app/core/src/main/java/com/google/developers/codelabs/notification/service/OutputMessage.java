package com.google.developers.codelabs.notification.service;

import com.github.mustachejava.DefaultMustacheFactory;
import com.github.mustachejava.Mustache;
import com.github.mustachejava.MustacheFactory;
import com.google.common.base.Charsets;
import com.google.common.io.Resources;
import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.message.OutputType;

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.net.URL;
import java.util.HashMap;
import java.util.logging.Logger;

public class OutputMessage {

  protected static final Logger LOG = Logger.getLogger(OutputMessage.class.getName());

  private static final String SUBJECT_TEMPLATE_COMPILED_KEY = "subject";
  private static final String BODY_TEMPLATE_COMPILED_KEY = "body";
  private static final String LONG_TEMPLATE = "mustache/long.mustache";
  private static final String SHORT_TEMPLATE = "mustache/short.mustache";
  private static final String FINDING_SUBJECT_TEMPLATE = "mustache/subject.finding.mustache";
  private static final String ASSET_SUBJECT_TEMPLATE = "mustache/subject.asset.mustache";

  private EventContext context;
  private ActionType actionType;
  private NotificationType ruleType;
  private String extraInfo;
  private String cloudFunctionResponse;
  private HashMap properties;


  public OutputMessage(NotificationType ruleType, ActionType type, EventContext context) {
    this.ruleType = ruleType;
    this.actionType = type;
    this.context = context;
  }

  /**
   * Gets the context.
   *
   * @return the context
   */
  public EventContext getContext() {
    return context;
  }

  /**
   * Gets the action type.
   *
   * @return the action type
   */
  public ActionType getActionType() {
    return actionType;
  }

  /**
   * Gets the extra info.
   *
   * @return the extra info
   */
  public String getExtraInfo() {
    return extraInfo;
  }

  /**
   * Sets the extra info.
   *
   * @param extraInfo the new extra info
   */
  public void setExtraInfo(String extraInfo) {
    this.extraInfo = extraInfo;
    this.context.setExtraInfo(extraInfo);
  }

  /**
   * Gets the notification type.
   *
   * @return the notification type
   */
  public String getNotificationType() {
    if (context != null) {
      return context.getNotificationType();
    }
    return null;
  }

  /**
   * Gets the rule type that was matched by the rule processing.
   *
   * @return the rule type
   */
  public NotificationType getRuleType() {
    return ruleType;
  }

  /**
   * Sets the cloud function response.
   *
   * @param cloudFunctionResponse the new cloud function response
   */
  public void setCloudFunctionResponse(String cloudFunctionResponse) {
    this.context.setCloudFunctionResponse(cloudFunctionResponse);
  }

  /**
   * Gets the cloud function response.
   *
   * @return the cloud function response
   */
  public String getCloudFunctionResponse() {
    return cloudFunctionResponse;
  }

  public HashMap getProperties() {
    return properties;
  }

  public String buildBody(OutputType outputType) {
    String templatePath = (outputType.equals(OutputType.LONG)) ? LONG_TEMPLATE : SHORT_TEMPLATE;
    String template = readTemplate(templatePath);
    return applyTemplate(BODY_TEMPLATE_COMPILED_KEY, template);
  }

  private String readTemplate(String resource) {
    URL url = Resources.getResource(resource);
    try {
        return Resources.toString(url, Charsets.UTF_8);
    } catch (IOException ex) {
        throw new RuntimeException(ex);
    }
  }

  public String buildSubject() {
    String templatePath = (NotificationType.ASSETS.name().equals(context.getNotificationType())) ? ASSET_SUBJECT_TEMPLATE : FINDING_SUBJECT_TEMPLATE;
    String template = readTemplate(templatePath);
    return applyTemplate(SUBJECT_TEMPLATE_COMPILED_KEY, template);
  }

  private String applyTemplate(String compiliedTemplate, String template) {
    MustacheFactory mf = new DefaultMustacheFactory();
    StringReader reader = new StringReader(template);
    StringWriter writer = new StringWriter();
  
    Mustache mustache = mf.compile(reader, compiliedTemplate);
    mustache.execute(writer, context);
  
    return writer.toString();
  }

}
