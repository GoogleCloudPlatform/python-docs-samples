package com.google.developers.codelabs.notification.adapter.jira;

import com.google.api.client.json.GenericJson;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.message.OutputType;
import com.google.developers.codelabs.notification.service.OutputMessage;

import java.util.Map;
import java.util.TreeMap;

/**
 * Class JiraIssueBuilder.
 */
public class JiraIssueBuilder {
  /**
   * Create a json String representing a Jira Issue with the parameters.
   * @param outputMessage
   * @param user
   * @param projectKey
   * @param issueTypeName
   * @return a string representing a Jira Issue.
   */
  public String asJson(OutputMessage outputMessage, NotificationUser user, String projectKey,
                       String issueTypeName) {
    if (outputMessage == null || user == null || projectKey == null || issueTypeName == null) {
      return "";
    }

    GenericJson genericJson = new GenericJson();
    genericJson.setFactory(JacksonFactory.getDefaultInstance());
    Map<String, Object> fields = new TreeMap<>();
    fields.put("summary", outputMessage.buildSubject());
    fields.put("description", outputMessage.buildBody(OutputType.LONG));

    Map<String, String> project = new TreeMap<>();
    project.put("key", projectKey);
    fields.put("project", project);

    Map<String, String> issueType = new TreeMap<>();
    issueType.put("name", issueTypeName);
    fields.put("issuetype", issueType);

    Map<String, String> assignee = new TreeMap<>();
    assignee.put("name", user.getJira_uid());
    fields.put("assignee", assignee);

    genericJson.set("fields", fields);
    return genericJson.toString();
  }

}
