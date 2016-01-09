# shuttleLED
Tracking the Harvard Shuttle with Raspberry Pi, NeoPixels, a Seven-Segment Display and More 

Gabriela Merz, Alexander Fisher, Erez Perelson, and Nathan Press 

 ![shuttle](es50.gif)

## Motivation 
How do students without smartphones know when the next shuttle will be? It's a hassle to track the shuttle from your laptop, and shuttle arrival times are erratic. To solve this problem, we built a giant LED map of the Harvard Quad Shuttle route to (eventually) display in dining halls so students don't have to battle with the app! 

## Overview 
For this project, we used
* Raspberry Pi Model B
* TransLOC's API (how we found out the location of the shuttle and it's arrival times)
* Seven Segment Display (for displaying the time until the shuttle arrived at the Quad Stop)
* NeoPixels strips (the lights for the track)
* Jeremy Garff's awesome library for integrating NeoPixels and the Pi (found [here](https://github.com/jgarff/rpi_ws281x))
* 5V power supply and a 74AHCT125 level converter (to safely convert the Pi's GPIO output from 3.3V to 5V, again to be compatible with the NeoPixels)
* Laser-cut acryllic (the labels for the stops) 


## What's on the github 
This github contains the code we had the Pi run. It could definitely be modified to work for different tracks, different bus routes, etc. The file tracker.py contains the majority of the functions -- functions for mapping each LED to a latitude and longitude, functions that parse the data from the API, functions for mapping the shuttles location to an LED, calculating the time to arrival and displaying it on the seven segment display, etc. In minutes.py is the code for writing numbers to the seven segment display. 

## Want to do something similar? 
1. To get started, We reccomend doing a headless set-up for your Pi. You'll need a WiFi dongle and an Ethernet cable. The best tutorial I found was [here](https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=74176). If you want to integrate with NeoPixels, I reccomend using a Pi model B (so you can just use Jeremy Garff's library) . We originally tried a newer model and ran in to a lot of compatibility issues. 
2. [Adafruit](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview) has some great tutorials for integrating Neopixels with a Raspberry Pi. 
3. Check out the code! 



