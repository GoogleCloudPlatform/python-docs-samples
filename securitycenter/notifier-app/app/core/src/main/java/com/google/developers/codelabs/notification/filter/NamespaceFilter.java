package com.google.developers.codelabs.notification.filter;

import com.google.appengine.api.NamespaceManager;
import com.google.common.base.Strings;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

/**
 * The Class NamespaceFilter.
 */
public class NamespaceFilter implements Filter {

  private static final String NOTIFICATION_NAMESPACE = "NOTIFICATION_NAMESPACE";
  private static final Logger LOG = Logger.getLogger(NamespaceFilter.class.getName());

  @Override
  public void init(FilterConfig filterConfig) throws ServletException {
    LOG.log(Level.INFO, NamespaceFilter.class.getName() + " started.");
  }

  @Override
  public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
      throws IOException, ServletException {
    if (NamespaceManager.get() == null) {

      String newNamespace = System.getenv(NOTIFICATION_NAMESPACE);

      if (!Strings.isNullOrEmpty(newNamespace)) {
        NamespaceManager.set(newNamespace);
        LOG.info("set namespace:" + NamespaceManager.get());
      } else {
        LOG.info("Custom namespace not configured.");
      }
    }
    chain.doFilter(request, response);
  }

  @Override
  public void destroy() {
    LOG.log(Level.INFO, NamespaceFilter.class.getName() + " destroyed.");
  }

}
