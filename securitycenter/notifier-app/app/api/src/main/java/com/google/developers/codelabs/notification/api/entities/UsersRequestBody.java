package com.google.developers.codelabs.notification.api.entities;

import com.google.api.server.spi.config.AnnotationBoolean;
import com.google.api.server.spi.config.ApiResourceProperty;

import java.util.List;

/**
 * The Class UsersRequestBody.
 */
public class UsersRequestBody {

  private List<ApiUser> users;

  /**
   * Gets the users.
   *
   * @return the users
   */
  public List<ApiUser> getUsers() {
    return users;
  }

  /**
   * Sets the users.
   *
   * @param users the new users
   */
  public void setUsers(List<ApiUser> users) {
    this.users = users;
  }

  /**
   * Checks if is empty.
   *
   * @return true, if is empty
   */
  @ApiResourceProperty(ignored = AnnotationBoolean.TRUE)
  public boolean isEmpty() {
    return users == null || users.isEmpty();
  }
}
