package com.google.developers.codelabs.notification.core.enums;

import com.google.common.base.Strings;

/**
 * Channel enum.
 */
public enum ChannelOption {

  /** SMS with Twilio. */
  SMS,

  /** JIRA. */
  JIRA,

  /** Google App Engine Email. */
  GAE_EMAIL,

  /** Email with Sendgrid. */
  SENDGRID;


  /**
   * Search ChannelOption by name, ignoring the case.
   * @param name to be searched on the values
   * @return ChannelOption found ignoring case
   */
  public static ChannelOption byName(String name) {
    ChannelOption notFound = null;
    if (!Strings.isNullOrEmpty(name)) {
      for (ChannelOption option : values()) {
        if (name.equalsIgnoreCase(option.toString())) {
          return option;
        }
      }
    }
    return notFound;
  }
}
