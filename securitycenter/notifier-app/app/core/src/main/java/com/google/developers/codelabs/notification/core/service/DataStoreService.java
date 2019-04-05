package com.google.developers.codelabs.notification.core.service;

import com.google.common.collect.Lists;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.*;
import com.googlecode.objectify.Key;
import com.googlecode.objectify.VoidWork;

import java.util.ArrayList;
import java.util.List;

/**
 * The Class DataStoreService.
 */
public class DataStoreService {

  /**
   * Save the users.
   *
   * @param users the users
   */
  public void saveUsers(final List<NotificationUser> users) {

    final List<Key<NotificationUser>> keys =
            OfyService.ofy().load().type(NotificationUser.class).keys().list();

    OfyService.ofy().transact(new VoidWork() {
      @Override
      public void vrun() {
        if (keys != null && !keys.isEmpty()) {
          OfyService.ofy().delete().keys(keys).now();
        }
        OfyService.ofy().save().entities(users).now();
      }
    });

  }

  /**
   * Gets the users.
   *
   * @return the users
   */
  public List<NotificationUser> getUsers() {
    return OfyService.ofy().load().type(NotificationUser.class).list();
  }

  /**
   * Save the channels.
   *
   * @param channels the channels
   */
  public void saveChannels(final List<Channel> channels) {

    final List<Key<Channel>> keys = OfyService.ofy().load().type(Channel.class).keys().list();

    OfyService.ofy().transact(new VoidWork() {

      @Override
      public void vrun() {
        if (keys != null && !keys.isEmpty()) {
          OfyService.ofy().delete().keys(keys).now();
        }
        OfyService.ofy().save().entities(channels).now();
      }
    });
  }

  /**
   * Save the processing status.
   *
   * @param status the status
   */
  public void saveProcessingStatus(final ProcessingStatus status) {
    OfyService.ofy().save().entity(status).now();
  }

  /**
   * Save the extra info for a notification type.
   *
   * @param extraInfo the extra info
   */
  public void saveExtraInfo(final ExtraInfo extraInfo) {
    OfyService.ofy().save().entity(extraInfo).now();
  }

  /**
   * List of Enum from the list on datastore.
   *
   * @return the channels
   */
  public List<ChannelOption> getChannelOptions() {
    List<ChannelOption> channels = Lists.newArrayList();
    List<Channel> list = getChannels();
    if (list != null && !list.isEmpty()) {
      for (Channel channel : list) {
        if (channel != null) {
          ChannelOption option = ChannelOption.byName(channel.getChannel());
          if (option != null) {
            channels.add(option);
          }
        }
      }
    }
    return channels;
  }

  /**
   * Gets the channels.
   *
   * @return List of Channel from datastore
   */
  public List<Channel> getChannels() {
    return OfyService.ofy().load().type(Channel.class).list();
  }

  /**
   * Gets the processing status.
   *
   * @return the processing status
   */
  public ProcessingStatus getProcessingStatus() {
    return OfyService.ofy()
            .load()
            .type(ProcessingStatus.class)
            .id(ProcessingStatus.KEY_VALUE)
            .now();
  }

  /**
   * Gets the extra info.
   *
   * @param type the type
   * @return the extra info
   */
  public ExtraInfo getExtraInfo(NotificationType type) {
    return OfyService.ofy()
            .load()
            .type(ExtraInfo.class)
            .id(ExtraInfo.getKeyByType(type))
            .now();
  }

  /**
   * Save message id.
   *
   * @param messageId the message id
   */
  public void saveMessageId(String messageId) {
    OfyService.ofy().save().entity(new MessageId(messageId)).now();
  }

  /**
   * Checks for message id.
   *
   * @param messageId the message id
   * @return true, if successful
   */
  public boolean hasMessageId(String messageId) {

    return null != OfyService.ofy().load().type(MessageId.class).id(messageId).now();
  }

  /**
   * Save rules.
   *
   * @param rules the rules
   */
  public void saveFlatRules(final List<FlatRule> rules) {

    final List<Key<FlatRule>> oldKeys = OfyService.ofy().load().type(FlatRule.class).keys().list();
    final List<Key<FlatRule>> keysToDelete = filterKeyToDelete(oldKeys, rules);
    OfyService.ofy().transact(new VoidWork() {
      @Override
      public void vrun() {
        if (keysToDelete != null && !keysToDelete.isEmpty()) {
          OfyService.ofy().delete().keys(keysToDelete).now();
        }
        OfyService.ofy().save().entities(rules).now();
      }
    });

  }

  private List<Key<FlatRule>> filterKeyToDelete(List<Key<FlatRule>> oldKeys, List<FlatRule> rules) {

    List<Key<FlatRule>> newKeys = buildNewRulesKeys(rules);

    List<Key<FlatRule>> discard = new ArrayList<>();

    for (Key<FlatRule> key : oldKeys) {
      if (!newKeys.contains(key)) {
        discard.add(key);
      }
    }
    return discard;
  }

  private List<Key<FlatRule>> buildNewRulesKeys(List<FlatRule> rules) {
    List<Key<FlatRule>> newKeys = new ArrayList<>();
    for (FlatRule flatRule : rules) {
      newKeys.add(Key.create(FlatRule.class, flatRule.getType()));
    }
    return newKeys;
  }

  /**
   * Gets the rules.
   *
   * @return the rules
   */
  public List<FlatRule> getFlatRules() {
    return OfyService.ofy().load().type(FlatRule.class).list();
  }

  /**
   * Save the configuration.
   *
   * @param configuration the configuration
   */
  public void saveConfiguration(Configuration configuration) {
    OfyService.ofy().save().entity(configuration).now();
  }

  /**
   * Gets the configuration.
   *
   * @return the configuration
   */
  public Configuration getConfiguration() {
    return OfyService.ofy()
            .load()
            .type(Configuration.class)
            .id(Configuration.KEY_VALUE)
            .now();
  }

  public boolean hasAssetHash(String assetHash) {
    return null != OfyService.ofy().load().type(AssetHash.class).id(assetHash).now();
  }

  public void saveAssetHash(String assetHash) {
    OfyService.ofy().save().entity(new AssetHash(assetHash)).now();
  }

  public boolean hasFindingHash(String findingHash) {
    return null != OfyService.ofy().load().type(FindingHash.class).id(findingHash).now();
  }

  public void saveFindingHash(String findinHash) {
    OfyService.ofy().save().entity(new FindingHash(findinHash)).now();
  }
}