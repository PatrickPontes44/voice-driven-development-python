"""
Main file of the VDD Project.
"""
import os
import time
import json
import sys
# speech recognition
import speech_recognition as sr
#pynput
from pynput.keyboard import Key
from pynput.keyboard import Controller as kController
from pynput.mouse import Button
from pynput.mouse import Controller as mController


class Vdd:
    def __init__(self, language="python"):
        self.__language = language
        self.__commands = ''
        self.__recognizer = sr.Recognizer()
        self.__speech = ''
        self.__mouse = mController()
        self.__keyboard = kController()
    
    def set_language(self, language):
        self.__language = language
        return True
    def set_commands(self, commands):
        self.__commands = commands
        return True
    def get_language(self) :
        return self.__language


    def read_commands(self):
        with open('./utils/{}.json'.format(self.__language), 'r') as json_file:
            try:
                commands = json.load(json_file)
                self.set_commands(commands)
            except Exception as e: 
                print('An error occurred!', e.__class__)
                return False

    def write_commands(self, command):
        try:
            if command in ["backspace", "erase"]:
                self.__keyboard.tap('backspace')
            elif command in ["enter", "next line"]:
                self.__keyboard.tap('enter')
            elif command in ["select all", "select everything", "control a", "command a"]:
                self.__keyboard.press('ctrl')
                self.__keyboard.press('a')
                self.__keyboard.release('ctrl')
                self.__keyboard.release('a')
            else:
                self.__keyboard.type(command)

            # for char in command:
            #     self.__keyboard.press(char)
            #     self.__keyboard.release(char)
            #     time.sleep(0.10)
        except Exception as e:
            print("An error occurred!", e.__class__)

        return

    def filter_command(self, command):
        if command in self.__commands.keys():
            return self.__commands[command]
        else:
            command = command + ' '
            return command
    
    def listen_commands(self):
        with sr.Microphone() as mic:
            self.__recognizer.adjust_for_ambient_noise(mic)

            while True:
                try:
                    print('>> :')
                    audio = self.__recognizer.listen(mic)
                        
                    speech = self.__recognizer.recognize_google(audio, language='en-US')
                    if speech == "close":
                        break
                    self.__speech = speech.lower()

                    command = self.filter_command(self.__speech)
                    self.write_commands(command)

                except Exception as e:
                    print ("An error occurred!", e.__class__)
            return
        
try:
    core = Vdd(sys.argv[1])
except Exception as e:
    core = Vdd()    

print(core.get_language())
core.read_commands()
core.listen_commands()