package com.google.developers.codelabs.notification.api;

import com.google.api.server.spi.ServiceException;
import com.google.api.server.spi.auth.common.User;
import com.google.api.server.spi.config.Api;
import com.google.api.server.spi.config.ApiMethod;
import com.google.api.server.spi.config.ApiMethod.HttpMethod;
import com.google.api.server.spi.config.AuthLevel;
import com.google.api.server.spi.response.UnauthorizedException;
import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.api.entities.Action;
import com.google.developers.codelabs.notification.api.entities.ApiUser;
import com.google.developers.codelabs.notification.api.entities.ChannelRequest;
import com.google.developers.codelabs.notification.api.entities.ChannelsRequestBody;
import com.google.developers.codelabs.notification.api.entities.ConfigurationRequestBody;
import com.google.developers.codelabs.notification.api.entities.ExtraInfoRequestBody;
import com.google.developers.codelabs.notification.api.entities.Rule;
import com.google.developers.codelabs.notification.api.entities.RulesRequestBody;
import com.google.developers.codelabs.notification.api.entities.StatusRequest;
import com.google.developers.codelabs.notification.api.entities.UsersRequestBody;
import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.Channel;
import com.google.developers.codelabs.notification.core.model.Configuration;
import com.google.developers.codelabs.notification.core.model.ExtraInfo;
import com.google.developers.codelabs.notification.core.model.FlatRule;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.model.ProcessingStatus;
import com.google.developers.codelabs.notification.core.model.ProcessingStatusOptions;
import com.google.developers.codelabs.notification.core.service.DataStoreService;
import com.google.developers.codelabs.notification.util.ApiConstants;
import com.google.inject.Inject;
import com.google.inject.Singleton;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/**
 * The Class Notification.
 */
@Api(name = "gcpNotiApi",
    version = "v1",
    title = "Notification codelab API.",
    authLevel = AuthLevel.REQUIRED,
    description = "This API provides services to configure and operate the Notification codelab.",
    clientIds = {
        ApiConstants.API_EXPLORER_CLIENT_ID,
        ApiConstants.GCLOUD_DEFAULT_CLIENT_ID
    },
    audiences = {
        ApiConstants.API_EXPLORER_CLIENT_ID,
        ApiConstants.GCLOUD_DEFAULT_CLIENT_ID
    })
@Singleton
public class Notification {

  private static final Logger LOG = Logger.getLogger(Notification.class.getName());

  @Inject
  private DataStoreService dataStoreService;

  /**
   * Sets the status.
   *
   * @param user authenticated user
   * @param body the new status
   * @throws ServiceException
   */
  @ApiMethod(name = "status",
      description = "Set the current status of the notification processing: STOP or START",
      path = "status",
      httpMethod = HttpMethod.POST)
  public void setStatus(User user, StatusRequest body)
      throws ServiceException {
    ensureUser(user);

    if (body != null) {
      ProcessingStatusOptions status = ProcessingStatusOptions.fromStatus(body.getStatus());
      if (status != ProcessingStatusOptions.UNKNOWN) {
        dataStoreService.saveProcessingStatus(new ProcessingStatus(status));
      } else {
        LOG.info("Unknown status value: " + body.getStatus());
      }
      LOG.info("setStatus:" + body.getStatus());
    } else {
      LOG.info("No status payload in post.");
    }
  }

  /**
   * Sets the extra info.
   *
   * @param user authenticated user
   * @param body the new extra info
   * @throws ServiceException
   */
  @ApiMethod(name = "extraInfo",
      description = "Configure extra information to be added to out going "
          + "notifications of a specific notification type.",
      path = "extrainfo",
      httpMethod = HttpMethod.POST)
  public void setExtraInfo(User user, ExtraInfoRequestBody body)
      throws ServiceException {
    ensureUser(user);
    if (body != null) {
      NotificationType type = NotificationType.formNotification(body.getNotificationType());
      if (type != NotificationType.UNKNOWN) {
        dataStoreService.saveExtraInfo(new ExtraInfo(type, Strings.nullToEmpty(body.getInfo())));
      } else {
        LOG.info("Unknown Notification Type value: " + body.getNotificationType());
      }
      LOG.info("Extra info - type :" + body.getNotificationType() + " info: " + body.getInfo());
    } else {
      LOG.info("No extra info payload in post.");
    }
  }

  /**
   * Channels.
   *
   * @param user authenticated user
   * @param body the body
   * @throws ServiceException
   */
  @ApiMethod(name = "channels",
      description = "Allows to choose the active notification channels"
          + " on the following options it the channel is configured: "
          + "NATIVE_EMAIL, SMS, SENDGRID, JIRA",
      path = "channels",
      httpMethod = HttpMethod.POST)
  public void channels(User user, ChannelsRequestBody body)
      throws ServiceException {
    ensureUser(user);

    if (body != null) {
      if (!body.isEmpty()) {
        dataStoreService.saveChannels(buildChannelModel(body.getActiveChannels()));
      }
      LOG.info("Active channels :" + body.getActiveChannels());
    } else {
      LOG.info("No active channels payload in post.");
    }

  }

