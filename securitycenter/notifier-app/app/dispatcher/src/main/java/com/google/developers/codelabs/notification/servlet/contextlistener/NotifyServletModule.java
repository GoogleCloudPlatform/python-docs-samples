package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.developers.codelabs.notification.enums.NotificationQueue;
import com.google.developers.codelabs.notification.filter.NamespaceFilter;
import com.google.developers.codelabs.notification.servlet.ReceiveMessageServlet;
import com.google.developers.codelabs.notification.servlet.cron.CronPubsubPullServlet;
import com.google.developers.codelabs.notification.servlet.task.NotificationWorkerServlet;
import com.google.inject.servlet.ServletModule;

import com.googlecode.objectify.ObjectifyFilter;

/**
 * The Class NotifyServletModule.
 */
public class NotifyServletModule extends ServletModule {
  @Override
  protected void configureServlets() {
    serve("/_ah/push-handlers/receive_message").with(ReceiveMessageServlet.class);

    serve("/cron/pubsub/pull").with(CronPubsubPullServlet.class);

    serve(NotificationQueue.ENTRY.getUrl()).with(NotificationWorkerServlet.class);

    filter("/*").through(ObjectifyFilter.class);
    filter("/*").through(NamespaceFilter.class);
  }

}
