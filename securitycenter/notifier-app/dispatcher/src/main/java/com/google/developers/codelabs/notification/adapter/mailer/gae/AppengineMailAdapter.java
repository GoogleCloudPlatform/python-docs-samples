package com.google.developers.codelabs.notification.adapter.mailer.gae;

import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.message.OutputType;
import com.google.developers.codelabs.notification.service.OutputMessage;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class AppengineMailAdapter.
 */
public class AppengineMailAdapter implements NotificationAdapter {

  /** The Constant LOG. */
  private static final Logger LOG = Logger.getLogger(AppengineMailAdapter.class.getName());

  /** The Constant FROM_EMAIL_KEY. */
  public static final String FROM_EMAIL_KEY = "GAE_EMAIL_FROM_EMAIL";

  private ConfigurationService configurationService;

  /** The appengine mail sender. */
  private AppengineMailSender appengineMailSender;

  /**
   * Instantiates a new appengine mail adapter.
   *
   * @param appengineMailSender the appengine mail sender
   * @param configurationService configuration service
   */
  public AppengineMailAdapter(AppengineMailSender appengineMailSender,
      ConfigurationService configurationService) {
    this.appengineMailSender = appengineMailSender;
    this.configurationService = configurationService;
  }

  @Override
  public ChannelOption getChannel() {
    return ChannelOption.GAE_EMAIL;
  }

  /**
   * Gets the from.
   *
   * @return the from
   */
  public String getFrom() {
    return configurationService.getConfig(FROM_EMAIL_KEY);
  }

  @Override
  public boolean isConfigured() {
    return !Strings.isNullOrEmpty(getFrom());
  }

  @Override
  public void notify(OutputMessage outputMessage, NotificationUser user) {
    if (!Strings.isNullOrEmpty(user.getEmail())) {
      Properties properties = new Properties();
      Session session = Session.getDefaultInstance(properties, null);

      try {
        Message message = new MimeMessage(session);
        message.setFrom(new InternetAddress(getFrom()));

        message.addRecipient(Message.RecipientType.TO,
            new InternetAddress(user.getEmail()));

        message.setSubject(outputMessage.buildSubject());
        message.setText(outputMessage.buildBody(OutputType.LONG));
        appengineMailSender.send(message);
        LOG.log(Level.INFO, "E-mail message sent");
      } catch (MessagingException e) {
        LOG.log(Level.SEVERE, "This mail was not sent.", e);
      }
    }

  }

}
