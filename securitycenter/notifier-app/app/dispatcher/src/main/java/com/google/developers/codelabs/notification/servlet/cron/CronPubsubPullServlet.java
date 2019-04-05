package com.google.developers.codelabs.notification.servlet.cron;

import com.google.common.base.Optional;
import com.google.common.base.Strings;
import com.google.common.primitives.Ints;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.enums.AppEngineHttpHeaders;
import com.google.developers.codelabs.notification.service.PubsubPuller;
import com.google.developers.codelabs.notification.servlet.SecurityHeaderVerifier;
import com.google.inject.Inject;
import com.google.inject.Singleton;

import java.io.IOException;
import java.util.logging.Logger;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Cron servlet that pulls from pubsub topic.
 */
@Singleton
public class CronPubsubPullServlet extends HttpServlet {

  private static final long serialVersionUID = 1L;

  private static final Logger LOG = Logger.getLogger(CronPubsubPullServlet.class.getName());

  private static final Integer DEFAULT_BATCH_SIZE = 1000;

  @Inject
  private PubsubPuller reader;

  @Inject
  private SecurityHeaderVerifier securityHeaderVerifier;

  @Inject
  private ConfigurationService configurationService;

  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
    doPost(request, response);
  }

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {

    securityHeaderVerifier.ensureAtLeastOneAppEngineHeader(request,
        AppEngineHttpHeaders.getCronHeaders());

    String project = configurationService.getConfig("PUBSUB_PULL_PROJECT");
    String subscription = configurationService.getConfig("PUBSUB_PULL_SUBSCRIPTION");

    if (isConfigured(project, subscription)) {
      
      int batchSize = Optional
          .fromNullable(Ints.tryParse(configurationService.getConfig("PUBSUB_PULL_BATCH_SIZE")))
          .or(DEFAULT_BATCH_SIZE);
      
      LOG.info(String.format("PULLING %d messages from %s on subscription %s",
          batchSize,
          project,
          subscription));

      this.reader.pullMessages(project, subscription, batchSize);
    } else {
      LOG.info(String.format("PULL subscription-type is not configured. PULLING is disabled."));
    }

  }

  private boolean isConfigured(String project, String subscription) {
    return !Strings.nullToEmpty(project).trim().isEmpty()
        && !Strings.nullToEmpty(subscription).trim().isEmpty();
  }

}
