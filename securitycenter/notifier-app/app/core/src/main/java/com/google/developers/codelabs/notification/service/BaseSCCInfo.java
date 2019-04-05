package com.google.developers.codelabs.notification.service;

public class BaseSCCInfo {

  private String key;
  private String originalKey;
  private String value;

  public BaseSCCInfo(String key, String originalKey, String value) {
    super();
    this.key = key;
    this.originalKey = originalKey;
    this.value = value;
  }

  public String getKey() {
    return key;
  }

  public String getValue() {
    return value;
  }

  public String getOriginalKey() {
    return originalKey;
  }
  
}
