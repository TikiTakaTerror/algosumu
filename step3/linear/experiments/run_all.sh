#!/bin/bash

mkdir -p results
rm -f results/*.csv

echo "Running small valid inputs..."
python3 parsers/method1_experiment.py < inputs/01_valid_small.txt > results/01_valid_small_method1.csv
python3 parsers/method2_experiment.py < inputs/01_valid_small.txt > results/01_valid_small_method2.csv

echo "Running small invalid inputs..."
python3 parsers/method1_experiment.py < inputs/01_invalid_small.txt > results/01_invalid_small_method1.csv
python3 parsers/method2_experiment.py < inputs/01_invalid_small.txt > results/01_invalid_small_method2.csv

echo "Running runtime scaling..."
python3 parsers/method1_experiment.py < inputs/02_runtime_scaling.txt > results/02_runtime_scaling_method1.csv
python3 parsers/method2_experiment.py < inputs/02_runtime_scaling.txt > results/02_runtime_scaling_method2.csv

echo "Done. Results are in results/"
