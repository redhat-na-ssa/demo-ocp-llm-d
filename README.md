# `llm-d` Deployment Guide

This guide provides a demonstration of how to get up and running with `llm-d` on RHOAI based on https://access.redhat.com/articles/7131048.

## Prerequisites - Get a cluster

- OpenShift 4.18+
  - role: `cluster-admin`

[Red Hat Demo Platform](https://demo.redhat.com) Options (Tested)

NOTE: The node sizes below are the **recommended minimum** to select for provisioning

- <a href="https://demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.sandbox-ocp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">AWS with OpenShift Open Environment</a>
  - 1 x Control Plane - `m6a.2xlarge`
  - 0 x Workers - `m6a.4xlarge`
- <a href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp-wksp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">Red Hat OpenShift Container Platform Cluster (AWS)</a>
  - 1 x Control Plane

## Quickstart

- OpenShift 4.18 - See [ocp-4.18-prereqs](gitops/ocp-4-18-prereqs) for installation of `llm-d` dependencies

```sh
until oc apply -k demo/llm-d; do : ; done
```

OpenShift 4.18

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

## Additional Info

- [Notes](NOTES.md)
- [Deploying a model by using the Distributed Inference Server with llm-d](https://access.redhat.com/articles/7131048)
- [LLM-D: GPU-Accelerated Cache-Aware LLM Inference](https://github.com/cnuland/hello-chris-llm-d)

## TODO

- [ ] Verify this works in a bare metal install (istio)
- [ ] Fix
  - `oc apply -f gitops/instance/llm-d/deployment.yaml`
  - `no matches for kind "LLMInferenceService" in version "serving.kserve.io/v1alpha1"
