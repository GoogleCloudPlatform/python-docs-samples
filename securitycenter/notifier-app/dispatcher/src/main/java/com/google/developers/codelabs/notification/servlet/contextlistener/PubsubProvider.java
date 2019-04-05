package com.google.developers.codelabs.notification.servlet.contextlistener;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.util.Utils;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.services.pubsub.Pubsub;
import com.google.api.services.pubsub.PubsubScopes;
import com.google.appengine.api.utils.SystemProperty;
import com.google.developers.codelabs.notification.service.RetryHttpInitializerWrapper;
import com.google.inject.Provider;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Pubsub provider.
 */
public class PubsubProvider implements Provider<Pubsub> {
  private static final Logger LOG = Logger.getLogger(PubsubProvider.class.getName());

  @Override
  public Pubsub get() {
    HttpTransport httpTransport = Utils.getDefaultTransport();
    JsonFactory jsonFactory = Utils.getDefaultJsonFactory();

    GoogleCredential credential = null;
    try {
      credential = GoogleCredential.getApplicationDefault(httpTransport, jsonFactory);
      if (credential.createScopedRequired()) {
        credential = credential.createScoped(PubsubScopes.all());
      }

      LOG.info(String
          .format("Credential for service account user [%s] created",
              credential.getServiceAccountUser()));

    } catch (IOException e) {
      LOG.log(Level.WARNING, "Error creating credential", e);
    }

    // Using custom HttpRequestInitializer for automatic retry upon failures.
    HttpRequestInitializer initializer = new RetryHttpInitializerWrapper(credential);
    return new Pubsub.Builder(httpTransport, jsonFactory, initializer)
        .setApplicationName(SystemProperty.applicationId.get())
        .build();
  }
}
