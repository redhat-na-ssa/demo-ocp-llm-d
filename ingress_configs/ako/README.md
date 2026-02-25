# Avi Kubernetes Operator (AKO) for llm-d Inference Gateway

This configuration deploys and configures the **Avi Kubernetes Operator (AKO)** to provide advanced Layer 4/7 load balancing for the **llm-d inference gateway** (the OpenAI-compatible endpoint for distributed vLLM serving via KServe) using VMware/Broadcom Avi Load Balancer.

AKO creates Avi Virtual Services (with VIPs) in front of the llm-d gateway service, offering enterprise features like WAF, analytics, connection multiplexing, auto-FQDN, and high-throughput support for streaming inference responses — without requiring MetalLB.

**Why Use Avi AKO for llm-d?**

- Sophisticated L7 routing, security, and observability for production AI workloads
- No dependency on OpenShift Routes or MetalLB
- Excellent for high-RPS, low-latency inference with bidirectional streaming
- Integrates seamlessly with Avi Controller for centralized management

**Trade-offs**  
Higher complexity and dependency on an external Avi Controller compared to native OpenShift Route or NodePort. Best for environments already using Avi or needing advanced L7 capabilities.

## Prerequisites

- Existing **Avi Load Balancer Controller** (v18.2.10+ or later) with:
  - Configured Cloud (e.g., vCenter, NSX-T, No-Access)
  - IPAM Profile and subnet for VIP allocation
  - Service Engine Group (SEG) for this cluster
- OpenShift 4.10+ cluster with llm-d deployed (InferenceService + gateway in e.g. `llm-demo` namespace)
- Helm 3+ installed
- Network reachability: Avi SEs must reach OpenShift node IPs/CIDRs
- Avi Controller credentials (username/password or cert)

## Files in this Directory

Apply these files **separately** in the order below for a clean, modular setup:

1. `namespace.yaml`  
   Creates the dedicated namespace for AKO (`avi-system` recommended).

2. `avi-secret.yaml` (template)  
   Secret for Avi Controller authentication (username/password or cert-based). Customize before applying.

3. `ako-values.yaml`  
   Helm values file for AKO installation/upgrade. Customize clusterName, controllerHost, network settings, etc.

4. `llmd-gateway-lb-service.yaml`  
   Wrapper Service of type LoadBalancer (annotated for AKO) to expose the existing llm-d gateway pods. AKO syncs this to an Avi Virtual Service.

5. `llmd-gateway-ingress.yaml` (optional)  
   Kubernetes Ingress resource for L7 hostname/path-based routing (if preferred over LoadBalancer service).

6. `kustomization.yaml` (optional)  
   Kustomize overlay to apply all configs at once (e.g., `oc apply -k .`).

## Quick Deploy Steps

1. **Apply Namespace** (if not already created)

   ```bash
   oc apply -f namespace.yaml
   ```

2. **Create Avi Credentials Secret**

Edit avi-secret.yaml with your real credentials, then:

```sh
oc apply -f avi-secret.yaml -n avi-system
```

3. **Customize and Install/Upgrade AKO via Helm**

Edit ako-values.yaml (key fields: controllerHost, cloudName, nodeNetworkList CIDRs, clusterName). Then:Bash

```sh
helm repo add ako https://projects.packages.broadcom.com/ako/helm-charts
helm repo update

helm upgrade --install ako-release oci://projects.packages.broadcom.com/ako/helm-charts/ako \
  --version 1.13.4 \  # Use latest stable version
  -f ako-values.yaml \
  --namespace avi-system \
  --create-namespace
```

Wait for AKO pods to be ready: oc get pods -n avi-system.

4. **Expose llm-d Gateway**

Choose one (or both):

Via LoadBalancer Service (simplest, L4/L7 auto):

```sh
oc apply -f llmd-gateway-lb-service.yaml -n llm-demo
```

Via Ingress (for explicit hostname routing):

```sh
oc apply -f llmd-gateway-ingress.yaml -n llm-demo
```

5. **Verify & Test**

- AKO logs: oc logs -n avi-system -l app=ako-operator
- Avi Virtual Service: Check Avi Controller UI (Infrastructure → Virtual Services)
- Get VIP: oc get svc llmd-gateway-lb -n llm-demo -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

Test endpoint:

```sh
curl http://<VIP>/v1/models
# or chat completions
curl http://<VIP>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "your-model", "messages": [{"role": "user", "content": "Hello!"}]}'
```

Use the VIP as --target in GuideLLM benchmarks.