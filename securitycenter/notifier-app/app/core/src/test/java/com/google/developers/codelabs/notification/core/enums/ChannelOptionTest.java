package com.google.developers.codelabs.notification.core.enums;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import org.junit.Test;

@SuppressWarnings("javadoc")
public class ChannelOptionTest {

  @Test
  public void byNameIgnoresCase() {
    assertNotNull(ChannelOption.byName("sms"));
    assertNotNull(ChannelOption.byName("SMS"));
    assertNotNull(ChannelOption.byName("sendgrid"));
    assertNotNull(ChannelOption.byName("gae_email"));
  }

  @Test
  public void byNameReturnsNullOnNotFoundCases() {
    assertNull(ChannelOption.byName("smss"));
  }
}
