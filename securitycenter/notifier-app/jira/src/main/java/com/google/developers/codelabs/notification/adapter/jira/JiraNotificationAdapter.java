package com.google.developers.codelabs.notification.adapter.jira;

import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.adapter.NotificationAdapter;
import com.google.developers.codelabs.notification.core.enums.ChannelOption;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.service.OutputMessage;

/**
 * Jira Notification Adapter.
 */
public class JiraNotificationAdapter implements NotificationAdapter {
  /** The Constant URL_KEY. */
  public static final String URL_KEY = "JIRA_URL";

  /** The Constant USER_NAME_KEY. */
  public static final String USER_NAME_KEY = "JIRA_USER_NAME";

  /** The Constant ISSUE_TYPE_NAME_KEY. */
  public static final String ISSUE_TYPE_NAME_KEY = "JIRA_ISSUE_TYPE_NAME";

  /** The Constant PROJECT_KEY_KEY. */
  public static final String PROJECT_KEY_KEY = "JIRA_PROJECT_KEY";

  /** The Constant API_TOKEN. */
  public static final String API_TOKEN = "JIRA_API_TOKEN";

  private ConfigurationService configurationService;

  /**
   * Constructor.
   * @param configurationService configuration service.
   */
  public JiraNotificationAdapter(ConfigurationService configurationService) {
    super();
    this.configurationService = configurationService;
  }

  @Override
  public ChannelOption getChannel() {
    return ChannelOption.JIRA;
  }

  /**
   * Gets the jira url.
   *
   * @return the jira url
   */
  public String getUrl() {
    return configurationService.getConfig(URL_KEY);
  }

  /**
   * Gets the jira project key.
   *
   * @return the jira project key
   */
  public String getProjectKey() {
    return configurationService.getConfig(PROJECT_KEY_KEY);
  }

  /**
   * Gets the issue type name.
   *
   * @return the issue type name
   */
  public String getIssueTypeName() {
    return configurationService.getConfig(ISSUE_TYPE_NAME_KEY);
  }

  /**
   * Gets the jira user name.
   *
   * @return the jira user name
   */
  public String getUserName() {
    return configurationService.getConfig(USER_NAME_KEY);
  }

  /**
   * Gets the jira api token.
   *
   * @return the jira api token
   */
  public String getApiToken() {
    return configurationService.getConfig(API_TOKEN);
  }

  /**
   * Verify if every parameter has been provided.
   * @return every parameter has been provided?
   */
  @Override
  public boolean isConfigured() {
    return !Strings.isNullOrEmpty(getUrl()) &&
        !Strings.isNullOrEmpty(getProjectKey()) &&
        !Strings.isNullOrEmpty(getIssueTypeName()) &&
        !Strings.isNullOrEmpty(getUserName()) &&
        !Strings.isNullOrEmpty(getApiToken());
  }

  @Override
  public void notify(OutputMessage outputMessage, NotificationUser user) {
    JiraRequest request = getJiraRequest();
    JiraIssueBuilder issueBuilder = getJiraIssueBuilder();
    String json = issueBuilder.asJson(outputMessage, user, getProjectKey(), getIssueTypeName());
    request.createIssue(json);
  }

  /**
   * @return jiraissueBuilder instance
   */
  private JiraIssueBuilder getJiraIssueBuilder() {
    return new JiraIssueBuilder();
  }

  /**
   * @return
   */
  private JiraRequest getJiraRequest() {
    return new JiraRequest(getUrl(), getUserName(), getApiToken());
  }

}
