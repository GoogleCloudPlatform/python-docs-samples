package com.google.developers.codelabs.notification.adapter.mailer.sendgrid;

import com.google.api.client.repackaged.com.google.common.base.Strings;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.exception.AdapterExecutionException;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.message.OutputType;
import com.google.developers.codelabs.notification.service.OutputMessage;
import com.sendgrid.*;

import java.io.IOException;
import java.util.Optional;
import java.util.logging.Logger;

/**
 * The Class SendgridEmailAdapter.
 */
public class SendgridEmailAdapter implements NotificationAdapter {

  /** The Constant REPLYTO_EMAIL_KEY. */
  public static final String REPLYTO_EMAIL_KEY = "SENDGRID_REPLYTO_EMAIL";

  /** The Constant FROM_EMAIL_KEY. */
  public static final String FROM_EMAIL_KEY = "SENDGRID_FROM_EMAIL";

  /** The Constant API_KEY_KEY. */
  public static final String API_KEY_KEY = "SENDGRID_API_KEY";

  private static final Logger LOG = Logger.getLogger(SendgridEmailAdapter.class.getName());

  private ConfigurationService configurationService;
  private SendGrid sendGrid;

  /**
   * Instantiates a new sendgrid email adapter.
   *
   * @param sendGrid the send grid
   * @param configurationService configuration service.
   */
  public SendgridEmailAdapter(SendGrid sendGrid,
      ConfigurationService configurationService) {
    super();
    this.sendGrid = sendGrid;
    this.configurationService = configurationService;
  }

  @Override
  public ChannelOption getChannel() {
    return ChannelOption.SENDGRID;
  }

  /**
   * Gets the key.
   *
   * @return the key
   */
  public String getKey() {
    return configurationService.getConfig(API_KEY_KEY);
  }

  /**
   * Gets the from.
   *
   * @return the from
   */
  public String getFrom() {
    return configurationService.getConfig(FROM_EMAIL_KEY);
  }

  /**
   * Gets the replyto.
   *
   * @return the replyto
   */
  public String getReplyto() {
    return Optional.ofNullable(configurationService.getConfig(REPLYTO_EMAIL_KEY)).orElse(Strings.nullToEmpty(getFrom()));
  }

  @Override
  public boolean isConfigured() {
    return !Strings.isNullOrEmpty(getReplyto())
        && !Strings.isNullOrEmpty(getFrom())
        && !Strings.isNullOrEmpty(getKey());
  }

  @Override
  public void notify(OutputMessage outputMessage, NotificationUser user) {
    Email from = new Email(getFrom());
    Email toEmail = new Email(user.getEmail());
    Email replyTo = new Email(getReplyto());

    Content plainContent =
        new Content("text/plain", outputMessage.buildBody(OutputType.LONG));

    Mail mail = new Mail(from, outputMessage.buildSubject(), toEmail, plainContent);
    mail.setReplyTo(replyTo);

    Response response;

    try {
      Request request = new Request();
      request.setMethod(Method.POST);
      request.setEndpoint("mail/send");
      request.setBody(mail.build());
      response = getSendGrid().api(request);
    } catch (IOException e) {
      throw new AdapterExecutionException("Error contacting sendgrid", e);
    }

    if (response != null) {
      LOG.info(String.format("statusCode=[%d]\nbody=[%s]\nheaders=[%s]\n",
          response.getStatusCode(),
          response.getBody(),
          response.getHeaders()));
    }
  }

  private SendGrid getSendGrid() {
    if (sendGrid == null) {
      return new SendGrid(getKey());
    }
    return sendGrid;
  }

}
