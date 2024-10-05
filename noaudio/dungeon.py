
from savedata import *

message = ""
def explore():
    global location
    global location_c
    global message
    lineskip()
    
    print("==========\nEXPLORATION OVERVIEW\n" + str(message) + "\n==========\n")

    if location_c["progress"] >= 10:
        print("1. Floor 1")
    if location_c["progress"] >= 15:
        print("2. Floor 2")
    if location_c["progress"] >= 30:
        print("3. Floor 3")
    if location_c["progress"] >= 40:
        print("4. Floor 4")
    if location_c["progress"] >= 50:
        print("5. Floor 5")

    print("0. Back")

    a=input("\n >")

    if a == "1" and location_c["progress"] >= 10:
        location["exact"] = 10
        floor()
    elif a == "2" and location_c["progress"] >= 15:
        location["exact"] = 20
        floor()
    elif a == "3" and location_c["progress"] >= 30:
        location["exact"] = 30
        floor()
    elif a == "4" and location_c["progress"] >= 40:
        location["exact"] = 40
        floor()
    elif a == "5" and location_c["progress"] >= 50:
        location["exact"] = 50
        floor()
    elif a == "0":
        menu_main()
    else:
        message = "Cannot explore here"
        explore()

    return
        

def floor():
    global location
    global location_c
    lineskip()

    location["floor"] = int(location["exact"] / 10)
    location["room"] = 0
    decision = 0

    print("==========\nFLOOR " + str(location["floor"]) + "\n==========\n")

    for i in range(1,9):
        if location_c[str(int(location["exact"] + i))] != "Blank":
            print(str(i) + ". Enter Room " + str(i))

    print("\n0. Back to overview")
    a=input("\n >")


    if a == "1" and location_c[str(int(location["exact"] + 1))] != "Blank":
        location["room"] = 1
        decision = 1
    elif a == "2" and location_c[str(int(location["exact"] + 2))] != "Blank":
        location["room"] = 2
        decision = 1
    elif a == "3" and location_c[str(int(location["exact"] + 3))] != "Blank":
        location["room"] = 3
        decision = 1
    elif a == "4" and location_c[str(int(location["exact"] + 4))] != "Blank":
        location["room"] = 4
        decision = 1
    elif a == "5" and location_c[str(int(location["exact"] + 5))] != "Blank":
        location["room"] = 5
        decision = 1
    elif a == "6" and location_c[str(int(location["exact"] + 6))] != "Blank":
        location["room"] = 6
        decision = 1
    elif a == "7" and location_c[str(int(location["exact"] + 7))] != "Blank":
        location["room"] = 7
        decision = 1
    elif a == "8" and location_c[str(int(location["exact"] + 8))] != "Blank":
        location["room"] = 8
        decision = 1
    elif a == "9" and location_c[str(int(location["exact"] + 9))] != "Blank":
        location["room"] = 9
        decision = 1
    elif a == "0":
        decision = 2
    else:
        decision = 3

    location["floor"] = int(location["exact"] / 10)

    if decision == 1:
        room()
    elif decision == 2:
        explore()
    elif decision == 3:
        floor()
        
    



def room():
    global location
    global location_c

    location["exact"] = int(location["floor"] * 10) + int(location["room"])
    location["contents"] = str(location_c[str(int(location["exact"]))])

    if location["contents"] == "Enemy":
        room_enemy()
    elif location["contents"] == "Chest":
        room_chest()
    elif location["contents"] == "Empty":
        room_empty()
    else:
        location["exact"] = int(location["floor"] * 10)
        floor()


#location_c[str(int(location["exact"]))] = "Empty"

def room_empty():
    lineskip()
    print("==========\nSilence fills the room from top to bottom.\nThe room is empty.\n==========\n")
    input("\nExit>")
    location["exact"] = int(location["floor"] * 10)
    floor()

    
def room_enemy():
    global startend
    lineskip()
    print("==========\nA monster lurks inside the room!\n==========\n")
    print("Fight it?")
    print("1. Yes")
    print("2. No")

    a=input("\n >")

    #1=Win,2=Lose,4=Invalid,3=Leave
    decision = 0

    if a == "1":
        result = battle_startend("Start")
        if result == "Victory":
            location_c["progress"] += 1
            decision = 1
        elif result == "Defeat":
            decision = 2
    elif a == "2":
        decision = 3
    else:
        decision = 4

    lineskip()

    if decision == 1:
        location_c[str(int(location["exact"]))] = "Empty"
        print("The room is now empty.\nYou decide to leave...")
        time.sleep(3)
        location["exact"] = int(location["floor"] * 10)
        floor()
    elif decision == 2:
        menu_main()
    elif decision == 3:
        print("You leave the monster be...")
        time.sleep(3)
        location["exact"] = int(location["floor"] * 10)
        floor()
    elif decision == 4:
        room_enemy()

def room_chest():
    startend = ""
    lineskip()
    print("==========\nA chest sits in the middle of the room.\nHow lucky!\n==========\n")
    print("Open it?")
    print("1. Yes")
    print("2. No")
    a=input("\n >")

    #DECISION: 1=WinBattle,2=GetItem,3=Leave,4=NoItem,5=LoseBattle
    decision = 0

    if a == "1":
        lineskip()
        location_c["progress"] += 1
        #rng determines whats in the chest
        rng = random.randint(1,3)
        if rng == 1:
            print("It's a trap!")
            time.sleep(2)
            #Start a battle
            result = battle_startend("Start")
            if result == "Victory":
                decision = 1
            elif result == "Defeat":
                decision = 5
        elif rng == 2:
            print("Weirdly enough, there is nothing inside.\nNot so lucky after all...")
            time.sleep(3)
            decision = 4
        elif rng == 3:
            print("get item")
            
    elif a == "2":
        decision = 3

    if decision == 1:
        lineskip()
        print("The room is now empty.\nYou decide to leave...")
        time.sleep(3)
        location_c[str(int(location["exact"]))] = "Empty"
        location["exact"] = int(location["floor"] * 10)
        floor()
    elif decision == 3:
        lineskip()
        print("You decide to leave")
        time.sleep(3)
        location["exact"] = int(location["floor"] * 10)
        floor()
    elif decision == 2 or decision == 4:
        lineskip()
        print("You decide to leave")
        time.sleep(3)
        location_c[str(int(location["exact"]))] = "Empty"
        location["exact"] = int(location["floor"] * 10)
        floor()
    elif decision == 5:
        welcome()
    else:
        room_chest()


def lineskip():
    print("\n" * 50)
