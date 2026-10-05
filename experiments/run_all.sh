#!/bin/bash

mkdir -p results
rm -f results/*.csv

echo "Running repeated parentheses..."
python3 parsers/naive_experiment.py < inputs/01_parentheses_repeated.txt > results/01_parentheses_repeated_naive.csv
python3 parsers/topdown_experiment.py < inputs/01_parentheses_repeated.txt > results/01_parentheses_repeated_topdown.csv
python3 parsers/bottomup_experiment.py < inputs/01_parentheses_repeated.txt > results/01_parentheses_repeated_bottomup.csv

echo "Running nested parentheses..."
python3 parsers/naive_experiment.py < inputs/01_parentheses_nested.txt > results/01_parentheses_nested_naive.csv
python3 parsers/topdown_experiment.py < inputs/01_parentheses_nested.txt > results/01_parentheses_nested_topdown.csv
python3 parsers/bottomup_experiment.py < inputs/01_parentheses_nested.txt > results/01_parentheses_nested_bottomup.csv

echo "Running a at start..."
python3 parsers/naive_experiment.py < inputs/02_start_a.txt > results/02_start_a_naive.csv
python3 parsers/topdown_experiment.py < inputs/02_start_a.txt > results/02_start_a_topdown.csv
python3 parsers/bottomup_experiment.py < inputs/02_start_a.txt > results/02_start_a_bottomup.csv

echo "Running a at end..."
python3 parsers/naive_experiment.py < inputs/02_end_a.txt > results/02_end_a_naive.csv
python3 parsers/topdown_experiment.py < inputs/02_end_a.txt > results/02_end_a_topdown.csv
python3 parsers/bottomup_experiment.py < inputs/02_end_a.txt > results/02_end_a_bottomup.csv

echo "Running runtime scaling..."
python3 parsers/topdown_experiment.py < inputs/03_runtime_scaling.txt > results/03_runtime_scaling_topdown.csv
python3 parsers/bottomup_experiment.py < inputs/03_runtime_scaling.txt > results/03_runtime_scaling_bottomup.csv

echo "Done. Results are in results/"
