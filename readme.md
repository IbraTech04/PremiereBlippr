# PremiereBlippr
A script inspired by [Evan Kale's Blipper Project](https://github.com/evankale/Blipper) which allows users to insert blips into an unused audio track in OBS, which are then detected in Premiere for marker placement. 

## Utilization

This script is meant to simplify editing large segments of video, such as podcasts, seminars, lectures, large events, etc. It allows the user to insert blips into an unused audio track OBS triggered by a hotkey to mark interesting/important moments in the video for later editing. This script then reads the audio file and places markers in the corresponding video file in Premiere Pro.

This script is *perfect* for creating highlight reels, cutting out dead air, removing unnecessary content, and more! 

This script has been tested with Adobe Premiere Pro 2024 V24.3.0 (Build 59), however it *should* work with any version of Premiere Pro CC 2019 or later. No guarantees though ¯\_(ツ)_/¯

## OBS Setup

1. Create a new source in OBS and select `Media Source`.
2. Ensure the `Local File` box is checked and select the audio file you want to use. I personally use a censor beep sound effect, but you can use whatever you want so long as it's a blip sound.
3. Check the `Restart playback when source becomes active` box. You're now done with the media source setup and can close the properties window.
4. From the `Audio Mixer` section, select the `Blip Sound` we created in the previous steps and ensure it only outputs to the `Audio Track` you want to use. I personally use `Audio Track 3` as it's usually unused in my projects.
5. Finally, go through the rest of your audio sources and ensure they're **NOT** outputting to the audio track selected in the previous step. This is to ensure the blip sound is the only thing on that track. ***__Otherwise, the script will not work.__***

## Installation - Debugging and Development

Due to ExtendScript's limitations, this script **cannot** work standalone. It requires a supplementary Python script to read the audio file and communicate with the ExtendScript. Once again, due to ExtendScript limitations this forces me to basically use a pair of files as a set of pipes to communicate between the two scripts. This is a disgusting hack of a solution, but it works.

### Step 0: Clone the Repository

### Step 1: Python Setup

1. Install Python 3.9 or later from [here](https://www.python.org/downloads/). This script was developed and tested with Python 3.10.11, though any version 3.9 or later should work.
2. Install the required Python packages by running `pip install -r requirements.txt` in the terminal. This will install the required packages for the Python script to run.

### Step 2: ExtendScript Setup

1. Open Premiere Pro and create a new project.
2. Install the ExtendScript extensions for Visual Studio Code from [here](https://marketplace.visualstudio.com/items?itemName=Adobe.extendscript-debug).
3. Open the `main.jsx` file in Visual Studio Code and run the script by pressing `F5`. This will hook the debugger into the running instace of Premiere Pro and execute the script.

## Installation - Production

`TODO: This script isn't ready for production yet. I need to figure out how to package it into a single executable or something.`