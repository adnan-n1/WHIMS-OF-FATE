import random
import time
from pygame import mixer
from savedata import *


# •

#Fire=HP based, Water=RES based, Wind=CRIT based

#Uncomment import mixer above^^ to turn on sound
#True = ON, False = OFF
#Fix line 882
if input("Music? (Y/N)\n >").lower() == "y": myMixerSwitch = True
else: myMixerSwitch = False

message = ""
battle_result = ""
old_player_stats=player_stats
old_player_inventory=player_inventory
old_location=location
old_location_c=location_c


def myMixer(decision):
  global myMixerSwitch
  decision = str(decision)
  
  if decision == "" or myMixerSwitch == False:
    return
  elif decision == "init":
    mixer.init()
  elif ".wav" in decision:
    try:
      mixer.Sound(decision).play()
    except Exception as e:
      print("Cannot play sound '" + str(decision) + "':\n" + str(e))
    
myMixer("init")

def menu_main(message):
  global player_stats
  global player_inventory
  global location_c
  global location
  global savedata
  global old_player_stats
  global old_player_inventory
  global old_location
  global old_location_c

  #Putting enemies in empty rooms to enable grinding
  for floors in location_c:
    #remove progress!!
    if floors != "progress":
      for rooms in location_c[floors]:
        if location_c[floors][rooms] == "Empty":
          location_c[floors][rooms] = "Grind"

  if message == "Game Over":
      player_stats=old_player_stats
      player_inventory=old_player_inventory
      location=old_location
      location_c=old_location_c
      message = "You were kicked out of the dungeon"
      
  player_stats["HP"] = player_stats["MHP"]
  print("\n" * 50)
  print("=====\nMain Menu\n=====\n" + str(message) + "\n=====\n")

  options = {"1" : "Explore Dungeon", "2" : "Learn Talents", "3" : "Check Stats","4" : "reset","5" : "exp", "0" : "Save Data"}



  for i in options:

    print(str(i) + ". " + str(options[i]))



  decision = input("\n >")

  if decision not in options:
    myMixer("menu_invalid.wav")
    menu_main("Invalid Option")
    return

  else:
    if options[decision] == "Save Data":
      myMixer("menu_enter.wav")
      for i in range(1,11):
          lineskip()
          print("Saving...\n[" + (make_progressbar(i,10,20)) + "] " + str(i*10) + "%")
          time.sleep(0.1)
      try:
          file = open("savedata.py","w")
          file.write("player_stats=" + str(player_stats))
          file.write("\nplayer_inventory=" + str(player_inventory))
          file.write("\nlocation=" + str(location))
          file.write("\nlocation_c=" + str(location_c))
          file.close()
          #Old data to load when Game Over
          old_player_stats=player_stats
          old_player_inventory=player_inventory
          old_location=location
          old_location_c=location_c
          menu_main("Data saved successfully!")
          return
      except Exception as e:
          myMixer("menu_invalid.wav")
          menu_main("Save failed:\n" + str(e))
          return
    elif options[decision] == "Explore Dungeon":
      myMixer("menu_enter.wav")
      explore()

    elif options[decision] == "Learn Talents":
      myMixer("menu_enter.wav")
      menu_inventory(player_inventory)

    elif options[decision] == "Check Stats":
      myMixer("menu_enter.wav")
      lineskip()
      print("=====\nCheck\n=====\n")
      print("=====\n" + str(player_stats["name"].upper()) + " Lvl." + str(player_stats["LVL"]) + "\n=====\n")
      print("(" + str(player_stats["EXP"]) + "/" + str(player_stats["MEXP"]) + "EXP)")
      print("\nHP: " + str(player_stats["HP"]) + "/" + str(player_stats["MHP"]))
      print("STR:[" + str(player_stats["STR"]) + str(make_progressbar(player_stats["STR"]-100,100,20)) + "]\nRES: [" + str(player_stats["RES"]) + str(make_progressbar(player_stats["RES"],100,20)) + "]\nEVA: [" + str(player_stats["EVA"]) + str(make_progressbar(player_stats["EVA"],100,20)) + "]\nCRIT:[" + str(player_stats["CRIT"]) + str(make_progressbar(player_stats["CRIT"],100,20)) + "]")
      print("\nFusion:")
      print("   - " + str(player_stats["fusion"][0]))
      print("   - " + str(player_stats["fusion"][1]))
      print("Moves:")
      for move in player_stats["moves"]:
          print("   • " + str(move) + " - " + str(battle_moveslookup(move)[7]))
      print("Weakness:\n   - " + str(player_stats["weakness"]))

      input("\nBack>")
      myMixer("menu_back.wav")
      menu_main("Select an Option")

      return

    elif options[decision] == "exp":
      myMixer("menu_enter.wav")
      amount = 50000
      player_stats = battle_levelup(player_stats,amount)

      menu_main("Earned " + str(amount) + " EXP")
  
      return

    elif options[decision] == "reset":
      #BASE STATS
      myMixer("menu_enter.wav")
      player_stats = {'name': 'Navee',
                      'weapon': 'Gold Sword',
                      'LVL': 1, 'MEXP': 100, 'EXP': 0,
                      'MHP': 250,'HP': 250,
                      'STR': 100, 'RES': 0, 'CRIT': 5, 'EVA': 5,
                      'buff': {}, 'debuff': {},
                      "charms" : [],
                      'fusion': ['Wind Type 01', 'Landing CRIT hits regenerate 1% HP'],
                      'moves': {'Lunge': 0,"Garu" : 0, "Dia" : 0},
                      "weakness" : "Fire"}
      player_inventory={'Skill Cards': {}, 'Fusion Cards': {},"Support Items" : {}}
      location={'contents': 'Chest','exact': ["A","1"]}
      location_c={"progress" : 10,
                  "A" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest"},
                  "B" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Miniboss"},
                  "C" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Chest",
                         "5" : "Enemy"},
                  "D" : {"1" : "Chest",
                         "2" : "Enemy",
                         "3" : "Enemy",
                         "4" : "Enemy",
                         "5" : "Chest",
                         "6" : "Miniboss"},
                  "E" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Enemy",
                         "5" : "Enemy",
                         "6" : "Enemy",
                         "7" : "Enemy"},
                  "F" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Enemy",
                         "5" : "Chest",
                         "6" : "Enemy",
                         "7" : "Enemy",
                         "8" : "Miniboss"},
                  "G" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Enemy",
                         "5" : "Chest",
                         "6" : "Enemy",
                         "7" : "Enemy",
                         "8" : "Enemy",
                         "9" : "Enemy"},
                  "H" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Enemy",
                         "5" : "Chest",
                         "6" : "Enemy",
                         "7" : "Enemy",
                         "8" : "Enemy",
                         "9" : "Miniboss"},
                  "I" : {"1" : "Enemy",
                         "2" : "Enemy",
                         "3" : "Chest",
                         "4" : "Enemy",
                         "5" : "Chest",
                         "6" : "Enemy",
                         "7" : "Enemy",
                         "8" : "Enemy",
                         "9" : "Enemy"},
                  }
      menu_main("All stats reset")     
      return

    else:
      myMixer("menu_invalid.wav")
      menu_main("Invalid Option")

      return













