package com.google.developers.codelabs.notification.core.service;

import com.google.developers.codelabs.notification.core.model.*;
import com.googlecode.objectify.Objectify;
import com.googlecode.objectify.ObjectifyFactory;
import com.googlecode.objectify.ObjectifyService;

/**
 * The Class OfyService.
 */
public class OfyService {
  static {
    factory().register(AssetHash.class);
    factory().register(FindingHash.class);
    factory().register(NotificationUser.class);
    factory().register(Channel.class);
    factory().register(ProcessingStatus.class);
    factory().register(ExtraInfo.class);
    factory().register(MessageId.class);
    factory().register(FlatRule.class);
    factory().register(Configuration.class);
  }

  /**
   * Factory.
   *
   * @return the objectify factory
   */
  public static ObjectifyFactory factory() {
    return ObjectifyService.factory();
  }

  /**
   * Ofy.
   *
   * @return the objectify
   */
  public static Objectify ofy() {
    return ObjectifyService.ofy();
  }
}
