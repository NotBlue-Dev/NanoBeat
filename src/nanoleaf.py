# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 21:20:52 2020

@author: NotBlue
"""
from nanoleafapi import *
from nanoleafapi import discovery
from nanoleafapi import Nanoleaf
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
import os
from appJar import gui
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import asyncio
import websockets
import json
import random
import nest_asyncio
  

Config.set('graphics', 'resizable', False)
Window.size = (800, 250)

lis = []

modes = "Light"

nest_asyncio.apply()

class NanoBeatConnection(GridLayout):
    
    def __init__(self, **kwargs):
        super(NanoBeatConnection, self).__init__(**kwargs)

        self.cols = 1
        
        self.outside = GridLayout()
                
        self.outside.cols = 3
    
        self.inside = GridLayout()
        
        self.inside.cols = 3
        
        self.ip = Label(text='find an ip !')
        
        self.token = Label(text='Generate a token')

        self.output = Label(text="Output will be print here")
        
        self.add_widget(self.inside)
        
        self.inside.add_widget(Label(text='IP'))
        
        self.inside.add_widget(self.ip)
        
        self.scan = Button(text="Scan for ip")
        self.scan.bind(on_press=self.scanip)
        self.inside.add_widget(self.scan)
        
        self.inside.add_widget(Label(text='Token'))
        
        self.inside.add_widget(self.token)
        
        self.gentoken = Button(text="Generate Auth Token")
        self.gentoken.bind(on_press=self.auth)
        self.inside.add_widget(self.gentoken)
        
        self.add_widget(self.outside)
        
        self.connect = Button(text="Connect",size_hint_y=None, height=80)
        self.connect.bind(on_press=self.connection)
        self.outside.add_widget(self.connect)
        
        self.reset = Button(text="Reset Ip/Token",size_hint_y=None, height=80)
        self.reset.bind(on_press=self.clear)
        self.outside.add_widget(self.reset)
        
        self.exit = Button(text="Exit",size_hint_y=None, height=80)
        self.outside.add_widget(self.exit)
        self.exit.bind(on_press=self.close)
        
        self.outside.add_widget(Label(text='Console Output :'))
        
        self.outside.add_widget(self.output)
        
        def check():
            if not os.path.exists('connect.txt'):
                with open('connect.txt', 'w'): pass
            if os.stat("connect.txt").st_size != 0:
                with open('connect.txt','r') as f :
                    for ligne in f:
                        ligne=ligne.replace("\n","")
                        lis.append(ligne)     
                    if len(open('connect.txt').readline( )) < 13:
                        self.ip.text = ''
                        self.ip.text = lis[0]
                        print("no token")
                    else:
                        self.ip.text = ''
                        self.token.text = ''
                        self.ip.text = lis[0]
                        self.token.text = lis[1]
            
        if not lis or len(lis) == 1:
            check()
            
    def scanip(self, instance):
        nanoleaf_dict = discovery.discover_devices()
        res1 = list(nanoleaf_dict.values())
        res2 = ''.join(res1)          
        if res2 == "":
            print("ip not found")
            self.ip.text = ""
            self.ip.text = "Error"
            self.output.text = 'Check if Nanoleaf is on the same network, and power on/setup'
        else:
            self.ip.text = ""
            self.ip.text = res2
            print(res2)
            with open('connect.txt','a') as f :
                f.write(res2 + "\n")
                lis.append(res2)
        
    def auth(self, instance):
        try:
            nlip = Nanoleaf(lis[0])
            tok = nlip.generate_auth_token()
            if tok == False:
                self.token.text = '' 
                self.token.text = 'Token Generation Error' 
            else:
                self.token.text = ''
                self.token.text = tok
                with open('connect.txt','a') as f :
                      f.write(tok + "\n")
                      lis.append(tok + "\n")
        except Exception as e:
            self.output.text = str(e)
         
    def connection(self, instance):
        try:
            global nl
            nl = Nanoleaf(lis[0], lis[1])
            self.output.text = "Connect succesfully to the Nanoleaf"
            Nano.screen_manager.current = 'Mode'
        except Exception as e:
            self.output.text = str(e)
        
    def close(self,instance):
        nl.power_off()  
        loop.close()
        Nano.get_running_app().stop()    
    
    def clear(self, instance):
        open('connect.txt', 'w').close()
        self.ip.text = 'find an ip !'
        self.token.text = 'Generate a token'
        self.output.text = 'Restart the program to complet the reset'
        
class NanoBeatMode(GridLayout):
    def __init__(self, **kwargs):
        super(NanoBeatMode, self).__init__(**kwargs)
        self.cols = 1
        
        self.mode = GridLayout()
        
        self.mode.cols = 4
        
        self.outsides = GridLayout()
                
        self.outsides.cols = 3
        
        self.connect = GridLayout()
        
        self.connect.cols = 1
        
        self.outputs = Label(text="Output will be print here")    
        
        self.add_widget(Label(text='Mode'))
        
        self.mode.add_widget(Label(text ='Light')) 
        self.light = CheckBox(active = True) 
        self.light.bind(active=light)
        self.mode.add_widget(self.light)
        
        self.mode.add_widget(Label(text ='Saber')) 
        self.saber = CheckBox(active = False)
        self.saber.bind(active=saber)
        self.mode.add_widget(self.saber)
        
        self.add_widget(self.mode)
        
        self.backer = Button(text="Back",size_hint_y=None, height=60)
        self.connect.add_widget(self.backer)
        self.backer.bind(on_press=self.back)

        self.add_widget(self.connect)
       
        self.outsides.add_widget(Label(text='Console Output :'))
            
        self.outsides.add_widget(self.outputs)

        self.add_widget(self.outsides)
              
    async def loop_websocket(self):         
        try:
            websocket = await websockets.connect('ws://127.0.0.1:6557/socket', ping_interval=None)
            self.outputs.text = 'Connected to http-status plugin'
            while True:
                result = await websocket.recv()
                parsing = parse_json(result)
        except Exception as e:
            self.outputs.text = str(e)
            print(e)
            asyncio.get_event_loop().run_until_complete(self.loop_websocket())
        except asyncio.CancelledError as e:
            print(e)
        
    def back(self, instance):
        Nano.screen_manager.current = 'Connect'
        
class NanoBeatApp(App):
    screen_manager = ScreenManager()
    def build(self):
        
        self.connection = NanoBeatConnection()
        screen = Screen(name='Connect')
        screen.add_widget(self.connection)
        self.screen_manager.add_widget(screen)
        
        self.mode = NanoBeatMode()
        screen = Screen(name='Mode')
        screen.add_widget(self.mode)
        self.screen_manager.add_widget(screen)
        return self.screen_manager
    
    def app_func(self):
        nbm = NanoBeatMode()
        self.other_task = asyncio.ensure_future(nbm.loop_websocket())
        
        async def run_wrapper():
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.other_task.cancel()

        return asyncio.gather(run_wrapper(), self.other_task)
        
def saber(self, checkboxInstance):
    global modes
    modes = "Saber"
        
def light(self, checkboxInstance):
    global modes
    modes = "Light"

def parse_json(input_json):
    json_content = json.loads(input_json)
    current_event = json_content["event"]
    if current_event == "noteCut" or current_event == "noteFullyCut":
        event_note_cut(json_content["noteCut"])
    elif current_event == "bombCut":
        event_bomb_cut()
    elif current_event == "beatmapEvent":
        event_beat_map(json_content["beatmapEvent"])
    elif current_event == "hello":
        print("hello")
    elif current_event == "menu":
        nl.set_effect(effect_name='Rain')
    elif modes == "Saber":
        if current_event == "obstacleEnter":
            nl.set_color((ORANGE))
    elif current_event == "obstacleExit":
        nl.set_color((0,0,0))
    elif not current_event == "noteMissed":
        print("other event: " + current_event)
        
def event_note_cut_parse(note_cut_object):
    saber_type = note_cut_object["saberType"]
    note_type = note_cut_object["noteType"]
    light_value = 0
    if note_type == "NoteA":
        light_value = 7
    elif note_type == "NoteB":
        light_value = 3
    if saber_type == "SaberA":
        trigger_saber_a(light_value)
    elif saber_type == "SaberB":
        trigger_saber_b(light_value)
    
def event_beat_map(event_object):
    event_beat_map_parse(event_object)
    
def event_beat_map_parse(beatmap_event_object):
    type = beatmap_event_object["type"]
    value = beatmap_event_object["value"]
    if modes == "Light":
        if 0 < type < 5:
            if type == 0:
                trigger_light_small(value)
            elif type == 1:
                trigger_light_big(value)
            elif type == 2:
                trigger_light_left(value)
            elif type == 3:
                trigger_light_right(value)
            elif type == 4:
                trigger_light_center(value)
                    
def event_note_cut(note_cut_object):
    print("Note Cut")
    event_note_cut_parse(note_cut_object)
    
def trigger_light_center(value):
    if value == 2 or value == 3:
        nl.set_color(BLUE)
        print("lgc b")
    elif value == 6 or value == 7:
        nl.set_color(RED)
        print("lgc r")

def trigger_light_left(value):
    if value == 2 or value == 3:
        nl.set_color((51,153,255))        
        print("lgl b")
    elif value == 6 or value == 7:
        nl.set_color((134,12,12))
        print("lgl r")

def trigger_light_right(value):
    if value == 2 or value == 3:
        nl.set_color((0,102,204))
        print("lgr b")
    elif value == 6 or value == 7:
        nl.set_color((255,144,144))
        print("lgr r")

def trigger_light_small(value):
    if value == 2 or value == 3:
        nl.set_color((51,51,255))
        print("lgs b")
    elif value == 6 or value == 7:
        nl.set_color((255,51,51))
        print("lgs r")

def trigger_light_big(value):
    if value == 2 or value == 3:
        nl.set_color((0,128,255))
        print("lgb b")
    elif value == 6 or value == 7:
        nl.set_color((255,102,102))
        print("lgb r")

def trigger_saber_a(light_value):
    nl.set_color((random.randint(80,255),0,0))
    print("saber a")    

def trigger_saber_b(light_value):
    nl.set_color((0,0,random.randint(80,255)))
    print("saber b")

def event_bomb_cut():
    nl.set_color((ORANGE))
    print("bomb")

if __name__ == '__main__':
    Nano = NanoBeatApp()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(NanoBeatApp().app_func())
    loop.close()
    
#192.168.1.20
#FqOhMVnrfkmckE6aDlSJrRiFbwgbEtZB