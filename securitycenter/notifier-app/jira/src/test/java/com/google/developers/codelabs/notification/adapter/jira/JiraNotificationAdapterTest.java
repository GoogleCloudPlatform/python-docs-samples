package com.google.developers.codelabs.notification.adapter.jira;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.google.developers.codelabs.notification.core.service.ConfigurationService;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
@SuppressWarnings("javadoc")
public class JiraNotificationAdapterTest {

  @Mock
  private ConfigurationService configurationService;


  @Test
  public void withEveryParameterFilledItIsConfigured() {
    when(configurationService.getConfig(Mockito.anyString()))
        .thenReturn("A");
    JiraNotificationAdapter jiraNotificationAdapter =
        new JiraNotificationAdapter(configurationService);
    assertTrue(jiraNotificationAdapter.isConfigured());
  }

  @Test
  public void withOneEmptyParameterItIsNotConfigured() {
    when(configurationService.getConfig(Mockito.anyString()))
        .thenReturn("A");
    when(configurationService.getConfig(Mockito.eq(JiraNotificationAdapter.API_TOKEN)))
        .thenReturn("");
    JiraNotificationAdapter jiraNotificationAdapter =
        new JiraNotificationAdapter(configurationService);
    assertFalse(jiraNotificationAdapter.isConfigured());
  }

}