def menu_inventory(inventory):
  global player_stats
  global player_inventory
  lineskip()


  #Display skill cards owned
  print("SKILL CARDS:")
  for skill in inventory["Skill Cards"]:
    if skill in player_stats["moves"]:
      print(" • " + str(skill) + " - (" + str(inventory["Skill Cards"][skill]["Owned"]) + "/" + str(inventory["Skill Cards"][skill]["Required"]) + ") Equipped")
    elif inventory["Skill Cards"][skill]["Owned"] >= inventory["Skill Cards"][skill]["Required"]:
      print(" • " + str(skill) + " - (" + str(inventory["Skill Cards"][skill]["Owned"]) + "/" + str(inventory["Skill Cards"][skill]["Required"]) + ") Available now!")
    elif inventory["Skill Cards"][skill]["Owned"] > 0:
      print(" • " + str(skill) + " - (" + str(inventory["Skill Cards"][skill]["Owned"]) + "/" + str(inventory["Skill Cards"][skill]["Required"]) + ")")


  #Display fusion cards owned
  print("\nFUSION CARDS:")
  for fusion in inventory["Fusion Cards"]:
    if player_stats["fusion"][0] == fusion:
      print(" • " + str(fusion) + " - (" + str(inventory["Fusion Cards"][fusion]["Owned"]) + "/" + str(inventory["Fusion Cards"][fusion]["Required"]) + ") Equipped")
    elif inventory["Fusion Cards"][fusion]["Owned"] >= inventory["Fusion Cards"][fusion]["Required"]:
      print(" • " + str(fusion) + " - (" + str(inventory["Fusion Cards"][fusion]["Owned"]) + "/" + str(inventory["Fusion Cards"][fusion]["Required"]) + ") Available now!")
    elif inventory["Fusion Cards"][fusion]["Owned"] > 0:
      print(" • " + str(fusion) + " - (" + str(inventory["Fusion Cards"][fusion]["Owned"]) + "/" + str(inventory["Fusion Cards"][fusion]["Required"]) + ")")

  print("")
  options = {"1" : "Learn Skills", "2" : "Learn Fusions", "3" : "Sacrifice"}

  for i in options:
    print(str(i) + ". " + str(options[i]))
  print("Back")


  decision = input("\n >")
  
  if decision.lower() == "back" or decision.lower() == "b":
    myMixer("menu_back.wav")
    player_inventory = inventory
    menu_main("Select an Option")
    return
  elif decision not in options:
    myMixer("menu_invalid.wav")
    menu_inventory(inventory)
    return
  else:
    myMixer("menu_enter.wav")
    if options[decision] == "Learn Skills":

      message = "Choose Skill to Learn"

      while True:
        lineskip()
        print("=====\nLearn Skills\n" + str(message) + "\n=====\n")
        options = {}
        count = 1

        for i in inventory["Skill Cards"]:
          if inventory["Skill Cards"][i]["Owned"] >= inventory["Skill Cards"][i]["Required"] and i not in player_stats["moves"]:
            options[str(count)] = i
            count += 1
        for i in options:
          print(str(i) + ". " + options[i] + " (" + str(battle_moveslookup(options[i])[7]) + ")")

        print("Back")

        decision = input("\n >")

        #Go back a menu
        if decision.lower() == "back" or decision.lower() == "b":
          myMixer("menu_back.wav")
          menu_inventory(inventory)
          return
          break
        #Input invalid
        elif decision not in options:
          myMixer("menu_invalid.wav")
          message = "Invalid Skill"
          pass
        #Enough cards required and there is space in Player move list
        elif inventory["Skill Cards"][options[decision]]["Owned"] >= inventory["Skill Cards"][options[decision]]["Required"] and len(player_stats["moves"]) < 6:
          player_stats["moves"][options[decision]] = 0
          myMixer("menu_skilllearnt.wav")
          message = str(options[decision]) + " learnt!"
        #Enough cards required but not enough space in Player move list. Must replace a skill
        elif inventory["Skill Cards"][options[decision]]["Owned"] >= inventory["Skill Cards"][options[decision]]["Required"] and len(player_stats["moves"]) >= 6:
          message = "Choose a Skill to replace with '" + str(options[decision]) + "'"
          while True:
            lineskip()
            print("=====\nStock Full!\n=====\n" + str(message) + "\n=====\n")
            options1 = {}
            count = 1
            for skill in player_stats["moves"]:
              options1[str(count)] = skill
              count += 1
            for skill in options1:
              print(str(skill) + ". " + str(options1[skill]) + " (" + str(battle_moveslookup(options1[skill])[7]) + ")")
            print("Back")
            decision1 = input("\n>")

            if decision1.lower() == "back" or decision1.lower() == "b":
              message = "Choose Skill to learn"
              myMixer("menu_back.wav")
              break
            elif decision1 not in options1:
              myMixer("menu_invalid.wav")
              message = "Invalid Skill. Choose a Skill to replace with '" + str(options[decision]) + "'"
            else:
              #Removing old skill and replacing with new one
              player_stats["moves"].pop(options1[decision1])
              player_stats["moves"][options[decision]] = 0
              myMixer("menu_skilllearnt.wav")
              message = str(options[decision]) + " learnt!"
              break
            
        else:
          myMixer("menu_invalid.wav")
          message = "Cannot learn " + str(options[decision]) + " yet!"

    elif options[decision] == "Learn Fusions":

      message = "Choose Fusion to Learn"
      while True:
        lineskip()
        print("=====\nLearn Fusions\n" + str(message) + "\n=====\n")
        options = {}
        count = 1

        for i in inventory["Fusion Cards"]:
          if inventory["Fusion Cards"][i]["Owned"] >= inventory["Fusion Cards"][i]["Required"] and i != player_stats["fusion"][0]:
            options[str(count)] = i
            count += 1
        for i in options:
          print(str(i) + ". " + str(options[i]) + " (" + str(getfusion(options[i])[1]) + ")")
        print("Back")

        decision = input("\n >")

        if decision.lower() == "back" or decision.lower() == "b":

          myMixer("menu_back.wav")
          menu_inventory(inventory)
          return
          break

        elif decision not in options:
          myMixer("menu_invalid.wav")
          message = "Invalid Fusion"
          pass

        elif inventory["Fusion Cards"][options[decision]]["Owned"] >= inventory["Fusion Cards"][options[decision]]["Required"]:
          player_stats["fusion"] = getfusion(options[decision])
          if "Fire" in player_stats["fusion"][0]: player_stats["weakness"] = "Water"
          elif "Water" in player_stats["fusion"][0]: player_stats["weakness"] = "Wind"
          elif "Wind" in player_stats["fusion"][0]: player_stats["weakness"] = "Fire"
          else: player_stats["weakness"] = ""
          myMixer("menu_fusionlearnt.wav")
          message = "You've become one with " + str(options[decision]) + "!"

        else:
          myMixer("menu_invalid.wav")
          message = "Cannot fuse with " + str(options[decision]) + " yet!"

    elif options[decision] == "Sacrifice":
      message = "Choose Skill cards to Sacrifice"
      while True:
        lineskip()
        print("=====\nSacrifice\n" + str(message) + "\n=====\n")
        options = {}
        count = 1
        #add the options
        for i in inventory["Skill Cards"]:
          if inventory["Skill Cards"][i]["Owned"] > 0:
            options[str(count)] = i
            count += 1

        #display the options
        for i in options:
          print(str(i) + ". " + options[i] + " (" + str(inventory["Skill Cards"][options[i]]["Owned"]) + ")")
        options["0"] = "-Sacrifice All-"
        print("0. " + str(options["0"]))
        print("Back")

        decision = input("\n >")

        if decision.lower() == "back" or decision.lower() == "b":
          myMixer("menu_back.wav")
          menu_inventory(inventory)
          return
          break

        elif decision not in options:
          myMixer("menu_invalid.wav")
          message = "Invalid Skill"
          pass
        
        elif options[decision] == "-Sacrifice All-":
          myMixer("menu_enter.wav")
          while True:
            lineskip()
            print("=====\nAre you sure you want to Sacrifice ALL your Skill Cards?\n=====")

            a=input("\nY/N >")
            if a.lower() == "y":
              #amount is The EXP of how many cards have been sacrificed
              amount = 0
              for card in inventory["Skill Cards"]:
                while inventory["Skill Cards"][card]["Owned"] > 0:
                  inventory["Skill Cards"][card]["Owned"] -= 1
                  amount += random.randint(200,225)
              inventory["Skill Cards"] = {}
              message = "Sacrificed everything successfully"
              player_stats = battle_levelup(player_stats, amount)
              break
            elif a.lower() == "n":
              myMixer("menu_back.wav")
              message = "Choose Skill cards to Sacrifice"
              break
              
              
        elif inventory["Skill Cards"][options[decision]]["Owned"] > 0:
          myMixer("menu_enter.wav")
          while True:
            lineskip()
            print("=====\nAre you sure you want to Sacrifice one\n'" + str(options[decision]) + "' Card?\n=====")
            a=input("\nY/N >")

            if a.lower() == "y":
              myMixer("menu_enter.wav")
              inventory["Skill Cards"][options[decision]]["Owned"] -= 1

              if inventory["Skill Cards"][options[decision]]["Owned"] <= 0:
                inventory["Skill Cards"].pop([options[decision]])

              player_stats = battle_levelup(player_stats, random.randint(200,225))

              message = "Sacrificed '" + str(options[decision]) + "' successfully"

              break

            elif a.lower() == "n":
              myMixer("menu_back.wav")
              message = "Choose Skill cards to Sacrifice"

              break

        else:
          myMixer("menu_invalid.wav")
          message = "Cannot Sacrifice " + str(options[decision]) + "!"

def getcharm(charm):
  charm = {
    "Fire Emblem" : "Increases Fire damage by 10%",
    "Water Emblem" : "Increases Water damage by 10%",
    "Wind Emblem" : "Increases Wind damage by 10%",
    "Power Emblem" : "Increases Physical damage by 15%"
    }

  output = [charm,"?????"]
  for i in charms:
    if charm == charms[i]:
      output = [charm,charms[i]]
      break

  return output


def getfusion(fusion):

  fusions = [

  {"Abyss Type 01" : "When taking a hit, gain 1 Spiral stack, increasing DMG by 6%. Max 5 stacks.",

  "Abyss Type 02" : "When landing a hit with an Element, "},

  {"Wind Type 01" : "Landing CRIT hits regenerate 1% HP"

  ,"Wind Type 02" : "When HP below 70%, increases CRIT by 30"

  ,"Wind Type 03" : "Increases Wind damage by 25%"

  ,"Wind Type 04" : "When in Critical condition, increases CRIT by 50% and increases CRIT damage by 30%"

  ,"Wind Type 05" : "Landing CRIT hits regenerate 5% HP"

  ,"Wind Type 06" : "Increases Wind damage by 50%"

  ,"Wind Type 07" : "When HP below 50%, CRIT damage increased by 75%"

  ,"Wind Type 08" : "Getting hit by a CRIT hit provides 5% HP to self"

  ,"Wind Type 09" : "CRIT damage increased by 75%"

  ,"Prototype: GALE" : "Use the might of GALE, gaining the power to control all raging tempests: Removes enemy's CRIT DMG bonuses. When above 50% HP, increases CRIT by 20 and CRIT damage by 100%. When below 50% HP, increases CRIT by 40 and CRIT damage by 50%. Obtain all CRIT bonuses when in Critical condition"},



  {"Fire Type 01" : "All damage increased by 2% Max HP"

  ,"Fire Type 02" : "When in Critical condition, regenerate 2% HP every turn"

  ,"Fire Type 03" : "Increases Fire damage by 25%"

  ,"Fire Type 04" : "When in Critical condition, All damage is increased by 5% Max HP"

  ,"Fire Type 05" : "Using 'Attack' increases its damage by 100%, but drains 10% HP from self"

  ,"Fire Type 06" : "Increases Fire damage by 50%"

  ,"Fire Type 07" : "Increases Healing effectiveness by 100%"

  ,"Fire Type 08" : "When in Critical condition, inflicts 'Vulnerable' on opponent and inflicts 'Charged' on self"

  ,"Fire Type 09" : "All damage is increased by 5% Max HP. This effect is doubled when in Critical condition"

  ,"Prototype: BLZE" : "Use the might of BLZE, gaining the power to ignite cataclysms: Landing hits drains 5% HP from self. When below 50% Max HP, All damage increased by 20% Max HP. Damage bonuses gained is doubled when in Critical condition"},


  {"Water Type 01" : "RES is doubled when in Critical condition",
   
   "Water Type 02" : "Increases Physical damage by 50%",
   
   "Water Type 03" : "Increases Water damage by 25%",

   "Water Type 04" : "When hit by a CRIT hit, 50% chance to block the attack",
   
   "Water Type 05" : "Increases Physical damage by 75%",
   
   "Water Type 06" : "Increases Water damage by 50%",

  "Water Type 07": "Take 33% less Elemental damage",

  "Water Type 08": "When taking a CRIT or WEAK Hit, applies the 'Resistance' buff onto self and applies the 'Drained' debuff onto opponent.",

  "Water Type 09": "Effects of Buffs and Debuffs for opponent are doubled.",

  "Prototype: AQUA": "Use the might of AQUA, gaining the power to manipulate currents: When taking a hit, applies the 'Awakened' buff to self, increasing all Elemental damage by 60% and increasing RES by 60%. The effects of any Buffs, including 'Awakened', on self are doubled in Critical condition."}]

  output = [0,0]
  for i in fusions:
    if fusion in i:
      output = [fusion, i[fusion]]

  if output == [0,0]:
    output = [fusion,"?????"]

  #e.g output = ["Wind Type 01", "Passive, etc ..."]
  return output


def battle_levelup(player_stats, exp):
  levelups = 0
  baseexp = exp
  while exp > 0:
    print("\n" * 20)
    if exp >= (int(baseexp * 0.01)):
        #earning exp
      player_stats["EXP"] += int(baseexp * 0.01)
      exp -= int(baseexp * 0.01)
    else:
      player_stats["EXP"] += 1
      exp -= 1



    if player_stats["EXP"] >= player_stats["MEXP"]:
        #level up!
      player_stats["EXP"] = 0
      player_stats["MEXP"] += 25
      levelups += 1
    print(str(player_stats["name"]) + " • LVL " + str(player_stats["LVL"]+levelups) + "\n["+  make_progressbar(player_stats["EXP"], player_stats["MEXP"], 20) + "] " + str(player_stats["EXP"]) + "/" + str(player_stats["MEXP"]) + "EXP")
    if exp > 0:
      print("   Earned +" + str(exp) + " EXP")
    time.sleep(0.02)



  if levelups > 0:
    print("\nLVL UP! " + str(player_stats["LVL"]) + " -> " + str(player_stats["LVL"] + levelups))
    player_stats["LVL"] += levelups
  stats_choice = ["RES", "CRIT", "EVA", "MHP", "STR"]
  stats_new = {"RES" : 0, "CRIT" : 0, "EVA" : 0, "MHP" : 0, "STR" : 0}



  while levelups > 0:
    levelups -= 1
    loops = 5
    while loops > 0:
      rng = random.choice(stats_choice)
      if rng == "MHP":
        stats_new[rng] += random.randint(40,50)
      else:
        stats_new[rng] += 1
      loops -= 1



  for i in stats_choice:
    if stats_new[i] > 0:
      print(str(i) + " UP! " + str(player_stats[i]) + " -> " + str(player_stats[i] + stats_new[i]))
      player_stats[i] += stats_new[i]



  input("\nContinue>")
  myMixer("menu_enter.wav")

  return player_stats



