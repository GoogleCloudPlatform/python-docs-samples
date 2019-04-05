package com.google.developers.codelabs.notification.servlet.task;

import com.google.common.base.Splitter;
import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.enums.AppEngineHttpHeaders;
import com.google.developers.codelabs.notification.helper.QueueHelper;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.NotificationService;
import com.google.developers.codelabs.notification.servlet.SecurityHeaderVerifier;
import com.google.inject.Inject;
import com.google.inject.Singleton;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Servlet that attends queue.
 */
@Singleton
public class NotificationWorkerServlet extends HttpServlet {

  private static final long serialVersionUID = 1L;

  private static final Logger LOG = Logger.getLogger(NotificationWorkerServlet.class.getName());

  @Inject
  private NotificationService notificationService;

  @Inject
  private SecurityHeaderVerifier securityHeaderVerifier;

  @Override
  protected void doPost(
      final HttpServletRequest request,
      final HttpServletResponse response)
      throws ServletException, IOException {

    securityHeaderVerifier.ensureAtLeastOneAppEngineHeader(request,
        AppEngineHttpHeaders.getTaskHeaders());

    String messageId = getMessageId(request);
    Map<String, String> attributes = getAttributes(request);
    LOG.log(Level.INFO, "Message attributes: {0}", attributes);
    EventContext context = new EventContext(getMessage(request), attributes);

    notificationService.applyRules(messageId, context);

    // Acknowledge the message by returning a success code
    response.setStatus(HttpServletResponse.SC_OK);
    response.getWriter().close();
  }

  private String getMessageId(HttpServletRequest request) {
    return request.getParameter(QueueHelper.MESSAGE_ID);
  }

  private String getMessage(HttpServletRequest request) {
    return request.getParameter(QueueHelper.DATA_KEY);
  }

  private Map<String, String> getAttributes(HttpServletRequest request) {
    Map<String, String> attributes = new HashMap<String, String>();
    String usedKeys = Strings.nullToEmpty(request.getParameter(QueueHelper.USED_KEYS)).trim();
    if (!usedKeys.isEmpty()) {
      for (String key : Splitter.on(',').split(usedKeys)) {
        attributes.put(key, request.getParameter(key));
      }
    }
    return attributes;
  }

}
