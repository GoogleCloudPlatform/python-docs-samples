'use strict';

// Imports
const should = require('should');
const BinAuthzSamples = require('./samples/binauthz-samples');
const converter = require('../converter');

describe('Binary Authorization log entry Mapping', function () {
    context('When receiving a Binary Authorization log entry', function () {
        it('should process a Binary Authorization allow by default rule pod creation.', function () {
            const allowPodCreation = BinAuthzSamples.allowDeployAuthorizedImage();
            const source_finding = converter.convertToFinding(allowPodCreation, {});
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.category.should.equal('BinAuthz deployment successful');
            source_finding.eventTime.should.equal('2019-02-15T10:23:13Z');
            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4"]');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');
        });

        it('should process a Binary Authorization deny by default cluster rule pod creation.', function () {
            const denyPodCreation = BinAuthzSamples.denyByDefaultRuleDeployUnauthorizedImage();
            const source_finding = converter.convertToFinding(denyPodCreation, {});
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.category.should.equal('BinAuthz blocked deployment attempt');
            source_finding.eventTime.should.equal('2019-02-15T11:43:23Z');
            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba"]');
            source_finding.sourceProperties.description.should.equal('\"pods \\"image-without-attestation\\" is forbidden: image policy webhook backend denied one or more images: Denied by cluster admission rule for us-central1-a.test-cluster. Overridden by evaluation mode\"');
            source_finding.sourceProperties.remediation.should.equal('Review image to determine why it was not signed by the required authority prior to deploying. You should also review your Binary Authorization policy to ensure the attestation requirement is correct.');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');

            source_finding.sourceProperties.deniedImageNames.should.equal('[]');
        });

        it('should process a Binary Authorization allow by default rule pod creation using break glass.', function () {
            const allowWithBreakGlass = BinAuthzSamples.allowDeployWithBreakGlass();
            const source_finding = converter.convertToFinding(allowWithBreakGlass, {});
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.category.should.equal('Breakglass deployment against BinAuthz policy');
            source_finding.eventTime.should.equal('2019-02-15T10:20:30Z');
            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba"]');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');
            source_finding.sourceProperties['protoPayload_request_metadata_annotations_alphaimagepolicyk8siobreakglass'].should.equal('true');
        });

        it('should process a Binary Authorization allow by default rule pod creation using break glass with new format.', function () {
            const allowWithBreakGlassNewFormat = BinAuthzSamples.allowDeployWithBreakGlassNewFormat();
            const source_finding = converter.convertToFinding(allowWithBreakGlassNewFormat, {});
            console.log(JSON.stringify(source_finding));
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam-beta/zones/europe-west2-a/clusters/test-europe-west2-a-cluster');
            source_finding.category.should.equal('Breakglass deployment against BinAuthz policy');
            source_finding.eventTime.should.equal('2019-02-28T14:13:13Z');
            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4"]');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');
            source_finding.sourceProperties['protoPayload_request_metadata_annotations_alphaimagepolicyk8siobreakglass'].should.equal('true');
        });

        it('should process a Binary Authorization deny by default rule pod creation using attestors.', function () {
            const allowWithBreakGlass = BinAuthzSamples.denyDeployWithAttestors();
            const source_finding = converter.convertToFinding(allowWithBreakGlass, {});
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.category.should.equal('BinAuthz blocked deployment attempt');
            source_finding.eventTime.should.equal('2019-01-16T18:40:22Z');
            source_finding.sourceProperties.severity.should.equal('ERROR');
            source_finding.sourceProperties.imageNames.should.equal('["k8s.gcr.io/k8s-dns-kube-dns-amd64:1.14.13","k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64:1.14.13","k8s.gcr.io/k8s-dns-sidecar-amd64:1.14.13","gcr.io/google-containers/prometheus-to-sd:v0.2.3"]');
            source_finding.sourceProperties.description.should.equal('\"pods \\"kube-dns-548976df6c-f5gn4\\" is forbidden: image policy webhook backend denied one or more images: Denied by default admission rule. Denied by Attestor. Image gcr.io/google-containers/prometheus-to-sd:v0.2.3 denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor\"');
            source_finding.sourceProperties.remediation.should.equal('Review image to determine why it was not signed by the required authority prior to deploying. You should also review your Binary Authorization policy to ensure the attestation requirement is correct.');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');
            source_finding.sourceProperties['protoPayload_request_metadata_annotations_seccompsecurityalphakubernetesiopod'].should.equal('docker/default');
        });

        it('should process a Binary Authorization deny by default rule pod creation using multiple attestors.', function () {
            const allowWithBreakGlass = BinAuthzSamples.denyByDefaultRuleMultipleImagesByMultipleAttestors();
            const source_finding = converter.convertToFinding(allowWithBreakGlass, {});
            source_finding.eventTime.should.equal('2019-02-15T10:20:31Z');
            source_finding.category.should.equal('BinAuthz blocked deployment attempt');
            source_finding.sourceProperties.remediation.should.equal('Review image to determine why it was not signed by the required authority prior to deploying. You should also review your Binary Authorization policy to ensure the attestation requirement is correct.');
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');

            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014","gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba"]');
            source_finding.sourceProperties.description.should.equal('\"pods \\"image-mixed-attestation-5947994cf8-wwsq6\\" is forbidden: image policy webhook backend denied one or more images: Denied by default admission rule. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014 denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor. Denied by default admission rule. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor\"');

            source_finding.sourceProperties.deniedImageNames.should.equal('["gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014","gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba"]');
            source_finding.sourceProperties.image_0_name.should.equal('gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014');
            source_finding.sourceProperties.image_0_denialRule_0.should.equal('projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor.');

            source_finding.sourceProperties.image_1_name.should.equal('gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba');
            source_finding.sourceProperties.image_1_denialRule_0.should.equal('projects/binary-control-clsecteam/attestors/build-secure: No attestations found that were valid and signed by a key trusted by the attestor');
            source_finding.sourceProperties.image_1_denialRule_1.should.equal('projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor');
        });

        it('should process a Binary Authorization deny by cluster rule pod creation using multiple attestors.', function () {
            const denyByClustereRuleDeployWithoutAttestors = BinAuthzSamples.denyByClustereRuleDeployWithoutAttestors();
            const source_finding = converter.convertToFinding(denyByClustereRuleDeployWithoutAttestors, {});
            source_finding.eventTime.should.equal('2019-02-15T14:59:40Z');
            source_finding.category.should.equal('BinAuthz blocked deployment attempt');
            source_finding.sourceProperties.remediation.should.equal('Review image to determine why it was not signed by the required authority prior to deploying. You should also review your Binary Authorization policy to ensure the attestation requirement is correct.');
            source_finding.resourceName.should.equal('//container.googleapis.com/projects/binary-control-clsecteam/zones/us-central1-a/clusters/test-cluster');
            source_finding.sourceProperties.protoPayload_methodName.should.equal('io.k8s.core.v1.pods.create');
            source_finding.sourceProperties.resource_type.should.equal('k8s_cluster');

            source_finding.sourceProperties.imageNames.should.equal('["gcr.io/binary-control-clsecteam/hello-world@sha256:c6f9b301683fef3dfb461078332a7d4e85fdffb9ab96222fb9bc58ef2dc4a014","gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba","gcr.io/google-samples/hello-app@sha256:c62ead5b8c15c231f9e786250b07909daf6c266d0fcddd93fea882eb722c3be4"]');
            source_finding.sourceProperties.description.should.equal('\"pods \\"image-mixed-attestation-5b9bb876b9-bx7rv\\" is forbidden: image policy webhook backend denied one or more images: Denied by cluster admission rule for us-central1-a.test-cluster. Denied by Attestor. Image gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba denied by projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor\"');

            source_finding.sourceProperties.image_0_name.should.equal('gcr.io/binary-control-clsecteam/hello-world@sha256:c35f311be50613cab019bc5cc9f1b90c02266dba6972e6d0a0aa82e930f53eba');
            source_finding.sourceProperties.image_0_denialRule_0.should.equal('projects/binary-control-clsecteam/attestors/amandak-deployment: No attestations found that were valid and signed by a key trusted by the attestor');

        });
    });
});