def battle_drops(inventory, drops):
  print("")

  if "Skill Cards" in drops:
    if len(drops["Skill Cards"]) > 0:

      rng = random.choice(drops["Skill Cards"])

      if rng in inventory["Skill Cards"]:
        inventory["Skill Cards"][rng]["Owned"] += 1
        if inventory["Skill Cards"][rng]["Owned"] >= inventory["Skill Cards"][rng]["Required"]:
          inventory["Skill Cards"][rng]["Owned"] = inventory["Skill Cards"][rng]["Required"]
      else:
        inventory["Skill Cards"][rng] = {"Required" : 2, "Owned" : 1}

      print("Earned '" + str(rng) + "'! (" + str(inventory["Skill Cards"][rng]["Owned"]) + "/" + str(inventory["Skill Cards"][rng]["Required"]) + ")")

  if "Fusion Cards" in drops:
    if len(drops["Fusion Cards"]) > 0:
      rng = random.choice(drops["Fusion Cards"])

      if rng in inventory["Fusion Cards"]:
        inventory["Fusion Cards"][rng]["Owned"] += 1
        if inventory["Fusion Cards"][rng]["Owned"] >= inventory["Fusion Cards"][rng]["Required"]:
          inventory["Fusion Cards"][rng]["Owned"] = inventory["Fusion Cards"][rng]["Required"]
      else:
        inventory["Fusion Cards"][rng] = {"Required" : 3, "Owned" : 1}
        
      print("Earned '" + str(rng) + "'! (" + str(inventory["Fusion Cards"][rng]["Owned"]) + "/" + str(inventory["Fusion Cards"][rng]["Required"]) + ")")

  if "Support Items" in drops:
    if len(drops["Support Items"]) > 0:

      rng = random.choice(drops["Support Items"])
      
      if rng in inventory["Support Items"]:
        inventory["Support Items"][rng] += 1
      else:
        inventory["Support Items"][rng] = 1

      print("Earned " + str(rng) + "!")

  if "Key Items" in drops:
    if len(drops["Key Items"]) > 0:

      rng = random.choice(drops["Key Items"])
      
      if rng in inventory["Key Items"]:
        inventory["Key Items"][rng] += 1
      else:
        inventory["Key Items"][rng] = 1

      print("Earned " + str(rng) + "!")

    

  myMixer("menu_enter.wav")
  input("\nContinue>")

  return inventory

def printplus(title, auto, speed, text):
    #   TITLE The starting text that comes before Content
    #   SPEED # = Slow, @ = Slower, £ = Slowest
    #   AUTO  Symbols = Continue without input for (#@£) seconds long
    #   TEXT The content to be outputted

    #Symbols represent time to pause for (seconds)
    symbols_all = {"#" : 0.2, "@" : 0.3, "£" : 0.4, "Other" : 0.03}
    output = str(title) + "\n\n"
    text = str(text)
    count = 3
    if str(speed) in symbols_all:
        speed = symbols_all[str(speed)]
    else:
        speed = symbols_all["Other"]
    for letter in text:
        letter = str(letter)
        if letter in symbols_all:
            time.sleep(symbols_all[str(letter)])
        else:
            time.sleep(speed)
            if (count % 3) == 0: myMixer("menu_text.wav")
            output += letter
            print("\n" * 50)
            print(output)
            count += 1

    if auto in symbols_all:
        time.sleep(symbols_all[str(auto)])
    else:
        input(" >")

def get_enemies():
  #Enemy names:
  #Elemental, Fighter, Guardian, Sentinel
  enemies = [

    {"name" : "Wind Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 25, "RES" : 1, "CRIT" : 30, "EVA" : 5, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 01", "Landing CRIT hits regenerate 1% HP"], "moves" : {"Thousand Slaps":0, "Garu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Thousand Slaps"], "Fusion Cards" : ["Wind Type 01"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 50, "RES" : 2, "CRIT" : 30, "EVA" : 10, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 02", "When HP below 70%, increases CRIT by 30"], "moves" : {"Attack":0, "Garu":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Garu"], "Fusion Cards" : ["Wind Type 02"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 75, "RES" : 3, "CRIT" : 30, "EVA" : 15, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 03", "Increases Wind damage by 25%"], "moves" : {"Attack":0, "Garu":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Garu"], "Fusion Cards" : ["Wind Type 03"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 30, "EVA" : 20, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 04", "When in Critical condition, increases CRIT  by 50% and increases CRIT damage by 30%"], "moves" : {"Attack":0, "Garula":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Garula"], "Fusion Cards" : ["Wind Type 04"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 125, "RES" : 5, "CRIT" : 30, "EVA" : 25, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 05", "Landing CRIT hits regenerate 5% HP"], "moves" : {"Attack":0, "Cyclone":0, "Garula" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Cyclone","Garula"], "Fusion Cards" : ["Wind Type 05"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 150, "RES" : 6, "CRIT" : 30, "EVA" : 30, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 06", "Increases Wind damage by 50%"], "moves" : {"Attack":0, "Garula":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Garula"], "Fusion Cards" : ["Wind Type 06"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 175, "RES" : 7, "CRIT" : 30, "EVA" : 35, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 07", "When HP below 50%, CRIT damage increased by 75%"], "moves" : {"Attack":0, "Garudyne":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Garudyne"], "Fusion Cards" : ["Wind Type 07"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 200, "RES" : 8, "CRIT" : 30, "EVA" : 40, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 08", "Getting hit by a CRIT hit provides 5% HP to self"], "moves" : {"Attack":0, "Garudyne":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Garudyne"], "Fusion Cards" : ["Wind Type 08"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 225, "RES" : 9, "CRIT" : 30, "EVA" : 45, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 09", "CRIT damage increased by 75%"], "moves" : {"Cyclone":0, "Garubarion":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Cyclone", "Garubarion"], "Fusion Cards" : ["Wind Type 09"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Kaze", "LVL" : 45, "MHP" : 3000, "HP" : 3000, "STR" : 300, "RES" : 10, "CRIT" : 30, "EVA" : 50, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: GALE", "Use the might of GALE, gaining the power to control all raging tempests: Removes enemy's CRIT DMG bonuses. When above 50% HP, increases CRIT by 20 and CRIT damage by 100%. When below 50% HP, increases CRIT by 40 and CRIT damage by 50%. Obtain all CRIT bonuses when in Critical condition"], "moves" : {"Wrath Tempest":0,"Cyclone":0,"Concentrate":0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Cyclone","Concentrate","Wrath Tempest"], "Fusion Cards" : ["Prototype: GALE"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Fire Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 25, "RES" : 1, "CRIT" : 2, "EVA" : 5, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 01", "All damage increased by 2% Max HP"], "moves" : {"Attack":0, "Agi":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 01"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 50, "RES" : 2, "CRIT" : 4, "EVA" : 10, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 02", "When in Critical condition, regenerate 2% HP"], "moves" : {"Attack":0, "Agi":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 02"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 75, "RES" : 3, "CRIT" : 6, "EVA" : 15, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 03", "Increases Fire damage by 25%"], "moves" : {"Attack":0, "Agi":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 03"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 8, "EVA" : 20, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 04", "When in Critical condition, All damage is increased by 5% Max HP"], "moves" : {"Agilao":0, "Attack":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Agilao"], "Fusion Cards" : ["Fire Type 04"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 125, "RES" : 5, "CRIT" : 10, "EVA" : 25, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 05", "Using 'Attack' increases its damage by 100%, but drains 10% HP from self"], "moves" : {"Attack":0, "Charge":0, "Megido" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Charge", "Agilao", "Megido"], "Support Items" : ["Molotov"], "Fusion Cards" : ["Fire Type 05"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 150, "RES" : 6, "CRIT" : 12, "EVA" : 30, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 06", "Increases Fire damage by 50%"], "moves" : {"Attack":0, "Concentrate":0, "Agilao" : 0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Concentrate", "Agilao"], "Fusion Cards" : ["Fire Type 06"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 175, "RES" : 7, "CRIT" : 14, "EVA" : 35, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 07", "Increases Healing effectiveness by 100%"], "moves" : {"Dia":0, "Agidyne":0, "Attack" : 0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Dia", "Agidyne"], "Fusion Cards" : ["Fire Type 07"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 200, "RES" : 8, "CRIT" : 16, "EVA" : 40, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 08", "When in Critical condition, inflicts 'Vulnerable' on opponent and inflicts 'Charged' on self"], "moves" : {"Attack":0, "Agidyne":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Agidyne"], "Fusion Cards" : ["Fire Type 08"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 225, "RES" : 9, "CRIT" : 18, "EVA" : 45, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 09", "All damage is increased by 5% Max HP. This effect is doubled when in Critical condition"], "moves" : {"Attack":0, "Agibarion":0, "Fire Dance" : 0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Agibarion", "Fire Dance"], "Fusion Cards" : ["Fire Type 09"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Hi'", "LVL" : 45, "MHP" : 5000, "HP" : 5000, "STR" : 300, "RES" : 10, "CRIT" : 20, "EVA" : 75, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: BLZE", "Use the might of BLZE, gaining the power to ignite cataclysms: Landing hits drains 5% HP from self. When below 50% Max HP, All damage increased by 20% Max HP. Damage bonuses gained is doubled when in Critical condition"], "moves" : {"Concentrate":0,'Burning Hell': 0, "Fire Dance" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Burning Hell", "Fire Dance"], "Fusion Cards" : ["Prototype: BLZE"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Water Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 25, "RES" : 10, "CRIT" : 2, "EVA" : 5, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 01", "RES is doubled when in Critical condition"], "moves" : {"Attack":0, "Bufu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Bufu"], "Fusion Cards" : ["Water Type 01"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 50, "RES" : 2, "CRIT" : 4, "EVA" : 10, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 02", "Increases Physical damage by 50%"], "moves" : {"Attack" : 0,"Megido":0, "Bufu":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Bufu", "Megido"], "Fusion Cards" : ["Water Type 02"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 75, "RES" : 3, "CRIT" : 6, "EVA" : 15, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 03", "Increases Water damage by 25%"], "moves" : {"Attack":0, "Rush":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Rush"], "Fusion Cards" : ["Water Type 03"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 8, "EVA" : 20, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 04", "When hit by a CRIT hit, 50% chance to block the attack"], "moves" : {"Bufula":0, "Attack":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Bufula"], "Fusion Cards" : ["Water Type 04"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 125, "RES" : 5, "CRIT" : 10, "EVA" : 25, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 05", "Increases Physical damage by 75%"], "moves" : {"Megido":0, "Charge":0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Charge"], "Fusion Cards" : ["Water Type 05"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 150, "RES" : 6, "CRIT" : 12, "EVA" : 30, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 06", "Increases Water damage by 50%"], "moves" : {"Bufula":0, "Concentrate":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Bufula"], "Fusion Cards" : ["Water Type 06"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 175, "RES" : 7, "CRIT" : 14, "EVA" : 35, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 07", "Take 33% less Elemental damage"], "moves" : {"Bufula":0, "Resist":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Resist"], "Fusion Cards" : ["Water Type 07"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 200, "RES" : 8, "CRIT" : 16, "EVA" : 40, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 08", "When taking a CRIT or WEAK Hit, applies the 'Resistance' buff onto self and applies the 'Drained' debuff onto opponent."], "moves" : {"Bufudyne":0, "Drain Energy":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Drain Energy","Bufudyne"], "Fusion Cards" : ["Water Type 08"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 225, "RES" : 9, "CRIT" : 18, "EVA" : 45, "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 09", "Effects of Buffs and Debuffs are doubled."], "moves" : {"Bufubarion":0, "Megidola" : 0,"Charge":0,"Debilitate":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Debilitate","Charge","Megidola","Bufubarion"], "Fusion Cards" : ["Water Type 09"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Mizu", "LVL" : 45, "MHP" : 3000, "HP" : 3000, "STR" : 300, "RES" : 10, "CRIT" : 20, "EVA" : 75, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: AQUA", "Use the might of AQUA, gaining the power to manipulate currents: When taking a hit, applies the 'Awakened' buff to self, increasing all Elemental damage by 60% and increasing RES by 60%. The effects of any Buffs on self are doubled in Critical condition."], "moves" : {"Thalassic Calamity":0, "Bufubarion" : 0,"Concentrate":0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Thalassic Calamity","Concentrate"], "Fusion Cards" : ["Prototype: AQUA"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"}
     ]
  return enemies

