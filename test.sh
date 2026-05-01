#!/usr/bin/env bash
set -euo pipefail

curl -f http://localhost:8000/health
echo

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Research latest AI agent deployment patterns"}'
echo
