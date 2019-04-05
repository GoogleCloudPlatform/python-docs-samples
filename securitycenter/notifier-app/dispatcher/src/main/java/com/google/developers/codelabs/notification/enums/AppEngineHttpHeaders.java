package com.google.developers.codelabs.notification.enums;

import com.google.common.collect.Sets;

import java.util.Set;

/**
 * The Enum AppEngineHttpHeaders.
 */
public enum AppEngineHttpHeaders {

  /** The x appengine cron. */
  X_APPENGINE_CRON("X-AppEngine-Cron", "cron"),

  /** The x appengine queue name. */
  X_APPENGINE_QUEUENAME("X-AppEngine-QueueName", "task"),

  /** The x appengine task name. */
  X_APPENGINE_TASKNAME("X-AppEngine-TaskName", "task"),

  /** The x appengine task retry count. */
  X_APPENGINE_TASKRETRYCOUNT("X-AppEngine-TaskRetryCount", "task"),

  /** The x appengine task execution count. */
  X_APPENGINE_TASKEXECUTIONCOUNT("X-AppEngine-TaskExecutionCount", "task"),

  /** The x appengine task eta. */
  X_APPENGINE_TASKETA("X-AppEngine-TaskETA", "task");
  // @formatter:on

  /** The header. */
  private String header;

  /** The type. */
  private String type;

  /**
   * Instantiates a new app engine http headers.
   *
   * @param header the header
   * @param type the type
   */
  private AppEngineHttpHeaders(String header, String type) {
    this.header = header;
    this.type = type;
  }

  /**
   * Get the cron headers.
   *
   * @return list with cron headers.
   */
  public static Set<AppEngineHttpHeaders> getCronHeaders() {
    Set<AppEngineHttpHeaders> cronHeaders = Sets.newHashSet();
    for (AppEngineHttpHeaders header : AppEngineHttpHeaders.values()) {
      if (header.getType().equals("cron")) {
        cronHeaders.add(header);
      }
    }
    return cronHeaders;
  }

  /**
   * Get the task headers.
   *
   * @return list with task headers.
   */
  public static Set<AppEngineHttpHeaders> getTaskHeaders() {
    Set<AppEngineHttpHeaders> taskHeaders = Sets.newHashSet();
    for (AppEngineHttpHeaders header : AppEngineHttpHeaders.values()) {
      if (header.getType().equals("task")) {
        taskHeaders.add(header);
      }
    }
    return taskHeaders;
  }

  /**
   * Gets the header.
   *
   * @return the header
   */
  public String getHeader() {
    return header;
  }

  /**
   * Gets the type.
   *
   * @return the type
   */
  public String getType() {
    return type;
  }



}
