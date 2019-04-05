package com.google.developers.codelabs.notification.service;

import com.google.developers.codelabs.notification.core.model.ActionType;
import com.google.developers.codelabs.notification.core.model.NotificationType;
import com.google.developers.codelabs.notification.message.FieldId;
import com.google.developers.codelabs.notification.message.OutputType;
import org.junit.Test;

import java.util.HashMap;

import static org.junit.Assert.assertEquals;

/**
 * The Class MessageHelperTest.
 */
@SuppressWarnings("javadoc")
public class OutputMessageTest {

  private final String LINE_BRAKE = System.getProperty("line.separator");

  @Test
  public void parseFindingsMessageWithoutMarksOnBodyLongFormat() {
    // GIVEN
    final String lastExecutionResult = "10";
    final String lastExecutionDate = "2018-08-13T16:47:42.714228";
    final String organizationId = "0";
    final String category = "3-category-3";
    final String sourceId = "organizations/" + organizationId + "/sources/12121100766606648606";
    final String assetName =
        "//compute.googleapis.com/projects/binauth-demo/global/firewalls/gke-demo-cluster-5dd7583a";
    final String findingId = sourceId + "/findings/2KTOK5Z1tN4MNC8AGVg7pghi02";
    final String eventTime = "2018-11-01T17:03:58Z";
    final String securityMarksName = sourceId
        + "/findings/2KTOK5Z1tN4MNC8AGVg7pghi02/securityMarks";
    final String queryName = "Serch for findings";

    String findingIncomingMessagePayload =
        getFindingsMessage(lastExecutionResult, lastExecutionDate, category, sourceId, assetName,
            findingId, eventTime, securityMarksName, queryName);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.FINDINGS,
            ActionType.OPENED_EVENT_TEXT,
            ActionType.ALL, findingIncomingMessagePayload,
            null, assetName);

    String expectedNotifierMessageBody =
        getFindingsExpectedResult(lastExecutionResult, lastExecutionDate, organizationId, category,
            sourceId, assetName, findingId, eventTime, queryName);

    // WHEN
    final String notifierMessageBody = assetOutputMessage.buildBody(OutputType.LONG);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseAssetMessageBodyWithMarksOnLongFormatWithExtraInfoAndCFResult() {
    // GIVEN
    final String organizationId = "0";
    final String projectNumber = "111111";
    final String projectName = "asset-dev-project";
    final String projectId = "asset-dev-project";
    final String[] owners = {"user:user1@company.net", "user:user2@company.net"};
    final String resourcePropertiesCreateTime = "2018-02-19t17:02:09.842z";
    final String queryName = "two step query for project join with attributes";
    final String lastExecutionResult = "2";
    final String lastExecutionDate = "2018-11-21 17:44:52.968840";
    final String resourceProject =
        "//cloudresourcemanager.googleapis.com/projects/" + projectNumber;
    final String resourceParent = "//cloudresourcemanager.googleapis.com/organizations/"
        + organizationId;
    final String resourceType = "google.cloud.resourcemanager.Project";
    final String resourceName = "//cloudresourcemanager.googleapis.com/projects/" + projectNumber;

    final String[] securityMarks = {"environment", "development",
                                    "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12", "true"};

    String assetIncomingMessagePayload = getAssetMessage(organizationId, projectNumber, projectName,
        projectId, owners, resourcePropertiesCreateTime, queryName, lastExecutionResult,
        lastExecutionDate, resourceProject, resourceParent, resourceType, resourceName, securityMarks);

    String expectedNotifierMessageBody = getAssetExpectedResult(organizationId, projectNumber, projectName,
        projectId, owners, resourcePropertiesCreateTime, queryName, lastExecutionResult,
        lastExecutionDate, resourceProject, resourceParent, resourceName, resourceType, securityMarks);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.ASSETS,
            "UNUSED",
            ActionType.ALL, assetIncomingMessagePayload,
            "mark." + securityMarks[0] + ":" + securityMarks[1],
            resourceName);
    assetOutputMessage.setExtraInfo("Confidential Information.");
    assetOutputMessage.setCloudFunctionResponse("Cloud Function Running.");

