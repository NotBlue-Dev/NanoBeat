# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:16:34 2020

@author: Enzo
"""

from nanoleafapi import Nanoleaf
import time

nl = Nanoleaf('192.168.1.20', 'FqOhMVnrfkmckE6aDlSJrRiFbwgbEtZB')


time.sleep(2)

print(nl.set_color((255,0,0)))

print(nl.set_color((0,255,0)))