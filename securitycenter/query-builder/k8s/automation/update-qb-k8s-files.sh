#!/usr/bin/env bash
main() {
    local env_template_dir='';
    for env_template_dir in $(find scc-query-builder/k8s/manifests/templates/envs -type d); do
        local env_name=$(basename $env_template_dir);
        if [[ $env_name != 'envs' ]]; then
            echo $env_template_dir
            mkdir -p scc-query-builder/k8s/manifests/generated/$env_name/
            kustomize build $env_template_dir > scc-query-builder/k8s/manifests/generated/$env_name/kustomized-deployments.yaml
        fi
    done
}

main "$@"