    // WHEN
    final String notifierMessageBody = assetOutputMessage.buildBody(OutputType.LONG);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseMessageBodyFindingsWhenStateActiveOnShortFormat() {
    // GIVEN
    final String lastExecutionResult = "10";
    final String organizationId = "0";
    final String sourceId = "organizations/" + organizationId + "/sources/12121100766606648606";
    final String findingId = sourceId + "/findings/2KTOK5Z1tN4MNC8AGVg7pghi02";
    final String queryName = "Serch for findings";
    final String state = "ACTIVE";

    String expectedNotifierMessageBody = "Query \"" + queryName + "\" returned " + lastExecutionResult +
        " finding(s) for example.org - finding id : " + findingId + " " + state + LINE_BRAKE;

    String incomingMessagePayload = getFindingsMessage(lastExecutionResult, null, null, null,
        null, findingId, null, null, queryName);

    OutputMessage findingOutputMessage = buildWithReturnInMessage(NotificationType.FINDINGS,
        state, ActionType.ALL, incomingMessagePayload, null, findingId);

    // WHEN
    final String notifierMessageBody = findingOutputMessage.buildBody(OutputType.SHORT);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseMessageBodyFindingsWhenStateUnspecifiedOnShortFormat() {
    // GIVEN
    final String lastExecutionResult = "10";
    final String organizationId = "0";
    final String sourceId = "organizations/" + organizationId + "/sources/12121100766606648606";
    final String findingId = sourceId + "/findings/2KTOK5Z1tN4MNC8AGVg7pghi02";
    final String queryName = "Serch for findings";
    final String state = "STATE_UNSPECIFIED";

    String expectedNotifierMessageBody = "Query \"" + queryName + "\" returned " + lastExecutionResult +
        " finding(s) for example.org - finding id : " + findingId + " " + LINE_BRAKE;

    String incomingMessagePayload = getFindingsMessage(lastExecutionResult, null, null, null,
        null, findingId, null, null, queryName);

    OutputMessage findingOutputMessage = buildWithReturnInMessage(NotificationType.FINDINGS,
        state, ActionType.ALL, incomingMessagePayload, null, findingId);

    // WHEN
    final String notifierMessageBody = findingOutputMessage.buildBody(OutputType.SHORT);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseMessageBodyAssetsWhenStateUnusedOnShortFormat() {
    final String organizationId = "0";
    final String projectNumber = "111111";
    final String projectName = "asset-dev-project";
    final String projectId = "asset-dev-project";
    final String queryName = "two step query for project join with attributes";
    final String lastExecutionResult = "2";
    final String resourceName = "//cloudresourcemanager.googleapis.com/projects/" + projectNumber;
    final String state = "UNUSED";

    final String expectedNotifierMessageBody = "Query \"" + queryName + "\" returned " + lastExecutionResult
        + " asset(s) for example.org - asset id : " + resourceName + " " + LINE_BRAKE;

    String incomingMessagePayload = getAssetMessage(organizationId, projectNumber, projectName, projectId,
        new String[2], "", queryName, lastExecutionResult,
        "", "", "", "", resourceName, null);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.ASSETS,
            state,
            ActionType.ALL, incomingMessagePayload, null, resourceName);

    // WHEN
    final String notifierMessageBody = assetOutputMessage.buildBody(OutputType.SHORT);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseMessageBodyAssetsWhenStateAddedOnShortFormat() {
    final String organizationId = "0";
    final String projectNumber = "111111";
    final String projectName = "asset-dev-project";
    final String projectId = "asset-dev-project";
    final String queryName = "one step query";
    final String lastExecutionResult = "5";
    final String resourceName = "//compute.googleapis.com/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-kqq4";
    final String state = "ADDED";

    final String expectedNotifierMessageBody = "Query \"" + queryName + "\" returned " + lastExecutionResult
        + " asset(s) for example.org - asset id : " + resourceName + " " + state + LINE_BRAKE;

    String incomingMessagePayload = getAssetMessage(organizationId, projectNumber, projectName, projectId,
        new String[2], "", queryName, lastExecutionResult,
        "", "", "", "", resourceName, null);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.ASSETS,
            state,
            ActionType.ALL, incomingMessagePayload, null, resourceName);

    // WHEN
    final String notifierMessageBody = assetOutputMessage.buildBody(OutputType.SHORT);

    // THEN
    assertEquals(expectedNotifierMessageBody, notifierMessageBody);
  }

  @Test
  public void parseSubjectAssetsEventTypeUnused() {
    final String organizationId = "0";
    final String projectNumber = "111111";
    final String projectName = "asset-dev-project";
    final String projectId = "asset-dev-project";
    final String queryName = "two step query for project join with attributes";
    final String lastExecutionResult = "2";
    final String resourceName = "//cloudresourcemanager.googleapis.com/projects/" + projectNumber;
    final String state = "UNUSED";

    String incomingMessagePayload = getAssetMessage(organizationId, projectNumber, projectName, projectId,
        new String[2], "", queryName, lastExecutionResult,
        "", "", "", "", resourceName, null);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.ASSETS,
            state, ActionType.ALL, incomingMessagePayload, null, resourceName);

    assertEquals(
        "Query \"" + queryName + "\" returned " + lastExecutionResult + " asset(s) for example.org - asset id : " + resourceName + "." + LINE_BRAKE,
        assetOutputMessage.buildSubject());
  }
  
