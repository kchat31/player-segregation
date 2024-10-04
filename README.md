
# Player Classification Project

## Overview

This repository contains code for classifying badminton players based on images. The project is organized into different implementations, each showcasing distinct approaches to player classification.

## Report

A comprehensive report detailing the ideas, approaches, and implementation methods can be found in the `report.pdf` file.

## Implementation Structure

Each approach to player classification is stored in a separate directory. The structure is as follows:

- **Implementation_1**: Contains the code for the first player classification approach. The folder includes the `execute.sh` script for running the code.

## Output Folder

Upon execution, an output folder will be created inside the corresponding `Implementation_1` directory. This folder will include four subfolders (`player0`, `player1`, `player2`, `player3`), each holding images for a specific player.

## Execution Instructions

**Operating System**:  
The project was developed and tested on **MacOS**.

**Python Version**:  
The project uses the latest version of Python 3.

### How to Run:

To execute the code, navigate to the respective implementation folder (e.g., `Implementation_1`), and run the following command:

```bash
./execute.sh
```

## Shell Script (`execute.sh`)

The shell script performs the following tasks:

1. Installs all required Python dependencies.
2. Runs the player classification code.
3. Creates the output folder and generates four subfolders (`player0`, `player1`, `player2`, `player3`).
4. Saves classified images into the appropriate subfolders.

## Dependencies

All necessary Python packages will be installed automatically by the `execute.sh` script. Alternatively, you can install the required dependencies manually using:

```bash
pip install -r requirements.txt
```

## Resume

My resume is located inside the `Resume` folder.
