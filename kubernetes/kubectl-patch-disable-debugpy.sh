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

kubectl patch deployment fast-api-deployment -n example --patch '{
  "spec": {
    "template": {
      "spec": {
        "containers": [
          {
            "name": "fast-api",
            "livenessProbe": {
              "httpGet": {
                "path": "/ping",
                "port": 5000
              },
              "initialDelaySeconds": 5,
              "failureThreshold": 10,
              "periodSeconds": 10
            }
          }
        ]
      }
    }
  }
}'