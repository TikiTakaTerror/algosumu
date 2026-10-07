#!/bin/bash

mkdir -p results
rm -f results/*.csv

echo "Running small valid inputs..."
python3 parsers/method1_experiment.py < inputs/01_valid_small.txt > results/01_valid_small_method1.csv
python3 parsers/method2_experiment.py < inputs/01_valid_small.txt > results/01_valid_small_method2.csv

echo "Running small invalid inputs..."
python3 parsers/method1_experiment.py < inputs/01_invalid_small.txt > results/01_invalid_small_method1.csv
python3 parsers/method2_experiment.py < inputs/01_invalid_small.txt > results/01_invalid_small_method2.csv

echo "Running input-length scaling..."
python3 parsers/method1_experiment.py < inputs/02_runtime_scaling.txt > results/02_runtime_scaling_method1.csv
python3 parsers/method2_experiment.py < inputs/02_runtime_scaling.txt > results/02_runtime_scaling_method2.csv

echo "Running grammar-size scaling..."
for size in 5 10 20 30 40
do
    python3 parsers/method1_experiment.py < inputs/03_grammar_$size.txt | sed "s/^/$size,/" >> results/03_grammar_size_method1.csv
    python3 parsers/method2_experiment.py < inputs/03_grammar_$size.txt | sed "s/^/$size,/" >> results/03_grammar_size_method2.csv
done

echo "Done. Results are in results/"
