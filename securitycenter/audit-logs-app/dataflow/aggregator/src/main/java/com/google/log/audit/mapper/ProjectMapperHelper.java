package com.google.log.audit.mapper;

import java.io.IOException;
import java.net.URL;
import java.security.GeneralSecurityException;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.cloudresourcemanager.CloudResourceManager;
import com.google.api.services.cloudresourcemanager.CloudResourceManager.Projects;
import com.google.api.services.cloudresourcemanager.CloudResourceManagerScopes;
import com.google.api.services.cloudresourcemanager.model.Project;
import com.google.common.io.ByteSource;
import com.google.common.io.Resources;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Helper class for project extra information.
 * @author dandrade
 *
 */
public class ProjectMapperHelper {

  private static final Logger LOG = LoggerFactory.getLogger(ProjectMapperHelper.class);
  private static final String SERVICE_ACCOUNT_KEY_FILE = "google_api_client.json";
  private static final ByteSource BROWSER_CREDENTIAL = getBrowserCredential();

  private ProjectMapperHelper() {
  }

  /**
   * get a project number prom the given project id using CloudResourceManager API.
   * @param projectId The immutable Id of the Project 
   * @return the immutable Project Number as a String or null if project not found or an error occurs.
   * @throws RuntimeException if it fails to get a TrustedTransport for the HTTP connection.
   */
  public static String getProjectNumber(String projectId) {
    try {
      Project project = getProjectsEndpoint().get(projectId).execute();
      if (project != null) {
        return Long.toString(project.getProjectNumber());
      } else {
        LOG.info("project {} not found on lookup for project number.", projectId);
        return null;
      }
    } catch (GeneralSecurityException e1) {
      LOG.error("Error getting TrustedTransport when calling CloudResourceManager for project:" + projectId, e1);
      throw new RuntimeException(e1);
    } catch (IOException e1) {
      LOG.error("Error processing CloudResourceManager call to project:" + projectId, e1);
      return null;
    }
  }

  private static Projects getProjectsEndpoint() throws GeneralSecurityException, IOException {
    JsonFactory jsonFactory = JacksonFactory.getDefaultInstance();
    HttpTransport transport = GoogleNetHttpTransport.newTrustedTransport();
    GoogleCredential credential = getScopedCredential(jsonFactory, transport);
    return new CloudResourceManager.Builder(transport, jsonFactory, credential).build().projects();
  }

  private static GoogleCredential getScopedCredential(JsonFactory jsonFactory, HttpTransport transport) throws IOException {
    GoogleCredential credential = GoogleCredential.fromStream(BROWSER_CREDENTIAL.openStream(), transport, jsonFactory);
    return credential.createScoped(CloudResourceManagerScopes.all());
  }

  private static ByteSource getBrowserCredential() {
    try {
        URL url = Resources.getResource(SERVICE_ACCOUNT_KEY_FILE);
        return Resources.asByteSource(url);
      } catch (IllegalArgumentException e) {
        LOG.error("Resource browser service account file \"{}\" not found.", SERVICE_ACCOUNT_KEY_FILE);
        throw new RuntimeException(e);
      }
  }
}
