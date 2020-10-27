# NanoBeat
Sync BeatSaber event to NanoLeaf Canvas

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Advanced Information](#advanced-information)
* [NanoBeat Mode](#nanobeat-mode)
* [Patch Notes](#patch-notes)
* [Updates](#updates)
* [Demos](#demos)
* [Requierements](#requierements)
* [Credits](#credits)

## General info
This project will link event from beatsaber like light or hitblock, bombhit, wallhit etc to your nanoleaf and change color in function of this event
	
## Setup
To run this project you need to run 'connection.py'
and then follow the step given by the script

## Advanced Information
* Scan ip for nanoleaf : it will scan your network and try to find your canvas if it don't find it you will need to find it yourself
* Generate token : hold power button of the nanoleaf for 5-7s then type done

## NanoBeat Mode
* **Saber**, blue when right saber, red when left saber, if touch a bomb orange color and if hit a wall orange while you are in
* **Light**, connect to 5 light : center, left, right, big, small, color(blue-red) vary for each light
* **Chroma**[Incoming], Like the chroma light mode, rainbow light instead of blue red
* **ScoreNote**[Incoming], Color different for each score on the note, green if 115, orange if 90 ...
* **Score**[Incoming], like ScoreNote but for Score (SS, S, A, B, C)

## Patch Notes
* Light Blue showing red on the nanoleaf
* Sync issue(delay to big)
* Websocket connection error(partially fixed)

## Updates
* Added Saber mode
* Added a system to connect the nanoleaf instead of change the variable (input)
* Wall event
* Bomb event

## Demos
* Live Demo : https://www.youtube.com/watch?v=bIAraV3Dl6A
* GUI

![Capture](https://user-images.githubusercontent.com/64601123/97317710-62051680-186b-11eb-94fa-71959c201643.PNG)
![1](https://user-images.githubusercontent.com/64601123/97317802-7812d700-186b-11eb-88a5-698e0a83cd97.PNG)

## Requierements 
* (External) Beatsaber http-status plugin

## Working on
* GUI and .exe instead of .py

## Credits
* Based on mqttproxy by [@Elektrospy](https://github.com/Elektrospy/BeatSaberMqttProxy)
* and on http-status by [@opl-](https://github.com/opl-/beatsaber-http-status)
