# Notes for a Disconnected install

Create `isc.yaml` - edit the copy for your needs

```sh
[ -d scratch ] || mkdir scratch
cp gitops/disconnected/isc*.yaml scratch/

# edit scratch/isc.yaml
```

Create `mapping.txt`

```sh
REGISTRY=registry:5000

# NOTE: replace with 'quay.io' if oc mirror loses its mind
# REGISTRY=quay.io

oc-mirror \
  -c scratch/isc-rhoai.yaml \
  --workspace file:///${PWD}/scratch/oc-mirror \
  docker://"${REGISTRY}" \
  --v2 \
  --dry-run \
  --authfile scratch/pull-secret.txt
```

Create `images.txt` - a list of images to copy

```sh
DATE=$(date +%Y-%m-%d)
sed '
  s@^docker://@@g
  s@=docker://'"${REGISTRY}"'.*@@g
  /localhost/d' \
    scratch/oc-mirror/working-dir/dry-run/mapping.txt \
    > scratch/images-"${DATE}".txt
```
