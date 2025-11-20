# Walkthrough

Original repo - https://github.com/robertgshaw2-redhat/llm-d-demo

## Install Infra Prereqs

- OpenShift 4.19 - dependencies needed for `llm-d` are shipped in OCP 4.19

## Configure RHOAI to Disable Knative Serving

RHOAI 2.x leverages Knative Serving by default. The following configurations disable Knative.

### `DSCInitialization`

- Set the `serviceMesh.managementState` to removed, as shown in the following example (this requires an admin role):

```yaml
serviceMesh:
    ...
    managementState: Removed
```

- You can do this through the RHOAI UI as shown below:

<details>
<summary>Click to expand</summary>
<img src="images/dsci.png" alt="dsci_ui">
</details>

### `DSC`

- Create a data science cluster (`DSC`) with the following information set in `kserve` and `serving`:

```yaml
spec:
  components:
    kserve:
      defaultDeploymentMode: RawDeployment
      managementState: Managed
      ...
      serving:
          ...
          managementState: Removed
          ...
```

- You can create the `DSC` through the RHOAI UI as shown below, using the `dsc.yaml` provided in this repo:

<details>
<summary>Click to expand</summary>
<img src="images/dsc.png" alt="dsc_ui">
</details>

## Deploy A Gateway

`llm-d` leverages [Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/).

As described in [Getting Started with Gateway API for the Ingress Operator](https://docs.okd.io/latest/networking/ingress_load_balancing/configuring_ingress_cluster_traffic/ingress-gateway-api.html#nw-ingress-gateway-api-enable_ingress-gateway-api), we can can deploy a `GatewayClass` and `Gateway` named
named `openshift-ai-inference` in the `openshift-ingress` namespace:

```sh
oc apply -k gitops/instance/llm-d/gateway
```

We can see the Gateway is deployed:

```sh
oc get gateways -n openshift-ingress

>> NAME                     CLASS   ADDRESS                                                            PROGRAMMED   AGE
>> openshift-ai-inference   istio   openshift-ai-inference-istio.openshift-ingress.svc.cluster.local   True         9d
```

## Deploy the demo-llm namespace

```
oc apply -k gitops/instance/llm-d/namespace
```

## Deploy An LLMService with `llm-d`

With the gateway deployed, we can now deploy an `LLMInferenceService` using KServe, which creates an inference pool of vLLM servers and an end-point-picker (EPP) for smart scheduling across the vLLM servers.

```sh
oc apply -k gitops/instance/llm-d/intelligent-inference/gpt-oss-20b/overlays/modelcar
```

- We can see the `llminferenceservice` is deployed ...

```sh
oc get llminferenceservice -n demo-llm

>> NAME   URL   READY   REASON   AGE
>> gpt-oss-20b         True             9m44s
```

- ... and that the `router-scheduler` and `vllm` pods are ready to go:

```sh
oc get pods -n demo-llm

>> NAME                                            READY   STATUS    RESTARTS   AGE
>> gpt-oss-20b-kserve-c59dbf75-5ztf2                      1/1     Running   0          9m15s
>> gpt-oss-20b-kserve-c59dbf75-dlfj6                      1/1     Running   0          9m15s
>> gpt-oss-20b-kserve-router-scheduler-67dbbfb947-hn7ln   1/1     Running   0          9m15s
```

Send an HTTP request with the OpenAI API:

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

## Cleanup

```sh
oc delete llminferenceservice gpt-oss-20b -n demo-llm
oc delete ns demo-llm
```