def battle_startend(status):
  global sound
  global battle_result
  global player_stats
  global enemy_stats
  global player_inventory
  global location

  #All enemies
  all_enemies = get_enemies()
  #Enemies selected for battle, suitable for floor
  rng_enemies = []
  #boss: Indicator to play Boss music or not
  boss = False

  
  #if location_c[location["exact"][0]][location["exact"][1]] == "Boss":

  #Miniboss is 5 levels above normal
  if location_c[location["exact"][0]][location["exact"][1]] == "Miniboss":
    boss = True
    for enemy in all_enemies:
      #If enemy is 1 ABOVE current floor difficulty
      if enemy["LVL"] == ((ord(location["exact"][0])-63)*5):
        rng_enemies.append(enemy)
  elif location_c[location["exact"][0]][location["exact"][1]] == "Enemy" or location_c[location["exact"][0]][location["exact"][1]] == "Chest" or location_c[location["exact"][0]][location["exact"][1]] == "Grind":
    if location["exact"][0] == "A":
      for enemy in all_enemies:
        if enemy["LVL"] == 1:
          rng_enemies.append(enemy)
    else:
      for enemy in all_enemies:
        #If enemy is AT current floor difficulty
        if enemy["LVL"] == ((ord(location["exact"][0])-64)*5):
          rng_enemies.append(enemy)

  #Random enemy chosen
  enemy_stats = random.choice(rng_enemies)

  lineskip()
  if boss == True:  printplus("=====\nBATTLE START!\n=====", "£", "", "You are fighting:# " + str(enemy_stats["name"]) + " (BOSS)")
  else: printplus("=====\nBATTLE START!\n=====", "£", "", "You are fighting:# " + str(enemy_stats["name"]))
  
  #Play battle/boss music depending on situation
  #FINISH myMixer()
  if myMixerSwitch == True:
    if boss == True and (ord(location["exact"][0])-64) >= 6:  mixer.music.load("boss_vocal.wav")
    elif boss == False and (ord(location["exact"][0])-64) > 3:  mixer.music.load("battle_vocal.wav")
    elif boss == True and (ord(location["exact"][0])-64) < 6: mixer.music.load("boss.wav")
    else: mixer.music.load("battle.wav")
        
    mixer.music.set_volume(0.2)
    mixer.music.play(loops=99)
    if boss == True:  time.sleep(7.2)
    else: time.sleep(1.4)
  #Start the battle with player and enemy stats
  battle_player(player_stats, enemy_stats)
  #Stop battle music

  if myMixerSwitch == True: mixer.music.fadeout(3000)

  lineskip()
  if battle_result == "Victory":
    printplus("=====\nBATTLE: VICTORY!\n=====", "", "", "You won!")
    myMixer("menu_enter.wav")

    player_stats = battle_levelup(player_stats, enemy_stats["drops"]["EXP"])

    player_inventory = battle_drops(player_inventory, enemy_stats["drops"])


  elif battle_result == "Defeat":
    messages = ["Watch your health!",
                "Defend against strong attacks!",
                "Use Skills effectively!",
                "Gain extra turns using CRIT and Weaknesses!"]
    printplus("=====\nBATTLE: DEFEAT!\n=====", "", "", random.choice(messages))
    myMixer("menu_back.wav")

  else:
    print("Error: " + str(status))

  return battle_result



def battle_moveslookup(move):
  #Light, Weak, Medium, Heavy, Severe, Colossal
  #"Name : [BaseDMG, Range of hits, Type Offence/Defence/Heal, Buff/Debuff infliction, Element, Unique attribute]"
  all_moves = {"Nothing" : [0, [0,0], "Other", "None","",""]
                  #Healing
                  ,"Dia" : [0, [0,0], "Heal", "None","",""]
                  #Physical
                  , "Attack" : [90, [1,0], "Offence", "None","Physical",""]
                  ,"Thousand Slaps" : [10, [10,0], "Offence", "None","Physical",""]
                  ,"Lunge" : [100, [1,0], "Offence", "None","Physical","High Critical rate"]
                  ,"Megi" : [150, [1,0], "Offence", "None","Physical",""]
                  ,"Megido" : [175, [1,0], "Offence", "None","Physical",""]
                  ,"Megidola" : [200, [1,0], "Offence", "None","Physical",""]
                  ,"Shining Arrows" : [50, [4,8], "Offence", "None","Physical",""]
                  #Water
                  ,"Bufu" : [90, [1,0], "Offence", "None","Water",""]
                  ,"Rush" : [50,[2,0], "Offence", "None","Water",""]
                  ,"Bufula" : [115, [1,0], "Offence", "None","Water",""]
                  ,"Bufudyne" : [130, [1,0], "Offence", "None","Water",""]
                  ,"Bufubarion" : [150, [1,0], "Offence", "None","Water",""]
                  ,"Thalassic Calamity" : [83, [3,0], "Offence", "None","Water",""]
                  ,"Striking Tide" : [25,[10,0], "Offence", "None","Water",""]
                  #Fire
                  ,"Agi" : [90, [1,0], "Offence", "None","Fire",""]
                  ,"Agilao" : [115, [1,0], "Offence", "None","Fire",""]
                  ,"Agidyne" : [130, [1,0], "Offence", "None","Fire",""]
                  ,"Agibarion" : [150, [1,0], "Offence", "None","Fire",""]
                  ,"Fire Dance" : [83, [3,0], "Offence", "None","Water",""]
                  ,"Burning Hell" : [250, [1,0], "Offence", "None","Fire",""]
                  #Wind
                  ,"Garu" : [90, [1,0], "Offence", "None","Wind",""]
                  ,"Garula" : [115, [1,0], "Offence", "None","Wind",""]
                  ,"Garudyne" : [130, [1,0], "Offence", "None","Wind",""]
                  ,"Garubarion" : [150,[1,0], "Offence", "None","Wind",""]
                  ,"Cyclone" : [31,[8,0], "Offence", "None","Wind",""]
                  ,"Wrath Tempest" : [100,[2,0], "Offence", "None","Wind",""]
                  #Support
                  , "Debilitate" : [0, [0,0], "Offence", "Vulnerable","","Opponent recieves more damage"]
                  , "Concentrate" : [0, [0,0], "Defence", "Concentrated","","Self deals more Elemental damage"]
                  , "Charge" : [0, [0,0], "Defence", "Charged","","Self deals more Physical damage"]
                  ,"Drain Energy" : [0, [0,0], "Offence", "Drained","","Opponent deals less damage"]
                  ,"Resist" : [0, [0,0], "Defence", "Invulnerable","","Self recieves less damage"]
                  ,"Defend" : [0, [0,0], "Defence", "Defending","","Self recieves less damage"]
                  ,"Swiftness" : [0, [0,0], "Defence", "Swift","","Self can dodge Opponent's attacks"]
                  ,"Pinpoint" : [0, [0,0], "Defence", "Unerring","","Self's attacks are 100% accurate"]
                  #Items
                  ,"Bead" : [0, [0,0], "Heal", "None","",""]
                  ,"Healing Orb" : [0, [0,0], "Heal", "None","",""]
                  ,"Hydro Bomb" : [90, [1,0], "Offence", "None","Water",""]
                  ,"Molotov" : [90, [1,0], "Offence", "None","Fire",""]
                  ,"Flashbang" : [90, [1,0], "Offence", "None","Wind",""]
                  }
  

  if move in all_moves:
    #Decides if amount of hits is fixed or in a random range
    if all_moves[move][1][0] >= all_moves[move][1][1]: hits = all_moves[move][1][0]
    else: hits = random.randint(all_moves[move][1][0],all_moves[move][1][1])
    
    move = {
      "name" : move,
      "basedmg" : all_moves[move][0],
      "hits" : hits,
      "type" : all_moves[move][2],
      "affliction" : all_moves[move][3],
      "element" : all_moves[move][4],
      "unique" : all_moves[move][5],
      "description" : ""}
  else:
    return [move,0,0,"Other","None",0,"",""]

  #Generating description

  #Amount of hits
  if move["hits"] != 0:
    if all_moves[move["name"]][1][1] > all_moves[move["name"]][1][0]: move["description"] += str(all_moves[move["name"]][1][0]) + "-" + str(all_moves[move["name"]][1][1]) + " "
    else: move["description"] += str(move["hits"]) + " "

  #Base dmg
  if move["basedmg"] == 0:  move["description"] += ""  
  elif move["basedmg"] <= 10: move["description"] += "Light "
  elif move["basedmg"] <= 30: move["description"] += "Light-Weak "
  elif move["basedmg"] <= 50: move["description"] += "Weak "
  elif move["basedmg"] <= 70: move["description"] += "Weak-Medium "
  elif move["basedmg"] <= 90: move["description"] += "Medium "
  elif move["basedmg"] <= 110:  move["description"] += "Medium-Heavy "
  elif move["basedmg"] <= 130:  move["description"] += "Heavy "
  elif move["basedmg"] <= 150:  move["description"] += "Heavy-Severe "
  elif move["basedmg"] <= 170:  move["description"] += "Severe "
  elif move["basedmg"] <= 190:  move["description"] += "Severe-Colossal "
  elif move["basedmg"] > 190: move["description"] += "Colossal "

  #Element
  if move["element"] != "" and move["basedmg"] != 0:
    move["description"] += move["element"] + " DMG "
    if move["hits"] > 1:  move["description"] += "hits. "
    else: move["description"] += "hit. "

  #Buff/Debuff infliction
  if move["affliction"] != "None":
    move["description"] += "Inflicts " + str(move["affliction"]) + " on"
    #Inflicted on opponent/self
    if move["type"] == "Offence": move["description"] += " opponent. "
    elif move["type"] == "Defence" or move["type"] == "Heal": move["description"] += " self. "

  #Unique attribute
  if move["unique"] != "":  move["description"] += str(move["unique"]) + ". "
      

  output = [move["name"],move["basedmg"], hits, move["type"],move["affliction"],move["element"],move["unique"],move["description"]]
    
  return output



