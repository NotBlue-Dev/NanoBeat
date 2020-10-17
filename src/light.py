# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:51:38 2020

@author: Enzo
"""

from saber import *
from nanoleaf import *
from nanoleafapi import Nanoleaf
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE

def trigger_light_center(value):
    if value == 2 or value == 3:
        nl.set_color(BLUE)
        #print("lgc b")
    elif value == 6 or value == 7:
        nl.set_color(RED)
       #print("lgc r")

def trigger_light_left(value):
    if value == 2 or value == 3:
        nl.set_color((51,153,255))        
        #print("lgl b")
    elif value == 6 or value == 7:
        nl.set_color((153,0,0))
        #print("lgl r")

def trigger_light_right(value):
    if value == 2 or value == 3:
        nl.set_color((0,102,204))
        #print("lgr b")
    elif value == 6 or value == 7:
        nl.set_color((170,0,0))
        #print("lgr r")

def trigger_light_small(value):
    if value == 2 or value == 3:
        nl.set_color((51,51,255))
        #print("lgs b")
    elif value == 6 or value == 7:
        nl.set_color((255,51,51))
        #print("lgs r")

def trigger_light_big(value):
    if value == 2 or value == 3:
        nl.set_color((0,128,255))
        #print("lgb b")
    elif value == 6 or value == 7:
        nl.set_color((255,102,102))
        #print("lgb r")
        