  @Test
  public void parseSubjectFindingsEventTypeActive() {
    final String lastExecutionResult = "10";
    final String organizationId = "0";
    final String sourceId = "organizations/" + organizationId + "/sources/12121100766606648606";
    final String findingId = sourceId + "/findings/2KTOK5Z1tN4MNC8AGVg7pghi02";
    final String queryName = "Serch for findings";
    String state = "ACTIVE";

    String incomingMessagePayload = getFindingsMessage(lastExecutionResult, null, null, null, null,
        findingId, null, null, queryName);

    OutputMessage assetOutputMessage =
        buildWithReturnInMessage(
            NotificationType.FINDINGS,
            state,
            ActionType.ANY_OPENED, incomingMessagePayload, null, findingId);

    assertEquals(
        "Query \"" + queryName + "\" returned " + lastExecutionResult + " finding(s) for example.org - finding id : " + findingId + " " + state + "." + LINE_BRAKE,
        assetOutputMessage.buildSubject());
  }

  private OutputMessage buildWithReturnInMessage(
      NotificationType notificationType,
      String eventType,
      ActionType actionType, String message, String marks, String id) {

    final String organizationName = "example.org";
    final String organizationId = "0";
    final String updateTime = "2018-10-17T22:03:23.376Z";

    EventContext context = new EventContext(message,
        buildMockAttributes(notificationType, eventType,
            marks, organizationId, organizationName, id, updateTime));

    return new OutputMessage(notificationType, actionType, context);
  }

  public HashMap<String, String> buildMockAttributes(NotificationType notificationType,
      String eventType, String marks, String organizationId, String organizationName,
      String id, String updateTime) {
    HashMap<String, String> attributes = new HashMap<>();
    attributes.put(EventContext.NOTIFICATION_TYPE_KEY, notificationType.name());
    attributes.put(EventContext.EVENT_TYPE_KEY, eventType);
    attributes.put(FieldId.PROJECT_ID.getFieldName(), "house-196005");
    if (NotificationType.ASSETS == notificationType) {
      attributes.put(FieldId.ASSET_TYPE.getFieldName(), "PROJECT");
      attributes.put(EventContext.ASSET_ID, id);
    } else {
      attributes.put(EventContext.FINDING_ID, id);
    }
    attributes.put(EventContext.ORGANIZATION_ID, organizationId);
    attributes.put(EventContext.ORGANIZATION_NAME, organizationName);
    attributes.put(EventContext.MARKS, marks);
    attributes.put(EventContext.UPDATE_TIME, updateTime);
    
    return attributes;
  }

