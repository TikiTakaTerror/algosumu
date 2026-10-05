Step 2 experiments

The original Step 1 submissions are kept unchanged in s1.

The experiments folder contains the input files and parser versions used for the
Step 2 experiments. These use the same parsing algorithms as Step 1, with timing
and output added for collecting the experimental results.

Go to the experiments folder and run:

./run_all.sh

To create the plots:

python3 make_plots.py

The CSV results are saved in results/ and the figures are saved in plots/.