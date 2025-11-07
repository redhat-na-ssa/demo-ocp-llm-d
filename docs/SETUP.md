# Additional Prerequisites

### OpenShift 4.19+

> [!NOTE]
> The [Gateway API dependencies](gitops/ocp-4.18/prereqs/gateway-api.yaml) are part of OpenShift 4.19+

See [ocp-4.19](gitops/ocp-4.19) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.19; do : ; done
```

### OpenShift 4.18 (Alternative)

> **⚠️ Disclaimer**: This configuration is not officially supported and is provided for experimental/development
> purposes only.

See [ocp-4.18](gitops/ocp-4.18) for installation of `llm-d` dependencies

```sh
until oc apply -k gitops/ocp-4.18; do : ; done
```

### Bare Metal Dependencies (YOLO)

The `MetalLB` operator, and a working configuration, is needed to [use `gatewayAPI` in OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/ingress_and_load_balancing/configuring-ingress-cluster-traffic#ingress-gateway-api).

Install `MetalLB` operator

```sh
oc apply -k demo/bare-metal
```

[Basic BGP / L2 examples](gitops/instance/metallb-operator/) (requires modification)
