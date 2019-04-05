# Kubernetes with Kustomize

To use our Kubernetes YAMLs, you will need to install Kustomize. It's a add-on that helps to customize informations per environment.

## Install Kustomize
You can install Kustomize follow the instructions in this [page](https://github.com/kubernetes-sigs/kustomize/blob/master/INSTALL.md)

## How to use
After install Kustomize, you will be able to customize our YAMLs per environment.
To do this, you can execute the following command:

```bash
kustomize build scc-query-builder/k8s/manifests/templates/envs/prod/ > scc-query-builder/k8s/manifests/generated/prod/kustomized-deployments.yaml
```

This command will apply the informations contained on YAMLs file on prod folder into base folder YAMLs file.

After that, you can apply the output YAML with specific informations for the environment.
