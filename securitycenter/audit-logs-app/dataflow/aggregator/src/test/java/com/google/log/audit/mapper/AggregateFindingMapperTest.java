package com.google.log.audit.mapper;

import static org.junit.Assert.*;

import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.io.IOUtils;
import org.junit.Test;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class AggregateFindingMapperTest {

  private static final String WINDOW_START = "1";

  private static final String WINDOW_END = "2";

  private static final String AUDIT_LOG = "audit_log.json";

  private String getFromJSON(String json) {
    try {
      return new JsonParser().parse(IOUtils.resourceToString("/" + json, Charset.defaultCharset())).toString();
    } catch (Exception e) {
      return "";
    }
  }

  @Test
  public void testBaseFindingMapperToFindingId() {
    List<String> logs = new ArrayList<>();
    logs.add(getFromJSON(AUDIT_LOG));
    logs.add(getFromJSON(AUDIT_LOG));
    AggregateFindingMapper findingMapper = new AggregateFindingMapper(logs, WINDOW_START, WINDOW_END);
    String jsonFinding = findingMapper.parse().build();

    JsonParser jsonParser = new JsonParser();
    JsonObject findingJson = jsonParser.parse(jsonFinding).getAsJsonObject();

    assertEquals("ACTIVE", findingJson.get("state").getAsString());

    assertEquals("//compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
            findingJson.get("resourceName").getAsString());

    assertEquals(
            "Aggregated finding resourceName://compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1 v1.compute.instances.delete",
            findingJson.get("category").getAsString());

    assertEquals(
            "https://console.cloud.google.com/logs/viewer?"
                    + "project=gce-audit-logs-216020&minLogLevel=0&expandAll=true&interval=NO_LIMIT&"
                    + "expandAll=true&advancedFilter=insertId%3D%22-epdbpzcec8%22%20OR%20insertId%3D%22-epdbpzcec8%22%0A",
            findingJson.get("externalUri").getAsString());

    JsonObject sourceProperties = findingJson.get("sourceProperties").getAsJsonObject();

    assertEquals("2", sourceProperties.get("total_logs_aggregated").getAsString());

    assertEquals("gce_instance", sourceProperties.get("resource_type").getAsString());

    assertEquals("projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1",
            sourceProperties.get("protoPayload_resourceName").getAsString());

    assertEquals(
            "[\"insertId:-epdbpzcec8 author:dandrade@ciandt.com resourceType:gce_instance methodName:v1.compute.instances.delete timestamp:2018-09-10T22:53:29.697Z severity:NOTICE instance_id:7001864148707138537 project_id:gce-audit-logs-216020 zone:us-east1-b\","
                    + "\"insertId:-epdbpzcec8 author:dandrade@ciandt.com resourceType:gce_instance methodName:v1.compute.instances.delete timestamp:2018-09-10T22:53:29.697Z severity:NOTICE instance_id:7001864148707138537 project_id:gce-audit-logs-216020 zone:us-east1-b\"]",
            sourceProperties.get("aggregate_value").getAsString());

    assertEquals(
            "Aggregated finding resourceName://compute.googleapis.com/projects/gce-audit-logs-216020/zones/us-east1-b/instances/instance-victim-1 v1.compute.instances.delete",
            sourceProperties.get("full_scc_category").getAsString());
  }

}
