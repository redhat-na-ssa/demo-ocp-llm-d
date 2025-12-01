#!/bin/bash

python heterogeneous-workload-generator.py --total-prompts 100 --output-csv "heterogeneous-10.csv"
python heterogeneous-workload-generator.py --total-prompts 250 --output-csv "heterogeneous-25.csv" --start-index 101
python heterogeneous-workload-generator.py --total-prompts 500 --output-csv "heterogeneous-50.csv" --start-index 351
python heterogeneous-workload-generator.py --total-prompts 1000 --output-csv "heterogeneous-100.csv" --start-index 851
