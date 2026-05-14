#!/bin/bash

# Script chạy Spectral 2 lần:
# 1. Lint paths trước (không resolve) - bắt inline schema
# 2. Lint toàn bộ (có resolve) - validate schemas

set -e  # Exit on error

echo "================================================"
echo "🔍 Step 1: Checking paths for inline schemas..."
echo "================================================"
echo ""

# Lint từng file trong paths/ với ruleset riêng
PATHS_ERROR=0
for file in $(find paths -name "*.yaml" -o -name "*.yml"); do
  echo "Checking $file..."

  # Kiểm tra xem file có chứa inline schema không
  # Pattern: schema: theo sau bởi type: (không có $ref)
  if grep -A 5 'schema:' "$file" | grep -E '^\s+type:\s+(object|array)' > /dev/null; then
    # Kiểm tra xem có $ref không
    if ! grep -A 5 'schema:' "$file" | grep '\$ref:' > /dev/null; then
      echo "  ❌ INLINE SCHEMA FOUND"
      PATHS_ERROR=1
    else
      echo "  ✅ OK (uses \$ref)"
    fi
  else
    echo "  ✅ OK"
  fi
done

echo ""

if [ $PATHS_ERROR -eq 1 ]; then
  echo "❌ Found inline schemas in paths/"
  exit 1
fi

echo "✅ No inline schemas in paths/"
echo ""

echo "================================================"
echo "🔍 Step 2: Validating full OpenAPI document..."
echo "================================================"
echo ""

# Lint toàn bộ document với ruleset chính (tắt rule no-inline-schema)
spectral lint openapi.yaml --ruleset .spectral.yaml

echo ""
echo "✅ All checks passed!"