def make_progressbar(fill, maxi, squares):

  #Fill = How much bar is full

  #Maxi = Max size of bar

  #Squares = Bar visual size

  #squares_types = ["▢", "▧", "▩"]
  #squares_types = ["▱", "▰", "▰"]
  squares_types = [" ", "█", "█"]



  percent = (fill/maxi)
  if percent > 1:
    percent = 1

  squares_fill = int(squares * percent)

  if percent <= 0:

    squares_empty = squares

  else:

    squares_empty = squares - squares_fill



  if percent <= 0.3:

      text = str(squares_types[2]*squares_fill) + str(squares_types[0]*squares_empty)

  else:

      text = str(squares_types[1]*squares_fill) + str(squares_types[0]*squares_empty)



  return text



def battle_player(stats, estats):
  global battle_result
  print("\n" * 50)

  percent = int((stats["HP"]/stats["MHP"]) * 100)
  print("=====")
  print(str(stats["name"]) + ": [" + str(make_progressbar(stats["HP"],stats["MHP"],15)) + " " + str(percent) + "% HP]")
  percent = int((estats["HP"]/estats["MHP"]) * 100)
  print(str(estats["name"]) + ": [" + str(make_progressbar(estats["HP"],estats["MHP"],15)) + " " + str(percent) + "% HP]")
  print("=====")



  options = {"1" : "Attack", "2" : "Skill", "3" : "Item", "4" : "Defend", "5" : "Check", "0" : "Run"}



  for i in options:

    print(str(i) + ". " + str(options[i]))



  decision = input("\n >")

  if decision not in options:
    myMixer("menu_invalid.wav")
    battle_player(stats, estats)

    return

  else:

    if options[decision] == "Skill":
      myMixer("menu_enter.wav")
      message = "Choose skill to perform"

      while True:

        print("\n" * 50)

        print("=====\nSkill\n" + str(message) + "\n=====\n")

        options = {}

        count = 1

        for i in stats["moves"]:

          options[str(count)] = i

          count += 1

        for i in options:

          print(str(i) + ". " + options[i])

        print("Back")



        decision = input("\n >")



        if decision.lower() == "back" or decision.lower() == "b":
          myMixer("menu_back.wav")
          battle_player(stats,estats)

          return

          break

        elif decision not in options:
          myMixer("menu_invalid.wav")
          message = "Invalid skill"

          pass

        elif stats["moves"][str(options[decision])] <= 0:
          #Accepted
          break

        else:
          myMixer("menu_invalid.wav")
          message = str(options[decision]) + " on cooldown! (" + str(stats["moves"][options[decision]]) + " turns)"

          pass

        
    elif options[decision] == "Run":
      myMixer("menu_enter.wav")
      while True:
        print("\n" * 50)
        print("=====\nAre you sure you want to Run?\n=====\n")
        decision = input("Y/N>")
        if decision.lower() == "y":
          myMixer("menu_enter.wav")
          battle_result = "Defeat"
          return
          break
        elif decision.lower() == "n":
          myMixer("menu_back.wav")
          battle_player(stats,estats)
          return
          break

        
    elif options[decision] == "Item":
      myMixer("menu_enter.wav")
      message = "Choose an Item to use"
      while True:
        lineskip()
        print("=====\nItem\n" + str(message) + "\n=====\n")
        options = {}
        count = 1
        for item in player_inventory["Support Items"]:
          if player_inventory["Support Items"][item] > 0:
            options[str(count)] = item
            count += 1
        for item in options:
          print(str(item) + ". " + str(options[item]) + " (" + str(player_inventory["Support Items"][str(options[item])]) + ")")
        if len(options) == 0:
          print("-None-")
          
        print("\nBack")
        decision = input("\n >")
        if decision.lower() == "back" or decision.lower() == "b":
          myMixer("menu_back.wav")
          battle_player(stats,estats)
          return
          break
        elif decision not in options:
          myMixer("menu_invalid.wav")
          message="Invalid Item"
          pass
        else:
          myMixer("menu_enter.wav")
          break
        
    elif options[decision] == "Check":
      myMixer("menu_enter.wav")
      while True:
        print("\n" * 50)
        print("=====\nCheck\n=====\n")
        print("=====\n" + str(stats["name"].upper()) + " Lvl." + str(stats["LVL"]) + "\n=====\n")
        print("HP: " + str(stats["HP"]) + "/" + str(stats["MHP"]))
        print("STR:[" + str(stats["STR"]) + str(make_progressbar(stats["STR"]-100,100,20)) + "]\nRES: [" + str(stats["RES"]) + str(make_progressbar(stats["RES"],100,20)) + "]\nEVA: [" + str(stats["EVA"]) + str(make_progressbar(stats["EVA"],100,20)) + "]\nCRIT:[" + str(stats["CRIT"]) + str(make_progressbar(stats["CRIT"],100,20)) + "]")
        print("\nFusion:")
        print("   - " + str(stats["fusion"][0]))
        print("   - " + str(stats["fusion"][1]))
        print("Moves:")
        for move in stats["moves"]:
          print("   • " + str(move) + " - " + str(battle_moveslookup(move)[7]))
        if len(stats["buff"]) > 0:
          print("\nBuffs:")
          for buff in stats["buff"]:
            print("   •" + str(buff) + " (" + str(stats["buff"][buff]) + ")")
        if len(stats["debuff"]) > 0:
          print("\nDebuffs:")
          for debuff in stats["debuff"]:
            print("   •" + str(debuff) + " (" + str(stats["debuff"][debuff]) + ")")
        print("Weakness:\n   - " + str(stats["weakness"]))

        
        print("\n\n=====\n" + str(estats["name"].upper()) + " Lvl." + str(estats["LVL"]) + "\n=====\n")
        print("HP: " + str(estats["HP"]) + "/" + str(estats["MHP"]))
        print("STR:[" + str(estats["STR"]) + str(make_progressbar(estats["STR"]-100,100,20)) + "]\nRES: [" + str(estats["RES"]) + str(make_progressbar(estats["RES"],100,20)) + "]\nEVA: [" + str(estats["EVA"]) + str(make_progressbar(estats["EVA"],100,20)) + "]\nCRIT:[" +str(estats["CRIT"]) +str(make_progressbar(estats["CRIT"],100,20)) + "]")
        print("\nFusion:")
        print("   - " + str(estats["fusion"][0]))
        print("   - " + str(estats["fusion"][1]))
        print("Moves:")
        for move in estats["moves"]:
          print("   • " + str(move) + " - " + str(battle_moveslookup(move)[7]))
        if len(estats["buff"]) > 0:
          print("\nBuffs:")
          for buff in estats["buff"]:
            print("   •" + str(buff) + " (" + str(estats["buff"][buff]) + ")")
        if len(estats["debuff"]) > 0:
          print("\nDebuffs:")
          for debuff in estats["debuff"]:
            print("   •" + str(debuff) + " (" + str(estats["debuff"][debuff]) + ")")
        print("Weakness:\n   - " + str(estats["weakness"]))
        print("\nDrops:")
        print("   - " + str(estats["drops"]["EXP"]) + "EXP")
        for card in estats["drops"]["Skill Cards"]:
          print("   - " + str(card))
        for card in estats["drops"]["Fusion Cards"]:
          print("   - " + str(card))

        print("\nBack")

        decision = input("\n >")

        if decision.lower() == "back" or decision.lower() == "b":
          myMixer("menu_back.wav")
          battle_player(stats,estats)
          return
          break
        myMixer("menu_invalid.wav")


  while True:
    lineskip()
    print("=====\nUse " + str(options[decision]) + "?\n=====\n" + str(battle_moveslookup(options[decision])[7]))
    if battle_moveslookup(options[decision])[5] == estats["weakness"] and battle_moveslookup(options[decision])[5] != "":  print("(WEAK!)")
    print("=====\n")
    print("1. Yes\n2. No")
    final_decision = input("\n >")
    if final_decision == "1":
      battle_neutral(stats, options[decision], estats)
      break
    elif final_decision == "2":
      myMixer("menu_back.wav")
      battle_player(stats,estats)
      break
    else:
      myMixer("menu_invalid.wav")

  return



def battle_passive(actor,target,data):

  #Heals 1% HP for every crit hit
  if data["crit"] > 0 and actor["fusion"][0] == "Wind Type 01" and actor["name"] == data["turn"]:
    for i in range(0,data["crit"]):
      print(str(actor["name"]) + " +" + str(int(actor["MHP"] * 0.01)) + "HP")
      actor["HP"] += int(actor["MHP"] * 0.01)
      if actor["HP"] >= actor["MHP"]:
        actor["HP"] = actor["MHP"]

  #Heals 5% HP for every crit hit
  if data["crit"] > 0 and actor["fusion"][0] == "Wind Type 05" and actor["name"] == data["turn"]:
    for i in range(0,data["crit"]):
      print(str(actor["name"]) + " +" + str(int(actor["MHP"] * 0.05)) + "HP")
      actor["HP"] += int(actor["MHP"] * 0.05)
      if actor["HP"] >= actor["MHP"]:
        actor["HP"] = actor["MHP"]


  #Heals 10% HP for every crit hit
  if data["crit"] > 0 and actor["fusion"][0] == "Wind Type 08" and target["name"] == data["turn"]:
    for i in range(0,data["crit"]):
      print(str(actor["name"]) + " +" + str(int(actor["MHP"] * 0.05)) + "HP")
      actor["HP"] += int(actor["MHP"] * 0.05)
      if actor["HP"] >= actor["MHP"]:
        actor["HP"] = actor["MHP"]


  #Heals 2% HP when in critical condition
  if (actor["fusion"][0] == "Fire Type 02" and data["actorcondition"] == "Critical" and actor["name"] == data["turn"]) and actor["HP"] > 0:
    actor["HP"] += int(actor["MHP"] * 0.02)
    print(str(actor["name"]) + " +" + str(int(actor["MHP"] * 0.02)) + "HP")
    if actor["HP"] >= actor["MHP"]:
      actor["HP"] = actor["MHP"]


  #Drains 10% HP when using "Attack"
  if actor["fusion"][0] == "Fire Type 05" and data["action"] == "Attack" and data["turn"] == actor["name"]:
    actor["HP"] -= int(actor["MHP"] * 0.1)
    print(str(actor["name"]) + " -" + str(int(actor["MHP"] * 0.1)) + "HP")
    if actor["HP"] <= 0:
      actor["HP"] = 1

  #Applies Charged to self and Vulnerable to target when in Critical condition
  if actor["fusion"][0] == "Fire Type 08" and data["actorcondition"] == "Critical":
    actor["buff"]["Charged"] = 3
    target["debuff"]["Vulnerable"] = 3

  #Applies Drained to target and Resistance to self when taking a crit hit
  if target["fusion"][0] == "Water Type 08" and data["crit"] > 0 and data["turn"] == actor["name"]:
    actor["debuff"]["Drained"] = 3
    target["buff"]["Resistance"] = 3

  #Applies Awakened to self when taking damage
  if target["fusion"][0] == "Prototype: AQUA" and data["hit"] > 0 and data["turn"] == actor["name"]:
    target["buff"]["Awakened"] = 3
    
  #Drains 5% HP for every hit
  if actor["fusion"][0] == "Prototype: BLZE" and data["hit"] > 0 and data["turn"] == actor["name"]:
    for i in range(0,data["hit"]):
      print(str(actor["name"]) + " -" + str(int(actor["MHP"] * 0.05)) + "HP")
      actor["HP"] -= int(actor["MHP"] * 0.05)
      if actor["HP"] <= 0:
        actor["HP"] = 1

  return actor





