package com.google.developers.codelabs.notification.service;

public class SCCQueryInfo {
  
  private String name;
  private String description;
  private String excutionDate;
  private String executionResults;
  private String uniqueMark;
  
  
  
  public SCCQueryInfo(String name, String description, String uniqueMark, String excutionDate,
      String executionResults) {
    super();
    this.name = name;
    this.description = description;
    this.uniqueMark = uniqueMark;
    this.excutionDate = excutionDate;
    this.executionResults = executionResults;
  }
  public String getName() {
    return name;
  }
  
  public String getDescription() {
    return description;
  }
  
  public String getExcutionDate() {
    return excutionDate;
  }
  
  public String getExecutionResults() {
    return executionResults;
  }
  
  public String getUniqueMark() {
    return uniqueMark;
  }
  

}
