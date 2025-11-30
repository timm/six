---
date: November 29, 2025
footer: 1.0
header: User Commands
section: 1
title: TWO.LUA
---

# NAME

two.lua - stochastic incremental Explainable AI (XAI) tool

# SYNOPSIS

**./two.lua** \[*OPTIONS*\] \[*COMMANDS*\]

# DESCRIPTION

**two.lua** is a Lua script that implements a stochastic incremental
Explainable AI (XAI) algorithm. It processes data from CSV files to
cluster data into \"best\" and \"rest\" sets, calculates distances
between rows using weighted Euclidean distance (for attributes) or
normalized distance to goals (for class variables), and incrementally
updates a model.

The script handles both numeric and symbolic data types, supports
normalization, and includes a test suite for demonstrating various
internal statistical functions.

# OPTIONS

These options configure the hyperparameters and inputs for the
algorithm. They must be provided as key-value pairs or flags.

**-h**

:   Show the help message and exit.

**-b** *bins*

:   Set the number of bins for discretization.

    Default: 7

**-e** *era*

:   Set the frequency (number of rows) at which the model updates.

    Default: 30

**-f** *file*

:   Specify the path to the input CSV file. The file should contain a
    header row. Columns starting with uppercase letters are treated as
    Numerics, others as Symbols. Columns ending in \'+\' or \'-\' are
    treated as optimization goals (maximize/minimize). Columns ending in
    \'X\' are ignored.

    Default: ../lua6/auto93.csv

**-r** *ruleMax*

:   Set the maximum number of conditions allowed in a rule.

    Default: 3

**-s** *seed*

:   Set the random number generator seed for reproducibility.

    Default: 42

# COMMANDS

The script includes several built-in test hooks and execution modes.
These arguments trigger specific functions within the script.

**\--csv**

:   Read the input file defined by **-f** and print every parsed row to
    standard output.

**\--cut**

:   Demonstrate the list splitting (cutting) function.

**\--data**

:   Load the data file and display summary statistics for the
    independent variables (X columns).

**\--distx**

:   Calculate and display distance statistics between rows based on
    independent variables (X).

**\--disty**

:   Calculate and display distance statistics based on dependent
    optimization goals (Y).

**\--inc**

:   Demonstrate incremental data updates (adding and removing rows from
    the statistical model).

**\--mode**

:   Demonstrate the mode (most frequent item) calculation.

**\--num**

:   Demonstrate Gaussian random number generation and summary statistics
    (mean, standard deviation).

**\--shuffle**

:   Demonstrate the array shuffling function.

**\--the**

:   Print the current configuration settings (the \`the\` table).

**\--two**

:   Run the main stochastic incremental XAI clustering algorithm. This
    splits the data into training/testing sets, performs clustering, and
    outputs model performance metrics.

# EXAMPLES

**Run the main XAI algorithm with default settings:**

        ./two.lua --two

**Process a custom dataset with a specific random seed:**

        ./two.lua -f data/weather.csv -s 101 --two

**Inspect the columns of a dataset:**

        ./two.lua -f ../lua6/auto93.csv --data

# EXIT STATUS

Returns 0 on successful execution.

# AUTHOR

Tim Menzies (timm@ieee.org)

# LICENSE

MIT License (mit-license.org)

# COPYRIGHT

Copyright (c) 2025 Tim Menzies.
