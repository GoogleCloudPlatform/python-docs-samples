package com.google.developers.codelabs.notification.adapter.mailer.gae;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.OutputMessage;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

import javax.mail.Message;
import javax.mail.MessagingException;
import java.util.HashMap;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * The Class AppengineMailAdapterTest.
 */
@RunWith(MockitoJUnitRunner.class)
@SuppressWarnings("javadoc")
public class AppengineMailAdapterTest {

  @Mock
  private AppengineMailSender appengineMailSender;

  @Mock
  private ConfigurationService configurationService;

  @Test
  public void notifyCallsMailSender() throws MessagingException {
    String from = "sender@example.com";
    when(configurationService.getConfig(Mockito.eq(AppengineMailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(from);
    String to = "destination@example.com";
    String subject = "{\"name\": \"AppengineMailAPI test\"}";

    NotificationUser user = new NotificationUser(to, null, null, null);

    AppengineMailAdapter adapter =
        new AppengineMailAdapter(appengineMailSender, configurationService);
    EventContext context = new EventContext(subject, new HashMap<String, String>());
    OutputMessage outputMessage =
        new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);
    adapter.notify(outputMessage, user);

    verify(appengineMailSender).send(any(Message.class));
  }

  @Test
  public void withoutFromMailItIsNotConfigured() throws Exception {
    String from = "";
    when(configurationService.getConfig(Mockito.eq(AppengineMailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(from);
    AppengineMailAdapter adapter =
        new AppengineMailAdapter(appengineMailSender, configurationService);
    assertFalse(adapter.isConfigured());
  }

  @Test
  public void withFromMailItIsConfigured() throws Exception {
    String from = "from@example.com";
    when(configurationService.getConfig(Mockito.eq(AppengineMailAdapter.FROM_EMAIL_KEY)))
        .thenReturn(from);
    AppengineMailAdapter adapter =
        new AppengineMailAdapter(appengineMailSender, configurationService);
    assertTrue(adapter.isConfigured());
  }

}
