package com.google.developers.codelabs.notification.api.entities;

import com.google.common.base.MoreObjects;

/**
 * The Class ApiUser.
 */
public class ApiUser {

  private String email;
  private String telephoneNumber;
  private String jiraUid;
  private String role;

  /**
   * Gets the email.
   *
   * @return the email
   */
  public String getEmail() {
    return email;
  }

  /**
   * Sets the email.
   *
   * @param email the new email
   */
  public void setEmail(String email) {
    this.email = email;
  }

  /**
   * Gets the telephone number.
   *
   * @return the telephone number
   */
  public String getTelephoneNumber() {
    return telephoneNumber;
  }

  /**
   * Sets the telephone number.
   *
   * @param telephoneNumber the new telephone number
   */
  public void setTelephoneNumber(String telephoneNumber) {
    this.telephoneNumber = telephoneNumber;
  }

  /**
   * Gets the jira uid.
   *
   * @return the jira uid
   */
  public String getJiraUid() {
    return jiraUid;
  }

  /**
   * Sets the jira uid.
   *
   * @param jiraUid the new jira uid
   */
  public void setJiraUid(String jiraUid) {
    this.jiraUid = jiraUid;
  }

  /**
   * Gets the role.
   *
   * @return the role
   */
  public String getRole() {
    return role;
  }

  /**
   * Sets the role.
   *
   * @param role the new role
   */
  public void setRole(String role) {
    this.role = role;
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("email", email)
        .add("telephoneNumber", telephoneNumber)
        .add("jiraUid", jiraUid)
        .add("role", role)
        .toString();
  }

}
