package com.google.developers.codelabs.notification.service;

import com.google.developers.codelabs.notification.core.model.NotificationType;

import java.util.ArrayList;
import java.util.List;

public class SCCResourceInfo {

  private String organizationName;
  private String organizationId;
  private String type;
  private String id;
  private List<BaseSCCInfo> attributes;
  private List<BaseSCCInfo> properties;
  private List<BaseSCCInfo> marks;
  private List<BaseSCCInfo> query;
  
  public SCCResourceInfo(String id, String type, String organizationId, String organizationName) {
    super();
    this.organizationName = organizationName;
    this.organizationId = organizationId;
    this.type = type;
    this.id = id;
    this.attributes = new ArrayList<BaseSCCInfo>();
    this.properties = new ArrayList<BaseSCCInfo>();
    this.marks = new ArrayList<BaseSCCInfo>();
    this.query = new ArrayList<BaseSCCInfo>();
  }
  
  
  private String getValue(List<BaseSCCInfo> colection, String key) {
    for (BaseSCCInfo baseSCCInfo : colection) {
      if (baseSCCInfo.getKey().equals(key)) {
        return baseSCCInfo.getValue();
      }
    }
    return "";
  }
  public String getOrganizationName() {
    return organizationName;
  }
  
  public String getOrganizationId() {
    return organizationId;
  }
  
  public String getType() {
    return type;
  }
  
  public String getId() {
    return id;
  }
  
  public List<BaseSCCInfo> getAttributes() {
    return attributes;
  }
  
  public List<BaseSCCInfo> getProperties() {
    return properties;
  }
  
  public List<BaseSCCInfo> getMarks() {
    return marks;
  }
  
  public List<BaseSCCInfo> getQuery() {
    return query;
  }
  
  public String getQueryResult() {
    return getValue(this.query,"LAST_EXECUTION_RESULT");
  }
  
  public String getQueryDate() {
    return getValue(this.query,"LAST_EXECUTION_DATE");
  }
  
  public String getQueryName() {
    return getValue(this.query,"NAME");
  }
  
  public String getQueryDescription() {
    return getValue(this.query,"DESCRIPTION");
  }

  public boolean isAsset() {
    return NotificationType.ASSETS.name().equals(getType());
  }
  public boolean isFinding() {
    return NotificationType.FINDINGS.name().equals(getType());
  }
  
}
