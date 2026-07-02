#!/bin/bash

set -e

echo "🧪 Testing MCP DAG API..."

curl -s -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "find the newest iphones "
  }' | jq

echo ""
echo "✅ Done"