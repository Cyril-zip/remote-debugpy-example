#!/bin/bash
kubectl patch deployment fast-api-deployment -n example --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args",
    "value": ["python3 -m debugpy --listen 127.0.0.1:5678 --wait-for-client --log-to ./debugpy_logs -m uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 5000"]
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/command",
    "value": [
      "/bin/sh",
      "-c"
    ]
  }
]'

kubectl patch deployment fast-api-deployment -n example --type='json' -p='[
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/livenessProbe"
  },
]'


# kubectl patch deployment fast-api-deployment -n example --type='json' -p='[
#   {
#     "op": "add",
#     "path": "/spec/template/spec/containers/0/args",
#     "value": [
#       "infinity"
#     ]
#   },
#   {
#     "op": "add",
#     "path": "/spec/template/spec/containers/0/command",
#     "value": [
#       "sleep"
#     ]
#   }
# ]'
