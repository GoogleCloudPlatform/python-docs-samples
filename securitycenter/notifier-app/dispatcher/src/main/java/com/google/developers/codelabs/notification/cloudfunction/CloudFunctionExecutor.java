package com.google.developers.codelabs.notification.cloudfunction;

import com.google.api.client.json.GenericJson;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.appengine.api.urlfetch.*;
import com.google.common.base.Strings;
import com.google.developers.codelabs.notification.core.service.ConfigurationService;
import com.google.developers.codelabs.notification.service.OutputMessage;
import com.google.inject.Inject;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeMap;
import java.util.logging.Level;
import java.util.logging.Logger;

import static java.net.HttpURLConnection.HTTP_MULT_CHOICE;
import static java.net.HttpURLConnection.HTTP_OK;

/**
 * The Class CloudFunctionExecutor.
 */
public class CloudFunctionExecutor {

  private static final String UNSUCCESSFUL_MSG =
      "Cloud function returned error code %s and info: %s";
  private static final String ERROR_MSG = "Error callling cloud endpoint";
  private static final String ACTIVE_BUT_NOT_CONFIGURED_MSG =
      "Cloud function integration active but not configured";
  private static final String CLIENT_KEY = "CLOUD_FUNCTION_CLIENT_KEY";
  private static final String URL_KEY = "CLOUD_FUNCTION_URL";
  private static final String SECURITY_HEADER = "x-client-key";

  private static final Logger LOG = Logger.getLogger(CloudFunctionExecutor.class.getName());

  private ConfigurationService configurationService;

  /**
   * Constructor.
   * @param configurationService
   */
  @Inject
  public CloudFunctionExecutor(ConfigurationService configurationService) {
    this.configurationService = configurationService;
  }

  /**
   * Call.
   *
   * @param outputMessage the output message
   * @return the string
   */
  public String call(OutputMessage outputMessage) {

    String functionUrl = configurationService.getConfig(URL_KEY);
    String clientKey = configurationService.getConfig(CLIENT_KEY);

    if (!isConfigured(functionUrl, clientKey)) {
      LOG.log(Level.WARNING, ACTIVE_BUT_NOT_CONFIGURED_MSG);
      return null;
    }
    try {
      LOG.log(Level.INFO, "Calling cloud function at " + functionUrl);
      HTTPRequest request = buildHttpRequest(functionUrl, clientKey, outputMessage);
      HTTPResponse response = fetchResponse(request);
      return getMessageFromResponse(response);
    } catch (IOException e) {
      return getErrorMessage(e);
    }
  }

  private String getErrorMessage(IOException e) {
    LOG.log(Level.SEVERE, ERROR_MSG, e);
    return null;
  }

  private String getMessageFromResponse(HTTPResponse response) {
    String responseText = new String(response.getContent(), StandardCharsets.UTF_8);
    int code = response.getResponseCode();
    if (isSuccessful(code)) {
      LOG.log(Level.INFO, responseText);
      return responseText;
    } else {
      LOG.log(Level.WARNING, String.format(UNSUCCESSFUL_MSG, Integer.toString(code), responseText));
      return null;
    }
  }

  private HTTPResponse fetchResponse(HTTPRequest request) throws IOException {
    URLFetchService fetcher = URLFetchServiceFactory.getURLFetchService();
    HTTPResponse response = fetcher.fetch(request);
    return response;
  }

  private HTTPRequest buildHttpRequest(String functionUrl, String clientKey,
      OutputMessage outputMessage) throws MalformedURLException {
    URL url = new URL(functionUrl);
    HTTPRequest request = new HTTPRequest(url, HTTPMethod.POST);
    request.addHeader(new HTTPHeader(SECURITY_HEADER, clientKey));
    request.setPayload(buildPayload(outputMessage).getBytes());
    return request;
  }

  private boolean isConfigured(String functionUrl, String clientKey) {
    return !Strings.nullToEmpty(functionUrl).trim().isEmpty()
        && !Strings.nullToEmpty(clientKey).trim().isEmpty();
  }

  private boolean isSuccessful(int code) {
    return code >= HTTP_OK && code < HTTP_MULT_CHOICE;
  }

  private String buildPayload(OutputMessage outputMessage) {
    GenericJson genericJson = new GenericJson();
    genericJson.setFactory(JacksonFactory.getDefaultInstance());

    Map<String, Object> message = new TreeMap<>();
    message.put("humanReadableMessage", outputMessage.buildSubject());
    message.put("ruleType", outputMessage.getRuleType().name());
    message.put("notificationType", outputMessage.getNotificationType());
    message.put("actionType", outputMessage.getActionType().name());
    message.put("extraInfo", outputMessage.getExtraInfo());

    Set<Entry<String, String>> entrySet = outputMessage.getContext().getAttributes().entrySet();
    Map<String, String> attributes = new TreeMap<>();
    for (Entry<String, String> entry : entrySet) {
      attributes.put(entry.getKey(), entry.getValue());
    }//TODO add other values
    message.put("attributes", attributes);

    genericJson.set("message", message);
    return genericJson.toString();
  }
}
