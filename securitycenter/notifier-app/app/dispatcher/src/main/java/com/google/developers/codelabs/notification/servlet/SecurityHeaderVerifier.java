package com.google.developers.codelabs.notification.servlet;

import com.google.common.base.Joiner;
import com.google.developers.codelabs.notification.enums.AppEngineHttpHeaders;

import java.util.Set;

import javax.servlet.http.HttpServletRequest;

/**
 * Class that validates security headers presence.
 */
public class SecurityHeaderVerifier {

  /**
   * Ensure At Least One AppEngineHeader on request.
   * @param request
   * @param headers
   */
  public void ensureAtLeastOneAppEngineHeader(HttpServletRequest request,
      Set<AppEngineHttpHeaders> headers) {

    boolean noHeader = true;
    for (AppEngineHttpHeaders header : headers) {
      if (request.getHeader(header.getHeader()) != null) {
        noHeader = false;
        break;
      }
    }
    if (noHeader) {
      throw new IllegalStateException("attempt to access handler directly, "
          + "missing custom App Engine header: " + Joiner.on(";").join(headers));
    }
  }

}
