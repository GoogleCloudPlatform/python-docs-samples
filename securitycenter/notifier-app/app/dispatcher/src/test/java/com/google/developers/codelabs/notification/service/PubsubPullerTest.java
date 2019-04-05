package com.google.developers.codelabs.notification.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.google.api.services.pubsub.model.PubsubMessage;
import com.google.api.services.pubsub.model.PullResponse;
import com.google.api.services.pubsub.model.ReceivedMessage;
import com.google.common.collect.Lists;
import com.google.developers.codelabs.notification.enums.NotificationQueue;
import com.google.developers.codelabs.notification.helper.QueueHelper;

import org.junit.Test;

import java.util.List;

/**
 * The Class PubsubPullerTest.
 */
@SuppressWarnings("javadoc")
public class PubsubPullerTest {

  @Test
  public void pullMessageWithoutMessageInsideResponseWontEnqueue() throws Exception {
    QueueHelper queueHelper = mock(QueueHelper.class);
    PubsubCommunication pubsubCommunication = mock(PubsubCommunication.class);

    PullResponse response = new PullResponse();

    when(pubsubCommunication.executePull(anyString(), any(Integer.class)))
        .thenReturn(response);

    PubsubPuller reader = new PubsubPuller(queueHelper, pubsubCommunication);
    reader.pullMessages("asset-notifications-test", "test-subscription-1", 10);

    verify(queueHelper, times(0))
        .addMessageToQueue(any(NotificationQueue.class), any(PubsubMessage.class));
  }

  @Test
  public void pullMessageWithMessageInsideEnqueueSameNumberOfMessages() throws Exception {
    QueueHelper queueHelper = mock(QueueHelper.class);
    PubsubCommunication pubsubCommunication = mock(PubsubCommunication.class);

    PullResponse response = new PullResponse();
    List<ReceivedMessage> receivedMessages = Lists.newArrayList();
    ReceivedMessage receivedMessage = new ReceivedMessage();
    PubsubMessage pubsubMessage = new PubsubMessage();
    receivedMessage.setMessage(pubsubMessage);
    receivedMessages.add(receivedMessage);
    response.setReceivedMessages(receivedMessages);

    when(pubsubCommunication.executePull(anyString(), any(Integer.class)))
        .thenReturn(response);

    PubsubPuller reader = new PubsubPuller(queueHelper, pubsubCommunication);
    reader.pullMessages("asset-notifications-test", "test-subscription-1", 10);

    verify(queueHelper, times(1))
        .addMessageToQueue(any(NotificationQueue.class), any(PubsubMessage.class));
  }

}
