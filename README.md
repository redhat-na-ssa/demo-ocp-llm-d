# `llm-d` Deployment Guide

This guide provides a demonstration of how to get up and running with `llm-d` on RHOAI based on:

- https://access.redhat.com/articles/7131048
- https://github.com/opendatahub-io/kserve/tree/release-v0.15/docs/samples/llmisvc/ocp-4-18-setup
- https://github.com/llm-d/llm-d/blob/main/guides/precise-prefix-cache-aware/README.md

> **⚠️ Disclaimer**: This configuration is not officially supported and is provided for experimental/development
> purposes only.

## Prerequisites - Get a cluster

- OpenShift - 4.18+
  - role: `cluster-admin`
- OpenShift AI - 2.25+

[Red Hat Demo Platform](https://demo.redhat.com) Options (Tested)

NOTE: The node sizes below are the **recommended minimum** to select for provisioning

- <a href="https://demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.sandbox-ocp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">AWS with OpenShift Open Environment</a>
  - 1 x Control Plane - `m6a.2xlarge`
  - 0 x Workers - `m6a.4xlarge`
- <a href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp-wksp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">Red Hat OpenShift Container Platform Cluster (AWS)</a>
  - 1 x Control Plane

### OpenShift 4.18

See [ocp-4.18](gitops/ocp-4.18) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

### OpenShift 4.19+

See [ocp-4.19](gitops/ocp-4.19) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.19; do : ; done
```

## Quickstart

```sh
until oc apply -k demo/llm-d; do : ; done
```

## Additional Info

- [Notes](NOTES.md)
- [Deploying a model by using the Distributed Inference Server with llm-d](https://access.redhat.com/articles/7131048)
- [LLM-D: GPU-Accelerated Cache-Aware LLM Inference](https://github.com/cnuland/hello-chris-llm-d)
- [Demystifying Inferencing at Scale with LLM-D on Red Hat Openshift on IBM Cloud](https://community.ibm.com/community/user/blogs/tyler-lisowski/2025/05/30/ai-demystifying-llmd)
- [OAI Release Notes - 2.25](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.25/html-single/release_notes/index#developer-preview-features_relnotes)
