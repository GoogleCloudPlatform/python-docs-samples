package com.google.developers.codelabs.notification.message;

/**
 * The Enum FieldId.
 */
public enum FieldId {

  /** The count. */
  COUNT("COUNT"),

  /** The project id. */
  PROJECT_ID("PROJECT-ID"),

  /** The asset ids. */
  ASSET_IDS("ASSET-IDS"),

  /** The asset type. */
  ASSET_TYPE("ASSET-TYPE"),
  
  ORGANIZATION_NAME("ORGANIZATION-NAME"),

  FINDINGS_RESULT_TYPE("RESULT-TYPE"),

  FINDINGS_SCANNER_ID("SCANNER-ID"),
  
  MARKS("MARKS");

  private String fieldName;

  private FieldId(String fieldName) {
    this.fieldName = fieldName;
  }

  /**
   * Gets the field name.
   *
   * @return the field name
   */
  public String getFieldName() {
    return fieldName;
  }
}
