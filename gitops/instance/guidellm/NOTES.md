# Notes

## Disconnected Notes

Copy model files

```sh
oc cp tokenizer_config.json guidellm:/config
oc cp tokenizer.json guidellm:/config
```

Watch logs for an automated benchmark

```sh
oc logs -f guidellm
```

## More Ramblings

Open shell and debug

```sh
oc rsh guidellm
```

You use a python container to install guidellm

```sh
pip install guidellm[recommended]==0.3.1

# vi /tmp/functions
. /tmp/functions

run_guidellm
```
