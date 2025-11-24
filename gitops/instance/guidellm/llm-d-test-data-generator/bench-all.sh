#!/bin/bash

TARGET=http://<gateway-hostname>/<namespace>/<llm-d-instance>
MODEL=Qwen/Qwen3-4B
SCENARIO_NAME="llm-d-intelligent-inference-x2"
MAX_SECONDS=120

# List of pairs: rate and corresponding data file
BENCHMARKS=(
  "500 prompts-500.csv"
  "250 prompts-250.csv"
  "100 prompts-100.csv"
  "50 prompts-50.csv"
  "25 prompts-25.csv"
  "10 prompts-10.csv"
)

# Loop through the list and run guidellm benchmark for each pair
for benchmark in "${BENCHMARKS[@]}"; do
  RATE=$(echo $benchmark | awk '{print $1}')
  DATA=$(echo $benchmark | awk '{print $2}')
  
  echo "Running benchmark with rate=$RATE and data=$DATA"
  guidellm benchmark run --target $TARGET \
    --model $MODEL \
    --data $DATA \
    --rate-type concurrent \
    --rate $RATE \
    --max-seconds $MAX_SECONDS \
    --output-path $SCENARIO_NAME-$RATE.json
done

# Tar all the JSON output files
echo "Creating tar archive of benchmark results..."
tar -cf $SCENARIO_NAME.tar $SCENARIO_NAME-*.json
echo "Archive created: $SCENARIO_NAME.tar"