def battle_dmgbonus(damage, actor, target,data):
  global player_inventory
  #List of damage items
  item_list = ["Hydro Bomb", "Flashbang", "Molotov"]

  #DAMAGE BONUS
  damagebonus = 0
  

  #Damage increased by 2% Max HP
  if actor["fusion"][0] == "Fire Type 01":
    damagebonus += int(actor["MHP"] * 0.02)
    
  #Elemental damage increased by 60%. Doubled in Critical condition
  if "Awakened" in actor["buff"] and data["actionelement"] != "Physical":
    damagebonus += int(damage * 0.6)
    if data["actorcondition"] == "Critical":
      damagebonus += int(damage * 0.6)

  #Damage increased by 5% Max HP
  if (actor["fusion"][0] == "Fire Type 04" and (int(actor["HP"]/actor["MHP"] * 100)) <= 30) or (actor["fusion"][0] == "Fire Type 09"):
    damagebonus += int(actor["MHP"] * 0.05)

  #Elemental damage increases
  if actor["fusion"][0] == "Fire Type 03" and data["actionelement"] == "Fire":
    damagebonus += int(damage * 0.25)
  if actor["fusion"][0] == "Wind Type 03" and data["actionelement"] == "Wind":
    damagebonus += int(damage * 0.25)
  if actor["fusion"][0] == "Water Type 02" and data["actionelement"] == "Physical":
    damagebonus += int(damage * 0.5)
  if actor["fusion"][0] == "Water Type 03" and data["actionelement"] == "Water":
    damagebonus += int(damage * 0.25)

  #"Attack" damage is doubled
  if actor["fusion"][0] == "Fire Type 05" and data["action"] == "Attack":
    damagebonus += int(damage)

  #More elemental damage increases
  if actor["fusion"][0] == "Fire Type 06" and data["actionelement"] == "Fire":
    damagebonus += int(damage * 0.5)
  if actor["fusion"][0] == "Wind Type 06" and data["actionelement"] == "Wind":
    damagebonus += int(damage * 0.5)
  if actor["fusion"][0] == "Water Type 05" and data["actionelement"] == "Physical":
    damagebonus += int(damage * 0.75)
  if actor["fusion"][0] == "Water Type 06" and data["actionelement"] == "Water":
    damagebonus += int(damage * 0.5)

  #Damage increased by 5% MHP
  if actor["fusion"][0] == "Fire Type 09" and int(actor["HP"]/actor["MHP"] * 100) <= 30:
    damagebonus += int(actor["MHP"] * 0.05)

  #Damage increased by 20% MHP. Doubled in critical condition
  if actor["fusion"][0] == "Prototype: BLZE" and int(actor["HP"]/actor["MHP"] * 100) <= 50:
    damagebonus += int(actor["MHP"] * 0.2)
  if actor["fusion"][0] == "Prototype: BLZE" and int(actor["HP"]/actor["MHP"] * 100) <= 30:
    damagebonus += int(actor["MHP"] * 0.2)

  #Buffs are doubled by Water passives
  #"Charged" Doubles physical damage
  if "Charged" in actor["buff"] and data["actionelement"] == "Physical":
    damagebonus += int(damage * 1)
    if actor["fusion"][0] == "Water Type 09" or ("Awakened" in actor["buff"] and actor["fusion"][0] == "Prototype: AQUA"):
      damagebonus += int(damage * 1)
      
  #"Concentrated" Doubled elemental damage
  if "Concentrated" in actor["buff"] and data["actionelement"] == "Fire" and data["actionelement"] == "Water" and data["actionelement"] == "Wind":
    damagebonus += int(damage * 1)
    if actor["fusion"][0] == "Water Type 09" or ("Awakened" in actor["buff"] and actor["fusion"][0] == "Prototype: AQUA"):
      damagebonus += int(damage * 1)

  #"Vulnerable" makes enemy take 50% more damage
  if "Vulnerable" in target["debuff"]:
    damagebonus += int(damage * 0.5)
    if actor["fusion"][0] == "Water Type 09":
      damagebonus += int(damage * 0.5)
      
  if damagebonus < 0:
    damagebonus = 0

  #Use up an Item in the inventory
  if data["action"] in item_list and player_stats["name"] == actor["name"]:
    damagebonus = 0
    player_inventory["Support Items"][data["action"]] -= 1
    if player_inventory["Support Items"][data["action"]] <= 0:  player_inventory["Support Items"].pop(data["action"])
   

  return damagebonus



def battle_dmgreduc(damage, actor, target,data):

  #DAMAGE REDUCTION

  damagereduc = 0

  #RES Doubled in Critical condtion
  if data["targetcondition"] == "Critical" and target["fusion"][0] == "Water Type 01":
    damagereduc += int(damage * target["RES"]/100)

  #RES increased by 60%. Doubled in critical condition
  if "Awakened" in target["buff"] and target["fusion"][0] == "Prototype: AQUA":
    damagereduc += int(damage * (target["RES"] * 0.6)/100)
    if data["targetcondition"] == "Critical":
      damagereduc += int(damage * (target["RES"] * 0.6)/100)

  #"Drained" makes actor deal less damage
  if "Drained" in actor["debuff"]:
    damagereduc += int(damage * 0.2)
    if target["fusion"][0] == "Water Type 09":
      damagereduc += int(damage * 0.2)


  #"Invulnerable" and "Defending" makes opponent recieve less damage
  if "Invulnerable" in target["buff"]:
    damagereduc += int(damage * 0.2)
    if target["fusion"][0] == "Water Type 09" or ("Awakened" in target["buff"] and target["fusion"][0] == "Prototype: AQUA"):
      damagereduc += int(damage * 0.2)
  if "Defending" in target["buff"]:
    damagereduc += int(damage * 0.2)
    if target["fusion"][0] == "Water Type 09" or ("Awakened" in target["buff"] and target["fusion"][0] == "Prototype: AQUA"):
      damagereduc += int(damage * 0.2)

  #Target recieves less Elemental damage
  if target["fusion"][0] == "Water Type 07" and (data["actionelement"] == "Wind" or data["actionelement"] == "Water" or data["actionelement"] == "Fire"):
    damagereduc += int(damage * 0.33)
  
  if damagereduc < 0:
    damagereduc = 0
  elif damagereduc > damage:
    damagereduc = damage

  return damagereduc



def battle_dmgcrit(actor, target,data):

  #CRITICAL RATE
  #If 'flag' value below crit chance, lands a critical hit
  #The lower the value of "flag", higher chance of landing critical hit

  flag = random.randint(1,100)

  if data["action"] == "Lunge":
    flag -= 30

  #Crit rate increased by 30
  if actor["fusion"][0] == "Wind Type 02" and int(((actor["HP"]/actor["MHP"])*100)) <= 70:
    flag -= 30


  #Crit rate increased by 50%
  if actor["fusion"][0] == "Wind Type 04" and int(((actor["HP"]/actor["MHP"])*100)) <= 30:
    flag -= int(actor["CRIT"]*0.5)

  #Crit rate increased by 20
  if actor["fusion"][0] == "Prototype: GALE" and (int(((actor["HP"]/actor["MHP"])*100)) >= 50 or data["actorcondition"] == "Critical"):
    flag -= 20
  #Crit rate increased by 40
  if actor["fusion"][0] == "Prototype: GALE" and (int(((actor["HP"]/actor["MHP"])*100)) <= 50 or data["actorcondition"] == "Critical"):
    flag -= 40


  return flag



def battle_dmgmiss(actor,target):

  #EVASION RATE
  #The higher the value of "flag", higher chance of dodging attack
  flag = random.randint(1,100)

  #Impossible to miss
  if actor["EVA"] > target["EVA"]:
    flag = 101

  #Target can dodge attacks regardless of EVA
  if "Swift" in target["buff"]:
    flag = random.randint(1,100)

  #Impossible to miss
  if "Unerring" in actor["buff"]:
    flag = 101



  return flag



def battle_dmgcritbonus(damage, actor, target,data):

  #CRITICAL DMG BONUS

  #Base damage increase: Increases damage by 50%
  damagebonus = int(damage*0.5)

  #Increases damage by 100%
  if data["action"] == "Wrath Tempest":
    damagebonus + int(damage)

  #Increases damage by 75%
  if actor["fusion"][0] == "Wind Type 09" or (actor["fusion"][0] == "Wind Type 07" and int(((actor["HP"]/actor["MHP"])*100)) <= 50):
    damagebonus += int(damage * 0.75)

  #Increases damage by 30%
  if actor["fusion"][0] == "Wind Type 04" and int(((actor["HP"]/actor["MHP"])*100)) <= 30:
    damagebonus += int(damage * 0.3)

  #All damage blocked
  if target["fusion"][0] == "Water Type 04" and random.randint(1,100) <= 50:
    print(" Blocked!")
    damagebonus = -damage

  #Increases damage by 100%
  if actor["fusion"][0] == "Prototype: GALE" and (int(((actor["HP"]/actor["MHP"])*100)) >= 50 or data["actorcondition"] == "Critical"):
    damagebonus += int(damage)
  #Increases damage by 50%
  if actor["fusion"][0] == "Prototype: GALE" and (int(((actor["HP"]/actor["MHP"])*100)) <= 50 or data["actorcondition"] == "Critical"):
    damagebonus += int(damage * 0.5)

  #Any bonus damage is cancelled
  if target["fusion"][0] == "Prototype: GALE":
    damagebonus = 0


  return damagebonus



def battle_removebuffs(buffs):

  remove = []
  for i in buffs:
    buffs[i] -= 1
    if buffs[i] <= 0:
      remove.append(str(i))
    else:
      print(str(i) + " (" + str(buffs[i]) + ")")
      
  for i in remove:
    print("(" + str(i) + " effect wore off)")
    buffs.pop(str(i))

  return buffs



def battle_movecd(moves):

  for i in moves:
    moves[i] -= 1
    if moves[i] <= 0:
      moves[i] = 0

  return moves



def battle_heal(action,actor,target):
  global player_inventory
  global player_stats

  healing = 0
  item = ""

  #Heals 20% HP
  if action == "Dia":
    healing += int(actor["MHP"] * 0.2)
  if action == "Diarama":
    healing += int(actor["MHP"] * 0.4)
  if action == "Diarahan":
    healing += int(actor["MHP"] * 0.6)
  if action == "Healing Orb":
    healing += int(actor["MHP"] * 0.4)
    item = action
  if action == "Bead":
    healing += int(actor["MHP"] * 0.6)
    item = action

  #Use up an Item in the inventory
  if item != "" and player_stats["name"] == actor["name"]:
    player_inventory["Support Items"][item] -= 1
    if player_inventory["Support Items"][item] <= 0:  player_inventory["Support Items"].pop(item)
      

  #Healing is doubled
  if actor["fusion"][0] == "Fire Type 07":
    healing += healing

  return healing



