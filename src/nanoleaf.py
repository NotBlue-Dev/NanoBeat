# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 21:20:52 2020

@author: NotBlue
"""
from nanoleafapi import Nanoleaf
from nanoleafapi import discovery
import os

transTime = 0

lis = []

def check():
    if os.stat("connect.txt").st_size != 0:
        with open('connect.txt','r') as f :
            for ligne in f:
                ligne=ligne.replace("\n","")
                lis.append(ligne)          
if not lis:
    check()
            
if os.stat("connect.txt").st_size == 0:
    inp = input("want to try to find auto ip of canvas ? (yes or no) can take 30-60s \n")
    if inp == "yes":
        nanoleaf_dict = discovery.discover_devices() 
        res1 = list(nanoleaf_dict.values())
        res2 = ''.join(res1)
        if res2 == "":
            print("ip not found")
        else:
            print("ip: " + res2) 
    ip = input("enter the canvas ip \n")
    inp2 = input("want to generate a token ? yes or no \n")
    if inp2 == "yes":
        nlip = Nanoleaf(ip)
        tok = input("hold the power button on the lights for 5-7 seconds when done type done \n")
        if tok == "done":   
            if nlip.generate_auth_token() == False:
                print("token not found check if you hold corretly the power button")
            else:
                print(nlip.generate_auth_token())  
        token = input("enter token \n")
        with open('connect.txt','a') as f :
            f.write(ip + "\n"), f.write(token + "\n")
            lis.append(ip), lis.append(token)        
    else:
        token = input("enter token \n")
        with open('connect.txt','a') as f :
            f.write(ip + "\n"), f.write(token + "\n")
            lis.append(ip), lis.append(token)

def clear():
    open('connect.txt', 'w').close()

nl = Nanoleaf(lis[0], lis[1])


#192.168.1.20
#FqOhMVnrfkmckE6aDlSJrRiFbwgbEtZB

#if Exception: No valid Nanoleaf device found on IP : your nanoleaf ip is not good
#if all is set but nothing append check if your token is good
