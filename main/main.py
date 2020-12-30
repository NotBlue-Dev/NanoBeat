# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 14:57:33 2020

@author: Enzo
"""
#Main Import
import asyncio
import websockets
import json
import random
import nest_asyncio
import sys
import os

#PyQT5 Import
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication

#Window Import
from ip import Ui_MainWindow
from tokens import Ui_token
from connected import Ui_Connected
from connection import Ui_Connection

#Nanoleaf Import
from nanoleafapi import discovery
from nanoleafapi import Nanoleaf
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE

#definie la loop
loop = asyncio.get_event_loop()

#list pour token/ip
lis = [] 

#status pour la loop 1
stoploop = False

#status pour la loop 2
stoploopdp = False

#définis le modes / défault Light
modes = "Light"

#patch une erreur async
nest_asyncio.apply()

#fonction pour arrondir a 10
def myround(x, base=10):
    return base * round(x/base)


#Main class
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        #différent bouton connecter
        self.pushButton_2.clicked.connect(self.gototoken)
        self.pushButton.clicked.connect(self.scanip)
        self.pushButton_3.clicked.connect(self.clear)
        
        #check
        print(len(lis))   
        def check():
            #check si le fichier connect existe
            if not os.path.exists('connect.txt'):
                with open('connect.txt', 'w'): pass
            #check si il est vide et remplis le label si y'a une ip dedans
            if os.stat("connect.txt").st_size != 0:
                with open('connect.txt','r') as f :
                    for ligne in f:
                        ligne=ligne.replace("\n","")
                        if len(lis) >= 1:
                            pass
                        else:
                            print("append")
                            lis.append(ligne)
            if len(lis) == 0:
                pass
            else:
                self.label_3.setText(lis[0])
            print("ip set")
        print(lis)                        
        check()   
    
    #scan l'ip
    def scanip(self):
        nanoleaf_dict = discovery.discover_devices()
        res1 = list(nanoleaf_dict.values())
        global res2
        res2 = ''.join(res1)
        if res2 == "":
            print("ip not found")
            self.label_3.setText("Error retry")
        else:
            print(res2)
            self.label_3.setText(res2)
            with open('connect.txt','a') as f :
                f.write(res2 + "\n")
                lis.append(res2)
                
    #vide le fichier et les labels        
    def clear(self):
        lis.clear()
        self.label_3.setText("No ip start scan")
        open('connect.txt', 'w').close()
    
    #switch window vers token 
    def gototoken(self):
        Ui_token = token()
        widget.addWidget(Ui_token)
        widget.setCurrentIndex(widget.currentIndex()+1)

#token window  
class token(QtWidgets.QMainWindow, Ui_token):
    def __init__(self):
        super(token,self).__init__()
        self.setupUi(self)
        #différent bouton connecter
        self.pushButton_4.clicked.connect(self.gotoip)
        self.pushButton_2.clicked.connect(self.gotocon)
        self.pushButton.clicked.connect(self.auth)
        self.pushButton_3.clicked.connect(self.clear)
        print(lis)
        #check si y'a un token dans connect.txt
        def check():
            #check si il est vide et remplis le label si y'a un token dedans
            if os.stat("connect.txt").st_size != 0:
                lis.clear()
                with open('connect.txt','r') as f :
                    for ligne in f:
                        ligne=ligne.replace("\n","")
                        lis.append(ligne)   
                with open('connect.txt','r') as f :
                    data = f.read()
                char = len(data)  
                print(char)
                print(lis)
                #si moins de 20 charactere signife pas de token sinon y'en a
                if char < 20:
                    print("no token")
                    self.label_3.setText("No Token Found Generate one")
                else:
                    print("token")
                    self.label_3.setText(lis[1])
        check()     
        
    #clear list et labels
    def clear(self):
        lis.clear()
        self.label_3.setText("No ip start scan")
        open('connect.txt', 'w').close()    
    
    #authentifie les nanoleafs
    def auth(self):
        try:
            nlip = Nanoleaf(lis[0])
            tok = nlip.generate_auth_token()
            if tok == False:
                self.label_3.setText('Token Generation Error')
            else:
                self.label_3.setText(tok)
                with open('connect.txt','w') as f :
                    print('### FILE CLEAR ###')
                with open('connect.txt', 'a') as f:
                    res2 = lis[0]
                    lis.clear()
                    f.write(res2 + "\n")
                    f.write(tok + "\n")
                    lis.append(res2)
                    lis.append(tok)   
                    print(f'### {res2} + {tok} RESET IN FILE ###')
                    print('generated')      
        except Exception as e:
            self.label_3.setText(str(e))
    
    #switch vers ip
    def gotoip(self):
        Ui_MainWindow = Main()
        widget.addWidget(Ui_MainWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    #switch vers connection 
    def gotocon(self):
        try:
            global nl
            nl = Nanoleaf(lis[0], lis[1])
            print("Connect succesfully to the Nanoleaf")
            Ui_Connection = connection()
            widget.addWidget(Ui_Connection)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except Exception as e:
            print(str(e))      
        print(lis)

#status des threads
rune = False
runes = False

#threads http stauts loop
class QThread1(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        global rune
        rune = True
        loop.run_until_complete(connected.loop_websocket(0))
        
#threads data puller loop
class QThread2(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        global runes
        runes = True
        loop.run_until_complete(connected.loop_websocketdp(0))

#class connected
class connected(QtWidgets.QMainWindow, Ui_Connected):
    def __init__(self):
        super(connected,self).__init__()
        self.setupUi(self)
        #les différents boutons
        self.pushButton_4.clicked.connect(self.gotocon)
        self.pushButton_4.clicked.connect(self.start)
        self.pushButton_5.clicked.connect(self.exit)
        self.hide()
    #lance la loop en fonction du mode dépend des status threads/loop
    def start(self):
        global stoploop
        global runes
        global rune
        global stoploopdp
        if modes == 'Saber':
            if runes == False:
                rune = False
                stoploopdp = False
                stoploop = True
                print('data puller loop start')
                self.thread2 = QThread2()
                self.thread2.start()
        elif modes == 'Light':
            if rune == False:
                runes = False
                stoploopdp = True
                stoploop = False
                print('http status loop start')
                self.thread1 = QThread1()
                self.thread1.start()         
        if modes == 'Hit':
            if runes == False:
                rune = False
                stoploopdp = False
                stoploop = True
                print('data puller loop start')
                self.thread2 = QThread2()
                self.thread2.start()
        elif modes == 'Score':
            if runes == False:
                rune = False
                stoploopdp = False
                stoploop = True
                print('data puller loop start')
                self.thread2 = QThread2()
                self.thread2.start()
    #ferme tout
    def exit(self):
        sys.exit()
    #switch vers connection   
    def gotocon(self):
        Ui_Connection = connection()
        widget.addWidget(Ui_Connection)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    #loop httpstatus
    async def loop_websocket(timer): 
        try:
            websocket = await websockets.connect('ws://127.0.0.1:6557/socket', ping_interval=None)
            print('connect to httpstatus')
            await asyncio.sleep(timer)
            while True:
                result = await websocket.recv()
                parsing = parse_json(result)
        except Exception as e:
            print("Httpstatus", e)
            timer = 2
            #loop stop si status = Vrai
            if stoploop == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocket(timer))
        except asyncio.CancelledError as e:
            timer = 2
            if stoploop == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocket(timer))
            print("Httpstatus", e)
        except websocket.ConnectionClosed as e:
            timer = 3
            if stoploop == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocket(timer))
            print("Httpstatus", e)
            
    #loop datapuller     
    async def loop_websocketdp(timer):  
        try:
            websocket = await websockets.connect('ws://127.0.0.1:2946/BSDataPuller/LiveData', ping_interval=None)
            print('connect to datapuller')
            await asyncio.sleep(timer)
            while True:
                result = await websocket.recv()
                parse_jsondp(result)
        except Exception as e:
            print("Datapuller", e)
            timer = 2
            #loop stop si status = Vrai
            if stoploopdp == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocketdp(timer))
        except asyncio.CancelledError as e:
            timer = 2
            if stoploopdp == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocketdp(timer))
            print("Datapuller", e)
        except websocket.ConnectionClosed as e:
            timer = 3
            if stoploopdp == True:
                pass
            else:
                loop.run_until_complete(connected.loop_websocketdp(timer))
            print("Datapuller", e)
        
#Connection window    
class connection(QtWidgets.QMainWindow, Ui_Connection):
    def __init__(self):
        super(connection,self).__init__()
        self.setupUi(self)
        #button 
        self.pushButton_2.clicked.connect(self.gototoken)
        self.pushButton.clicked.connect(self.gotoconnected)
        self.radioButton_5.clicked.connect(self.light)
        self.radioButton_6.clicked.connect(self.saber)  
        self.radioButton_7.clicked.connect(self.score)
        self.radioButton_8.clicked.connect(self.hit)  

    #switch token
    def gototoken(self):
        Ui_token = token()
        widget.addWidget(Ui_token)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    #switch connected   
    def gotoconnected(self):
        Ui_Connected = connected()
        widget.addWidget(Ui_Connected)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    
    #saber mode      
    def saber(self):
        print("saber")
        global modes
        modes = "Saber"
        
    #light mode   
    def light(self):
        print("light")
        global modes
        modes = "Light"  
        
    #score mode   
    def score(self):
        print("score")
        global modes
        modes = "Score"
        
    #hit mode   
    def hit(self):
        print("hit")
        global modes
        modes = "Hit"  

#var nécéssaire pour les modes hit et score et saber
lenght = 0
current = 100
tempmiss = 0
tempcombo = 0
temp = 0
val = 1
#datapuller parsing json
def parse_jsondp(input_json):
    json_content = json.loads(input_json)
    zone = json_content["InLevel"]
    hitscore = json_content["BlockHitScores"]
    acc = json_content["Accuracy"]
    combo = json_content["Combo"]
    miss = json_content["Misses"]
    fullcombo = json_content["FullCombo"]
    global tempmiss
    global tempcombo
    global lenght
    global current
    #saber modes bsdatapuller
    if modes == 'Saber':
        #miss
        if tempmiss != miss:
            tempmiss = miss 
            misses(miss)
        #combo
        if tempcombo != myround(combo):
            tempcombo = myround(combo)
            combof(tempcombo)
        #full combo
        if fullcombo == True:
            print('fullcombo !')
        
    #lance fonction hit
    if modes == 'Hit':
        if lenght != len(hitscore):
            lenght = len(hitscore)
            hit(hitscore[len(hitscore)-1])
    #lance fonction scores
    if modes == 'Score':
        if current != myround(acc):
            current = myround(acc)
            scores(current)
    #check if in game or not
    if zone == False:
        print('datapuller info: menu')
        nl.set_effect(effect_name='Rain')
    
#saber mode function part 1
def combof(combo):
    global temp
    global val
    if temp < combo:
        temp = combo
        val += 1
        if not val > 100:
            nl.increment_brightness(val)   

#saber mode function part 2
def fullcombo():
    nl.set_effect(effect_name='Fireworks')
    print('FULL COMBO')

#saber mode function part 3
def misses(miss):
    nl.set_color((255,0,0))
    nl.set_color((0,0,0))
        
#score modes function
def scores(current):
    if current < 40:
        print('datapuller info: rouge')
        nl.set_color((255,0,0))
    elif current < 50:
        print('datapuller info: orange rouge')
        nl.set_color((255,85,0))
    elif current < 60:
        print('datapuller info: orrange')
        nl.set_color((255,128,0))
    elif current < 70:
        print('datapuller info: jaune')
        nl.set_color((255,255,0))
    elif current < 80:
        print('datapuller info: vert clair')
        nl.set_color((85,255,0))
    elif current < 90:
        print('datapuller info: vert')
        nl.set_color((0,255,0))
    elif current < 100:
        print('datapuller info: vert foncé')
        nl.set_color((230,255,247))

#hit mode function
def hit(score): 
    if score < 20:
        print('datapuller info : rouge, score: ', score)
        nl.set_color((255,0,0))
    elif score < 40:
        print('datapuller info: rouge clair, score: ', score)
        nl.set_color((255,25,102))
    elif score < 60:
        print('datapuller info: orange, score: ', score)
        nl.set_color((255,111,0))       
    elif score < 80:
        print('datapuller info: jaune, score: ', score)
        nl.set_color((255,255,0))      
    elif score < 100:
        print('datapuller info: vers clair, score: ', score)
        nl.set_color((170,255,0))  
    elif score < 115:
        print('datapuller info: green, score: ', score)
        nl.set_color((43,255,0))
    
#http status parsing
def parse_json(input_json):
    json_content = json.loads(input_json)
    current_event = json_content["event"]
    if current_event == "beatmapEvent":
        event_beat_map(json_content["beatmapEvent"])
    elif current_event == "hello":
        print("hello")
        nl.set_effect(effect_name='Rain')
    elif current_event == 'pause':
        print('pause')
        nl.set_effect(effect_name='Rain')
    elif current_event == "menu":
        nl.set_effect(effect_name='Rain')
        print("menu")

#get beatmap event
def event_beat_map(event_object):
    event_beat_map_parse(event_object)

#parse beatmap event
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
    
#LIGHT
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

#app main       
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
Ui_MainWindow = Main()
widget.addWidget(Ui_MainWindow)
widget.setFixedSize(761, 474)
widget.show()
sys.exit(app.exec_())

#json type datapuller

#{'InLevel': False, 'LevelPaused': False, 'LevelFinished': False, 'LevelFailed': False, 'LevelQuit': False, 'Score': 0, 'FullCombo': True,
# 'Combo': 0, 'Misses': 0, 'Accuracy': 100.0, 'BlockHitScores': [], 'PlayerHealth': 50.0, 'TimeElapsed': 0}