def battle_neutral(actor, action, target):
  global battle_result
  global player_stats
  global player_inventory

  global enemy_stats

  lineskip()
  #0 Name
  
  #1 Base DMG

  #2 Number of Hits

  #3 Move type: Damage, Offence, Defence, Heal, Other

  #4 Infliction

  #5 Element

  #6 Unique attribute

  #7 Description
  
  action = battle_moveslookup(action)


  #Move cooldown
  #Player CD
  if actor["name"] == player_stats["name"] and action[0] in actor["moves"] and action[0] not in player_inventory["Support Items"]:
    actor["moves"][str(action[0])] += 4
  #Enemy CD
  elif actor["name"] == enemy_stats["name"] and action[0] in actor["moves"]:
    actor["moves"][str(action[0])] += 4


  #Decrease Player and Enemy CD
  actor["moves"] = battle_movecd(actor["moves"])
  target["moves"] = battle_movecd(target["moves"])


  #Actor and Target Condition: Normal/Critical/Defeated
  x="Normal"
  y="Normal"

  if actor["HP"] <= 0:

    actor["HP"] = 0

    x = "Defeated"

  elif int((actor["HP"]/actor["MHP"]) * 100) <= 30:

    x = "Critical"

  if target["HP"] <= 0:

    target["HP"] = 0

    y = "Defeated"

  elif int((target["HP"]/target["MHP"]) * 100) <= 30:

    y = "Critical"


  #Contains all data of the current Turn
  battle_turndata = {
                     "turn" : actor["name"],
                     "action" : str(action[0]),
                     "actionelement" : action[5],
                     "miss" : 0,
                     "crit" : 0,
                     "hit" : 0,
                     "heal" : 0,
                     "inflictself" : False,
                     "inflictopp" : False,
                     "actorcondition" : x,
                     "targetcondition" : y}


  #Decreasing Buff + Debuff duration
  if len(actor["buff"]) > 0 or len(actor["debuff"]) > 0:
    print(actor["name"] + ":")
    actor["buff"] = battle_removebuffs(actor["buff"])
    actor["debuff"] = battle_removebuffs(actor["debuff"])
  if len(target["buff"]) > 0 or len(target["debuff"]) > 0:
    print(target["name"] + ":")
    target["buff"] = battle_removebuffs(target["buff"])
    target["debuff"] = battle_removebuffs(target["debuff"])

  dmg = 0
  hits = 0
  message = ""


  if action[0] != "":
    basedmg = action[1]
    hits = action[2]

  else:
    basedmg = 0
    hits = 0










  #Output who did what
  print("\n" + str(actor["name"]) + " used " + str(action[0]) + "! (" + str(hits) + " hits!)")
  #Output dashes where damage is displayed
  print("\n-" * hits)
  #Output the Target's current HP in a Large progressbar
  if action[3] == "Defence" or action[3] == "Heal":
    print("\n" + str(actor["name"]) + ": [" + str(make_progressbar(actor["HP"],actor["MHP"],40)) + "] " + str(actor["HP"]) + "/" + str(actor["MHP"]) + " HP")
  else:
    print("\n" + str(target["name"]) + ": [" + str(make_progressbar(target["HP"],target["MHP"],40)) + "] " + str(target["HP"]) + "/" + str(target["MHP"]) + " HP")

  output = ""

  input("\n>")

  basehits = hits
  while hits > 0:
    
    if int((target["HP"]/target["MHP"]) * 100) <= 30:
      battle_turndata["targetcondition"] = "Critical"

    dmg = int(basedmg * actor["STR"]/100)
    dmg += int(battle_dmgbonus(dmg, actor, target,battle_turndata))
    dmg -= int(dmg * target["RES"]/100)
    dmg -= int(battle_dmgreduc(dmg, actor, target,battle_turndata))

    if dmg <= 0:
      dmg = 0
    hits -= 1

    lineskip()
    print(str(actor["name"]) + " used " + str(action[0]) + "! (" + str(hits) + " hits!)")

    output += "\n"
    if battle_dmgmiss(actor,target) <= 10:
      myMixer("hit_miss.wav")
      output += ("-0 DMG (MISS!)")
      battle_turndata["miss"] += 1
      
    else:
      #Play sound effects
      sounds = {"Physical" : "hit_physical.wav", "Fire" : "hit_fire.wav", "Water" : "hit_water.wav", "Wind" : "hit_wind.wav", }
      sounds_crit = {"Physical" : "hit_physicalcrit.wav", "Fire" : "hit_firecrit.wav", "Water" : "hit_watercrit.wav", "Wind" : "hit_windcrit.wav", }
      
      totaldmg = dmg
      print("Total dmg: " + str(totaldmg))
      #outputtemp Displays if WEAK or CRITICAL has been hit
      outputtemp = ""
      if battle_dmgcrit(actor,target,battle_turndata) <= actor["CRIT"] and totaldmg > 0 and (battle_turndata["actionelement"] == "Physical" or battle_turndata["actionelement"] == "Wind"):
        totaldmg += battle_dmgcritbonus(dmg, actor,target,battle_turndata)
        outputtemp += ("(CRITICAL!)")
        battle_turndata["crit"] += 1
      if battle_turndata["actionelement"] in target["weakness"] and totaldmg > 0:
        totaldmg += battle_dmgcritbonus(dmg, actor,target,battle_turndata)
        outputtemp += ("(WEAK!)")
        battle_turndata["crit"] += 1

      #Normal hit sound effect
      if outputtemp == "":
        myMixer(sounds[battle_turndata["actionelement"]])
      #Critical hit sound effect
      else:
        myMixer(sounds_crit[battle_turndata["actionelement"]])

      output += ("-" + str(totaldmg) + " DMG " + str(outputtemp))
      battle_turndata["hit"] += 1
      if totaldmg <= 0:
        totaldmg = 0
      target["HP"] -= totaldmg

    #display dmg dealt. e.g:
    #"-50dmg"
    print(output)
    #display hits to come. e.g:
    #"- "
    print("-\n" * hits)

    percent = int((target["HP"]/target["MHP"]) * 100)

    print(str(target["name"]) + ": [" + str(make_progressbar(target["HP"],target["MHP"],40)) + "] " + str(target["HP"]) + "/" + str(target["MHP"]) + " HP")



    time.sleep(0.75/basehits)



  time.sleep(0.75)



  if action[4] != "None" and action[3] == "Offence":

    if action[4] in target["debuff"]:

      target["debuff"][action[4]] += 5

    else:

      target["debuff"][action[4]] = 5

    battle_turndata["inflictopp"] = True
    myMixer("hit_debuff.wav")
    message += str(target["name"] + " inflicted with '" + str(action[4]) + "'!")

  elif action[4] != "None" and action[3] == "Defence":

    if action[4] in actor["buff"]:

      actor["buff"][action[4]] += 5

    else:

      actor["buff"][action[4]] = 5

    battle_turndata["inflictself"] = True
    myMixer("hit_buff.wav")
    message += str(actor["name"] + " inflicted with '" + str(action[4]) + "'!")

  elif action[3] == "Heal":

    battle_turndata["heal"] += battle_heal(action[0],actor,target)

    actor["HP"] += battle_turndata["heal"]
    myMixer("heal.wav")
    print(str(actor["name"]) + " +" + str(battle_turndata["heal"]) + "HP")

    if actor["HP"] >= actor["MHP"]:

      actor["HP"] = actor["MHP"]

    if action[4] != "None":

      if action[4] in actor["buff"]:

        actor["buff"][action[4]] += 5

      else:

        actor["buff"][action[4]] = 5

      battle_turndata["inflictself"] = True
      myMixer("hit_buff.wav")
      message += str(actor["name"] + " inflicted with '" + str(action[4]) + "'!")









  if actor["HP"] <= 0:
    actor["HP"] = 0
    battle_turndata["actorcondition"] = "Defeated"

  elif int((actor["HP"]/actor["MHP"]) * 100) <= 30:
    battle_turndata["actorcondition"] = "Critical"
    
  else:
    battle_turndata["actorcondition"] = "Normal"

  if target["HP"] <= 0:
    target["HP"] = 0
    battle_turndata["targetcondition"] = "Defeated"

  elif int((target["HP"]/target["MHP"]) * 100) <= 30:
    battle_turndata["targetcondition"] = "Critical"
    
  else:
    battle_turndata["targetcondition"] = "Normal"





  actor = battle_passive(actor,target,battle_turndata)

  target = battle_passive(target,actor,battle_turndata)



  print("")

  percent = int((actor["HP"]/actor["MHP"]) * 100)

  print(str(actor["name"]) + ": [" + str(make_progressbar(actor["HP"],actor["MHP"],10)) + "] " + str(percent) + "% HP [" + str(battle_turndata["actorcondition"]) + "]")

  percent = int((target["HP"]/target["MHP"]) * 100)

  print(str(target["name"]) + ": [" + str(make_progressbar(target["HP"],target["MHP"],10)) + "] " + str(percent) + "% HP [" + str(battle_turndata["targetcondition"]) + "]")

  print("")

  print(message)





  input(" >")



  if actor["HP"] <= 0 and actor["name"] == player_stats["name"]:

    battle_result = "Defeat"

  elif actor["HP"] <= 0 and actor["name"] == enemy_stats["name"]:

    battle_result = "Victory"

  elif target["HP"] <= 0 and target["name"] == player_stats["name"]:

    battle_result = "Defeat"

  elif target["HP"] <= 0 and target["name"] == enemy_stats["name"]:

    battle_result = "Victory"

  elif (actor["name"] == enemy_stats["name"] and battle_turndata["crit"] == 0) or (actor["name"] == player_stats["name"] and battle_turndata["crit"] > 0):

    if actor["name"] == player_stats["name"]:

      battle_player(actor,target)

    elif target["name"] == player_stats["name"]:

      battle_player(target,actor)

  elif (actor["name"] == player_stats["name"] and battle_turndata["crit"] == 0) or (actor["name"] == enemy_stats["name"] and battle_turndata["crit"] > 0):

    if actor["name"] == enemy_stats["name"]:

      battle_enemy(actor,target)

    elif target["name"] == enemy_stats["name"]:

      battle_enemy(target,actor)

  return



