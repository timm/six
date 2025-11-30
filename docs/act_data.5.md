---
date: November 29, 2025
footer: 1.0
header: File Formats
section: 5
title: TWO_DATA
---

# NAME

two_data - input CSV format for the two.lua XAI tool

# DESCRIPTION

The **two.lua** script processes data stored in comma-separated value
(CSV) files. The format relies heavily on a structured header row to
define variable types, optimization goals, and ignored columns.

The file must be plain text, with rows separated by newlines and columns
separated by commas.

# HEADER SYNTAX

The first row of the file is crucial. It defines the schema. The naming
convention of the column headers tells the script how to treat the data
in that column.

## Data Types

**Uppercase Start (e.g., *Age*, *Salary*)**

:   Columns where the header name starts with an uppercase letter are
    treated as **NUM** (Numeric). The script will calculate mean and
    standard deviation for these.

**Lowercase Start (e.g., *job*, *race*)**

:   Columns where the header name starts with a lowercase letter are
    treated as **SYM** (Symbolic). The script will calculate mode and
    entropy for these.

## Column Roles

**Suffix \'+\' (e.g., *Class+*, *Acc+*)**

:   Indicates a dependent variable (target) that should be
    **MAXIMIZED**. These columns constitute the \"Y\" (goal) variables.

**Suffix \'-\' (e.g., *Lbs-*, *Cost-*)**

:   Indicates a dependent variable (target) that should be
    **MINIMIZED**. These columns constitute the \"Y\" (goal) variables.

**Suffix \'X\' (e.g., *idX*, *DateX*)**

:   Indicates a column that should be **IGNORED** entirely. These are
    often used for unique identifiers, comments, or raw data not
    suitable for clustering.

**No Suffix**

:   Any column without a \'+\', \'-\', or \'X\' suffix is treated as an
    independent variable (\"X\" variable) used for clustering and
    distance calculations.

# DATA FORMAT

**Numeric Values**

:   Standard integer or floating-point numbers.

**Symbolic Values**

:   String identifiers. Note that the script splits strictly on commas,
    so strings containing commas may cause parsing errors.

**Missing Values**

:   Missing data should be represented by the question mark character
    (**?**). The script contains logic to handle these during distance
    calculations (assumed max distance).

# EXAMPLES

**Example 1: A simple optimization dataset**

In this example:\
- *nameX* is ignored (ends in X).\
- *Age* is numeric independent (starts Upper).\
- *job* is symbolic independent (starts lower).\
- *Salary+* is a numeric goal to maximize.

    nameX,Age,job,Salary+
    1,25,engineer,50000
    2,30,doctor,90000
    3,?,artist,40000

**Example 2: Multi-objective car selection**

In this example:\
- *Clndrs*, *Vol*, *Hp* are numeric inputs.\
- *origin* is a symbolic input.\
- *Lbs-* is a goal to minimize (weight).\
- *Acc+* is a goal to maximize (acceleration).

    Clndrs,Vol,Hp,origin,Lbs-,Acc+
    8,304,193,1,4732,18.5
    8,360,215,1,4615,14
    4,97,52,3,2130,24.6

# SEE ALSO

**two.lua**(1)
