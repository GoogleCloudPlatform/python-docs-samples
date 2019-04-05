package com.google.developers.codelabs.notification.adapter.jira;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.core.model.NotificationUser;
import com.google.developers.codelabs.notification.service.EventContext;
import com.google.developers.codelabs.notification.service.OutputMessage;
import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;

import static org.junit.Assert.assertEquals;

@SuppressWarnings("javadoc")
public class JiraIssueBuilderTest {
  private final String state = "ADDED";
  private JiraIssueBuilder builder;
  private EventContext context;
  private NotificationUser user;
  private OutputMessage outputMessage;
  
  private final String LINE_BRAKE = System.getProperty("line.separator").toString().length() == 2 ? "\\r\\n":"\\n";

  @Before
  public void setup() {
    builder = new JiraIssueBuilder();
    HashMap<String, String> attributes = new HashMap<>();
    attributes.put(EventContext.NOTIFICATION_TYPE_KEY, NotificationType.ASSETS.name());
    attributes.put(EventContext.EVENT_TYPE_KEY, state);
    attributes.put("PROJECT-ID", "example-project");
    attributes.put(EventContext.ORGANIZATION_ID, "0");
    attributes.put(EventContext.ORGANIZATION_NAME, "example.org");
    attributes.put("ASSET-TYPE", "network");
    attributes.put("COUNT", "1");
    attributes.put(EventContext.ASSET_ID, "other-view-999");
    attributes.put(EventContext.FINDING_ID, "finding_id");
    String message = "{\"resourceProperties\":{\"risk-level\": \"high\"},"
        + "\"query\": {"
        + "\"description\": \"Searching for target projects\", "
        + "\"last_execution_result\": \"10\", "
        + "\"name\": \"Serch for projects\"}"
        + "}";
    context = new EventContext(message, attributes) ;
    user = new NotificationUser("", "", "jira_user", "");
    outputMessage = new OutputMessage(NotificationType.ASSETS,ActionType.ANY_CREATED,context);
  }

  @Test
  public void testAsJson() {
    String expected =
            "{\"fields\":{"
            + "\"assignee\":{\"name\":\"jira_user\"},"
            + "\"description\":"
            + "\"Organization: example.org - 0"
            + LINE_BRAKE + LINE_BRAKE
            + "Query:  Serch for projects - Searching for target projects"
            + LINE_BRAKE + LINE_BRAKE
            + "Last execution:"
            + LINE_BRAKE
            + " Number of results: 10"
            + LINE_BRAKE
            + " Execution date: "
            + LINE_BRAKE + LINE_BRAKE
            + LINE_BRAKE
            + "Link: https://console.cloud.google.com/security/command-center/dashboard?organizationId=0"
            + LINE_BRAKE + LINE_BRAKE
            + "Security Marks:"
            + LINE_BRAKE + LINE_BRAKE + LINE_BRAKE
            + "Security Center Properties:"
            + LINE_BRAKE + LINE_BRAKE
            + "state - " + state + LINE_BRAKE + LINE_BRAKE
            + "Resource Properties:"
            + LINE_BRAKE + LINE_BRAKE
            + "risk-level - high"
            + LINE_BRAKE
            + "\","
            + "\"issuetype\":{\"name\":\"BUG\"},"
            + "\"project\":{\"key\":\"TEPJ\"},"
            + "\"summary\":\"Query \\\"Serch for projects\\\" returned 10 asset(s) for example.org - asset id : other-view-999 " + state + "." + LINE_BRAKE + "\"}}";
    assertEquals(expected, builder.asJson(outputMessage, user, "TEPJ", "BUG"));
  }

}
