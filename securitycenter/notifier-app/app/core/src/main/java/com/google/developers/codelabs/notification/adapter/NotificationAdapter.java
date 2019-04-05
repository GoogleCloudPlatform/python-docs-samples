package com.google.developers.codelabs.notification.adapter;

import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.service.OutputMessage;

/**
 * Commmon notification Adapter.
 */
public interface NotificationAdapter {

  /**
   * Notify.
   *
   * @param outputMessage Data to be used to compose the notification message.
   * @param user           An user with all the necessary information for sending notifications.
   */
  void notify(OutputMessage outputMessage, NotificationUser user);

  /**
   * Checks if is configured.
   *
   * @return if this adapter is configured.
   */
  boolean isConfigured();

  /**
   * Gets the channel.
   *
   * @return the ChannelOption of this adapter
   */
  ChannelOption getChannel();
}