  private String getAssetExpectedResult(String organizationId, String projectNumber,
      String projectName, String projectId, String[] owners, String resourcePropertiesCreateTime,
      String queryName, String lastExecutionResult, String lastExecutionDate,
      String resourceProject, String resourceParent, String resourceName,
      String resourceType, String[] securityMarks) {
    return "Organization: example.org - "+ organizationId + LINE_BRAKE
        + LINE_BRAKE
        + "Query:  " + queryName + " " + LINE_BRAKE
        + LINE_BRAKE
        + "Last execution:" + LINE_BRAKE
        + " Number of results: " + lastExecutionResult + LINE_BRAKE
        + " Execution date: " + lastExecutionDate + LINE_BRAKE
        + LINE_BRAKE
        + "Search Mark: mark." + securityMarks[0] + ":" + securityMarks[1] + LINE_BRAKE
        + "Link: https://console.cloud.google.com/security/command-center/dashboard?organizationId=" + organizationId + LINE_BRAKE
        + LINE_BRAKE
        + "Security Marks:" + LINE_BRAKE
        + LINE_BRAKE
        + securityMarks[0] + " - " + securityMarks[1] + LINE_BRAKE
        + securityMarks[2] + " - " + securityMarks[3] + LINE_BRAKE
        + LINE_BRAKE
        + "Security Center Properties:" + LINE_BRAKE
        + LINE_BRAKE
        + "resourceOwners - ["+ owners[0] + ", " + owners[1] + "]" + LINE_BRAKE
        + "resourceProject - " + resourceProject + LINE_BRAKE
        + "resourceParent - "+ resourceParent + LINE_BRAKE
        + "resourceName - " + resourceName + LINE_BRAKE
        + "updateTime - 2018-10-17T22:03:23.376Z" + LINE_BRAKE
        + "state - UNUSED" + LINE_BRAKE
        + "resourceType - " + resourceType +  LINE_BRAKE
        + LINE_BRAKE
        + "Resource Properties:" + LINE_BRAKE
        + LINE_BRAKE
        + "lifecycleState - active" + LINE_BRAKE
        + "parent - {\"id\":\"" + organizationId + "\",\"type\":\"organization\"}" + LINE_BRAKE
        + "createTime - " + resourcePropertiesCreateTime + LINE_BRAKE
        + "projectNumber - " + projectNumber + LINE_BRAKE
        + "name - "+ projectName + LINE_BRAKE
        + "projectId - " + projectId + LINE_BRAKE
        + LINE_BRAKE
        + "Cloud Function Running." + LINE_BRAKE
        + "Confidential Information.";
  }

  private String getAssetMessage(String organizationId, String projectNumber, String projectName,
      String projectId, String[] owners, String resourcePropertiesCreateTime, String queryName,
      String lastExecutionResult, String lastExecutionDate, String resourceProject,
      String resourceParent, String resourceType, String resourceName, String[] securityMarks) {
    return "{\"createTime\": \"2018-10-17T22:03:23.376Z\", "
        + "\"name\": \"organizations/" + organizationId + "/assets/6935692701314546019\", "
        + "\"query\": {\"last_execution_date\": \"" + lastExecutionDate + "\", "
        + "\"last_execution_result\": " + lastExecutionResult + ", "
        + "\"last_execution_status\": \"SUCCESS\", \"name\": \"" + queryName + "\"}, "
        + "\"resourceProperties\": {\"createTime\": \"" + resourcePropertiesCreateTime + "\", "
        + "\"lifecycleState\": \"active\", \"name\": \"" + projectName + "\", "
        + "\"parent\": \"{\\\"id\\\":\\\"" + organizationId
        + "\\\",\\\"type\\\":\\\"organization\\\"}\", "
        + "\"projectId\": \"" + projectId + "\", "
        + "\"projectNumber\": " + projectNumber + "}, "
        + "\"securityCenterProperties\": {"
        + "\"resourceName\": \"" + resourceName + "\", "
        + "\"resourceOwners\": [\"" + owners[0] + "\", \"" + owners[1] + "\"], "
        + "\"resourceParent\": \"" + resourceParent + "\", "
        + "\"resourceProject\": \"" + resourceProject + "\", "
        + "\"resourceType\": \"" + resourceType + "\"}, "
        + "\"securityMarks\": {"
        + "\"name\": \"organizations/" + organizationId
        + "/assets/6935692701314546019/securityMarks\","
        + (securityMarks != null
          ? "\"marks\": {\""+ securityMarks[0] +"\": \""+ securityMarks[1] +"\","
        +   "\""+ securityMarks[2] +"\": \""+ securityMarks[3] +"\"}, "
           : "")
        + "\"name\": \"organizations/" + organizationId
        + "/assets/6935692701314546019/securityMarks\"}, "
        + "\"state\": \"UNUSED\", "
        + "\"updateTime\": \"2018-10-17T22:03:23.376Z\"}";
  }

