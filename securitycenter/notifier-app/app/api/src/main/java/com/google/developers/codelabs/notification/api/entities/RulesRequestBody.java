package com.google.developers.codelabs.notification.api.entities;

import com.google.api.server.spi.config.AnnotationBoolean;
import com.google.api.server.spi.config.ApiResourceProperty;

import java.util.List;

/**
 * The Class RulesRequestBody.
 */
public class RulesRequestBody {

  private List<Rule> rules;

  /**
   * Gets the rules.
   *
   * @return the rules
   */
  public List<Rule> getRules() {
    return rules;
  }

  /**
   * Sets the rules.
   *
   * @param rules the new rules
   */
  public void setRules(List<Rule> rules) {
    this.rules = rules;
  }


  /**
   * Checks if is empty.
   *
   * @return true, if is empty
   */
  @ApiResourceProperty(ignored = AnnotationBoolean.TRUE)
  public boolean isEmpty() {
    return rules == null || rules.isEmpty();
  }
}