def battle_enemy(stats, pstats):

  percent = int((stats["HP"]/stats["MHP"]) * 100)

  attacks = {
            #Physical
             "Attack" : [90, 1, "Damage", "None","Physical"]
            ,"Thousand Slaps" : [10, 10, "Damage", "None","Physical"]
            ,"Lunge" : [100, 1, "Damage", "None","Physical"]
            ,"Megi" : [150, 1, "Damage", "None","Physical"]
            ,"Megido" : [175, 1, "Damage", "None","Physical"]
            ,"Megidola" : [200, 1, "Damage", "None","Physical"]
            ,"Shining Arrows" : [50, random.randint(4,8), "Damage", "None","Physical"]
            #Water
            ,"Bufu" : [90, 1, "Damage", "None","Water"]
            ,"Rush" : [50,2, "Damage", "None","Water"]
            ,"Bufula" : [115, 1, "Damage", "None","Water"]
            ,"Bufudyne" : [130, 1, "Damage", "None","Water"]
            ,"Bufubarion" : [150, 1, "Damage", "None","Water"]
            ,"Thalassic Calamity" : [83, 3, "Damage", "None","Water"]
            ,"Striking Tide" : [25,10, "Damage", "None","Water"]
            #Fire
            ,"Agi" : [90, 1, "Damage", "None","Fire"]
            ,"Agilao" : [115, 1, "Damage", "None","Fire"]
            ,"Agidyne" : [130, 1, "Damage", "None","Fire"]
            ,"Agibarion" : [150, 1, "Damage", "None","Fire"]
            ,"Fire Dance" : [83, 3, "Damage", "None","Water"]
            ,"Burning Hell" : [250, 1, "Damage", "None","Fire"]
            #Wind
            ,"Garu" : [90, 1, "Damage", "None","Wind"]
            ,"Garula" : [115, 1, "Damage", "None","Wind"]
            ,"Garudyne" : [130, 1, "Damage", "None","Wind"]
            ,"Garubarion" : [150, 1, "Damage", "None","Wind"]
            ,"Cyclone" : [31,8, "Damage", "None","Wind"]
            ,"Wrath Tempest" : [100,2, "Damage", "None","Wind"]}

  buffs = {"Concentrate" : [0, 0, "Defence", "Concentrated"]
           ,"Charge" : [0, 0, "Defence", "Charged"]
           ,"Resist" : [0, 0, "Defence", "Invulnerable"]
           ,"Swiftness" : [0, 0, "Defence", "Swift"]
           ,"Pinpoint" : [0, 0, "Defence", "Unerring"]}

  debuffs = {"Debilitate" : [0, 0, "Offence", "Vulnerable"]
             ,"Drain Energy" : [0, 0, "Offence", "Drained"]}

  heals = {"Dia" : [0, 0, "Heal", "None"]}

  other = {"Nothing" : [0, 0, "Other", "None"]}



  passes = 0

  while True:

    passes += 1

    for i in range(1,3):

      print("\n" * 50)

      print("Enemy turn!")

      count = random.randint(0,len(stats["moves"])-1)

      for i in stats["moves"]:

        if count <= 0:

          decision = i

          break

        count -= 1

      print("\nThinking of '" + str(decision) + "'...")

      time.sleep(0.2)

    time.sleep(0.1)



    if passes >= 5:

      decision = "Nothing"

      break

    if decision in attacks and stats["moves"][decision] <= 0:

      break

    elif (decision in buffs and len(stats["buff"]) < 2) and stats["moves"][decision] <= 0:

      if buffs[decision][3] not in stats["buff"]:

        break

    elif (decision in debuffs and len(pstats["debuff"]) < 2) and stats["moves"][decision] <= 0:

      if debuffs[decision][3] not in pstats["debuff"]:

        break

    elif decision in heals and percent <= 30 and stats["moves"][decision] <= 0:

      break

    elif decision in other and stats["moves"][decision] <= 0:

      break





  battle_neutral(stats, decision, pstats)

  return


def explore():
    global location
    global location_c
    global message
    lineskip()
    #Displays all the floors

    #Calculation % Completion
    cleared = 0
    total = 0
    for floors in location_c:
      if floors != "progress":
        for rooms in location_c[floors]:
          if location_c[floors][str(rooms)] == "Grind" or location_c[floors][str(rooms)] == "Empty": cleared += 1
          total += 1
    progress = int((cleared/total)*100)
        
    #Display
    print("====================\nEXPLORATION OVERVIEW\n(" + str(progress) + "% Completed)\n====================\n" + str(message) + "\n====================\n")

    print("1. Floor A")
    #Deciding which floors the Player is allowed to go to
    #count is the options for input (1.,2.,3.,4.,etc)
    count = 2
    #floor_available contains the floors that the player is allowed to go to
    floor_available = {"1" : "A"}
    for floors in location_c:
      if floors != "progress":
        cleared = True
        for rooms in location_c[floors]:
          if location_c[floors][str(rooms)] != "Grind" and location_c[floors][str(rooms)] != "Empty":
            cleared = False
            break
        #If a floor is cleared, the next floor will be available
        if cleared == True and chr(ord(floors)+1) in location_c:
          print(str(count) + ". Floor " + str(chr(ord(floors)+1)))
          floor_available[str(count)] = str(chr(ord(floors)+1))
          count += 1
        else:
          print("   ?")

          
    print("\nBack")
    decision=input("\n >")
    #accepted checks if the input is accepted. If it isnt, restart the menu
    if decision.lower() == "back" or decision.lower() == "b":
      myMixer("menu_back.wav")
      menu_main("Returned from the Dungeon.\nWelcome back.")
      return
    elif decision in floor_available:
      myMixer("menu_enter.wav")
      location["exact"] = [floor_available[decision],"0"]
      floor("Select a Room")
    else:
      myMixer("menu_invalid.wav")
      message = "Cannot explore here"
      explore()

    return
        

def floor(message):
  global location
  global location_c
  
  lineskip()
  #Calculation % Completion
  cleared = 0
  total = 0
  for rooms in location_c[location["exact"][0]]:
    if location_c[location["exact"][0]][str(rooms)] == "Grind" or location_c[location["exact"][0]][str(rooms)] == "Empty": cleared += 1
    total += 1
  progress = int((cleared/total)*100)

  print("=====\nFLOOR " + str(location["exact"][0]) + " (" + str(progress) + "% Completed)\n" + str(message) + "\n=====\n")


  for rooms in location_c[location["exact"][0]]:
    print(str(rooms) + ". Enter Room " + str(rooms))

  print("\nBack")
  decision=input("\n >")

  if decision == "0" or decision.lower() == "back" or decision.lower() == "b":
    myMixer("menu_back.wav")
    explore()
  elif decision in location_c[location["exact"][0]]:
    myMixer("menu_enter.wav")
    location["exact"][1] = decision
    location["contents"] = location_c[location["exact"][0]][decision]
    if location["contents"] == "Enemy":
        room_enemy("An enemy lurks in the room!")
    elif location["contents"] == "Miniboss":
        room_miniboss("A Powerful enemy lurks in the room.")
    elif location["contents"] == "Grind":
        room_enemy("An enemy lurks in the room!\n(Already explored room)")
    elif location["contents"] == "Chest":
        room_chest()
    elif location["contents"] == "Empty":
        room_empty()
    else:
        myMixer("menu_invalid.wav")
        location["exact"][1] = "0"
        floor("Error. Select a Room")
  else:
    myMixer("menu_invalid.wav")
    floor("Invalid Room")

  return



#location_c[str(int(location["exact"]))] = "Empty"

def room_empty():
  #Room is empty
    lineskip()
    print("==========\nSilence fills the room from top to bottom.\nThe room is empty.\n==========\n")
    input("\nExit>")
    myMixer("menu_back.wav")
    location["exact"][1] = "0"
    floor("Select a Room")
    return

    
def room_enemy(message):
    global startend
    lineskip()
    print("==========\n" + str(message) + "\n==========\n")
    print("Fight it?")
    print("1. Yes")
    print("2. No")

    a=input("\n >")

    if a == "1":
        myMixer("menu_enter.wav")
        result = battle_startend("Start")
        if result == "Victory":
            location_c["progress"] += 1
            location_c[location["exact"][0]][location["exact"][1]] = "Empty"
            lineskip()
            print("The room is now empty.\nYou decide to leave...")
            time.sleep(3)
            floor("Room " + str(location["exact"][1]) + " explored!")
        elif result == "Defeat":
            menu_main("Game Over")
    elif a == "2":
        myMixer("menu_back.wav")
        floor("You leave the monster be...")
    else:
        myMixer("menu_invalid.wav")
        room_enemy(message)
        
    return

def room_miniboss(message):
    global startend
    lineskip()
    print("==========\n" + str(message) + "\n==========\n")
    print("Fight it?")
    print("1. Yes")
    print("2. No")

    a=input("\n >")

    if a == "1":
      myMixer("menu_enter.wav")
      while True:
        lineskip()
        print("==========\nAre you really sure you want to fight it?\n==========\n\n")
        print("1. Yes")
        print("2. No")
        a=input("\n>")
        if a == "1" or a == "2":
          break
        else:
          myMixer("menu_invalid.wav")
    elif a == "2":
        myMixer("menu_back.wav")
        floor("You leave the monster be...")
        return
    else:
        myMixer("menu_invalid.wav")
        room_miniboss(message)
        return

    if a == "1":
        myMixer("menu_enter.wav")
        result = battle_startend("Start")
        if result == "Victory":
            location_c["progress"] += 1
            location_c[location["exact"][0]][location["exact"][1]] = "Empty"
            lineskip()
            print("The room is now empty.\nYou decide to leave...")
            time.sleep(3)
            floor("Room " + str(location["exact"][1]) + " explored!")
        elif result == "Defeat":
            menu_main("Game Over")
    elif a == "2":
        myMixer("menu_back.wav")
        floor("You leave the monster be...")
    else:
        myMixer("menu_invalid.wav")
        room_miniboss(message)
        
    return

def room_chest():
    global player_inventory
    global player_stats
    lineskip()
    print("==========\nA chest sits in the middle of the room.\nHow lucky!\n==========\n")
    print("Open it?")
    print("1. Yes")
    print("2. No")
    a=input("\n >")


    if a == "1":
        myMixer("menu_enter.wav")
        lineskip()
        print("You open the chest...")
        time.sleep(2)
        location_c["progress"] += 1
        if random.randint(1,100) <= 10:
            lineskip()
            print("It's a trap!")
            time.sleep(2)
            #Start a battle
            result = battle_startend("Start")
        else:
            result = "Item got"
            
    elif a == "2":
        myMixer("menu_back.wav")
        floor("You left the chest alone...")
        return
    else:
        myMixer("menu_invalid.wav")
        room_chest()
        return

    if result == "Victory" or result == "Item got":
        item_list = ["Molotov", "Hydro Bomb", "Flashbang", "Healing Orb"]
        player_stats = battle_levelup(player_stats,200)
        player_inventory = battle_drops(player_inventory,{"Support Items" : item_list})
        player_inventory = battle_drops(player_inventory,{"Support Items" : item_list})
        player_inventory = battle_drops(player_inventory,{"Support Items" : item_list})
        lineskip()
        print("The room is now empty.\nYou decide to leave...")
        time.sleep(3)
        location_c[location["exact"][0]][location["exact"][1]] = "Empty"
        floor("Room " + str(location["exact"][1]) + " explored!")
    else:
        menu_main("Game Over")

    return


def lineskip():
    print("\n" * 50)



lineskip()
printplus("","","","=Ultimate 2022 RPG Fight Simulator=\nBy Navee#0004\n\n")
myMixer("menu_enter.wav")
menu_main("Select an Option by entering the Number")

#{"Nothing" : [0, 0, "Other", "None"],"Regenerate" : [0, 0, "Heal", "None"], "Attack" : [100, 1, "Damage", "None"], "Rush" : [65,2, "Damage", "None"], "Cyclone" : [25,8, "Damage", "None"], "Vacuum Wave" : [40,random.randint(2,5), "Damage", "None"], "Defend" : [0,0, "Defence", "None"], "Debilitate" : [0, 0, "Offence", "Vulnerable"], "Concentrate" : [0, 0, "Defence", "Concentrated"], "Charge" : [0, 0, "Defence", "Charged"],"Drain Energy" : [0, 0, "Offence", "Drained"],"Resist" : [0, 0, "Defence", "Invulnerable"],"Swiftness" : [0, 0, "Defence", "Swift"],"Pinpoint" : [0, 0, "Defence", "Unerring"]}
