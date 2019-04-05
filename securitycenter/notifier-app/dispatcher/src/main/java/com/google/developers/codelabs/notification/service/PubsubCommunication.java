package com.google.developers.codelabs.notification.service;

import com.google.api.services.pubsub.Pubsub;
import com.google.api.services.pubsub.model.AcknowledgeRequest;
import com.google.api.services.pubsub.model.PullRequest;
import com.google.api.services.pubsub.model.PullResponse;
import com.google.common.base.Preconditions;
import com.google.inject.Inject;

import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Executes the pull on a pubsub client.
 */
public class PubsubCommunication {

  private static final Logger LOG = Logger.getLogger(PubsubCommunication.class.getName());

  private final Pubsub client;

  /**
   * Default constructor.
   */
  public PubsubCommunication() {
    this(null);
  }

  /**
   * Constructor with client.
   * @param client
   */
  @Inject
  public PubsubCommunication(Pubsub client) {
    super();
    this.client = Preconditions.checkNotNull(client);
  }

  /**
   * Execute pull on a subscription
   * @param subscriptionName
   * @param batchSize
   * @return pubsub response
   */
  public PullResponse executePull(String subscriptionName, Integer batchSize) {
    PullResponse pullResponse = null;

    try {
      PullRequest pullRequest = new PullRequest()
          .setReturnImmediately(false)
          .setMaxMessages(batchSize);

      pullResponse = client.projects().subscriptions()
          .pull(subscriptionName, pullRequest)
          .execute();
    } catch (IOException e) {
      LOG.log(Level.WARNING, "Error pulling", e);
    }

    return pullResponse;
  }

  /**
   * Send ack to messages received.
   *
   * @param subscriptionName
   * @param ackIds
   */
  public void sendAck(String subscriptionName, List<String> ackIds) {
    AcknowledgeRequest ackRequest = new AcknowledgeRequest();
    ackRequest.setAckIds(ackIds);

    try {
      client.projects().subscriptions()
          .acknowledge(subscriptionName, ackRequest)
          .execute();
    } catch (IOException e) {
      LOG.log(Level.WARNING, "Error sending ack on pull", e);
    }
  }

}
