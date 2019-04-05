package com.google.developers.codelabs.notification.service;

import com.google.api.client.json.JsonParser;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.developers.codelabs.notification.core.model.NotificationType;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

/**
 * The Class EventContext.
 */
public class EventContext {

  /**
   * The Constant NOTIFICATION_TYPE_KEY to represent values from {@code {@link com.google.developers.codelabs.notification.core.model.NotificationType}}
   */
  public static final String NOTIFICATION_TYPE_KEY = "NOTIFICATION-TYPE";

  /**
   * The Constant EVENT_TYPE_KEY to represent values from {@code {@link com.google.developers.codelabs.notification.core.model.ActionType}}
   */
  public static final String EVENT_TYPE_KEY = "EVENT-TYPE";

  /**
   * The Constant ASSET-HASH that keeps the hash received about the Asset entity
   **/
  public static final String ASSET_HASH = "ASSET-HASH";

  public static final String ORGANIZATION_ID = "ORGANIZATION-ID";
  public static final String ORGANIZATION_NAME = "ORGANIZATION-DISPLAY-NAME";
  public static final String FINDING_HASH = "FINDING-HASH";

  public static final String SOURCE_ID = "SOURCE-ID";
  public static final String FINDING_ID = "FINDING-ID";
  public static final String ASSET_ID = "ASSET-ID";
  public static final String CATEGORY = "CATEGORY";
  public static final String UPDATE_TIME = "LAST-UPDATED-TIME";
  public static final String MARKS = "MARKS";

  public static final String ADDITIONAL_DEST_EMAIL = "ADDITIONAL_DEST_EMAIL";
  public static final String EVENT_TYPE_ADDED = "ADDED";
  public static final String EVENT_TYPE_REMOVED = "REMOVED";
  public static final String EVENT_TYPE_ACTIVE = "ACTIVE";
  public static final String EVENT_TYPE_INACTIVE = "INACTIVE";

  private SCCQueryInfo query;
  private SCCResourceInfo resource;

  private String message;
  private Map<String, String> attributes;
  private String extraInfo;
  private String cloudFunctionResponse;
  private HashMap properties;

  private String[]
      FINDINGS_ROOT_PROPERTIES = {"parent", "eventTime", "resourceName", "name", "category"};

  /**
   * Instantiates a new event context.
   *
   * @param message    the message
   * @param attributes the attributes
   */
  public EventContext(String message, Map<String, String> attributes) {

    this.message = message;

    Map<String, String> internalMap = new HashMap<>();
    for (Entry<String, String> entry : attributes.entrySet()) {
      internalMap.put(entry.getKey().trim().toUpperCase(), entry.getValue());
    }

    this.attributes = internalMap;
    this.resource = new SCCResourceInfo(getId(), getNotificationType(), getOrganizationId(), getOrganizationName());

    if (NotificationType.ASSETS.name().equals(getNotificationType())) {
      this.properties = getJsonProperties("resourceProperties");
      final HashMap securityCenterProperties = getJsonProperties("securityCenterProperties");
      if (getEventType() != null) {
        securityCenterProperties.put("state", getEventType());
      }
      if (getUpdateTime() != null) {
        securityCenterProperties.put("updateTime", getUpdateTime());
      }
      parseSection(this.resource.getAttributes(), securityCenterProperties);
    } else if (NotificationType.FINDINGS.name().equals(getNotificationType())) {
      this.properties = getJsonProperties("sourceProperties");
      final HashMap jsonRootProperties = getJsonProperties(null);
      Map<String, String> jsonProperties = filterFindingProperties(jsonRootProperties);
      parseSection(this.resource.getAttributes(), jsonProperties);
    }
    parseSection(this.resource.getProperties(), this.properties);
    parseSection(this.resource.getMarks(), filterMarks(getJsonProperties("securityMarks")));
    parseSection(this.resource.getQuery(), getJsonProperties("query"));
  }

  private Map<String, String> filterMarks(Map<String, Map<String, String>> securityMarks) {
    return securityMarks.get("marks");
  }