  /**
   * Users.
   *
   * @param user authenticated user
   * @param body the body
   * @throws ServiceException
   */
  @ApiMethod(name = "users",
      description = "Allows to choose the users that will receive the notifications.",
      path = "users",
      httpMethod = HttpMethod.POST)
  public void users(User user, UsersRequestBody body)
      throws ServiceException {
    ensureUser(user);

    if (body != null) {
      if (!body.isEmpty()) {
        dataStoreService.saveUsers(buildUserModel(body.getUsers()));
      }
      LOG.info("Users :" + body.getUsers());
    } else {
      LOG.info("No users payload in post.");
    }
  }

  /**
   * Rules.
   *
   * @param user authenticated user
   * @param body the body
   * @throws ServiceException
   */
  @ApiMethod(name = "rules",
      description = "Allows to define the processing rules to be applied "
          + "to the incoming messages ",
      path = "rules",
      httpMethod = HttpMethod.POST)
  public void rules(User user, RulesRequestBody body)
      throws ServiceException {
    ensureUser(user);

    if (body != null) {
      if (!body.isEmpty()) {
        List<FlatRule> rulesToSave = convertApiRuleToFlatRules(body.getRules());
        dataStoreService.saveFlatRules(rulesToSave);
      }
      LOG.info("Rules :" + body.getRules());
    } else {
      LOG.info("No rules payload in post.");
    }
  }

  private List<FlatRule> convertApiRuleToFlatRules(List<Rule> rules) {
    List<FlatRule> rulesToSave = new ArrayList<>();
    for (Rule rule : rules) {
      NotificationType notificationType = NotificationType.formNotification(rule.getType());
      if (notificationType != NotificationType.UNKNOWN) {
        rulesToSave.add(convertRule(notificationType, rule));
      }
    }

    return rulesToSave;
  }

  private FlatRule convertRule(NotificationType notificationType, Rule rule) {

    FlatRule flatRule = new FlatRule();
    flatRule.setType(notificationType.name());

    List<Action> actions = rule.getActions();
    if (actions != null) {
      for (Action action : actions) {
        ActionType actionType = ActionType.fromRuleAction(action.getType());
        if (actionType != ActionType.UNKNOWN) {
          addAction(flatRule, actionType, action);
        }
      }
    }

    return flatRule;
  }

  private void addAction(FlatRule rule, ActionType actionType, Action action) {
    switch (actionType) {
      case ALL:
        rule.setAllAction(actionType);
        break;
      case ANY_CREATED:
        rule.setCreatedAction(actionType);
        break;
      case ANY_DELETED:
        rule.setDeletedAction(actionType);
        break;
      case ANY_MODIFIED:
        rule.setModifiedAction(actionType);
        break;
      case ANY_ACTIVE:
          rule.setActiveAction(actionType);
          break;
      case ANY_OPENED:
          rule.setOpenedAction(actionType);
          break;
      case ANY_RESOLVED:
          rule.setResolvedAction(actionType);
          break;
      default:
        break;
    }
  }

  /**
   * Configure properties.
   *
   * @param user authenticated user
   * @param body the body
   * @throws ServiceException
   */
  @ApiMethod(name = "config",
      description = "Allows to configure the notification system parameters.",
      path = "config",
      httpMethod = HttpMethod.POST)
  public void config(User user, ConfigurationRequestBody body)
      throws ServiceException {
    ensureUser(user);
    if (body != null) {
      if (!body.isEmpty()) {
        Configuration conf = new Configuration(body.getConfiguration());
        dataStoreService.saveConfiguration(conf);
      }
      LOG.info("config :" + body.getConfiguration());
    } else {
      LOG.info("No configuration payload in post.");
    }
  }

  private void ensureUser(User user) throws UnauthorizedException {
    if (user == null) {
      throw new UnauthorizedException("Invalid credentials");
    } else {
      LOG.info(String.format("User id=[%s], email=[%s]", user.getId(), user.getEmail()));
    }
  }

  private List<NotificationUser> buildUserModel(List<ApiUser> users) {
    List<NotificationUser> userModels = new ArrayList<>();
    for (ApiUser user : users) {
      userModels.add(
          new NotificationUser(user.getEmail(), user.getTelephoneNumber(), user.getJiraUid(),
              user.getRole()));
    }
    return userModels;
  }

  private List<Channel> buildChannelModel(List<ChannelRequest> channels) {
    List<Channel> channelModels = new ArrayList<>();
    for (ChannelRequest channel : channels) {
      channelModels.add(new Channel(channel.getChannel()));
    }
    return channelModels;
  }

}
