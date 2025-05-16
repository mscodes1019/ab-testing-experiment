# A/B Testing Experiment with Simulated Datasets
## Overview
This project demonstrates an A/B testing workflow using simulated datasets. It includes data loading, experiment simulation, statistical analysis, and visualization components. The goal is to provide a reusable framework for running A/B tests on user events, with code organized to help you extend or modify the experiment.

The project simulates user behavior over a period of days, assigns users to experimental groups (control and treatment), and tracks quiz completion outcomes to analyze group effects.

# Repository Structure
## A_B test.ipynb
Jupyter notebook that demonstrates the full experiment pipeline — from data loading to analysis and visualization.

## business.py
Contains core business logic, including the StatsBuilder class which runs the experiment and computes statistics like contingency tables.

## database.py
Manages data loading and storage, including reading the CSV dataset and providing data access to the experiment classes.

## display.py
Contains code for displaying results, including interactive Dash callbacks and UI elements.

## dashboard.ipynb and dashboard-Copy1.ipynb
Notebooks for visualization and dashboard exploration.

## mydata/admissions_dataset.csv
The source dataset used to generate simulated user events.

# How to Run the Experiment
Clone this repo and install dependencies (e.g., pandas, plotly, dash).

Load the dataset (admissions_dataset.csv) using the CSVRepository class from database.py.

Use the StatsBuilder class from business.py to run the experiment simulation by calling run_experiment(days, seed).

Generate statistical summaries like contingency tables by calling get_contingency_table() on the repository.

Visualize results either via Jupyter notebooks or with the Dash app in display.py.

# Extending or Modifying
To change the simulation logic (e.g., add new user events or groups), modify the run_experiment method inside StatsBuilder (business.py).

To use your own data, replace admissions_dataset.csv with your CSV file formatted similarly, and update data loading logic if needed.

To add new visualizations or interactive elements, update display.py or create new Jupyter notebooks.

# Dependencies
Python 3.8+

pandas

numpy

plotly

dash
