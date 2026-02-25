# Direct NodePort Exposure of llm-d Inference Gateway

Exposes the llm-d Gateway / KServe InferenceService directly via Kubernetes NodePort (ports 30000–32767) on every cluster node. Offers the shortest possible network path with near-zero added latency and overhead, making it useful for development, performance baselining, and low-level testing — but lacks external load balancing, high availability, and production hardening features.

## Procedure:

### Identify the llm-d Gateway Service / Selector

```sh
oc get svc -n <your-namespace> | grep -i gateway
# or
oc get pods -n <your-namespace> -l serving.kserve.io/inferenceservice=<your-isvc-name>,component=gateway  # or app=llm-d-gateway, etc.
```

### Create a NodePort Service YAML

Create this as a separate Service that points to the gateway pods. Save as `llm-d-gateway-nodeport.yaml:YAML`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: llm-d-gateway-nodeport
  namespace: llm-demo  # ← change to your namespace
spec:
  type: NodePort
  selector:
    component: gateway                     # ← adjust to match your gateway pods' labels
    # OR more precisely:
    # serving.kserve.io/inferenceservice: my-llm
    # component: predictor                   # if targeting predictor directly
  ports:
    - name: http
      protocol: TCP
      port: 8000                           # ← common vLLM/OpenAI-compatible port; confirm with oc describe svc <gateway-svc>
      targetPort: 8000                     # port on the gateway pod
      nodePort: 30080                      # ← optional: pick a free port in 30000-32767; if omitted, auto-allocates
```

### apply it

```sh
oc apply -f llm-d-gateway-nodeport.yaml
```

### Verification

```sh
oc get svc llm-d-gateway-nodeport -n llm-demo -o wide
```

Expected output

```sh
NAME                      TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
llm-d-gateway-nodeport    NodePort   172.30.123.45   <none>        8000:30080/TCP   5m    component=gateway
```