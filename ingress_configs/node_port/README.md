# Direct NodePort Exposure of llm-d Inference Gateway

This configuration exposes the **llm-d inference gateway** (the OpenAI-compatible endpoint for distributed vLLM serving via KServe) directly using a Kubernetes **NodePort** Service.  

It provides the shortest possible network path with near-zero added latency and overhead — ideal for development, low-level performance baselining (e.g., with GuideLLM), and quick testing on bare-metal or on-premises OpenShift clusters.  

**Note:** This is **not** recommended for production due to missing external load balancing, high availability, automatic failover, and security features (e.g., no built-in TLS).

## Why Use NodePort for llm-d?

- Minimal hops → lowest possible latency for TTFT and token streaming
- No additional operators or ingress controllers required
- Direct access to gateway pods via node IPs + high ports (30000–32767)
- Excellent for benchmarking raw performance before adding MetalLB, Avi, or Routes
- Useful when fronting with an external hardware LB or for isolated test environments

**Trade-offs**  
Compared to Route or Gateway API: No DNS-friendly hostnames, no automatic TLS, no built-in balancing across nodes, and security exposure of high ports on all nodes.

## Prerequisites

- OpenShift 4.10+ cluster (NodePort is standard Kubernetes)
- llm-d deployed (via Helm / OpenShift AI) with InferenceService and gateway pods running
- The llm-d gateway service or pods exist (typically with labels like `component=gateway` or `app.kubernetes.io/component: gateway`)
- Namespace where llm-d is installed (e.g., `llm-demo`)
- Firewall rules allowing traffic to the chosen NodePort on worker node IPs

## Files in this Directory

- `nodeport-service.yaml`  
  Main Kubernetes Service manifest of type NodePort targeting the llm-d gateway pods.

- `kustomization.yaml` (optional)  
  Kustomize overlay for easy application and customization.

## Quick Deploy

1. **Identify the llm-d gateway selector**  
   Find the correct labels for the gateway pods/service:

   ```bash
   oc get svc -n <your-namespace> | grep -i gateway
   # or
   oc get pods -n <your-namespace> -l component=gateway --show-labels
   # Common labels: component=gateway, app.kubernetes.io/component: gateway,
   # serving.kserve.io/inferenceservice=<your-isvc-name>
   ```

2. **Review and customize nodeport-service.yaml**

    Update namespace, selector labels, port numbers (confirm with oc describe svc <gateway-svc>), and optional fixed nodePort.

3. **Apply the NodePort Service**

```sh
oc apply -f nodeport-service.yaml -n <your-namespace>
```

Or with Kustomize:

```sh
oc apply -k . -n <your-namespace>
```

4. **Get Access DetailsBash**

```sh
oc get svc llm-d-gateway-nodeport -n <your-namespace> -o wide
oc get nodes -o wide   # Note EXTERNAL-IP or INTERNAL-IP of worker nodes
```

Access URL example: http://<any-worker-node-ip>:30080

5. **Test the endpoint**

```sh
curl http://<node-ip>:30080/v1/models
# or OpenAI-compatible chat completions
curl http://<node-ip>:30080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

Use this as the --target for GuideLLM benchmarks.

Example: nodeport-service.yaml (Typical Content)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: llm-d-gateway-nodeport
  namespace: llm-demo
spec:
  type: NodePort
  externalTrafficPolicy: Local          # Recommended: preserves source IP, lower latency
  selector:
    component: gateway                  # Adjust to match your gateway pods' labels
    # OR more precise:
    # serving.kserve.io/inferenceservice: my-llm
    # component: gateway
  ports:
    - name: http
      protocol: TCP
      port: 8000                        # Common vLLM/OpenAI port; confirm via oc describe
      targetPort: 8000                  # Port exposed on gateway pods
      nodePort: 30080                   # Optional: fixed port (30000-32767); auto-allocates if omitted
```