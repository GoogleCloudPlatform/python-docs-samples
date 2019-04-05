package com.google.developers.codelabs.notification.servlet;

import com.google.api.client.json.JsonParser;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.pubsub.model.PubsubMessage;
import com.google.developers.codelabs.notification.enums.NotificationQueue;
import com.google.developers.codelabs.notification.helper.QueueHelper;
import com.google.inject.Inject;
import com.google.inject.Singleton;

import java.io.IOException;

import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Processes incoming messages and sends them to the client web app.
 */
@Singleton
public class ReceiveMessageServlet extends HttpServlet {
  private static final long serialVersionUID = 1L;

  @Inject
  private QueueHelper queueHelper;

  @Override
  public final void doPost(
      final HttpServletRequest request,
      final HttpServletResponse response)
      throws IOException {

    ServletInputStream inputStream = request.getInputStream();

    JsonParser parser = JacksonFactory.getDefaultInstance().createJsonParser(inputStream);
    parser.skipToKey("message");

    PubsubMessage message = parser.parseAndClose(PubsubMessage.class);

    getQueueHelper().addMessageToQueue(NotificationQueue.ENTRY, message);

    // Acknowledge the message by returning a success code
    response.setStatus(HttpServletResponse.SC_OK);
    response.getWriter().close();
  }

  /**
   * Gets the queue helper.
   *
   * @return the queue helper
   */
  public QueueHelper getQueueHelper() {
    return queueHelper;
  }



}
