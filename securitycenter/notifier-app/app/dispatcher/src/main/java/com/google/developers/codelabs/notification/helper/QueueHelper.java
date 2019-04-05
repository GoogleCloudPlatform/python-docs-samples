package com.google.developers.codelabs.notification.helper;

import com.google.api.services.pubsub.model.PubsubMessage;
import com.google.appengine.api.taskqueue.Queue;
import com.google.appengine.api.taskqueue.QueueFactory;
import com.google.appengine.api.taskqueue.TaskOptions;
import com.google.appengine.api.taskqueue.TaskOptions.Method;
import com.google.common.base.Joiner;
import com.google.developers.codelabs.notification.enums.NotificationQueue;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map.Entry;
import java.util.logging.Logger;

/**
 * The Class QueueHelper.
 */
public class QueueHelper {

  /** The Constant MESSAGE_ID. */
  public static final String MESSAGE_ID = "messageId";

  /** The Constant DATA_KEY. */
  public static final String DATA_KEY = "data";

  /** The Constant USED_KEYS. */
  public static final String USED_KEYS = "noti_internal_used_keys";

  private static final Logger LOG = Logger.getLogger(QueueHelper.class.getName());

  private String buildMessageText(PubsubMessage message) {
    String messageText = new String(message.decodeData(), StandardCharsets.UTF_8);
    LOG.info(String.format("Message: %s", messageText));
    return messageText;
  }

  private void addAttributesToTask(TaskOptions task, PubsubMessage message) {
    if (message.getAttributes() != null) {
      List<String> usedKeys = new ArrayList<>();

      for (Entry<String, String> entry : message.getAttributes().entrySet()) {
        task.param(entry.getKey(), entry.getValue());
        usedKeys.add(entry.getKey());
      }
      if (!usedKeys.isEmpty()) {
        task.param(USED_KEYS, Joiner.on(",").join(usedKeys));
      }
    }
  }

  /**
   * Adds the message to queue.
   *
   * @param notificationQueue the notification queue
   * @param message the message
   */
  public void addMessageToQueue(NotificationQueue notificationQueue, PubsubMessage message) {
    Queue queue = QueueFactory.getQueue(notificationQueue.getQueueName());

    TaskOptions task = TaskOptions.Builder
        .withMethod(Method.POST)
        .url(notificationQueue.getUrl())
        .param(DATA_KEY, buildMessageText(message))
        .param(MESSAGE_ID, message.getMessageId());

    addAttributesToTask(task, message);

    queue.add(task);
  }
}
