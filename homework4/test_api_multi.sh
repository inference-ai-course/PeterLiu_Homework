#!/bin/bash

# -------------- Config ----------------
BASE_URL="http://127.0.0.1:8000"
LOG_FILE="test_log.txt"
QUERY_LIST=("transformer model" "attention mechanism" "LLMs in NLP" "BERT vs GPT")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Check for jq
if ! command -v jq &> /dev/null; then
    echo "❌ jq is not installed. Please install it to format JSON nicely."
    exit 1
fi

# -------------- Start ----------------
echo "🧪 Running tests at $TIMESTAMP"
echo "📝 Logging to $LOG_FILE"
echo "===========================" > "$LOG_FILE"
echo "Test started at $TIMESTAMP" >> "$LOG_FILE"

# -------------- Test GET / -------------
echo "➡️ Testing GET /"
curl -s -X GET "$BASE_URL/" | jq
echo "" >> "$LOG_FILE"
echo "[GET /]" >> "$LOG_FILE"
curl -s -X GET "$BASE_URL/" >> "$LOG_FILE"
echo -e "\n" >> "$LOG_FILE"

# -------------- Loop over queries -------------
for query in "${QUERY_LIST[@]}"; do
    echo "➡️ Testing POST /search for query: \"$query\""
    START=$(date +%s.%N)
    RESPONSE=$(curl -s -X POST "$BASE_URL/search" \
        -H "Content-Type: application/json" \
        -d "{\"q\": \"$query\"}")
    END=$(date +%s.%N)
    ELAPSED=$(echo "$END - $START" | bc)

    echo "$RESPONSE" | jq
    echo ""

    echo "[POST /search] Query: \"$query\"" >> "$LOG_FILE"
    echo "Time: ${ELAPSED}s" >> "$LOG_FILE"
    echo "$RESPONSE" | jq >> "$LOG_FILE"
    echo -e "\n" >> "$LOG_FILE"
done

echo "✅ All tests completed."
