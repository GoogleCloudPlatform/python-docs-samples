package com.google.developers.codelabs.notification.service;

import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.cloudfunction.CloudFunctionExecutor;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.model.ProcessingStatus;
import com.google.developers.codelabs.notification.core.model.ProcessingStatusOptions;
import com.google.developers.codelabs.notification.core.service.DataStoreService;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Arrays;
import java.util.HashMap;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;

@RunWith(MockitoJUnitRunner.class)
public class NotificationServiceTest {

    @Mock
    private DataStoreService datastoreService;

    private NotificationService notificationService;
    private NotificationAdapter appengineEmailAdapter;

    @Before
    public void setUp() {
        this.appengineEmailAdapter = mock(NotificationAdapter.class);
        when(appengineEmailAdapter.getChannel()).thenReturn(ChannelOption.GAE_EMAIL);

        NotificationAdapter sendGridAdapter = mock(NotificationAdapter.class);
        when(sendGridAdapter.getChannel()).thenReturn(ChannelOption.SENDGRID);

        NotificationAdapter smsAdapter = mock(NotificationAdapter.class);
        when(smsAdapter.getChannel()).thenReturn(ChannelOption.SMS);

        NotificationAdapter jiraAdapter = mock(NotificationAdapter.class);
        when(jiraAdapter.getChannel()).thenReturn(ChannelOption.JIRA);

        notificationService = new NotificationService(appengineEmailAdapter,
                sendGridAdapter, smsAdapter, jiraAdapter, datastoreService, mock(CloudFunctionExecutor.class));
    }

    @Test
    public void idempotentWhenOnlyAssetMessageProcessed() {
        // GIVEN
        String assetHash = "vfjao94ur8943jfdasf";
        String messageId = "123456";
        String findingHash = "fa4839r3489yroiefha";
        EventContext context = getEventContext("ASSETS", EventContext.ASSET_HASH, assetHash);

        // GIVEN
        when(datastoreService.hasAssetHash(assetHash)).thenReturn(true);
        when(datastoreService.hasMessageId(messageId)).thenReturn(false);

        // WHEN
        boolean shouldProcessMessage = notificationService.shouldProcessMessage(messageId, context);

        // THEN
        assertFalse(shouldProcessMessage);
        verify(datastoreService, never()).saveAssetHash(assetHash);
        verify(datastoreService, times(1)).saveMessageId(messageId);
        verify(datastoreService, never()).hasFindingHash(findingHash);
    }

    @Test
    public void idempotentWhenOnlyFindingsMessageProcessed() {
        // GIVEN
        String assetHash = "vfjao94ur8943jfdasf";
        String messageId = "123456";
        String findingHash = "fa4839r3489yroiefha";
        EventContext context = getEventContext("FINDINGS", EventContext.FINDING_HASH, findingHash);

        // GIVEN
        when(datastoreService.hasFindingHash(findingHash)).thenReturn(true);
        when(datastoreService.hasMessageId(messageId)).thenReturn(false);

        // WHEN
        boolean shouldProcessMessage = notificationService.shouldProcessMessage(messageId, context);

        // THEN
        assertFalse(shouldProcessMessage);
        verify(datastoreService, never()).saveFindingHash(findingHash);
        verify(datastoreService, times(1)).saveMessageId(messageId);
        verify(datastoreService, never()).hasAssetHash(assetHash);
    }

    @Test
    public void idempotentWhenOnlyMessageIdProcessed() {
        // GIVEN
        String assetHash = "vfjao94ur8943jfdasf";
        String messageId = "123456";
        String findingHash = "fa4839r3489yroiefha";
        EventContext context = getEventContext("ASSETS", EventContext.ASSET_HASH, assetHash);

        // GIVEN
        when(datastoreService.hasAssetHash(assetHash)).thenReturn(false);
        when(datastoreService.hasMessageId(messageId)).thenReturn(true);

        // WHEN
        boolean shouldProcessMessage = notificationService.shouldProcessMessage(messageId, context);

        // THEN
        assertFalse(shouldProcessMessage);
        verify(datastoreService, times(1)).saveAssetHash(assetHash);
        verify(datastoreService, never()).saveMessageId(messageId);
        verify(datastoreService, never()).hasFindingHash(findingHash);
    }

    @Test
    public void notIdempotentWithMessageIdAndAsset() {
        // GIVEN
        String assetHash = "vfjao94ur8943jfdasf";
        String messageId = "123456";
        String findingHash = "fa4839r3489yroiefha";
        EventContext context = getEventContext("ASSETS", EventContext.ASSET_HASH, assetHash);

        // GIVEN
        when(datastoreService.hasAssetHash(assetHash)).thenReturn(false);
        when(datastoreService.hasMessageId(messageId)).thenReturn(false);

        // WHEN
        boolean shouldProcessMessage = notificationService.shouldProcessMessage(messageId, context);

        // THEN
        assertTrue(shouldProcessMessage);
        verify(datastoreService, times(1)).saveAssetHash(assetHash);
        verify(datastoreService, times(1)).saveMessageId(messageId);
        verify(datastoreService, never()).hasFindingHash(findingHash);
    }

    @Test
    public void notIdempotentWithMessageIdAndFindings() {
        // GIVEN
        String assetHash = "vfjao94ur8943jfdasf";
        String messageId = "123456";
        String findingHash = "fa4839r3489yroiefha";
        EventContext context = getEventContext("FINDINGS", EventContext.FINDING_HASH, findingHash);

        // GIVEN
        when(datastoreService.hasFindingHash(findingHash)).thenReturn(false);
        when(datastoreService.hasMessageId(messageId)).thenReturn(false);

        // WHEN
        boolean shouldProcessMessage = notificationService.shouldProcessMessage(messageId, context);

        // THEN
        assertTrue(shouldProcessMessage);
        verify(datastoreService, times(1)).saveFindingHash(findingHash);
        verify(datastoreService, times(1)).saveMessageId(messageId);
        verify(datastoreService, never()).hasAssetHash(assetHash);
    }

    @Test
    public void testNotifyWithAddAddictionalDestEmail() {
        // GIVEN
        when(datastoreService.getProcessingStatus()).thenReturn(new ProcessingStatus(ProcessingStatusOptions.START));
        when(datastoreService.getUsers()).thenReturn(Lists.newArrayList(new NotificationUser()));
        when(datastoreService.getChannelOptions()).thenReturn(Arrays.asList(
            ChannelOption.GAE_EMAIL, ChannelOption.JIRA, ChannelOption.SENDGRID, ChannelOption.SMS));
        when(appengineEmailAdapter.isConfigured()).thenReturn(true);
        String expectedEmail = "test@email.com";
        EventContext context = new EventContext("{\"name\": \"test message\"}", ImmutableMap.of("Additional_Dest_Email", expectedEmail));
        OutputMessage message = new OutputMessage(NotificationType.ASSETS, ActionType.ALL, context);

        // WHEN
        notificationService.callAdapters(message, false);

        // THEN
        verify(appengineEmailAdapter, atLeastOnce()).notify(any(), argThat(arg -> arg.getEmail() == null));
        verify(appengineEmailAdapter, atLeastOnce()).notify(any(), argThat(arg -> expectedEmail.equals(arg.getEmail())));
    }

    private EventContext getEventContext(String notificationType, String hashKey, String hashValue) {
        String message = "{\"name\": \"pubsub data\"}";
        HashMap<String, String> attributes = new HashMap<>();
        attributes.put(hashKey, hashValue);
        attributes.put(EventContext.NOTIFICATION_TYPE_KEY, notificationType);
        return new EventContext(message, attributes);
    }
}
