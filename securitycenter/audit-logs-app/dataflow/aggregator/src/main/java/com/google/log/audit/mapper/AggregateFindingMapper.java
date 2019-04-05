package com.google.log.audit.mapper;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import com.google.common.base.Joiner;
import com.google.common.base.Strings;
import com.google.common.collect.Iterables;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class AggregateFindingMapper {
  
  private static final int MAX_URL_LENGTH = 2000;

  private Iterable<String> originalLogItems;
  private List<JsonObject> logItems;
  private String windowStart;
  private String windowEnd;

  public AggregateFindingMapper(Iterable<String> originalLogItems, String windowStart, String windowEnd ) {
    this.originalLogItems = originalLogItems;
    this.windowStart = windowStart;
    this.windowEnd = windowEnd;
  }
  
  public AggregateFindingMapper parse() {
    this.logItems = new ArrayList<>();
    JsonParser jsonParser = new JsonParser();
    for (String originalLogItem : originalLogItems) {
      this.logItems.add(jsonParser.parse(originalLogItem).getAsJsonObject());
    }
    return this;
  }
  
  private String getAction(JsonObject logItem) {
    List<String> categoryParts = new ArrayList<>();
    categoryParts.add("insertId:"+ logItem.get("insertId").getAsString());
    categoryParts.add("author:" + MapperHelper.getPrincipalEmail(logItem));
    categoryParts.add("resourceType:" + MapperHelper.getResourceType(logItem));
    categoryParts.add("methodName:" + MapperHelper.getMethodName(logItem));
    categoryParts.add("timestamp:" + logItem.get("timestamp").getAsString());
    categoryParts.add("severity:" + logItem.get("severity").getAsString());
    categoryParts.add(Joiner.on(" ").join(getLableText(logItem)));
    List<String> deltaTexts = getBindingDeltasText(logItem); 
    if (!deltaTexts.isEmpty()) {
      categoryParts.add(Joiner.on(" ").join(deltaTexts));
    }
    return Joiner.on(" ").join(categoryParts);
  }

  private List<String> getBindingDeltasText(JsonObject logItem) {
    Map<String,List<String>> actionsMap = new HashMap<>();
    if(logItem.get("protoPayload").getAsJsonObject().get("serviceData") != null) {      
      JsonObject serviceData = logItem.get("protoPayload").getAsJsonObject().get("serviceData").getAsJsonObject();
      if (serviceData != null && serviceData.get("policyDelta") != null) {
        JsonObject policyDelta = serviceData.get("policyDelta").getAsJsonObject();
        if (policyDelta != null && policyDelta.get("bindingDeltas") != null) {
          JsonArray bindingDeltas = policyDelta.get("bindingDeltas").getAsJsonArray();
          if (bindingDeltas != null) {
            for (JsonElement delta : bindingDeltas) {
              JsonObject realDelta = delta.getAsJsonObject();
              String currentKey = realDelta.get("action").getAsString();
              if (!actionsMap.containsKey(currentKey)) {
                actionsMap.put(currentKey, new ArrayList<String>());
              }
              actionsMap.get(currentKey).add(Joiner.on(" ").join(realDelta.get("role").getAsString(),realDelta.get("member").getAsString()));
            }
          }
        }
      }
    }
    List<String> deltasTexts = new ArrayList<>();
    for (String currentKey : actionsMap.keySet()) {
      deltasTexts.add(Joiner.on(" - ").join(currentKey,Joiner.on(", ").join(actionsMap.get(currentKey))));
    }
    return deltasTexts;
  }

  private List<String> getLableText(JsonObject logItem) {
    JsonObject labels = MapperHelper.getLabels(logItem);
    List<String> labelTexts = new ArrayList<String>();
    for (Map.Entry<String,JsonElement> lable : labels.entrySet()) {
      labelTexts.add(lable.getKey() + ":" + lable.getValue().getAsString()); 
    }
    Collections.sort(labelTexts);
    return labelTexts;
  }
  
  public String build() {
      JsonObject finding = new JsonObject();
      finding.addProperty("state", "ACTIVE");
      String normalizedResourceName = MapperHelper.normalizedResourceNameWithExteranlCall(this.logItems.get(0));
      finding.addProperty("category", getAggregateCategory(this.logItems, normalizedResourceName));
      finding.addProperty("resourceName", normalizedResourceName);
      finding.addProperty("eventTime", OffsetDateTime.now().toString());
      finding.addProperty("externalUri", getGlobalUrl(this.logItems));
      finding.add("sourceProperties", addPropertiesFromItems(this.logItems));
      JsonObject sourceProperties = finding.get("sourceProperties").getAsJsonObject();
      sourceProperties.addProperty("full_scc_category", finding.get("category").getAsString());
      return finding.toString();
  }

  private String getGlobalUrl(List<JsonObject> logItems) {
    String projectId = parseProjectId(logItems.get(0));
    if (projectId != null) {
      List<String> ids = new ArrayList<>();
      for (JsonObject logItem : logItems) {
        ids.add("insertId%3D%22" + logItem.get("insertId").getAsString() + "%22");
      }
      String urlLink = "https://console.cloud.google.com/logs/viewer?" + "project=" + projectId
          + "&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter="
          + Joiner.on("%20OR%20").join(ids) + "%0A";
      if (urlLink.length() <= MAX_URL_LENGTH ) {
        return urlLink;
      }
    }
    return "";
  }
  
  private String getAggregateCategory(List<JsonObject> logItems, String normalizedResourceName) {
    Set<String> categoryItems = new TreeSet<>();
    for (JsonObject logItem : logItems) {
      categoryItems.add(MapperHelper.getMethodName(logItem));
    }
    return "Aggregated finding resourceName:" + normalizedResourceName + " "+ Joiner.on(" ").join(categoryItems);
  }

  private JsonElement addPropertiesFromItems(List<JsonObject> logItems) {
    JsonObject properties =  new JsonObject();
    properties.addProperty("aggregate_window_start", this.windowStart);
    properties.addProperty("aggregate_window_end", this.windowEnd);
    properties.addProperty("total_logs_aggregated", Long.toString(Iterables.size(this.originalLogItems)));
    JsonObject firstLog = logItems.get(0);
    properties.addProperty("resource_type", MapperHelper.getResourceType(firstLog));
    properties.addProperty("protoPayload_resourceName", MapperHelper.getResourceName(firstLog));
    addAggregate(logItems, properties, "");
    return properties;
  }

  private void addAggregate(List<JsonObject> logItems, JsonObject properties, String string) {
    JsonArray aggregateCat = new JsonArray(); 
    int currentLine = 1;
    for (JsonObject logItem : logItems) {
      String currentCategory = getAction(logItem);
      properties.addProperty(getActionItemPropertyName(currentLine), currentCategory);
      properties.addProperty(getItemUrlPropertyName(currentLine), buildSelfLink(logItem));
      aggregateCat.add(currentCategory);
      currentLine = currentLine + 1;
    }
    properties.addProperty("aggregate_value", aggregateCat.toString());
  }

  public String getItemUrlPropertyName(int currentLine) {
    return "action_url_" + Strings.padStart(Integer.toString(currentLine), 3, '0');
  }

  public String getActionItemPropertyName(int currentLine) {
    return "action_" + Strings.padStart(Integer.toString(currentLine), 3, '0');
  }
  
  private String buildSelfLink(JsonObject logItem) {
    String projectId = parseProjectId(logItem);
    if (projectId != null) {
      return "https://console.cloud.google.com/logs/viewer?"
          + "project=" + projectId
          + "&minLogLevel=0&expandAll=true&interval=NO_LIMIT&expandAll=true&advancedFilter=insertId%3D%22"
          + logItem.get("insertId").getAsString() + "%22%0A";
    }
    return "";
  }

  private String parseProjectId(JsonObject logItem) {
    JsonObject labels = MapperHelper.getLabels(logItem);
    if( labels != null && labels.get("project_id") != null) {
      return labels.get("project_id").getAsString();
    }
    return null;
  }
}
