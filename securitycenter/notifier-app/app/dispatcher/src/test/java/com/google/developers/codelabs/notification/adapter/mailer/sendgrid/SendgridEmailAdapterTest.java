package com.google.developers.codelabs.notification.adapter.mailer.sendgrid;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.OutputMessage;
import com.sendgrid.Request;
import com.sendgrid.Response;
import com.sendgrid.SendGrid;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.HashMap;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * The Class SendgridEmailAdapterTest.
 */
@RunWith(MockitoJUnitRunner.class)
@SuppressWarnings("javadoc")
public class SendgridEmailAdapterTest {

  @Mock
  private SendGrid sendGrid;

  @Mock
  private ConfigurationService configurationService;

  @Test
  public void notifyEmailCallsSendGridApiMethod() throws Exception {
    Response response = new Response();
    doReturn(response).when(sendGrid).api(any(Request.class));

    String fromEmail = "sender@example.com";
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(fromEmail);

    SendgridEmailAdapter adapter = new SendgridEmailAdapter(sendGrid, configurationService);

    String emailSubject = "{\"name\": \"Hello World from the SendGrid Java Library!\"}";
    String toEmail = "destination@example.com";
    NotificationUser user = new NotificationUser(toEmail, null, null, null);

    EventContext context = new EventContext(emailSubject, new HashMap<String, String>());
    OutputMessage outputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);
    adapter.notify(outputMessage, user);


    verify(sendGrid).api(any(Request.class));
  }

  @Test
  public void withoutApiKeyItIsNotConfigured() throws Exception {
    String fromEmail = "sender@example.com";
    String apiKey = null;
    String replyTo = "replyto@example.com";
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(fromEmail);
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.API_KEY_KEY)))
        .thenReturn(apiKey);
    when(
        configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.REPLYTO_EMAIL_KEY)))
            .thenReturn(replyTo);
    SendgridEmailAdapter adapter = new SendgridEmailAdapter(sendGrid,
        configurationService);

    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withoutReplyToItIsNotConfigured() throws Exception {
    String fromEmail = "sender@example.com";
    String replyTo = "";
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(fromEmail);
    when(
        configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.REPLYTO_EMAIL_KEY)))
            .thenReturn(replyTo);
    SendgridEmailAdapter adapter = new SendgridEmailAdapter(sendGrid,
        configurationService);

    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withNothingConfigured() throws Exception {

    SendgridEmailAdapter adapter = new SendgridEmailAdapter(sendGrid, configurationService);

    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withEveryDataNeedeItIsConfigured() throws Exception {
    String fromEmail = "sender@example.com";
    String apiKey = "apyKey";
    String replyTo = "replyto@example.com";
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(fromEmail);
    when(configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.API_KEY_KEY)))
        .thenReturn(apiKey);
    when(
        configurationService.getConfig(Mockito.eq(SendgridEmailAdapter.REPLYTO_EMAIL_KEY)))
            .thenReturn(replyTo);
    SendgridEmailAdapter adapter = new SendgridEmailAdapter(sendGrid,
        configurationService);

    assertTrue(adapter.isConfigured());
  }

}
