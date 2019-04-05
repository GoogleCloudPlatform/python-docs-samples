package com.google.developers.codelabs.notification.service;

import com.google.api.services.pubsub.model.PubsubMessage;
import com.google.api.services.pubsub.model.PullResponse;
import com.google.api.services.pubsub.model.ReceivedMessage;
import com.google.common.base.Joiner;
import com.google.developers.codelabs.notification.enums.NotificationQueue;
import com.google.developers.codelabs.notification.helper.QueueHelper;
import com.google.inject.Inject;

import java.util.ArrayList;
import java.util.List;

/**
 * Class that reads messages from a pubsub topic.
 */
public class PubsubPuller {
  private final QueueHelper queueHelper;
  private final PubsubCommunication pubsubCommunication;

  /**
   * Constructor that injects dependencies.
   * @param queueHelper
   * @param pubsubCommunication
   */
  @Inject
  public PubsubPuller(QueueHelper queueHelper,
      PubsubCommunication pubsubCommunication) {
    this.queueHelper = queueHelper;
    this.pubsubCommunication = pubsubCommunication;
  }

  /**
   * Pulls messages from the given subscription.
   *
   * @param project
   * @param subscription
   * @param batchSize
   */
  public void pullMessages(String project, String subscription, Integer batchSize) {
    String subscriptionName = createSubscriptionName(project, subscription);

    PullResponse pullResponse = getPubsubCommunication()
        .executePull(subscriptionName, batchSize);
    if (pullResponse != null) {
      List<ReceivedMessage> receivedMessages = pullResponse.getReceivedMessages();
      if (receivedMessages != null && !receivedMessages.isEmpty()) {
        List<String> ackIds = enqueueMessages(batchSize, receivedMessages);
        getPubsubCommunication().sendAck(subscriptionName, ackIds);
      }
    }
  }

  private PubsubCommunication getPubsubCommunication() {
    return this.pubsubCommunication;
  }

  private String createSubscriptionName(String project, String subscription) {
    return Joiner.on("/").join("projects", project, "subscriptions", subscription);
  }

  private List<String> enqueueMessages(Integer batchSize,
      List<ReceivedMessage> receivedMessages) {
    List<String> ackIds = new ArrayList<>(batchSize);
    for (ReceivedMessage receivedMessage : receivedMessages) {
      PubsubMessage message = receivedMessage.getMessage();
      getQueueHelper().addMessageToQueue(NotificationQueue.ENTRY, message);
      ackIds.add(receivedMessage.getAckId());
    }
    return ackIds;
  }

  private QueueHelper getQueueHelper() {
    return this.queueHelper;
  }
}