  private String getFindingsExpectedResult(String lastExecutionResult, String lastExecutionDate,
      String organizationId, String category, String sourceId, String assetName, String findingId,
      String eventTime, String queryName) {
    return "Organization: example.org - " + organizationId + LINE_BRAKE
        + LINE_BRAKE
        + "Query:  " + queryName + " " + LINE_BRAKE
        + LINE_BRAKE
        + "Last execution:" + LINE_BRAKE
        + " Number of results: " + lastExecutionResult + LINE_BRAKE
        + " Execution date: " + lastExecutionDate + LINE_BRAKE
        + LINE_BRAKE
        + LINE_BRAKE
        + "Link: https://console.cloud.google.com/security/command-center/dashboard?organizationId=" + organizationId + LINE_BRAKE
        + LINE_BRAKE
        + "Security Marks:" + LINE_BRAKE
        + LINE_BRAKE
        + LINE_BRAKE
        + "Security Center Properties:" + LINE_BRAKE
        + LINE_BRAKE
        + "parent - " + sourceId + LINE_BRAKE
        + "eventTime - " + eventTime + LINE_BRAKE
        + "name - " + findingId + LINE_BRAKE
        + "resourceName - " + assetName + LINE_BRAKE
        + "category - " + category + LINE_BRAKE
        + LINE_BRAKE
        + "Source Properties:" + LINE_BRAKE
        + LINE_BRAKE
        + "property-1 - property-1-value-8gq4yAjcehGpS0HHFp1DJzs92bdB" + LINE_BRAKE
        + "property-0 - property-0-value-Ruekw" + LINE_BRAKE
        + "property-2 - property-2-value-coETM0i8goJQ1oUdTk" + LINE_BRAKE;
  }

  private String getFindingsMessage(String lastExecutionResult, String lastExecutionDate,
      String category, String sourceId, String assetName, String findingId, String eventTime,
      String securityMarksName, String queryName) {
    return "{\n"
        + "  \"category\": \"" + category + "\",\n"
        + "  \"createTime\": \"2018-11-01T17:03:58Z\",\n"
        + "  \"eventTime\": \"" + eventTime + "\",\n"
        + "  \"externalUri\": \"am2kj4DBh2uvWvagW0bNDI1f27XRegSNqURFrTb36aGP928mAJ\",\n"
        + "  \"name\": \"" + findingId + "\",\n"
        + "  \"parent\": \"" + sourceId + "\",\n"
        + "  \"query\": {\n"
        + "    \"last_execution_date\": \"" + lastExecutionDate + "\",\n"
        + "    \"last_execution_result\": " + lastExecutionResult + ",\n"
        + "    \"last_execution_status\": \"SUCCESS\",\n"
        + "    \"name\": \"" + queryName + "\"\n"
        + "  },\n"
        + "  \"resourceName\": \"" + assetName + "\",\n"
        + "  \"securityMarks\": {\n"
        + "    \"name\": \"" + securityMarksName + "\"\n"
        + "  },\n"
        + "  \"sourceProperties\": {\n"
        + "    \"property-0\": \"property-0-value-Ruekw\",\n"
        + "    \"property-1\": \"property-1-value-8gq4yAjcehGpS0HHFp1DJzs92bdB\",\n"
        + "    \"property-2\": \"property-2-value-coETM0i8goJQ1oUdTk\"\n"
        + "  },\n"
        + "  \"state\": \"ACTIVE\"\n"
        + "}";
  }

}
