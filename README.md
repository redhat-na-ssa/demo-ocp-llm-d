# `llm-d` Deployment Guide

This guide provides a demonstration of how to get up and running with `llm-d` on RHOAI 2.25 and OCP 4.18 based on:
- https://access.redhat.com/articles/7131048
- https://github.com/opendatahub-io/kserve/tree/release-v0.15/docs/samples/llmisvc/ocp-4-18-setup

## Prerequisites - Get a RHOAI cluster

- OpenShift - 4.18+
  - role: `cluster-admin`
- OpenShift AI - 2.25+

### OpenShift 4.18 Prereqs

See [ocp-4.18](gitops/ocp-4.18) for installation of `llm-d` dependencies (Gateway API)

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

> NOTE: the Gateway API dependencies are vendored as part of OpenShift 4.19+

## Deploy

```sh
until oc apply -k deployment; do : ; done
```

### Send a Request

- Find the URL of the Gateway:

```sh
oc get gateways -A

NAMESPACE           NAME                     CLASS   ADDRESS                                                                   PROGRAMMED   AGE
openshift-ingress   openshift-ai-inference   istio   a5b04a5e001d74035aa36adde93e98f5-1797832142.us-east-2.elb.amazonaws.com   True         32m
```

- Send an HTTP request with the OpenAI API:
```
curl -X POST http://a5b04a5e001d74035aa36adde93e98f5-1797832142.us-east-2.elb.amazonaws.com/llm-test/qwen/v1/completions \
  -H "Content-Type: application/json" \
  -d '{ "model": "Qwen/Qwen3-0.6B", "prompt": "Explain the difference between supervised and unsupervised learning in machine learning. Include examples of algorithms used in each type.", "max_tokens": 200, "temperature": 0.7, "top_p": 0.9 }'
```

## Additional Info

- [Notes](NOTES.md)
- [Deploying a model by using the Distributed Inference Server with llm-d](https://access.redhat.com/articles/7131048)
- [LLM-D: GPU-Accelerated Cache-Aware LLM Inference](https://github.com/cnuland/hello-chris-llm-d)
- [Demystifying Inferencing at Scale with LLM-D on Red Hat Openshift on IBM Cloud](https://community.ibm.com/community/user/blogs/tyler-lisowski/2025/05/30/ai-demystifying-llmd)
- [OAI Release Notes - 2.25](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.25/pdf/release_notes/Red_Hat_OpenShift_AI_Self-Managed-2.25-Release_notes-en-US.pdf)
