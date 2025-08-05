SERVERS=("http://127.0.0.1:8000" "http://127.0.0.1:8001")

for server in "${SERVERS[@]}"; do
  for query in "${QUERY_LIST[@]}"; do
    echo "🔍 [$server] $query"
    curl -s -X POST "$server/search" ...
  done
done
