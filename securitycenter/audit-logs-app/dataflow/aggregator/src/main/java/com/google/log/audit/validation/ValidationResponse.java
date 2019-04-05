package com.google.log.audit.validation;

public class ValidationResponse {
  
  private boolean valid;
  private String message;
  
  public ValidationResponse(boolean valid, String message) {
    super();
    this.valid = valid;
    this.message = message;
  }

  public boolean isValid() {
    return valid;
  }

  public String getMessage() {
    return message;
  }

}
