#!/bin/bash

# --------- Configuration ---------
BASE_URL="http://127.0.0.1:8000"

# --------- Test GET / -----------
echo "➡️ Testing GET /"
curl -s -X GET "$BASE_URL/" | jq
echo -e "\n"

# --------- Test POST /search -----------
QUERY_TEXT="transformer model"

echo "➡️ Testing POST /search with query: \"$QUERY_TEXT\""
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d "{\"q\": \"$QUERY_TEXT\"}" | jq
echo -e "\n"

echo "✅ All tests completed."
