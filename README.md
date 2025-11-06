# `llm-d` Deployment Guide

This guide provides a demonstration of how to get up and running with `llm-d` on RHOAI based on:

- <a href="https://access.redhat.com/articles/7131048" target="_blank">Deploying a model by using the Distributed Inference with llm-d [Developer preview]</a>
- <a href="https://github.com/opendatahub-io/kserve/tree/release-v0.15/docs/samples/llmisvc/ocp-4-18-setup" target="_blank">Kserve Docs - OpenDataHub</a>
- <a href="https://github.com/llm-d/llm-d/blob/main/guides/precise-prefix-cache-aware/README.md" target="_blank">LLM-D Docs - Precise Prefix Cache Aware Routing</a>

## Prerequisites - Get a cluster

- OpenShift - 4.19+
  - role: `cluster-admin`
- OpenShift AI - 2.25+

[Red Hat Demo Platform](https://demo.redhat.com) Options (Tested)

NOTE: The node sizes below are the **recommended minimum** to select for provisioning

- <a href="https://demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.sandbox-ocp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">AWS with OpenShift Open Environment</a>
  - 1 x Control Plane - `m6a.2xlarge`
  - 0 x Workers - `m6a.4xlarge`
- <a href="https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp-wksp.prod&utm_source=webapp&utm_medium=share-link" target="_blank">Red Hat OpenShift Container Platform Cluster (AWS)</a>
  - 1 x Control Plane

### Install the [OpenShift Web Terminal](https://docs.openshift.com/container-platform/4.12/web_console/web_terminal/installing-web-terminal.html)

The following icon should appear in the top right of the OpenShift web console after you have installed the operator. Clicking this icon launches the web terminal.

![Web Terminal](docs/images/web-terminal.png "Web Terminal")

NOTE: Reload the page in your browser if you do not see the icon after installing the operator.

```sh
# apply the enhanced web terminal
oc apply -k https://github.com/redhat-na-ssa/llm-d-demo/demo/web-terminal

# delete old web terminal
$(wtoctl | grep 'oc delete')
```

Setup cluster nodes

```sh
# setup L40 single GPU machine set
ocp_aws_machineset_create_gpu g6.xlarge

# scale machineset to at least 1
ocp_machineset_scale 1

# setup cluster gpu autoscaling
apply_firmly demo/nvidia-gpu-autoscale
```

### OpenShift 4.19+

> [!NOTE]
> The [Gateway API dependencies](gitops/ocp-4.18/prereqs/gateway-api.yaml) are part of OpenShift 4.19+

See [ocp-4.19](gitops/ocp-4.19) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.19; do : ; done
```

### OpenShift 4.18 (Alternative)

> **⚠️ Disclaimer**: This configuration is not officially supported and is provided for experimental/development
> purposes only.

See [ocp-4.18](gitops/ocp-4.18) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

### Bare Metal Dependencies (YOLO)

The `MetalLB` operator, and a working configuration, is needed to [use `gatewayAPI` in OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/ingress_and_load_balancing/configuring-ingress-cluster-traffic#ingress-gateway-api).

Install `MetalLB` operator

```sh
oc apply -k demo/bare-metal
```

[Basic BGP / L2 examples](gitops/instance/metallb-operator/) (requires modification)

## Quickstart

The following command will create a `LLMInferenceService`
using the model [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b)
in the `demo-llm` namespace
with a `40G` persistent volume claim (to avoid downloading the model multiple times)

```sh
until oc apply -k demo/llm-d; do : ; done
```

## Send an HTTP request with the OpenAI API

```sh
# wait for the llm inference service to be available
oc get llminferenceservice -n demo-llm
```

Test with curl

```sh
INFERENCE_URL=$(
  oc -n openshift-ingress get gateway openshift-ai-inference \
    -o jsonpath='{.status.addresses[0].value}'
)

LLM=openai/gpt-oss-20b
LLM_SVC=${LLM##*/}

PROMPT="Explain the difference between supervised and unsupervised learning in machine learning. Include examples of algorithms used in each type."

llm_post_data(){
cat <<JSON
{
  "model": "${LLM}",
  "prompt": "${PROMPT}",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_p": 0.9
}
JSON
}

curl -s -X POST http://${INFERENCE_URL}/demo-llm/${LLM_SVC}/v1/completions \
  -H "Content-Type: application/json" \
  -d "$(llm_post_data)" | jq .choices[0].text
```

## Additional Info

- [Local Notes](docs/NOTES.md)
- [Deploying a model by using the Distributed Inference Server with llm-d](https://access.redhat.com/articles/7131048)
- [LLM-D: GPU-Accelerated Cache-Aware LLM Inference](https://github.com/cnuland/hello-chris-llm-d)
- [Demystifying Inferencing at Scale with LLM-D on Red Hat Openshift on IBM Cloud](https://community.ibm.com/community/user/blogs/tyler-lisowski/2025/05/30/ai-demystifying-llmd)
- [OAI Release Notes - 2.25](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.25/html-single/release_notes/index#developer-preview-features_relnotes)
- [OAI Distributed Inference - 2.25](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.25/html/deploying_models/deploying_models_on_the_single_model_serving_platform#deploying-models-using-distributed-inference_rhoai-user)
- [guideLLM](https://github.com/vllm-project/guidellm)
