import time
import random
from PRINTPLUS import *
from savefile import *

def game():
    global mySave
    if mySave["location"]["level"] == "1":
        if mySave["location"]["part"] == "a":
            printplus("???", "£", "", ".....")
            printplus("???", "£", "", ".....")
            printplus("???", "£", "", ".....")
            printplus("???", "", "", "i havent seen you before")
            printplus("???", "", "", "well,£ I haven't seen anyone before,# really")
            printplus("???", "", "", "what am I?")
            printplus("???", "", "", "where# am# I?")
            printplus("???", "", "", "please,# please tell me who you are")
            printplus("???", "", "", "what is this world.#.# I can't remember anything.#.#")
            printplus("???", "", "", "I need your name\n££but don't go telling me it's different later,#\nI need to..# remember# something..")
            while mySave["user"]["name"] == "" or len(mySave["user"]["name"]) < 3: 
                mySave["user"]["name"] = input(("\n" * 50) + "(Enter your Name\nYou cannot change this later)\n\nName> ")
            while True: 
                mySave["user"]["gen"] = input(("\n" * 50) + "(Enter Gender)\n(This will impact the story)\n(You cannot change this later)\n\n(M/F)> ").upper()
                if mySave["user"]["gen"] == "M" or mySave["user"]["gen"] == "F":
                    break
            printplus("???", "", "", ".#.#.#okay")
            printplus("???", "", "", "..@" + str(mySave["user"]["name"]))
            printplus("???", "", "", "..@" + str(mySave["user"]["name"]))
            printplus("???", "", "", "i'll try to remember that")
            printplus("???", "", "", "hold on\n##are you#.#.")
            printplus("???", "", "", "..@WAIT!")
            printplus("Nothing", "#", "", ".....")
            printplus("Nothing", "#", "", ".....")
            printplus("Nothing", "#", "", ".....")
            printplus("Nothing", "#", "", ".....")
            printplus("Nothing", "#", "", ".....")
            printplus("Nothing", "#", "", ".....")
            mySave["location"]["level"] = "2"
            mySave["location"]["part"] = "a"
            f = open("savefile.py", "w")
            f.write("mySave=" + str(mySave))
            f.close()
            print("\n" * 200)
            game()
            return
    elif mySave["location"]["level"] == "2":
        if mySave["location"]["part"] == "a" and mySave["user"]["gen"] == "M":
            print("m route")
        elif mySave["location"]["part"] == "a" and mySave["user"]["gen"] == "F":
            print("f route")

            
if mySave["user"]["name"] == "":
    mySave = {"user" : {"name" : "", "gen" : ""}, "location" : {"level" : "1", "part" : "a"}}

game()













































