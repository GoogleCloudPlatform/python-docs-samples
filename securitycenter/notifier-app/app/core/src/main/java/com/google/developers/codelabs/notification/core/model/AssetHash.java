package com.google.developers.codelabs.notification.core.model;

import com.googlecode.objectify.annotation.Entity;
import com.googlecode.objectify.annotation.Id;

@Entity
public class AssetHash {

    @Id
    private String assetHash;

    public AssetHash() {

    }

    public AssetHash(String assetHash) {
        super();
        this.assetHash = assetHash;
    }

    public String getAssetHash() {
        return assetHash;
    }
}
