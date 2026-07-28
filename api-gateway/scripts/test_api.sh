#!/bin/bash

set -e

echo "🧪 Testing MCP DAG API..."

curl -s -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "finhe  phes tht are  apple "
  }' | jq

echo ""
echo "✅ Done"