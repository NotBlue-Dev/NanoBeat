# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 19:06:02 2020

@author: Enzo
"""
from light import *
from nanoleaf import *
import time
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
import random

def trigger_saber_a(light_value):
    nl.set_color((random.randint(80,255),0,0))
def trigger_saber_b(light_value):
    nl.set_color((0,0,random.randint(80,255)))
def event_bomb_cut():
    nl.set_color((ORANGE))

