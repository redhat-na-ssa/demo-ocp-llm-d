# OpenShift Route for llm-d Inference Gateway

This configuration exposes the **llm-d inference gateway** (the OpenAI-compatible endpoint for distributed vLLM serving via KServe) using a native **OpenShift Route**.  

This is one of the simplest and most production-ready ways to provide external HTTP/HTTPS access in an OpenShift cluster — especially when you want built-in TLS termination, hostname-based routing, and integration with the OpenShift ingress controller (HAProxy-based).

## Why Use Route for llm-d?

- Built-in to OpenShift (no extra operators like MetalLB or Avi needed)
- Automatic edge TLS termination (or re-encrypt/passthrough modes)
- Path/host-based routing support
- Works seamlessly with KServe InferenceService and llm-d's gateway (Envoy/Istio proxy)
- Good for moderate-to-high throughput inference workloads with streaming responses
- Minimal added latency compared to more complex LBs

**Trade-offs**  
Compared to Gateway API + MetalLB: Slightly higher overhead under extreme load due to HAProxy proxying, but easier to manage and more "OpenShift-native".

## Prerequisites

- OpenShift 4.10+ cluster (Routes are GA)
- llm-d deployed via Helm / OpenShift AI (with InferenceService and gateway pods running)
- The llm-d gateway service exists (typically named something like `inference-gateway`, `llmd-gateway`, or `*-gateway-istio`)
- Namespace where llm-d is installed (e.g., `llm-demo`)

## Files in this Directory

- `route.yaml`  
  Main OpenShift Route manifest exposing the llm-d gateway service over HTTPS with edge TLS termination.

- `httproute-optional.yaml` (optional)  
  Example Gateway API HTTPRoute if you want to layer Gateway API semantics in front (requires Gateway API CRDs and controller enabled).

- `kustomization.yaml` (optional)  
  Kustomize overlay to apply all configs easily.

## Quick Deploy

1. **Review and customize `route.yaml`**  
   Update:
   - `namespace`
   - `host` (your desired DNS name, e.g. `llmd-gateway.apps.<cluster-domain>`)
   - `to` → service name/port (match your llm-d gateway service, usually port 80 or 8000)
   - TLS settings if needed (edge is default)

2. **Apply the Route**

   ```bash
   oc apply -f route.yaml -n <your-namespace>
   ```

3. **Get the Route URL**

   ```sh
   oc get route llmd-gateway-route -n <your-namespace> -o jsonpath='{.spec.host}'
   ```

4. **Test the endpoint**

   ```sh
   curl -k https://<route-host>/v1/models
# or OpenAI-compatible chat completions
curl https://<route-host>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
  ```