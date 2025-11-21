#!/bin/bash

python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 100 --chunk-size 20 --output-guidellm-csv "prompts-10.csv"
python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 250 --chunk-size 50 --output-guidellm-csv "prompts-25.csv"
python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 500 --chunk-size 100 --output-guidellm-csv "prompts-50.csv"
python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 1000 --chunk-size 200 --output-guidellm-csv "prompts-100.csv"
python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 5000 --chunk-size 500 --output-guidellm-csv "prompts-250.csv"
python test-data-generator.py --target-prefix-words 5000 --target-continuation-words 1000 --num-pairs 10000 --chunk-size 1000 --output-guidellm-csv "prompts-500.csv"