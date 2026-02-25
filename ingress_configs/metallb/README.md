# MetalLB + Gateway API for llm-d Inference Gateway

This configuration installs the **MetalLB Operator** to provide external LoadBalancer IPs on bare-metal or on-premises OpenShift clusters, then uses **Gateway API** (GatewayClass + Gateway + HTTPRoute) to route traffic to the **llm-d inference gateway** (OpenAI-compatible endpoint for distributed vLLM via KServe).

MetalLB assigns stable external IPs to services of type LoadBalancer, while Gateway API delivers Kubernetes-native L7 routing, traffic splitting, and HTTP/2 support — ideal for low-latency, high-throughput LLM inference with streaming responses.

**Why Use MetalLB + Gateway API for llm-d?**

- Low overhead and near-bare-metal performance for TTFT and TPS
- Native Kubernetes API (Gateway API is the future of ingress in OpenShift)
- Stable external IPs without cloud provider dependency
- Supports HTTP/2 streaming, path/host routing, and integration with KServe/llm-d gateway
- Excellent for production scale in bare-metal environments (e.g., with GuideLLM benchmarks)

**Trade-offs**  
Requires Gateway API CRDs (enabled in OpenShift 4.14+), MetalLB setup, and network config for IP reachability. Simpler than Avi but more manual than native Routes.

## Prerequisites

- OpenShift 4.14+ (Gateway API GA in 4.14+; MetalLB Operator available)
- Bare-metal/on-premises cluster (no cloud LB)
- llm-d deployed (InferenceService + gateway in e.g. `llm-demo` namespace)
- Gateway API CRDs installed (`oc explain GatewayClass` should work)
- Free IP range in your network for MetalLB pools (e.g., 192.168.100.240-192.168.100.250)
- Cluster-admin access; `oc` CLI logged in
- Nodes on L2-reachable subnet for ARP (Layer 2 mode) or BGP peers configured

## Files in this Directory

Apply these files **separately** in order for a clean setup:

1. `metallb-namespace.yaml`  
   Creates the `metallb-system` namespace (if not using `openshift-operators`).

2. `metallb-subscription.yaml`  
   Subscribes to the MetalLB Operator from `redhat-operators` catalog.

3. `metallb-instance.yaml`  
   Deploys the MetalLB controller + speaker via `MetalLB` CR.

4. `ipaddresspool.yaml`  
   Defines an IP pool for LoadBalancer services (e.g., for llm-d gateway).

5. `l2advertisement.yaml`  
   Advertises the pool using Layer 2 mode (ARP/NDP) — most common for simple setups.

6. `gatewayclass.yaml` (optional)  
   Defines a GatewayClass (references MetalLB or uses default if Istio/Contour/etc.).

7. `gateway.yaml`  
   Deploys a Gateway instance (LoadBalancer type, backed by MetalLB).

8. `httproute-llmd.yaml`  
   Routes traffic to the llm-d gateway service via HTTPRoute.

9. `kustomization.yaml` (optional)  
   Kustomize overlay to apply everything at once (`oc apply -k .`).

## Quick Deploy Steps

1. **Install MetalLB Operator** (if not already installed)

   ```bash
   oc apply -f metallb-namespace.yaml
   oc apply -f metallb-subscription.yaml
   ```

Wait for CSV/InstallPlan:

```sh
oc get clusterserviceversion -n metallb-system
oc get installplan -n metallb-system
```

1. **Deploy MetalLB Instance**

```sh
oc apply -f metallb-instance.yaml -n metallb-system
```

Verify pods: oc get deployment controller -n metallb-system and oc get daemonset speaker -n metallb-system.

2. **Configure IP Pool and Advertisement (Layer 2 example)**

```sh
oc apply -f ipaddresspool.yaml -n metallb-system
oc apply -f l2advertisement.yaml -n metallb-system
```

3. Deploy Gateway API Resources (for L7 routing)

```sh
oc apply -f gatewayclass.yaml -n llm-demo   # optional if using existing class
oc apply -f gateway.yaml -n llm-demo
oc apply -f httproute-llmd.yaml -n llm-demo
```

4. **Verify & Test**

Get external IP: `oc get svc <gateway-name> -n llm-demo -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
Check Gateway status: `oc get gateway -n llm-demo`

Test endpoint:

```sh
curl http://<external-ip>/v1/models
# or chat completions
curl http://<external-ip>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "your-model", "messages": [{"role": "user", "content": "Hello!"}]}'
```