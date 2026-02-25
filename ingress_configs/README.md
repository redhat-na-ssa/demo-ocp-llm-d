# Ingress Options: Scale & Performance Summary

| Option | Scale (High RPS / Autoscaling) | Performance (Latency / Throughput) | Best Use Case | Overhead Estimate | Support |
|-|-|-|-|-|-|
| **MetalLB + Gateway API** | ★★★★☆ (excellent, native K8s) | ★★★★★ (very low, near bare-metal)  | Production high-scale inference | +??–?? ms TTFT, high TPS | Red Hat |
| **Avi AKO** | ★★★★☆ (strong with multiplexing) | ★★★★☆ (good, but higher overhead due to split model) | Enterprise L7 + security needs | +??–?? ms TTFT, high but capped | VMware, then Red Hat |
| **OpenShift Route** | ★★★☆☆ (moderate, HAProxy limits) | ★★★☆☆ (acceptable, some jitter)   | Quick / moderate-scale production | +??–?? ms TTFT, medium-high TPS | Red Hat |
| **NodePort** | ★★☆☆☆ (poor in production) | ★★★★★ (lowest latency possible) | Testing / baselining only | <?–?? ms added, highest raw TPS | Unsupported |

**Quick Winner by Goal:**

- **Best scale + performance overall**: MetalLB + Gateway API  
- **Best with enterprise features**: Avi AKO  
- **Easiest moderate setup**: OpenShift Route
- **Best raw speed (testing)**: NodePort
