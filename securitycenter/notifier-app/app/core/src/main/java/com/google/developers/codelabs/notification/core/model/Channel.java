package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.MoreObjects;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class Channel.
 */
@Entity
public class Channel {

  @Id
  private String channel;

  /**
   * Instantiates a new channel.
   *
   * @param channel the channel
   */
  public Channel(String channel) {
    this.channel = channel;
  }

  /**
   * Instantiates a new channel.
   */
  public Channel() {}

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("channel", channel)
        .toString();
  }

  /**
   * Gets the channel.
   *
   * @return the channel
   */
  public String getChannel() {
    return channel;
  }

}
