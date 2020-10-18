import asyncio
import websockets
import json
from nanoleaf import *
from nanoleafapi import *
import logging
from light import *
from saber import *
import paho.mqtt.client as mqtt
import nest_asyncio

modes = input("Choose a mode : \n Saber \n Light \n")

nest_asyncio.apply()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    print('received message: {}'.format(msg))

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
    else:
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


async def loop_websocket():
    try:
        websocket = await websockets.connect('ws://127.0.0.1:6557/socket', ping_interval=None)
        while True:
            result = await websocket.recv()
            parse_json(result)
    except Exception as e:
        print('recconect')
        websocket = await websockets.connect('ws://127.0.0.1:6557/socket', ping_interval=None)      
        asyncio.get_event_loop().run_until_complete(loop_websocket())
        
asyncio.get_event_loop().run_until_complete(loop_websocket())

#blue 2,3
#red 6,7

