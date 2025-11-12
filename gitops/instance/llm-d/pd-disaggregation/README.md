# P/D Disaggregation

>> TODO: document RDMA setup

## Deploy the `LLMInferenceService`

```sh
oc apply -f pd-deployment -n demo-llm
```

- We can see the `vllm` pods and the `router-scheduler` are deployed:

```sh
oc get pods -n demo-llm

>> NAME                                               READY   STATUS     RESTARTS   AGE
>> qwen-pd-kserve-5c656c9f44-n4j78                    2/2     Running    0          2m39s
>> qwen-pd-kserve-prefill-7c4b496d86-9j48g            1/1     Running    0          2m39s
>> qwen-pd-kserve-router-scheduler-7fd9898c8c-qtqf9   1/1     Running    0          2m39s
```

- We can query the model at the gateway's address:

```sh
curl -X POST http://openshift-ai-inference-istio.openshift-ingress.svc.cluster.local/demo-llm/qwen-pd/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-0.6B",
    "prompt": "Explain the difference between supervised and unsupervised learning in machine learning. Include examples of algorithms used in each type.",
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9
  }'
```

## Cleanup

```sh
oc delete llminferenceservice qwen-pd -n demo-llm
```
