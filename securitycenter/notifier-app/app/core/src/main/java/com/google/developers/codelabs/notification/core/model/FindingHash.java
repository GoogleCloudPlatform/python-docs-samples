package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

@Entity
public class FindingHash {

  @Id
  private String findingHash;

  public FindingHash() {
  }

  public FindingHash(String findingHash) {
    this.findingHash = findingHash;
  }

  public String getFindingHash() {
    return findingHash;
  }
}
