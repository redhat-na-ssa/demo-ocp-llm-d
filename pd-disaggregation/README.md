# P/D Disaggregation

>> TODO: document RDMA setup

## Deploy the `LLMInferenceService`

```bash
oc apply -f pd-deployment -n llm-test
```

- We can see the `vllm` pods and the `router-scheduler` are deployed:

```bash
oc get pods -n llm-test

>> NAME                                               READY   STATUS     RESTARTS   AGE
>> qwen-pd-kserve-5c656c9f44-n4j78                    1/2     Running    0          2m
>> qwen-pd-kserve-prefill-7c4b496d86-9j48g            1/1     Running    0          2m
>> qwen-pd-kserve-router-scheduler-7fd9898c8c-qtqf9   1/1     Running    0          2m
```
