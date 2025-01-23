#!/bin/bash
kubectl patch deployment fast-api-deployment -n example --type='json' -p='[
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/args"
  },
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/command"
  }
]'
