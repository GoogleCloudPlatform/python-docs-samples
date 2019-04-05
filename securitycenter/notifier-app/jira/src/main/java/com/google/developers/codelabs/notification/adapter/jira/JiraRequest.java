package com.google.developers.codelabs.notification.adapter.jira;

import com.google.common.base.Joiner;
import com.google.common.base.MoreObjects;
import com.google.common.io.CharStreams;

import org.apache.commons.codec.binary.Base64;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Class that handles a Jira Request.
 */
public class JiraRequest {
  private static final Logger LOG = Logger.getLogger(JiraRequest.class.getName());

  /** The jira url. */
  private String baseUrl;

  /** The jira user name. */
  private String userName;

  /** The jira apiToken. */
  private String apiToken;

  /** The Constant START_OF_HTTP_SUCCESS_INTERVAL. */
  private static final int START_OF_HTTP_SUCCESS_INTERVAL = 200;

  /** The Constant END_OF_SUCCESS_INTERVAL. */
  private static final int END_OF_SUCCESS_INTERVAL = 300;

  /**
   * Default constructor.
   */
  public JiraRequest() {

  }

  /**
   * Constructor with configuration.
   * @param baseUrl
   * @param userName
   * @param apiToken
   */
  public JiraRequest(String baseUrl, String userName, String apiToken) {
    this.baseUrl = baseUrl;
    this.userName = userName;
    this.apiToken = apiToken;
  }

  /**
   * Create a issue on Jira.
   *
   * @param json body submitted.
   * @return HttpResponse
   */
  public HttpResponse createIssue(String json) {
    if (LOG.isLoggable(Level.INFO)) {
      LOG.info(String.format("%s with = [%s]", this.toString(), json));
    }
    String fullUrl = Joiner.on("/").join(this.baseUrl, "rest/api/2/issue/");

    CloseableHttpClient httpclient = HttpClients.custom().build();
    Base64 base64 = new Base64();
    HttpResponse response = null;
    try {
      HttpPost request = new HttpPost(fullUrl);
      String userAndApiToken = Joiner.on(":").join(this.userName, this.apiToken);
      byte[] userAndApiTokenBytes = (userAndApiToken).getBytes();
      request.addHeader("Authorization", "Basic " + base64.encodeAsString(userAndApiTokenBytes));
      request.addHeader("Content-Type", "application/json");
      request.setEntity(new StringEntity(json));
      response = httpclient.execute(request);
      int statusCode = response.getStatusLine().getStatusCode();
      Readable reader =
          new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
      String jsonResponse = CharStreams.toString(reader);

      if (statusCode >= START_OF_HTTP_SUCCESS_INTERVAL && statusCode < END_OF_SUCCESS_INTERVAL) {
        LOG.info(String.format("SUCCESS status=[%d] body=[%s]", statusCode, jsonResponse));
      } else {
        LOG.warning(String.format("ERROR status=[%d] body=[%s]", statusCode, jsonResponse));
      }
    } catch (IOException e) {
      LOG.log(Level.CONFIG, e.getMessage(), e);
    }
    return response;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("baseUrl", baseUrl)
        .add("userName", userName).toString();
  }
}
