package com.google.developers.codelabs.notification.adapter.mailer.gae;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Transport;

/**
 * The Class AppengineMailSender.
 */
public class AppengineMailSender {

  /**
   * Sends an email using send method from Transport Class.
   *
   * @param message the message
   * @throws MessagingException the messagingException
   */
  public void send(Message message) throws MessagingException {
    Transport.send(message);
  }

}
