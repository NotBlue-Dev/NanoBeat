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
execute the installer
execute the program choose a display and create a token, choose a mode that it's

## Advanced Information
* Scan ip: it will scan your network and try to find your canvas if it don't find it you will need to find it yourself
* Generate token : hold power button of the nanoleaf for 5-7s 

## NanoBeat Mode
* **Saber**, blue when right saber, red when left saber, if touch a bomb orange color and if hit a wall orange while you are in
* **Light**, connect to 5 light : center, left, right, big, small, color(blue-red) vary for each light
* **ScoreHit**, Color different for each score on the note, green if 115, orange if 90 ...
* **Score**, like ScoreNote but for Score (SS, S, A, B, C)
* **Chroma**[Incoming], Like the chroma light mode, rainbow light instead of blue red

## Patch Notes
* New connection system
* separate thread for the two plugins
* saber mode repaired
* delay decrease
* code is now commented
* code is optimized
* data can be parse speeder so the delay is less

## Updates
* GUI
* Reworked Saber mode
* add hit mode
* add scoremode
* reset ip/token


## Demos
* Live Demo : https://www.youtube.com/watch?v=bIAraV3Dl6A
* GUI

![3](https://user-images.githubusercontent.com/64601123/103375434-8a62f880-4ada-11eb-8c5d-4b8f826a08ab.png)
![1](https://user-images.githubusercontent.com/64601123/103375436-8afb8f00-4ada-11eb-81e0-029e85b6010e.png)
![2](https://user-images.githubusercontent.com/64601123/103375437-8afb8f00-4ada-11eb-83cf-102a2f3576f5.png)
![Capture](https://user-images.githubusercontent.com/64601123/103375438-8afb8f00-4ada-11eb-9902-f76f1a41467a.png)

## Requierements 
* (External) Beatsaber http-status plugin
* (External) DataPuller 

## Working on
* Chroma, more stable light mode
* repair the ip bug if you have two nanoleafs devices

## Credits
* Based on mqttproxy by [@Elektrospy](https://github.com/Elektrospy/BeatSaberMqttProxy)
* and on http-status by [@opl-](https://github.com/opl-/beatsaber-http-status)
* For the datapuller mod wich is require [@kOFReadie](https://github.com/kOFReadie/BSDataPuller)
