/*
 *
 */
package com.google.developers.codelabs.notification.service;

import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.exception.AdapterExecutionException;
import com.google.developers.codelabs.notification.binder.Appengine;
import com.google.developers.codelabs.notification.binder.Jira;
import com.google.developers.codelabs.notification.binder.Sendgrid;
import com.google.developers.codelabs.notification.binder.Twilio;
import com.google.developers.codelabs.notification.cloudfunction.CloudFunctionExecutor;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.*;
import com.google.developers.codelabs.notification.core.service.DataStoreService;
import com.google.developers.codelabs.notification.service.rules.Rule;
import com.google.developers.codelabs.notification.service.rules.RuleEngine;
import com.google.inject.Inject;
import org.apache.commons.lang3.StringUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class NotificationService.
 */
public class NotificationService {

  private static final Logger LOG = Logger.getLogger(NotificationService.class.getName());
  private final ImmutableMap<ChannelOption, NotificationAdapter> adapters;

  private DataStoreService dataStoreService;

  private CloudFunctionExecutor cloudFunctionExecutor;

  /**
   * Instantiates a new notification service.
   *
   * @param appengineEmailAdapter the appengine email adapter
   * @param sendGridAdapter       the send grid adapter
   * @param smsAdapter            the sms adapter
   * @param jiraAdapter           the sms adapter
   * @param dataStoreService      the data store service
   * @param cloudFunctionExecutor cloud function executor
   */
  @Inject
  public NotificationService(
          @Appengine NotificationAdapter appengineEmailAdapter,
          @Sendgrid NotificationAdapter sendGridAdapter,
          @Twilio NotificationAdapter smsAdapter,
          @Jira NotificationAdapter jiraAdapter,
          DataStoreService dataStoreService,
          CloudFunctionExecutor cloudFunctionExecutor) {
    super();

    this.adapters = new ImmutableMap.Builder<ChannelOption, NotificationAdapter>()
            .put(appengineEmailAdapter.getChannel(), appengineEmailAdapter)
            .put(sendGridAdapter.getChannel(), sendGridAdapter)
            .put(smsAdapter.getChannel(), smsAdapter)
            .put(jiraAdapter.getChannel(), jiraAdapter)
            .build();

    this.dataStoreService = dataStoreService;
    this.cloudFunctionExecutor = cloudFunctionExecutor;
  }

  /**
   * Apply the stored rules on a event context.
   *
   * @param context the context
   */
  public void applyRules(String messageId, EventContext context) {
    boolean isHashMechanismOff = checkHashMechanism();
    if (isHashMechanismOff || shouldProcessMessage(messageId, context)) {
      LOG.log(Level.INFO, "applying rules");
      List<FlatRule> flatRules = getDataStoreService().getFlatRules();
      new RuleEngine(this).check(convertRules(flatRules), context);
    }
  }

  private boolean checkHashMechanism() {
    String hashMechanism = System.getenv("HASH_MECHANISM");
    LOG.log(Level.INFO, "the hash mechanism is: " + hashMechanism);
    return hashMechanism == null || !System.getenv("HASH_MECHANISM").equals("ON");
  }

  private Map<String, Rule> convertRules(List<FlatRule> flatRules) {
    Map<String, Rule> rulesMap = new HashMap<>();
    RuleConverter converter = new RuleConverter();
    for (FlatRule flatRule : flatRules) {
      Rule rule = converter.convertFlatRule(flatRule);
      rulesMap.put(rule.getType().name(), rule);
    }
    return rulesMap;
  }

  /**
   * Call adapters.
   *
   * @param outputMessage       the outputMessage with the eventContext to be sent.
   * @param cloudFunctionActive TODO
   */
  public void callAdapters(OutputMessage outputMessage, boolean cloudFunctionActive) {
    LOG.info(String.format("Message received on pubsub [%s]", outputMessage.buildSubject()));

    if (isProcessingNotifications()) {
      List<NotificationUser> users = getDataStoreService().getUsers();
      users = addAddictionalDestEmail(users, outputMessage.getContext());
      if (users != null && !users.isEmpty()) {
        addExtraInfoToOutputMessage(outputMessage);
        List<ChannelOption> activeChannels = getDataStoreService().getChannelOptions();
        List<NotificationAdapter> adapters = getActiveAdapters(activeChannels);
        if (adapters != null && !adapters.isEmpty()) {
          if (cloudFunctionActive) {
            String cloudFunctionResponse = cloudFunctionExecutor.call(outputMessage);
            outputMessage.setCloudFunctionResponse(cloudFunctionResponse);
          }
          for (NotificationUser user : users) {
            for (NotificationAdapter adapter : adapters) {
              try {
                adapter.notify(outputMessage, user);
              } catch (AdapterExecutionException e) {
                LOG.log(Level.SEVERE, e.getMessage(), e);
              }
            }
          }
        } else {
          LOG.info("No active adapters configured.");
        }
      } else {
        LOG.info("No user configured.");
      }
    } else {
      LOG.info("Event processing is disabled.");
    }
  }

