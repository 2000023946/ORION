#!/bin/bash

set -e

echo "🧪 Testing MCP DAG API..."

curl -s -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "find user orders and profile"
  }' | jq

echo ""
echo "✅ Done"