  private Map<String, String> filterFindingProperties(HashMap<String, String> jsonRootProperties) {
    Map<String, String> findingsProperties = new HashMap<>();
    for (String key : jsonRootProperties.keySet()) {
      if (Arrays.asList(FINDINGS_ROOT_PROPERTIES).contains(key)) {
        findingsProperties.put(key, jsonRootProperties.get(key));
      }
    }
    return findingsProperties;
  }

  public void parseSection(List<BaseSCCInfo> targetSection, Map properties2) {
    if (properties2 != null) {
      for (Object key : properties2.keySet()) {
        targetSection.add(new BaseSCCInfo(
            key.toString().toUpperCase(), 
            key.toString(),
            properties2.get(key).toString())); 
      }
    }
  }

  public SCCQueryInfo getQuery() {
    return query;
  }

  public SCCResourceInfo getResource() {
    return resource;
  }

  public String getId() {
    return NotificationType.ASSETS.name().equals(getNotificationType()) ? getAssetId() : getFindingId();
  }

  /**
   * Gets the message.
   *
   * @return the message
   */
  public String getMessage() {
    return message;
  }

  /**
   * Gets the attributes.
   *
   * @return the attributes
   */
  public Map<String, String> getAttributes() {
    return attributes;
  }

  /**
   * Gets the extra info.
   *
   * @return the extra info
   */
  public String getExtraInfo() {
    return extraInfo;
  }

  /**
   * Sets the extra info.
   *
   * @param extraInfo the new extra info
   */
  public void setExtraInfo(String extraInfo) {
    this.extraInfo = extraInfo;
  }

  /**
   * Gets the notification type.
   *
   * @return the notification type
   */
  public String getNotificationType() {
    return getAttribute(NOTIFICATION_TYPE_KEY);
  }

  
  public String getOrganizationId() {
    return getAttribute(ORGANIZATION_ID);
  }
  
  
  public String getOrganizationName() {
    return getAttribute(ORGANIZATION_NAME);
  }
  
  
  /**
   * Gets the event type.
   *
   * @return the event type
   */
  public String getEventType() {
    return getAttribute(EVENT_TYPE_KEY);
  }

  public String getAssetHash() {
    return getAttribute(ASSET_HASH);
  }

  public String getFindingHash() {
    return getAttribute(FINDING_HASH);
  }

  public String getSearchMark() {
    return getAttribute(MARKS);
  }
  
  
  /**
   * Gets an attribute.
   *
   * @param attribute the attribute key
   * @return the attribute value or null if not found
   */
  public String getAttribute(String attribute) {
    if (this.attributes != null) {
      return this.attributes.get(attribute);
    }
    return null;
  }

  public String getSourceId() {
    return getAttribute(SOURCE_ID);
  }

  public String getAssetId() {
    return getAttribute(ASSET_ID);
  }

  public String getFindingId() {
    return getAttribute(FINDING_ID);
  }

  public String getCategory() {
    return getAttribute(CATEGORY);
  }

  public String getUpdateTime() {
    return getAttribute(UPDATE_TIME);
  }

  public HashMap getProperties() {
    return this.properties;
  }

  public String getMarks() {
    return getAttribute(MARKS);
  }

  public String getAddictionalDestEmail() {
    return getAttribute(ADDITIONAL_DEST_EMAIL);
  }

  private HashMap getJsonProperties(String section) {
    try {
      JsonParser parser = JacksonFactory.getDefaultInstance().createJsonParser(this.getMessage());
      if (section != null) {
        parser.skipToKey(section);
      }
      return parser.parseAndClose(HashMap.class);
    }catch (IOException e){
      e.printStackTrace();
    }
    return null;
  }

  public String getCloudFunctionResponse() {
    return cloudFunctionResponse;
  }

  public void setCloudFunctionResponse(String cloudFunctionResponse) {
    this.cloudFunctionResponse = cloudFunctionResponse;
  }

  public boolean isAddedOrRemoved() {
    return NotificationType.ASSETS.name().equals(getNotificationType()) &&
        (EVENT_TYPE_ADDED.equals(getEventType()) || EVENT_TYPE_REMOVED.equals(getEventType()));
  }

  public boolean isActiveOrInactive() {
    return NotificationType.FINDINGS.name().equals(getNotificationType()) &&
        (EVENT_TYPE_ACTIVE.equals(getEventType()) || EVENT_TYPE_INACTIVE.equals(getEventType()));
  }
}
