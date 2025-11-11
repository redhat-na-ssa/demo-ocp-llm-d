# llm-d monitoring Notes

This deploys:

- Prometheus for metrics collection and alerting
- Grafana for visualization with pre-configured LLM performance dashboard
- Auto-discovery of vLLM pods (no manual annotation required)

#### Access Grafana

```sh
# Get the Grafana route URL
oc get route grafana -n llm-d-monitoring -o jsonpath='{.spec.host}'
```

Default credentials (edit):

- Username: `admin`
- Password: `admin`

The LLM Performance dashboard will automatically display metrics from all vLLM pods.

#### Uninstall Monitoring

```sh
oc delete -k gitops/instance/llm-d-monitoring
```
