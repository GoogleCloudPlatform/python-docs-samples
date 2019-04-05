package com.google.developers.codelabs.notification.core.model;

import com.google.common.base.MoreObjects;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

/**
 * The Class User.
 */
@Entity
public class NotificationUser {

  /** The email. */
  @Id
  public String email;

  /** The telephone number. */
  public String telephone_number;

  /** The jira uid. */
  public String jira_uid;

  /** The role. */
  public String role;

  /**
   * Instantiates a new user.
   *
   * @param email the email
   * @param telephone_number the telephone number
   * @param jira_uid the jira uid
   * @param role the role
   */
  public NotificationUser(String email, String telephone_number, String jira_uid, String role) {
    this.email = email;
    this.telephone_number = telephone_number;
    this.jira_uid = jira_uid;
    this.role = role;
  }

  /**
   * Instantiates a new user.
   */
  public NotificationUser() {}

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(this)
        .add("email", email)
        .add("telephone_number", telephone_number)
        .add("jira_uid", jira_uid)
        .add("role", role)
        .omitNullValues()
        .toString();
  }

  /**
   * Gets the email.
   *
   * @return the email
   */
  public String getEmail() {
    return email;
  }

  /**
   * Gets the telephone number.
   *
   * @return the telephone number
   */
  public String getTelephone_number() {
    return telephone_number;
  }

  /**
   * Gets the jira uid.
   *
   * @return the jira uid
   */
  public String getJira_uid() {
    return jira_uid;
  }

  /**
   * Gets the role.
   *
   * @return the role
   */
  public String getRole() {
    return role;
  }

}
