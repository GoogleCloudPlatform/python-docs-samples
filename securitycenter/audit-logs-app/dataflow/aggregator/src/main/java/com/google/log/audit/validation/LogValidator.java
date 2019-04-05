package com.google.log.audit.validation;

public class LogValidator {

  public static ValidationResponse isValid(String logItem) {

    if (!logItem.contains("\"principalEmail\"")) {
      return new ValidationResponse(false, "Missing principalEmail");
    } else if (!logItem.contains("\"resourceName\"")) {
      return new ValidationResponse(false, "Missing resourceName");
    }
    return new ValidationResponse(true, "OK");
  }
}
