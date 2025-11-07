# Notes

Copy model files

```sh
oc cp tokenizer_config.json guidellm:/config
oc cp tokenizer.json guidellm:/config
```

Open shell and run guidellm

```sh
oc rsh guidellm
```

```sh
pip install guidellm[recommended]==0.3.1

# vi /tmp/functions
. /tmp/functions

run_guidellm
```

Watch logs for an automated benchmark

```sh
oc logs -f guidellm
```
