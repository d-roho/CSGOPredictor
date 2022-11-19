(Add GIF)

# Quick Start Guide

1. Install compatible versions of Python and Java mentioned in Requirements section below
2. run `pip install requirements.txt` to install required packages
3. copy `gamestate_integration_CSGOPredictor.cfg` file to `Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg`

4. run `python MainApp.py` plus any arguments of your choice in command terminal or equivalent from location of this repo

_Optional - run `gui.py` in another terminal while `MainApp.py` is running to display dynamic prediction bar_

**The program will begin making predictions once you begin spectating a match in CS:GO.**

## Requirements
* Python >= 3.5
* Java >= 8 and < 16
* all packages in `requirements.txt`

## Command Line Arguements

* -w = disable Welcome Message
* -p = disable Pause-and-Play functionality
* delay X = delay predictions by X seconds

# CSGOPredictor - An Overview

### ***CSGOPredictor is a python program that generates live round winner predictions of CS:GO Competitive matches.***

## How it works
(diagram)
A simple 3 step process

* When a match is live, *snapshots* of the the round in play, containing large amounts of precise data on round & players' status, are generated & captured using the `gsi_pinger` module through CS:GO's in-built Game State Integration functionality.

* Each snapshot is cleaned and parsed using the `snapshot_parser` module, resulting in the creation of an array of 23 attributes to be used by the predictive model to generate probability predictions. Attributes include:
  * Round Data - `Map`, `Time Left`, `Bomb Plant Status`
  * Player Data - `T/CT Players Alive`, `T/CT Total Health`, `Weapons`, `Utility`

* Finally, `MainApp.py` runs the pre-trained Logistic Regression model to generate probability prediction for round at that particular point in the round.
  * Prediction is in the form of a duo of probabilities - one for CT win % and one for t win %. Example - `[79.2, 20.8]`
  * The prediction is printed in the terminal as well as written to a text file in the parent directory (for use by other applications, such as `gui.py` which displays the predictions as a dynamic bar chart)

## Metrics

(accuracy charts)



#Acknowledgements:

1. Chris and Skybox for data
2. MD for GSI Code
3. 
