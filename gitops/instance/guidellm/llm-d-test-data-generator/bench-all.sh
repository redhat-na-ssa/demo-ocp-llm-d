#!/bin/bash

TARGET=http://<gateway-hostname>/<namespace>/<llm-d-instance>
MODEL=openai/gpt-oss-20b

guidellm benchmark --target $TARGET --model $MODEL --data prompts-10.csv --rate-type concurrent --rate 10
guidellm benchmark --target $TARGET --model $MODEL --data prompts-25.csv --rate-type concurrent --rate 25
guidellm benchmark --target $TARGET --model $MODEL --data prompts-50.csv --rate-type concurrent --rate 50
guidellm benchmark --target $TARGET --model $MODEL --data prompts-100.csv --rate-type concurrent --rate 100
guidellm benchmark --target $TARGET --model $MODEL --data prompts-250.csv --rate-type concurrent --rate 250
guidellm benchmark --target $TARGET --model $MODEL --data prompts-500.csv --rate-type concurrent --rate 500
