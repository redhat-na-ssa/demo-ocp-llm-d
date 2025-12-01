#!/bin/bash

TARGET=http://a970653680479411ea2687bb74860cd4-328874611.us-east-2.elb.amazonaws.com/demo-llm/qwen-pd
MODEL=Qwen/Qwen3-0.6B
SCENARIO_NAME="llm-d-pd"

# List of pairs: rate and corresponding data file
BENCHMARKS=(
  "10 heterogeneous-10.csv"
  "25 heterogeneous-25.csv"
  "50 heterogeneous-50.csv"
  "100 heterogeneous-100.csv"
)

# Loop through the list and run guidellm benchmark for each pair
for benchmark in "${BENCHMARKS[@]}"; do
  RATE=$(echo $benchmark | awk '{print $1}')
  DATA=$(echo $benchmark | awk '{print $2}')
  
  echo "Running benchmark with rate=$RATE and data=$DATA"
  guidellm benchmark run \
    --target $TARGET \
    --model $MODEL \
    --data $DATA \
    --rate-type concurrent \
    --rate $RATE \
    --max-requests $((RATE * 10)) \
    --output-path $SCENARIO_NAME-$RATE.json
done


# Tar all the JSON output files
echo "Creating tar archive of benchmark results..."
tar -cf $SCENARIO_NAME.tar $SCENARIO_NAME-*.json
echo "Archive created: $SCENARIO_NAME.tar"
