package com.google.developers.codelabs.notification.adapter.sms;

import com.google.common.base.Preconditions;
import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.exception.AdapterConfigurationException;
import com.google.developers.codelabs.notification.adapter.exception.AdapterExecutionException;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.message.OutputType;
import com.google.developers.codelabs.notification.service.OutputMessage;
import com.googlecode.objectify.ObjectifyService;
import com.twilio.exception.ApiConnectionException;
import com.twilio.exception.ApiException;
import com.twilio.http.TwilioRestClient;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.rest.api.v2010.account.MessageCreator;
import com.twilio.type.PhoneNumber;
import org.apache.commons.lang3.StringUtils;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * An implementation of a SMS adapter that uses Twilio API.
 * Depends on the configuration of the account sid, auth token and Twilio from telephone number.
 *
 * @author dandrade
 *
 */
public class TwilioSmsAdapter implements NotificationAdapter {

  /** The Constant ACCOUNT_SID_KEY. */
  static final String ACCOUNT_SID_KEY = "SMS_ACCOUNT_SID";

  /** The Constant AUTH_TOKEN_KEY. */
  static final String AUTH_TOKEN_KEY = "SMS_AUTH_TOKEN";

  /** The Constant FROM_NUMBER_KEY. */
  static final String FROM_NUMBER_KEY = "SMS_FROM_NUMBER";

  private static final String SERVICE_ERROR_LOG_MESSAGE = "Twilio API Response with error: "
      + "\nerrorCode[%s], \nerrorMessage[%s], \nbody=[%s], \nsid[%s], \nstatus=[%s]";

  private static final String COMMUNICATION_ERROR_LOG_MESSAGE = "Twilio API Response was null";

  private static final String SUCCESS_LOG_MESSAGE = "Twilio API Response: "
      + "\nBody=[%s], \nSID[%s], \nStatus=[%s]";

  private static final Logger LOG = Logger.getLogger(TwilioSmsAdapter.class.getName());

  private TwilioRestClient restClient;

  private ConfigurationService configurationService;

  /**
   * Constructor that receives a caller provided @{@link ConfigurationService}.
   * @param configurationService configuration service.
   */
  public TwilioSmsAdapter(ConfigurationService configurationService) {
    this(null, configurationService);
  }

  /**
   * Constructor that receives a caller provided {@link TwilioRestClient} and @{@link ConfigurationService}.
   * @param restClient a provided instance of a TwilioRestClient.
   * @param configurationService configuration service.
   */
  public TwilioSmsAdapter(TwilioRestClient restClient, ConfigurationService configurationService) {
    this.restClient = restClient;
    this.configurationService = configurationService;
  }

  @Override
  public ChannelOption getChannel() {
    return ChannelOption.SMS;
  }

  @Override
  public void notify(OutputMessage outputMessage, NotificationUser user) {
    if (StringUtils.isNotBlank(user.getTelephone_number())) {
      validateConfiguration();
      PhoneNumber to = new PhoneNumber(user.getTelephone_number());
      PhoneNumber from = new PhoneNumber(getTwilioFromNumber());
      callTwilio(to, from, outputMessage.buildBody(OutputType.SHORT));
    }
  }

  private void callTwilio(PhoneNumber to, PhoneNumber from, String msg) {
    try {
      Message message = new MessageCreator(to, from, msg).create(getRestClient());
      checkResponse(message);
      logSuccessResponse(message);
    } catch (ApiConnectionException | ApiException e) {
      LOG.severe(e.getMessage());
      throw new AdapterExecutionException("Exception when calling Twilio.", e);
    }
  }

  private String getTwilioFromNumber() {
    return configurationService.getConfig(FROM_NUMBER_KEY);
  }

  private String getTwilioAuthToken() {
    return configurationService.getConfig(AUTH_TOKEN_KEY);
  }

  private String getTwilioAccountSid() {
    return configurationService.getConfig(ACCOUNT_SID_KEY);
  }

  private void checkResponse(Message sms) {
    if (hasError(sms)) {
      String message = generateErrorMessage(sms);
      LOG.warning(message);
      throw new AdapterExecutionException(message);
    }
  }

  private boolean hasError(Message sms) {
    try {
      return sms == null || sms.getErrorCode() != null;
    } catch (IllegalArgumentException e) {
      return false;
    }
  }

  private String generateErrorMessage(Message sms) {
    if (sms == null) {
      return COMMUNICATION_ERROR_LOG_MESSAGE;
    }

    String message = String.format(SERVICE_ERROR_LOG_MESSAGE,
        sms.getErrorCode(),
        sms.getErrorMessage(),
        sms.getBody(),
        sms.getSid(),
        sms.getStatus());
    return message;
  }

  private void logSuccessResponse(Message sms) {
    LOG.info(
        String.format(
            SUCCESS_LOG_MESSAGE,
            sms.getBody(),
            sms.getSid(),
            sms.getStatus()));
  }

  @Override
  public boolean isConfigured() {
    return !Strings.isNullOrEmpty(getTwilioFromNumber())
            && !Strings.isNullOrEmpty(getTwilioAuthToken())
            && !Strings.isNullOrEmpty(getTwilioAccountSid());
  }

  private void validateConfiguration() {
    try {
      Preconditions.checkState(
          !Strings.isNullOrEmpty(getTwilioFromNumber()),
          "TWILIO_FROM_NUMBER is not configured");
      Preconditions.checkState(
          !Strings.isNullOrEmpty(getTwilioAccountSid()),
          "TWILIO_ACCOUNT_SID is not configured");
      Preconditions.checkState(
          !Strings.isNullOrEmpty(getTwilioAuthToken()),
          "TWILIO_AUTH_TOKEN is not configured");
    } catch (IllegalStateException e) {
      String message = "Invalid Twilio configuration.";
      LOG.log(Level.SEVERE, message, e);
      throw new AdapterConfigurationException(message, e);
    }

  }

  /**
   * The creation of {@code TwilioRestClient} may be done at {@code TwilioSmsAdapter} constructor, but we get an {@code {@link IllegalStateException}}
   * thrown by {@code {@link ObjectifyService#ofy()}}, due to the use of {@code {@link ConfigurationService}}, which access the datastore
   */
  private TwilioRestClient getRestClient() {
    if (restClient == null) {
      return new TwilioRestClient.Builder(getTwilioAccountSid(), getTwilioAuthToken()).build();
    }
    return restClient;
  }
}
