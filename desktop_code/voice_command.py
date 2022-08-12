import speech_recognition as sr
from time import ctime
import time
import Play_mp3
from gtts import gTTS
import requests, json
import machine_learn

import data_subs
import threading

def listen():
    """collect audio data from speaker
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data

def respond(audioString):
    """responds for instructions by creating and playing aduio file
        audioString(str): desired response
    """
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("speech.mp3")
    play_mp3.play("speech.mp3")

def forcast_generator():
    """generate weather forcast"""
    json_acceptable_string = open("message.txt","r").read()
    open("message.txt","r").close()
    json_acceptable_string = json_acceptable_string.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    temp =data["temp"]
    light = data["light"]
    tag = machine_learn.scoring()
    if tag == "No Precipitation":
        weather_str = "No precipitation, might be good to hang out."
    elif tag == "Low Precipitation":
        weather_str = "Low level of precipitation, might be good to bring an umbrella."
    elif tag == "High Precipitation":
        weather_str = "High level of precipitation, might be good to stay at home, be cautious in driving."
    if temp<=15:
        temp_str ="Today's temperature is {} degree, dress warm!".format(temp)
    else:
        temp_str = "Today's temperature is {} degree, good temperature!".format(temp)
    if light >=300:
        light_str = "Now is dark outside."
    else:
        light_str = "Now is the day time."
    return temp_str+light_str+weather_str

def digital_assistant(data):
    """recognize which command to be executed and execute response audio
        data(str): command input from user
        return nothing
    """
    listening = True
    if "how are you" in data:
        listening = True
        respond("I am well")
    elif "how is today" in data:
        listening = True
        respond(forcast_generator())
    elif "stop listening" in data:
        listening = False
        respond("stop listening, terminating program")
    else:
        respond("I cannot understand you")

    return listening
def data_subs_thread():
    data_subs.main()
def voiz_terminal_thread():
    listening= True
    while listening == True:
        data = listen()
        if "Alice" in data:
            respond("Hi, what can I help you")
            command = listen()
            listening = digital_assistant(command)

    
thread_data_subs = threading.Thread(name='data_subs',target = data_subs_thread)
thread_voiz_terminal = threading.Thread(name ="voiz_terminal", target = voiz_terminal_thread)
thread_data_subs.start()
thread_voiz_terminal.start()

