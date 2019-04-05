package com.google.developers.codelabs.notification.api.entities;

import com.google.api.server.spi.config.AnnotationBoolean;
import com.google.api.server.spi.config.ApiResourceProperty;

import java.util.List;

/**
 * The Class ChannelsRequestBody.
 */
public class ChannelsRequestBody {

  private List<ChannelRequest> activeChannels;

  /**
   * Gets the active channels.
   *
   * @return the active channels
   */
  public List<ChannelRequest> getActiveChannels() {
    return activeChannels;
  }

  /**
   * Sets the active channels.
   *
   * @param activeChannels the new active channels
   */
  public void setActiveChannels(List<ChannelRequest> activeChannels) {
    this.activeChannels = activeChannels;
  }

  /**
   * Checks if is empty.
   *
   * @return true, if is empty
   */
  @ApiResourceProperty(ignored = AnnotationBoolean.TRUE)
  public boolean isEmpty() {
    return activeChannels == null || activeChannels.isEmpty();
  }
}
