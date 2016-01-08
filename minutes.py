""" Contains functions that define how to write numbers to the seven segment 
    display we hooked up to the Pi. Contains lots of extra functions that were 
    written for testing. """
import RPi.GPIO as GPIO
import time
 

# Please find a visual of the mapping for pins the following link:
# https://www.dropbox.com/s/it6vjaoeddy67q6/LED-GPIO%20Mapping.pptx?dl=0
LED_2 = 2
LED_3 = 3
LED_4 = 4
LED_5 = 17
LED_6 = 27
LED_8 = 22
LED_9 = 10
LOW = 0
HIGH = 1
 
# turn off all lights
def allLightsOff():
  GPIO.output(LED_2, HIGH)
  GPIO.output(LED_3, HIGH)
  GPIO.output(LED_4, HIGH)
  GPIO.output(LED_5, HIGH)
  GPIO.output(LED_6, HIGH)
  GPIO.output(LED_8, HIGH)
  GPIO.output(LED_9, HIGH)
 
# turn on all lights
def allLightsOn():
  GPIO.output(LED_2, LOW)
  GPIO.output(LED_3, LOW)
  GPIO.output(LED_4, LOW)
  GPIO.output(LED_5, LOW)
  GPIO.output(LED_6, LOW)
  GPIO.output(LED_8, LOW)
  GPIO.output(LED_9, LOW)
 
# initialize the relevant GPIO ports so we can use them later
# once that is done, we turn all lights off
def setup():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  # put your setup code here, to run once:
  GPIO.setup(LED_2, GPIO.OUT);
  GPIO.setup(LED_3, GPIO.OUT);
  GPIO.setup(LED_4, GPIO.OUT);
  GPIO.setup(LED_5, GPIO.OUT);
  GPIO.setup(LED_6, GPIO.OUT);
  #GPIO.setup(LED_7, GPIO.OUT);
  GPIO.setup(LED_8, GPIO.OUT);
  GPIO.setup(LED_9, GPIO.OUT);
 
  GPIO.output(LED_2, LOW);
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);
  GPIO.output(LED_5, LOW);
  GPIO.output(LED_6, LOW);
  #GPIO.output(LED_7, LOW);
  GPIO.output(LED_8, LOW);
  GPIO.output(LED_9, LOW);
  
# these are the functions to display a number on the 7 segment display
def display_0():
  allLightsOn();
  GPIO.output(LED_3, HIGH); 
 
def display_1():
  allLightsOff();
  GPIO.output(LED_2, LOW); 
  GPIO.output(LED_6, LOW); 
 
def display_2():
  allLightsOff();  
  GPIO.output(LED_3, LOW);  
  GPIO.output(LED_5, LOW);
  GPIO.output(LED_6, LOW);
  #GPIO.output(LED_7, LOW);
  GPIO.output(LED_8, LOW);
  GPIO.output(LED_9, LOW);
 
def display_3():
  allLightsOff();  
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);
  GPIO.output(LED_5, LOW);  
  #GPIO.output(LED_7, LOW);
  GPIO.output(LED_8, LOW);
  GPIO.output(LED_9, LOW);
 
def display_4():
  allLightsOff();  
  GPIO.output(LED_2, LOW);
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);  
  #GPIO.output(LED_7, LOW);  
  GPIO.output(LED_9, LOW);
 
def display_5():
  allLightsOff();  
  GPIO.output(LED_2, LOW);
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);
  GPIO.output(LED_5, LOW);  
  #GPIO.output(LED_7, LOW);
  GPIO.output(LED_8, LOW);  
 
def display_6():
  allLightsOff();  
  GPIO.output(LED_2, LOW);
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);
  GPIO.output(LED_5, LOW);
  GPIO.output(LED_6, LOW);
  #GPIO.output(LED_7, LOW);
  GPIO.output(LED_8, LOW);  
 
def display_7():
  allLightsOff();  
  GPIO.output(LED_4, LOW);
  GPIO.output(LED_8, LOW);
  GPIO.output(LED_9, LOW);
   
def display_8():
  allLightsOff();
  allLightsOn();
 
def display_9():
  allLightsOff();
  GPIO.output(LED_2, LOW);
  GPIO.output(LED_3, LOW);
  GPIO.output(LED_4, LOW);  
  GPIO.output(LED_8, LOW);
  GPIO.output(LED_9, LOW);
 
# This is the function you want to use to a
def display_num(num):
    if num == 0:
        display_0();
    elif num ==1:
        display_1();
    elif num ==2:
        display_2();
    elif num ==3:
        display_3();
    elif num ==4:
        display_4();
    elif num ==5:
        display_5();
    elif num ==6:
        display_6();
    elif num ==7:
        display_7();
    elif num ==8:
        display_8();
    elif num ==9:
        display_9();
    else:
        return
 
 
 # this function i just for testing, it prints out all the numbers
def loop():
    display_num(0);
    time.sleep(1);
    display_num(1);
    time.sleep(1);
    display_num(2);
    time.sleep(1);
    display_num(3);
    time.sleep(1);
    display_num(4);
    time.sleep(1);
    display_num(5);
    time.sleep(1);
    display_num(6);
    time.sleep(1);
    display_num(7);
    time.sleep(1);
    display_num(8);
    time.sleep(1);
    display_num(9);
 

# lines used for testing
#print (("Setting up lights........"))
#setup()
#loop()
