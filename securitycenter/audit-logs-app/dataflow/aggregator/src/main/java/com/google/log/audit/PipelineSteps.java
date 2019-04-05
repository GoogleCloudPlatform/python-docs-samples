package com.google.log.audit;

public enum PipelineSteps {
  READ_PUB_SUB("Read lines from Pub/sub"),
  CONVERT_TO_KVP("Convert log string to key value pair"),
  GROUP_KVP_BY_KEY("Group string logs by assetId"),
  CONVERT_KVP_TO_STRING("Convert Key Value pair to string"),
  WRITE_TO_PUB_SUB("Write Aggregate Findings to Pub/Sub"),
  WRITE_INVALID_LOG_ITEMS("Write Invalid log items"),
  USE_FIXED_WINDOWS("Apply fixed window to unbound stream"),
  VALIDATE_LOG_ITEMS("Validate log items"),
  SPLIT_KVP_CHUNKS("Split KVP in fixed size chunks");
  
  public String text;
  
  PipelineSteps(String text) {
    this.text = text;
  }
}
