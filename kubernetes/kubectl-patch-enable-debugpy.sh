#!/bin/bash
kubectl patch deployment fast-api-deployment -n example --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args",
    "value": [
      "-m",
      "debugpy",
      "--listen",
      "localhost:5678",
      "-m",
      "uvicorn",
      "app.main:app",
      "--host",
      "0.0.0.0",
      "--port",
      "5000",
      "--workers",
      "1"
    ]
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/command",
    "value": [
      "python3"
    ]
  }
]'
