# `llm-d` Deployment Guide

This guide provides a demonstration of how to get up and running with `llm-d` on RHOAI based on https://access.redhat.com/articles/7131048.

## Prerequisites - Get a cluster

- OpenShift - 4.18+
  - role: `cluster-admin`
- OpenShift AI - 2.25+

>> NOTE: this demo assumes RHOAI 2.25 operator is already installed on the cluster

### OpenShift 4.18

See [ocp-4.18](gitops/ocp-4.18) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

## Deploy

```sh
until oc apply -k demo/llm-d; do : ; done
```

## Additional Info

- [Notes](NOTES.md)
- [Deploying a model by using the Distributed Inference Server with llm-d](https://access.redhat.com/articles/7131048)
- [LLM-D: GPU-Accelerated Cache-Aware LLM Inference](https://github.com/cnuland/hello-chris-llm-d)
- [Demystifying Inferencing at Scale with LLM-D on Red Hat Openshift on IBM Cloud](https://community.ibm.com/community/user/blogs/tyler-lisowski/2025/05/30/ai-demystifying-llmd)
- [OAI Release Notes - 2.24](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.24/html-single/release_notes/index#developer-preview-features_relnotes)

curl -X POST http://a5b04a5e001d74035aa36adde93e98f5-1797832142.us-east-2.elb.amazonaws.com/llm-test/qwen/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-0.6B",
    "prompt": "Explain the difference between supervised and unsupervised learning in machine learning. Include examples of algorithms used in each type.",
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9
  }'