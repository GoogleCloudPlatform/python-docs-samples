package com.google.developers.codelabs.notification.adapter.sms;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.adapter.exception.AdapterConfigurationException;
import com.google.developers.codelabs.notification.adapter.exception.AdapterExecutionException;
import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.OutputMessage;
import com.twilio.http.Request;
import com.twilio.http.Response;
import com.twilio.http.TwilioRestClient;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.HashMap;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.when;

/**
 * The Class TwilioSmsAdapterTest.
 */
@RunWith(MockitoJUnitRunner.class)
@SuppressWarnings("javadoc")
public class TwilioSmsAdapterTest {

  private static final String FROM_NUMBER = "+15558675309";
  private static final String TWILIO_ACCOUNT_SID = "TWILIO_ACCOUNT_SID";
  private static final String TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN";
  private static final String MSG_BODY = "{\"name\": \"Ignoranti, quem portum petat, nullus suus ventus est\"}";

  @Mock
  private TwilioRestClient restClient;

  @Mock
  private ConfigurationService configurationService;

  @SuppressWarnings("unchecked")
  @Before
  public void setup() throws Exception {
    Response response = new Response("{\"sid\":\"worked\",\"status\":\"delivered\"}", TwilioRestClient.HTTP_STATUS_CODE_OK);
    doReturn(response).when(restClient).request(any(Request.class));
    doReturn(new ObjectMapper()).when(restClient).getObjectMapper();
    when(configurationService.getConfig(TwilioSmsAdapter.ACCOUNT_SID_KEY))
        .thenReturn(TWILIO_ACCOUNT_SID);
    when(configurationService.getConfig(TwilioSmsAdapter.AUTH_TOKEN_KEY))
        .thenReturn(TWILIO_AUTH_TOKEN);
  }

  @Test
  public void sendSmsNotification() {
    when(configurationService.getConfig(Mockito.eq(TwilioSmsAdapter.FROM_NUMBER_KEY)))
        .thenReturn(FROM_NUMBER);
    NotificationUser user = new NotificationUser(null, FROM_NUMBER, null, null);
    NotificationAdapter adapter =
        new TwilioSmsAdapter(restClient, configurationService);
    EventContext context = new EventContext(MSG_BODY, new HashMap<>());
    OutputMessage OutputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

    adapter.notify(OutputMessage, user);
  }

  @Test(expected = AdapterConfigurationException.class)
  public void validateConfigurationToPhoneNumber() {
    NotificationUser user = new NotificationUser(null, FROM_NUMBER, null, null);
    NotificationAdapter adapter = new TwilioSmsAdapter(restClient, configurationService);
    EventContext context = new EventContext(MSG_BODY, new HashMap<>());
    OutputMessage OutputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

    adapter.notify(OutputMessage, user);
  }

  @Test(expected = AdapterConfigurationException.class)
  public void validateConfigurationRestClient() {
    NotificationUser user = new NotificationUser(null, FROM_NUMBER, null, null);
    NotificationAdapter adapter = new TwilioSmsAdapter(configurationService);
    EventContext context = new EventContext(MSG_BODY, new HashMap<>());
    OutputMessage OutputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

    adapter.notify(OutputMessage, user);
  }

  @SuppressWarnings("unchecked")
  @Test(expected = AdapterExecutionException.class)
  public void notificationExecutionConnectionFailure() throws Exception {
    doReturn(null).when(restClient).request(any(Request.class));

    when(configurationService.getConfig(Mockito.eq(TwilioSmsAdapter.FROM_NUMBER_KEY)))
        .thenReturn(FROM_NUMBER);

    NotificationUser user = new NotificationUser(null, FROM_NUMBER, null, null);
    NotificationAdapter adapter =
        new TwilioSmsAdapter(restClient, configurationService);
    EventContext context = new EventContext(MSG_BODY, new HashMap<>());
    OutputMessage OutputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

    adapter.notify(OutputMessage, user);
  }

  @SuppressWarnings("unchecked")
  @Test(expected = AdapterExecutionException.class)
  public void notificationExecutionApiError() throws Exception {
    doReturn(null).when(restClient).request(any(Request.class));
    when(configurationService.getConfig(TwilioSmsAdapter.FROM_NUMBER_KEY))
        .thenReturn(FROM_NUMBER);

    NotificationUser user = new NotificationUser(null, FROM_NUMBER, null, null);
    NotificationAdapter adapter = new TwilioSmsAdapter(restClient, configurationService);
    EventContext context = new EventContext(MSG_BODY, new HashMap<>());
    OutputMessage OutputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

    adapter.notify(OutputMessage, user);
  }

  @Test
  public void withoutNumberItIsNotConfigured() throws Exception {
    NotificationAdapter adapter =
        new TwilioSmsAdapter(restClient, configurationService);
    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withoutRestClientItIsNotConfigured() throws Exception {
    TwilioRestClient restClient = null;
    NotificationAdapter adapter =
        new TwilioSmsAdapter(restClient, configurationService);
    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withRestClientAndFromNumberItIsConfigured() throws Exception {
    String fromNumber = "+5531991212212";
    when(configurationService.getConfig(Mockito.eq(TwilioSmsAdapter.FROM_NUMBER_KEY)))
        .thenReturn(fromNumber);
    NotificationAdapter adapter =
        new TwilioSmsAdapter(restClient, configurationService);
    assertTrue(adapter.isConfigured());
  }

}
