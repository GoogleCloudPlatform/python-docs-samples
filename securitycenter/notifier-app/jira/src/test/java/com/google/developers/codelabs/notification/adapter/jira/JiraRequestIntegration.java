package com.google.developers.codelabs.notification.adapter.jira;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.OutputMessage;
import org.apache.http.HttpResponse;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

import java.util.HashMap;

import static org.hamcrest.Matchers.*;
import static org.junit.Assert.assertThat;

/**
 * The Class JiraRequestIntegration.
 */
@SuppressWarnings("javadoc")
public class JiraRequestIntegration {

  private JiraRequest request;

  private JiraIssueBuilder builder;
  private NotificationUser user;
  private OutputMessage outputMessage;

  @Before
  public void setup() {
    builder = new JiraIssueBuilder();
    HashMap<String, String> attributes = new HashMap<>();
    attributes.put("PROJECT-ID", "example-project");
    attributes.put("ORGANIZATION-NAME", "example-organization");
    attributes.put("ASSET-TYPE", "network");
    attributes.put("COUNT", "1");
    EventContext context = new EventContext("{\"properties\":{}}", attributes) ;
    user = new NotificationUser(
            System.getenv("NOTIFY_USER_EMAIL"),
            System.getenv("NOTIFY_USER_PHONE"),
            System.getenv("NOTIFY_JIRA_UID"),
            System.getenv("NOTIFY_USER_ROLE"));

    outputMessage = new OutputMessage(NotificationType.ASSETS,ActionType.ANY_CREATED,context);

    request = new JiraRequest(
            System.getenv("JIRA_URL"),
            System.getenv("JIRA_USER_NAME"),
            System.getenv("JIRA_API_TOKEN"));
  }

  @Test
  @Ignore
  public void createIssue() {
    HttpResponse response =
            request.createIssue(builder.asJson(outputMessage, user,
                    System.getenv("JIRA_PROJECT_KEY"),
                    System.getenv("JIRA_ISSUE_TYPE_NAME")));

    assertThat(response.getStatusLine().getStatusCode(),
            allOf(greaterThanOrEqualTo(200), lessThan(300)));
  }

}
