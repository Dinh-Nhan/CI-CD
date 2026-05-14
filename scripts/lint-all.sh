#!/bin/bash

# Script chạy kiểm tra API:
# 1. Check inline schema (Python script)
# 2. Validate với Spectral

echo "================================================"
echo "🔍 Step 1: Checking paths for inline schemas..."
echo "================================================"
echo ""

# Chạy Python script
python3 scripts/check-inline-schema.py

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Inline schema check failed"
  exit 1
fi

echo ""
echo "================================================"
echo "🔍 Step 2: Validating full OpenAPI document..."
echo "================================================"
echo ""

# Lint toàn bộ document với ruleset chính
spectral lint openapi.yaml --ruleset .spectral.yaml

echo ""
echo "✅ All checks passed!"
