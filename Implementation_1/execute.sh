#!/bin/bash

# Mentioning the OS for reference
echo "Tested on MAC OS"

# Create a virtual environment to avoid package version mismatches
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required Python packages
echo "Installing required packages..."
pip install --upgrade pip
pip install opencv-python scikit-image scikit-learn numpy

# Run the Python code
echo "Running player classification script..."
python3 player_classification.py

# Deactivate the virtual environment
deactivate

# Confirm script completion
echo "Execution completed, output stored in Implementation_1/output"
