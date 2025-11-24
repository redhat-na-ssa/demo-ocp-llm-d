# KV Awareness Check

```bash
oc get llminferenceservice

>> NAME   URL                                                                                            READY   REASON   AGE
>> qwen   http://a9e365716cefb444383f9247d2d3c4ae-2070748035.us-east-2.elb.amazonaws.com/demo-llm/qwen   True             35m

oc get pods

>> NAME                                            READY   STATUS    RESTARTS   AGE
>> qwen-kserve-c5d769949-b9nxx                     1/1     Running   0          34m
>> qwen-kserve-c5d769949-gl8sp                     1/1     Running   0          34m
>> qwen-kserve-c5d769949-p4tkg                     1/1     Running   0          34m
>> qwen-kserve-c5d769949-pfpd2                     1/1     Running   0          34m
>> qwen-kserve-router-scheduler-665878574d-q7r2s   1/1     Running   0          34m

oc get gateways -A

>> NAMESPACE           NAME                     CLASS               ADDRESS                                                                   PROGRAMMED   AGE
>> openshift-ingress   openshift-ai-inference   openshift-default   a9e365716cefb444383f9247d2d3c4ae-2070748035.us-east-2.elb.amazonaws.com   True         10d
```

- confirm the service is running:

```bash
curl -X GET http://a9e365716cefb444383f9247d2d3c4ae-2070748035.us-east-2.elb.amazonaws.com/demo-llm/qwen/v1/models

>> {"data":[{"created":1763690665,"id":"Qwen/Qwen3-4B","max_model_len":40960,"object":"model","owned_by":"vllm","parent":null,"permission":[{"allow_create_engine":false,"allow_fine_tuning":false,"allow_logprobs":true,"allow_sampling":true,"allow_search_indices":false,"allow_view":true,"created":1763690665,"group":null,"id":"modelperm-b12f363756d54150bd162f463d6ce6c9","is_blocking":false,"object":"model_permission","organization":"*"}],"root":"/mnt/models"}],"object":"list"}%    
```

- send a request (multiple times)

```bash
curl -X POST http://a9e365716cefb444383f9247d2d3c4ae-2070748035.us-east-2.elb.amazonaws.com/demo-llm/qwen/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-4B",
    "prompt": "The history of technological progress is a story of curiosity turned into capability. From the invention of writing to the rise of digital networks, each leap has expanded humanity’s collective memory. Artificial intelligence represents the next chapter, where thought itself becomes computable. Describe how collaboration between humans and intelligent systems might reshape creativity, productivity, and understanding in the next two decades, focusing on both the opportunities and the risks that emerge from shared cognition.",
    "max_tokens": 200,
    "temperature": 0.7
  }'
```

- we can see the request is routed to the same pod multiple times b/c of KV-cache affinity

```bash
oc logs -f qwen-kserve-router-scheduler-665878574d-q7r2s | grep -v "Level(-4)"

{"level":"Level(-2)","ts":"2025-11-21T01:46:00Z","caller":"requestcontrol/director.go:251","msg":"Request handled","x-request-id":"b43b7ccd-c87a-4f52-8ebe-717b5dcc48ad","model":"Qwen/Qwen3-4B","resolvedTargetModel":"Qwen/Qwen3-4B","criticality":"Critical","model":"Qwen/Qwen3-4B","targetModel":"Qwen/Qwen3-4B","endpoint":"{NamespacedName:demo-llm/qwen-kserve-c5d769949-p4tkg Address:10.129.2.21 Labels:map[app.kubernetes.io/component:llminferenceservice-workload app.kubernetes.io/name:qwen app.kubernetes.io/part-of:llminferenceservice kserve.io/component:workload llm-d.ai/role:both pod-template-hash:c5d769949]}"}
{"level":"Level(-3)","ts":"2025-11-21T01:46:05Z","caller":"handlers/response.go:52","msg":"Response generated","x-request-id":"b43b7ccd-c87a-4f52-8ebe-717b5dcc48ad","usage":{"prompt_tokens":85,"completion_tokens":200,"total_tokens":285}}
{"level":"Level(-2)","ts":"2025-11-21T01:51:46Z","caller":"requestcontrol/director.go:251","msg":"Request handled","x-request-id":"af171065-8f4f-4d73-941c-e5747f31ffc5","model":"Qwen/Qwen3-4B","resolvedTargetModel":"Qwen/Qwen3-4B","criticality":"Critical","model":"Qwen/Qwen3-4B","targetModel":"Qwen/Qwen3-4B","endpoint":"{NamespacedName:demo-llm/qwen-kserve-c5d769949-p4tkg Address:10.129.2.21 Labels:map[app.kubernetes.io/component:llminferenceservice-workload app.kubernetes.io/name:qwen app.kubernetes.io/part-of:llminferenceservice kserve.io/component:workload llm-d.ai/role:both pod-template-hash:c5d769949]}"}
{"level":"Level(-3)","ts":"2025-11-21T01:51:51Z","caller":"handlers/response.go:52","msg":"Response generated","x-request-id":"af171065-8f4f-4d73-941c-e5747f31ffc5","usage":{"prompt_tokens":85,"completion_tokens":200,"total_tokens":285}}
{"level":"Level(-2)","ts":"2025-11-21T01:58:00Z","caller":"requestcontrol/director.go:251","msg":"Request handled","x-request-id":"4d8753bc-0b35-423e-8859-3099c4ccba88","model":"Qwen/Qwen3-4B","resolvedTargetModel":"Qwen/Qwen3-4B","criticality":"Critical","model":"Qwen/Qwen3-4B","targetModel":"Qwen/Qwen3-4B","endpoint":"{NamespacedName:demo-llm/qwen-kserve-c5d769949-p4tkg Address:10.129.2.21 Labels:map[app.kubernetes.io/component:llminferenceservice-workload app.kubernetes.io/name:qwen app.kubernetes.io/part-of:llminferenceservice kserve.io/component:workload llm-d.ai/role:both pod-template-hash:c5d769949]}"}
{"level":"Level(-3)","ts":"2025-11-21T01:58:05Z","caller":"handlers/response.go:52","msg":"Response generated","x-request-id":"4d8753bc-0b35-423e-8859-3099c4ccba88","usage":{"prompt_tokens":85,"completion_tokens":200,"total_tokens":285}}
Th{"level":"Level(-2)","ts":"2025-11-21T02:05:03Z","caller":"requestcontrol/director.go:251","msg":"Request handled","x-request-id":"ab95b4d9-9df4-40c4-a2eb-ec7c4bd97f2f","model":"Qwen/Qwen3-4B","resolvedTargetModel":"Qwen/Qwen3-4B","criticality":"Critical","model":"Qwen/Qwen3-4B","targetModel":"Qwen/Qwen3-4B","endpoint":"{NamespacedName:demo-llm/qwen-kserve-c5d769949-p4tkg Address:10.129.2.21 Labels:map[app.kubernetes.io/component:llminferenceservice-workload app.kubernetes.io/name:qwen app.kubernetes.io/part-of:llminferenceservice kserve.io/component:workload llm-d.ai/role:both pod-template-hash:c5d769949]}"}
{"level":"Level(-3)","ts":"2025-11-21T02:05:07Z","caller":"handlers/response.go:52","msg":"Response generated","x-request-id":"ab95b4d9-9df4-40c4-a2eb-ec7c4bd97f2f","usage":{"prompt_tokens":85,"completion_tokens":200,"total_tokens":285}}
```

