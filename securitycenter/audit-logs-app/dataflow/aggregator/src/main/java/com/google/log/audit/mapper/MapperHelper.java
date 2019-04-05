package com.google.log.audit.mapper;

import java.io.IOException;
import java.net.URL;
import java.util.Properties;

import com.google.common.base.Charsets;
import com.google.common.io.CharSource;
import com.google.common.io.Resources;
import com.google.gson.JsonObject;

public class MapperHelper {
  
  static final String IAM_CATEGORY = "SetIamPolicy";
  
  static Properties displayNames;

  static {
    URL url = Resources.getResource("displayNames.properties");
    CharSource source = Resources.asCharSource(url, Charsets.UTF_8);
    try {
      displayNames = new Properties();
      displayNames.load(source.openStream());
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static String normalizedResourceNameWithExteranlCall(JsonObject rootObject) {
    
    String resourceType = getResourceType(rootObject);

    if (resourceType.equals("project") || resourceType.equals("gce_project")) {
      String projectId = getProjectIdFromLabels(getLabels(rootObject));
      String projectIdentifier = projectId;
      String projectNumber = ProjectMapperHelper.getProjectNumber(projectId);
      if (projectNumber != null) {
        projectIdentifier = projectNumber;
      }
      return "//cloudresourcemanager.googleapis.com/projects/" + projectIdentifier;
    }

    return normalizedResourceName(rootObject);
  }
  
  public static String normalizedResourceName(JsonObject rootObject) {
    String resourceType = getResourceType(rootObject);
    String resourceName = getResourceName(rootObject);
    String serviceName = getServiceName(rootObject);
    JsonObject labels = getLabels(rootObject);

    if (resourceName.startsWith("projects/_/buckets/")) {
      resourceName = resourceName.replace("projects/_/buckets/", "");
    }
    if (labels.has("cluster_name") && labels.has("location")) {
      resourceName = getAssetIdFomLabels(labels, "zones", "location", "cluster", "cluster_name");
    }
    if (resourceType.equals("dns_managed_zone")) {
      resourceName = getAssetIdFomLabels(labels, "managedZones", "zone_name");
    }
    if (resourceType.equals("service_account")) {
      resourceName = getAssetIdFomLabels(labels, "serviceAccounts", "unique_id");
    }
    return "//" + serviceName + "/" + resourceName;
  }

  public static String getResourceType(JsonObject rootObject) {
    return rootObject.get("resource").getAsJsonObject().get("type").getAsString();
  }

  public static String getAssetIdFomLabels(JsonObject labels, String primaryIndexType, String primaryIndex) {
    return getProjectIdFromLabels(labels) + "/" + primaryIndexType + "/" + labels.get(primaryIndex).getAsString();
  }

  private static String getProjectIdFromLabels(JsonObject labels) {
    return labels.get("project_id").getAsString();
  }

  public static String getAssetIdFomLabels(JsonObject labels, String primaryIndexType, String primaryIndex, String secondaryIndexType, String secondaryIndex) {
    return getProjectIdFromLabels(labels) + "/" + primaryIndexType + "/" + labels.get(primaryIndex).getAsString() + "/" + secondaryIndexType
        + "/" + labels.get(secondaryIndex).getAsString();
  }

  public static JsonObject getProtoPayload(JsonObject rootObject) {
    return rootObject.get("protoPayload").getAsJsonObject();
  }
  
  public static String getResourceName(JsonObject rootObject) {
    return getProtoPayload(rootObject).get("resourceName").getAsString();
  }

  public static String getMethodName(JsonObject JsonObject) {
    return getProtoPayload(JsonObject).get("methodName").getAsString();
  }
  
  public static String getServiceName(JsonObject JsonObject) {
    return getProtoPayload(JsonObject).get("serviceName").getAsString();
  }

  public static String getPrincipalEmail(JsonObject JsonObject) {
    return getProtoPayload(JsonObject).get("authenticationInfo").getAsJsonObject().get("principalEmail").getAsString();
  }

  public static JsonObject getLabels(JsonObject rootObject) {
    return rootObject.get("resource").getAsJsonObject().get("labels").getAsJsonObject();
  }

  static String getResourceDisplayName(String resource, String methodName) {
    
    if(MapperHelper.IAM_CATEGORY.equals(methodName)) {
      return MapperHelper.IAM_CATEGORY;
    }
    return displayNames.getProperty(resource, resource);
  }

}
