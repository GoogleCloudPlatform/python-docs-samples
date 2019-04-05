package com.google.developers.codelabs.notification.api.entities;

/**
 * The Class ChannelRequest.
 */
public class ChannelRequest {

  private String channel;

  /**
   * Gets the channel.
   *
   * @return the channel
   */
  public String getChannel() {
    return channel;
  }

  /**
   * Sets the channel.
   *
   * @param channel the new channel
   */
  public void setChannel(String channel) {
    this.channel = channel;
  }

  @Override
  public String toString() {
    return "ChannelRequest [channel=" + channel + "]";
  }
}