  private List<NotificationAdapter> getActiveAdapters(List<ChannelOption> activeChannels) {
    List<NotificationAdapter> activeAdapters = Lists.newArrayList();
    for (ChannelOption channel : activeChannels) {
      NotificationAdapter adapter = this.adapters.get(channel);
      if (adapter.isConfigured()) {
        activeAdapters.add(adapter);
      } else {
        String activeNotConfigured = "%s active but not configured";
        LOG.warning(String.format(activeNotConfigured, adapter.getClass().getName()));
      }
    }

    return activeAdapters;
  }

  private void addExtraInfoToOutputMessage(OutputMessage outputMessage) {
    NotificationType type = NotificationType.formNotification(outputMessage.getNotificationType());
    if (type != NotificationType.UNKNOWN) {
      ExtraInfo extraInfo = getDataStoreService().getExtraInfo(type);
      if (extraInfo != null) {
        outputMessage.setExtraInfo(extraInfo.getInfo());
      }
    }
  }

  private boolean isProcessingNotifications() {
    ProcessingStatus processingStatus = getDataStoreService().getProcessingStatus();
    LOG.finest("Current processing status is " + processingStatus);
    return processingStatus != null
            && ProcessingStatusOptions.START == processingStatus.getStatus();
  }

  /**
   * Gets the data store service.
   *
   * @return the data store service
   */
  protected DataStoreService getDataStoreService() {
    return dataStoreService;
  }

  /**
   * Verify if the message consumed on PubSub was already processed
   *
   * @param messageId The messageId generated at PubSub
   * @param context   {@link EventContext} object with PubSub message information like payload and message attributes
   * @return true if message was already processed. false otherwise.
   */
  public boolean shouldProcessMessage(String messageId, EventContext context) {
    switch (context.getNotificationType()) {
      case "ASSETS":
        return notIdempotentAssetHash(messageId, context);
      case "FINDINGS":
        return notIdempotentFindingHash(messageId, context);
      default:
        LOG.log(Level.WARNING, String.format("Notification-type not identified: %s", context.getNotificationType()));
        return false;
    }
  }

  private boolean notIdempotentAssetHash(String messageId, EventContext context) {
    boolean shouldProcessMessage = true;
    String assetHash = context.getAssetHash();
    if (StringUtils.isNotEmpty(assetHash)) {
      if (!this.dataStoreService.hasAssetHash(assetHash)) {
        this.dataStoreService.saveAssetHash(assetHash);
      } else {
        LOG.log(Level.INFO, "Asset {0} is already processed", assetHash);
        shouldProcessMessage = false;
      }
    }
    shouldProcessMessage = notIdempotentMessageId(messageId, shouldProcessMessage);
    return shouldProcessMessage;
  }

  private boolean notIdempotentFindingHash(String messageId, EventContext context) {
    boolean shouldProcessMessage = true;
    String findingHash = context.getFindingHash();
    if (StringUtils.isNotEmpty(findingHash)) {
      if (!this.dataStoreService.hasFindingHash(findingHash)) {
        this.dataStoreService.saveFindingHash(findingHash);
      } else {
        LOG.log(Level.INFO, "Finding {0} is already processed", findingHash);
        shouldProcessMessage = false;
      }
    }
    shouldProcessMessage = notIdempotentMessageId(messageId, shouldProcessMessage);
    return shouldProcessMessage;
  }

  private boolean notIdempotentMessageId(String messageId, boolean shouldProcessMessage) {
    if (!this.dataStoreService.hasMessageId(messageId)) {
      this.dataStoreService.saveMessageId(messageId);
    } else {
      LOG.log(Level.INFO, "Message {0} is already processed", messageId);
      shouldProcessMessage = false;
    }
    return shouldProcessMessage;
  }

  private List<NotificationUser> addAddictionalDestEmail(List<NotificationUser> dbUsers, EventContext context) {
    List<NotificationUser> users = Optional.ofNullable(dbUsers).orElse(new ArrayList<>());
    String destMail = context.getAddictionalDestEmail();
    if (StringUtils.isNotBlank(destMail) 
        && users.stream().noneMatch(user -> destMail.equals(user.getEmail()))) {
      users.add(new NotificationUser(destMail, null, null, null));
    }
    return users;
  }
}
