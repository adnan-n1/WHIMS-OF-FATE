import pygame
import random
import time
import button
import math
import csv
#For converting strings to dicts
import ast

# •
 
#---NOTES---
#Fix fonts
#Line 2283
#Fix AGG
#Add keybinds to all battle buttons
#Rework moves: 2 Basic, 1 Skill, 1 SPECIAL
#Improve UI for buffing/healing party members
#Multiple action instances inside "moveslookup". E.g Set of 7 lists in a single list for a move that attacks 7 times.
#   This way, instances can have own seperate functions.
#   Also allows multiple-hit-animation when casting, using a loop for combatant.move()
#   Each function added to the same singular description.
#Shop
#Charm sets with matching bonuses/ Line 1230
#NEW STATS: Shields. Apply buffs to self which increases shields. When attacked, take shield dmg instead

#Create way more moves, SPECIALS
#General balancing between enemy stats and increased stats when level up


version = "1.0.5"

#Creating character data based off csv file character data
with open("savedata.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    player_characters = {}

    #Skip over first line in file. (First line contains key names)
    #next(reader)
    #Create player_characters dictionary based off csv file data
    for line in reader:
        player_characters[line["name"]] = line
for member in player_characters:
    for stat in player_characters[member]:
        if stat != "name" and stat != "element" and stat != "weakness":
            #Reformatting data since they're all stored as strings 
            player_characters[member][stat] = ast.literal_eval(player_characters[member][stat])


#List of all the playable characters and their base stats
#Specialty. Sustain, Healing, Damage Crit, Damage Weak, Support.
#60% Increase between relevant stats, 20% decrease in other stats
characters = {
    'Seliph': {"specialty" : "Sustain",'name': 'Seliph','element': 'Water', 'MHP': 220, 'STR': 80, 'RES': 7, 'CRIT': 4, 'CRIT DMG': 40, 'MEG': 100, 'fusion': 'Water Type 05', 'moves': ['Bufudyne',"Dia", "SPECIAL: Eternal Endurance"], 'weakness': 'Wind', 'AGG': 100},
    'Mia': {"specialty" : "Healing",'name': 'Mia','element': 'Fire', 'MHP': 260, 'STR': 80, 'RES': 4, 'CRIT': 4, 'CRIT DMG': 40, 'MEG': 100, 'fusion': 'Fire Type 05', 'moves': ['Agidyne',"Dia", "SPECIAL: Life's Garden"], 'weakness': 'Water', 'AGG': 100},
    'Sothe': {"specialty" : "Damage (Critical)",'name': 'Sothe','element': 'Wind', 'MHP': 180, 'STR': 100, 'RES': 4, 'CRIT': 7, 'CRIT DMG': 60, 'MEG': 100, 'fusion': 'Wind Type 05', 'moves': ['Wind Blades',"Focus", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Anna': {"specialty" : "Damage (Weakness)",'name': 'Anna','element': 'Fire', 'MHP': 180, 'STR': 160, 'RES': 4, 'CRIT': 4, 'CRIT DMG': 40, 'MEG': 100, 'fusion': 'Fire Type 06', 'moves': ['Agidyne', "Fire Dance", "SPECIAL: Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Kris': {"specialty" : "Damage (Critical)",'name': 'Kris','element': 'Water', 'MHP': 180, 'STR': 100, 'RES': 4, 'CRIT': 5, 'CRIT DMG': 70, 'MEG': 100, 'fusion': 'Water Type 06', 'moves': ['Bufudyne',"Striking Tide", "SPECIAL: Total Focus"], 'weakness': 'Wind', 'AGG': 100},
    'Knight': {"specialty" : "Sustain",'name': 'Knight','element': 'Water', 'MHP': 180, 'STR': 80, 'RES': 8, 'CRIT': 5, 'CRIT DMG': 40, 'MEG': 100, 'fusion': 'Water Type 07', 'moves': ['Dia',"Taunt", "SPECIAL: Ultimate Defence"], 'weakness': 'Wind', 'AGG': 100},


    'Byleth': {'name': 'Byleth', 'element': 'Wind', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Wind Type 09', 'moves': ['Garudyne',"Cyclone","Debilitate", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Morgan': {'name': 'Morgan', 'element': 'Water', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Prototype: AQUA', 'moves': ['Bufudyne',"Striking Tide","Taunt", "SPECIAL: Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Claude': {'name': 'Claude', 'element': 'Fire', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Fire Type 07', 'moves': ['Agidyne', "Fire Dance", "SPECIAL: Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Alm': {'name': 'Alm','element': 'Wind', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Wind Type 08', 'moves': ['Garudyne',"Cyclone", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Dimitri': {'name': 'Dimitri', 'element': 'Water', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Water Type 08', 'moves': ['Bufudyne',"Bufubarion", "SPECIAL: Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Lilina': {'name': 'Lilina', 'element': 'Fire', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Fire Type 08', 'moves': ['Agidyne', "Fire Dance", "SPECIAL: Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Hilda': {'name': 'Hilda','element': 'Fire', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Fire Type 09', 'moves': ['Agidyne', "Agibarion", "SPECIAL: Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Lucina': {'name': 'Lucina','element': 'Water', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Water Type 09', 'moves': ['Bufudyne',"Striking Tide", "SPECIAL: Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Ninian': {'name': 'Ninian','element': 'Wind', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Prototype: GALE', 'moves': ['Garudyne',"Garubarion", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Shez': {'name': 'Shez', 'element': 'Fire', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Prototype: BLZE', 'moves': ['Agidyne', "Fire Dance", "SPECIAL: Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Lyn': {'name': 'Lyn', 'element': 'Wind', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Wind Type 07', 'moves': ['Garudyne',"Cyclone", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Reginn': {'name': 'Reginn','element': 'Wind', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Wind Type 06', 'moves': ['Garudyne',"Cyclone", "SPECIAL: Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Alear': {'name': 'Alear','element': 'Singularity', 'MHP': 200, 'STR': 100, 'RES': 5, 'CRIT': 5, 'CRIT DMG': 50, 'MEG': 100, 'fusion': 'Prototype: STAR', 'moves': ['Garudyne',"Cyclone", "SPECIAL: March Forward"], 'weakness': 'None', 'AGG': 100,}
}

player_characters = {
    #Starting characters
    "Seliph" : {"unlock":True,"name" : "Seliph", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Mia" : {"unlock":True,"name" : "Mia", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Sothe" : {"unlock":True,"name" : "Sothe", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Knight" : {"unlock":True,"name" : "Knight", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},

    #Unlockable characters
    "Byleth" : {"unlock":False,"name" : "Byleth", "LVL" : 1, "EXP" : 1,"HP" : 200,"EG" : 0, "charms" : []},
    "Claude" : {"unlock":False,"name" : "Claude", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Dimitri" : {"unlock":False,"name" : "Dimitri", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Lilina" : {"unlock":False,"name" : "Lilina", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Hilda" : {"unlock":False,"name" : "Hilda", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Lucina" : {"unlock":False,"name" : "Lucina", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Ninian" : {"unlock":False,"name" : "Ninian", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Shez" : {"unlock":False,"name" : "Shez", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Anna" : {"unlock":False,"name" : "Anna", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Kris" : {"unlock":False,"name" : "Kris", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Lyn" : {"unlock":False,"name" : "Lyn", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Reginn" : {"unlock":False,"name" : "Reginn", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Alear" : {"unlock":False,"name" : "Alear", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []},
    "Morgan" : {"unlock":False,"name" : "Morgan", "LVL" : 1, "EXP" : 1,"HP" : 200, "EG" : 0,"charms" : []}
}
BASE_MEXP = 500

battle_characters = {}

worlds = {
    "World 1" :
        {
        "Floor 1" :
                     {"id" : "1","bgm" : "battle", "Enemies" : ["1"],"Rewards" : {"GOLD" : 2, "EXP" : 1000}},
        "Floor 2" :
                     {"id" : "2","bgm" : "battle", "Enemies" : ["3"],"Rewards" : {"GOLD" : 3, "EXP" : 1500}},
        "Floor 3" :
                     {"id" : "3","bgm" : "battle", "Enemies" : ["5"],"Rewards" : {"GOLD" : 4, "EXP" : 2000, "Character" : "Anna"}},
        "Floor 4" :
                     {"id" : "4","bgm" : "boss", "Enemies" : ["7"],"Rewards" : {"GOLD" : 5, "EXP" : 2500}},
        "Floor 5" :
                     {"id" : "5","bgm" : "boss_vocal", "Enemies" : ["9","9"],"Rewards" : {"GOLD" : 6, "EXP" : 3000}}
         },
    "World 2" :
        {
        "Floor 1" :
                     {"id" : "6","bgm" : "battle_vocal", "Enemies" : ["11"],"Rewards" : {"GOLD" : 4, "EXP" : 2500}},
        "Floor 2" :
                     {"id" : "7","bgm" : "battle_vocal", "Enemies" : ["13"],"Rewards" : {"GOLD" : 6, "EXP" : 3000, "Character" : "Kris"}},
        "Floor 3" :
                     {"id" : "8","bgm" : "tears", "Enemies" : ["10"],"Rewards" : {"GOLD" : 8, "EXP" : 3500}},
        "Floor 4" :
                     {"id" : "9","bgm" : "battle_vocal", "Enemies" : ["17"],"Rewards" : {"GOLD" : 10, "EXP" : 4000}},
        "Floor 5" :
                     {"id" : "10","bgm" : "boss_vocal", "Enemies" : ["19","19"],"Rewards" : {"GOLD" : 12, "EXP" : 4500, "Character" : "Lilina"}}
         },
    "World 3" :
        {
        "Floor 1" :
                     {"id" : "11","bgm" : "katamusubi", "Enemies" : ["21"],"Rewards" : {"GOLD" : 8, "EXP" : 4000, "Character" : "Byleth"}},
        "Floor 2" :
                     {"id" : "12","bgm" : "katamusubi", "Enemies" : ["23"],"Rewards" : {"GOLD" : 12, "EXP" : 4500}},
        "Floor 3" :
                     {"id" : "13","bgm" : "katamusubi", "Enemies" : ["25"],"Rewards" : {"GOLD" : 16, "EXP" : 5000}},
        "Floor 4" :
                     {"id" : "14","bgm" : "katamusubi", "Enemies" : ["27"],"Rewards" : {"GOLD" : 20, "EXP" : 5500}},
        "Floor 5" :
                     {"id" : "15","bgm" : "frenzy", "Enemies" : ["29","29"],"Rewards" : {"GOLD" : 24, "EXP" : 6000}}
         }
}

#Player progress
player_worlds = {
    "World" : 1,
    "Floor" : 1,
    "Available" : {"1" : "rank_0"}#Keys are available floors. Ids are the ranking for that floor
}

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#framerate
clock = pygame.time.Clock()
global framesrate
framesrate = 60

#game window
global screen_width
global screen_height
screen_width = 1920
screen_height = 1080
global screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Whims of Fate")
pygame.display.set_icon(pygame.image.load("img/Char/Alear/icon.png"))
global display
display = pygame.Surface((screen_width,screen_height))

def diagonal(w,h):
    return math.sqrt((w*w)+(h*h))
global screen_diag
screen_diag = int(diagonal(screen_width,screen_height))

#fonts
def init_font(diag):
    output ={
           "small":pygame.font.SysFont("default", screen_mult(diag,26)),
           "franksmall":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,26)),
           "dmgsmall":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,39)),
           "dmgmed":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,45)),
           "medium":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,58)),
           "large":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,84)),
           "verylarge":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,110)),
           "battlemove":pygame.font.SysFont("Franklin Gothic Medium Cond", screen_mult(diag,230)),
           "title":pygame.font.SysFont("Aharoni", screen_mult(diag,200))}
    return output


#For rainbow colour
# Set the increment or decrement value for each color channel
incr = [4, 4, 4]

# Set the upper and lower bounds for each color channel
upper_bound = [255, 255, 255]
lower_bound = [0, 50, 0]
#All colours
colour = {"red" : (255, 0, 0), "green" : (0, 255, 0), "white" : (255,255,255), "black" : (0,0,0),"grey" : (100,100,100),"brightgrey" : (190,190,190), "menu" : (172, 254, 255), "rainbowcycle" : (255,0,0),
          "Fire" : (247, 65, 15), "Water" : (10, 86, 240), "Wind" : (48, 242, 129),"Singularity" : (252, 228, 104),
          "Buff" : (66, 135, 245), "Debuff" : (162, 78, 222), "Heal" : (0, 255, 0)}

#images

#image loaded
background = {
    "menu_main" : pygame.image.load("img/Background/menu_main.png").convert_alpha(),
    "Battle_1" : pygame.image.load("img/Background/battle_1.png").convert_alpha(),
    "Battle_2" : pygame.image.load("img/Background/battle_2.png").convert_alpha(),
    "Battle_3" : pygame.image.load("img/Background/battle_3.png").convert_alpha(),
    "Battle_1pre" : pygame.image.load("img/Background/battle_1pre.png").convert_alpha(),
    "Battle_2pre" : pygame.image.load("img/Background/battle_2pre.png").convert_alpha(),
    "Battle_3pre" : pygame.image.load("img/Background/battle_3pre.png").convert_alpha(),
    "Battle_4" : pygame.image.load("img/Background/battle_4.png").convert_alpha(),
    "Battle_5" : pygame.image.load("img/Background/battle_5.png").convert_alpha(),
    "Battle_5pre" : pygame.image.load("img/Background/battle_5pre.png").convert_alpha(),
    "Battle_spec" : pygame.image.load("img/Background/battle_5.png").convert_alpha(),
    "Battle_chall" : pygame.image.load("img/Background/battle_6.png").convert_alpha(),
    "Battle_final" : pygame.image.load("img/Background/battle_7.png").convert_alpha(),
    "menu_options" : pygame.image.load("img/Background/menu_options.png").convert_alpha(),
    "Levelup" : pygame.image.load("img/Background/Levelup.png").convert_alpha()
    }

img_skip = pygame.image.load("img/Other/icon_skip.png").convert_alpha()



img_party = {}

player=0
enemy=0
old_player_characters=player_characters
inviscircle=0
player_hp=0
player_eg=0
enemy_hp=0
damage_text_group=0
projectile_group=0
abilities=0
party=0


#background display
def draw_background(name,option):
    x,y = mouse_hovereffect(0,0,option)
    display.blit(pygame.transform.scale(background[name],(screen_width,screen_height)).convert(), (x,y))

def move_to_point(current_x, current_y, target_x, target_y, speed):
  #Calculate the distance to the target point
  #distance = math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2)

  #Calculate the direction to the target point
  angle = math.atan2(target_y - current_y, target_x - current_x)

  #Calculate the velocity in the x and y directions
  vel_x = math.cos(angle) * speed
  vel_y = math.sin(angle) * speed

  #Move the object to the target point
  current_x += vel_x
  current_y += vel_y

  return current_x, current_y, angle

def battle_draw_equips(person,target, x, y):
    #Icons 30x30, 10 pixels spacing in y
    #Increases when new equipment in list
    #Width and Height
    size = screen_mult(screen_diag,30)
    mouse_pos = pygame.mouse.get_pos()
    message = ""
    myColour = ""

    #BUFFS
    if len(list(person["buff"])) > 0:
        for buff in person["buff"]:
            buff_stats = get_buff(person, target, buff)
            image = pygame.transform.scale(img_buffs[buff],(size,size)).convert()
            display.blit(image, (x,y))
            pygame.draw.rect(display, colour["Buff"], (x, y, size+2, size+2), 2)
            if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
                message = str(buff) + ": " + str(buff_stats[2]) + " (" + str(person["buff"][buff]) + ")"
                myColour = "Buff"
            x += size + screen_mult(screen_width,10)
    if len(list(person["debuff"])) > 0:
        for buff in person["debuff"]:
            buff_stats = get_buff(person, target, buff)
            image = pygame.transform.scale(img_buffs[buff],(size,size)).convert()
            display.blit(image, (x,y))
            pygame.draw.rect(display, colour["Debuff"], (x, y, size+2, size+2), 2)
            if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
                message = str(buff) + ": " + str(buff_stats[2]) + " (" + str(person["debuff"][buff]) + ")"
                myColour = "Debuff"
            x += size + screen_mult(screen_width,10)

    #Mouse hovering
    if message != "" and myColour != "":
        draw_text(str(message), fonts["small"], colour[myColour],mouse_pos[0],mouse_pos[1], False)


def battle_draw_bonus(myBonuses, x, y):
    #Bonuses 30x30, 10 pixels spacing in y
    #Increases when new Bonus in list
    #Width and Height
    size = screen_mult(screen_diag,30)
    #For mouse hover
    mouse_pos = pygame.mouse.get_pos()
    message = ""
    myColour = ""
    #x and y are that of Bonus
    
    symbols = {"MHP" : "","AGG" : "","ER" : "%", "CRIT" : "", "CRIT DMG" : "%","Fire DMG" : "%",  "Water DMG" : "%",  "Wind DMG" : "%",  "RES" : "",  "STR" : "", "All DMG" : "%"}
            
    for bonus in myBonuses:
        if myBonuses[bonus] != 0:
            if myBonuses[bonus] > 0:    symbol = "+"
            else:   symbol = ""
            image = pygame.transform.scale(img_bonus[bonus],(size,size)).convert()
            display.blit(image, (x,y))
            #Outline
            if symbol == "+":
                pygame.draw.rect(display, colour["Buff"], (x, y, size+2, size+2), 2)
                col = "Buff"
            elif symbol == "":
                pygame.draw.rect(display, colour["Debuff"], (x, y, size+2, size+2), 2)
                col = "Debuff"

            if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
                message = str(bonus) + " " + str(symbol) + str(myBonuses[bonus]) + str(symbols[bonus])
                myColour = col
            x += size + screen_mult(screen_width,10)

    if message != "" and myColour != "":
        draw_text(str(message), fonts["small"], colour[myColour],mouse_pos[0],mouse_pos[1], False)

        
def battle_draw_stats(stats, x, y, col):
    message = ""
    for info in stats:
        if info.lower() != "charms" and info.lower() != "fusion" and info.lower() != "moves" and info.lower() != "bonuses":
            #Base stat value
            output = stats[info]
            #Adds to base stat if bonus available
            if info in stats["bonuses"]:  output += stats["bonuses"][info]
            output = str(info.upper()) + ": " + str(output)
            message += str(output) + " # "

    draw_text(str(message), fonts["small"], col, x, y, True)

def battle_draw_health(person, healthbar, mouse_pos):
    global player_characters
    x = person.rect.x
    y = person.rect.y+person.rect.height+screen_mult(screen_height,10)
    x,y = mouse_hovereffect(x,y,"circle")

    #If person is the player
    if person.stats["name"] in player_characters:
        rect_width, rect_height = screen_mult(screen_width,150),screen_mult(screen_height,70)
        myColour = person.stats["element"]
        hpColour = "green"
    else:
        rect_width, rect_height = screen_mult(screen_width,150),screen_mult(screen_height,40)
        myColour = "red"
        hpColour = "red"
    
    #Outline width makes box slightly wider to not cover text
    outline_width = screen_mult(screen_diag,3)
    box = pygame.Rect(x-outline_width, y-outline_width, rect_width+outline_width, rect_height+outline_width)
    #Main box
    pygame.draw.rect(display, colour["grey"], box)
    #Outline
    pygame.draw.rect(display, colour[myColour], (x-outline_width, y-outline_width, rect_width+outline_width, rect_height+outline_width), 3)

    #Healthbars
    draw_text(str(person.stats["name"]), fonts["small"], colour[myColour], x+screen_mult(screen_width,3), y+screen_mult(screen_height,3), False)
    healthbar.draw(x+screen_mult(screen_width,3),y+screen_mult(screen_height,22),person.stats["HP"],person.stats["MHP"]+person.stats["bonuses"]["MHP"],mouse_pos,hpColour)
    if "EG" in person.stats:
        if person.stats["EG"] == person.stats["MEG"]:   player_eg.draw(x+screen_mult(screen_width,3),y+screen_mult(screen_height,44),person.stats["EG"],person.stats["MEG"],mouse_pos,"rainbowcycle")
        else:   player_eg.draw(x+screen_mult(screen_width,3),y+screen_mult(screen_height,44),person.stats["EG"],person.stats["MEG"],mouse_pos,myColour)

    #Display stat bonuses
    #battle_draw_bonus(person.stats["bonuses"],x,y+rect_height+screen_mult(screen_height,5))
    #battle_draw_equips(player.stats,enemy.stats,x,y+rect_height+screen_mult(screen_height,5))

def battle_draw_enemyhealth(person, healthbar, mouse_pos):
    x = (person.rect.x+(person.rect.width/2))-((screen_width/4)/2)
    y = person.rect.y+person.rect.height+screen_mult(screen_height,10)
    x,y = mouse_hovereffect(x,y,"circle")

    rect_width, rect_height = (screen_width/4),screen_mult(screen_height,60)
    myColour = "red"
    hpColour = "red"

    #Outline width makes box slightly wider to not cover text
    outline_width = screen_mult(screen_diag,3)
    box = pygame.Rect(x-outline_width-screen_mult(screen_width,5), y-outline_width, rect_width+outline_width+screen_mult(screen_width,55), rect_height+outline_width)
    outline = pygame.Rect(x-outline_width-screen_mult(screen_width,5), y-outline_width, rect_width+outline_width+screen_mult(screen_width,55), rect_height+outline_width)
    #Main box
    pygame.draw.rect(display, colour["grey"], box)
    #Outline
    pygame.draw.rect(display, colour[myColour], outline, 3)

    #Healthbars
    draw_text(str(person.stats["name"]) + " Lvl." + str(person.stats["LVL"]), fonts["small"], colour[myColour], x+screen_mult(screen_width,3), y+screen_mult(screen_height,3), False)
    healthbar.draw(x+screen_mult(screen_width,3),y+screen_mult(screen_height,22),person.stats["HP"],person.stats["MHP"]+person.stats["bonuses"]["MHP"],mouse_pos,hpColour)

    #Display stat bonuses
    #battle_draw_bonus(person.stats["bonuses"],x,y+rect_height+screen_mult(screen_height,5))
    battle_draw_equips(enemy.stats,player.stats,x,y+rect_height+screen_mult(screen_height,5))


def get_lines(text, char_limit):
    lines = []
    line = ""
    for word in text.split(" "):
        if word == "#":
            lines.append(line)
            line = ""
        elif len(line) + len(word) >= char_limit:
            lines.append(line)
            line = word + " "
        else:
            line += word + " "
    lines.append(line)
    return lines

def draw_text(text,font,textcolour,x,y, includebox,alpha=255):
    if text == "":
        return

    #How long a single line of text can be
    char_limit = 40
    lines = get_lines(text, char_limit)

    #Find the character length of the longest line in text
    longest_line = ""
    for line in lines:
        if len(line) > len(longest_line):
            longest_line = line

    if includebox:
        #Outline width makes box slightly wider to not cover text
        outline_width = 3
        #Formulate textbox for text to appear in front of
        #"text[0]" to get a single character
        text_width, text_height = font.size(longest_line)
        textbox_rect = pygame.Rect(x-outline_width, y-outline_width, text_width+outline_width, text_height*len(lines)+outline_width)

        #Main box
        pygame.draw.rect(display, colour["grey"], textbox_rect)
        #Outline
        pygame.draw.rect(display, textcolour, (x-outline_width, y-outline_width, int(text_width+outline_width), int(text_height*len(lines))+outline_width), outline_width)

    #Render text line by line
    line_y = 0
    for line in lines:
        text_surface = font.render(line, True, textcolour)
        text_surface.set_alpha(alpha)
        display.blit(text_surface, (x, line_y + y))
        line_y += text_surface.get_height()
        
    #img = font.render(text, True, colour)
    #screen.blit(img, (x ,y))

def battle_music(track="streaked"):
    if track == "End":
        pygame.mixer.music.fadeout(3000)
        return

    pygame.mixer.music.load("snd/" + str(track) + ".wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=99)

def mouse_hovereffect(x,y,option):
    global inviscircle
    if option == "mouse":   mouse_x, mouse_y = pygame.mouse.get_pos() #Movement following the mouse
    elif option == "circle":    mouse_x,mouse_y = inviscircle.top_x,inviscircle.top_y #Moving in a circular motion
    else:   mouse_x,mouse_y = x,y
    spd = -0.01
    
    image_x, image_y = x,y
    image_x += (mouse_x - image_x) * spd
    image_y += (mouse_y - image_y) * spd

    return image_x, image_y

def colour_rainbowcycle():
    myColour = [colour["rainbowcycle"][0],colour["rainbowcycle"][1],colour["rainbowcycle"][2]]
    for i in range(3):
        myColour[i] += incr[i]
        if myColour[i] > upper_bound[i]:
            myColour[i] = upper_bound[i]
            incr[i] *= -1
        elif myColour[i] < lower_bound[i]:
            myColour[i] = lower_bound[i]
            incr[i] *= -1
    colour["rainbowcycle"] = myColour

def image_shake(intensity):
    #Image shake
    return random.randint(-intensity,intensity), random.randint(-intensity,intensity)

#combatents

def battle_updatestats(actor, target, battle_turndata):
    global player_characters
    bonus_values = {"MHP" : 0,"CRIT" : 0, "CRIT DMG" : 0, "STR" : 0, "RES" : 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, "AGG" : 0}
    newstats = battle_bonuscheck(actor,target,battle_turndata,bonus_values)

    return newstats

def get_element(prop):
    the_elements = ["Fire", "Water", "Wind","Singularity","Buff","Debuff","Heal"]
    for e in the_elements:
        if e in prop:
            return e
            break
    return "None"#Element not found


class Fighter():
    def __init__(self, x,y,statistics):
        global battle_characters
        self.status = "idle"
        self.stats = statistics
        self.x = x
        self.y = y
        self.condition = "Normal"
        
        #image loaded, and its scale is changeable
        
        self.image_list = {
            "turn" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/turn.png").convert_alpha(),
            "idle" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png").convert_alpha(),
            "dead" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/hurt.png").convert_alpha(),
            "hurt" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/hurt.png").convert_alpha(),
            "move" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/move.png").convert_alpha()}
        #Player has extra img
        if self.stats["name"] in battle_characters:
            self.image_list["ready"] = pygame.image.load("img/Char/" + str(self.stats["name"]) + "/ready.png").convert_alpha()

        #Projectiles
        self.img_proj = {
                "Fire" : pygame.image.load("img/Effects/proj_fire.png").convert_alpha(),
                "Fire_crit" : pygame.image.load("img/Effects/proj_fire_crit.png").convert_alpha(),
                "Wind" : pygame.image.load("img/Effects/proj_wind.png").convert_alpha(),
                "Wind_crit" : pygame.image.load("img/Effects/proj_wind_crit.png").convert_alpha(),
                "Water" : pygame.image.load("img/Effects/proj_water.png").convert_alpha(),
                "Water_crit" : pygame.image.load("img/Effects/proj_water_crit.png").convert_alpha(),
                "Singularity" : pygame.image.load("img/Effects/proj_sing.png").convert_alpha(),
                "Singularity_crit" : pygame.image.load("img/Effects/proj_sing_crit.png").convert_alpha()
                }
        
        #size = 1
        #self.image = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        

    def move(self, action, target,player_party):
        global damage_text_group
        

        #Functions acts as "Battle neutral"
        self.status = "move"
        message = ""
        message_colour = colour["white"]
        
        action_name = action
        action = battle_moveslookup(action)
        actionelement = get_element(action["prop"])
        if "inflict" in action:
            actioninflict = action["inflict"]
        else:
            actioninflict = "None"

        the_types = ["Offence", "Defence","Party"]
        actiontype = "None"
        for t in the_types:
            if t in action["prop"]:
                actiontype = t
                break

        #Contains all data of the current Turn
        battle_turndata = {
                     "action" : action,
                     "actionelement" : actionelement,
                     "actiontype" : actiontype,
                     "actioninflict" : actioninflict,
                     "actor" : self,#this is a class
                     "target" : target,#not a class, only stats
                     "turn" : self.stats["name"],
                     "totaldmg" : 0,
                     "crit" : False,
                     "critamount" : 0,
                     "weak" : False,
                     "weakamount" : 0,
                     "hit" : 0,
                     "heal" : 0,
                     "actorcondition" : "",
                     "targetcondition" : ""}

        if action_name not in player_party:
            #Stat bonuses to self and target
            self.stats["bonuses"] = battle_updatestats(self.stats,target,battle_turndata)
            target["bonuses"] = battle_updatestats(target,self.stats,battle_turndata)

        #Enemy attacking character in party
        if self.stats["name"] == enemy.stats["name"] and target["name"] in player_party and target["name"] != player.stats["name"]:
            player.switch(target["name"],player_party)
            
        #Change conditions
        if self.stats["HP"] <= 0: battle_turndata["actorcondition"] = "Defeated"
        elif self.stats["HP"]/(self.stats["MHP"]+self.stats["bonuses"]["MHP"]) <= 30:    battle_turndata["actorcondition"] = "Critical"
        else:   battle_turndata["actorcondition"] = "Normal"
        if target["HP"] <= 0: battle_turndata["targetcondition"] = "Defeated"
        elif target["HP"]/(target["MHP"]+target["bonuses"]["MHP"]) <= 30:    battle_turndata["targetcondition"] = "Critical"
        else:   battle_turndata["targetcondition"] = "Normal"

        #Reduce energy to 0 if performing a SPECIAL
        if "EG" in self.stats and "SPECIAL" in battle_turndata["action"]:
            self.stats["EG"] = 0

        #Calculate dmg/healing/etc

        if action_name == "Skip":
            message_colour = colour["white"]
            battle_damagetext(random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height), action_name, message_colour,"medium")
        elif action_name in player_party:
            self.switch(player_party[player_party.index(action_name)],player_party)
            myMixer("partyswitch.wav",-0.5)
            return battle_turndata,target
        elif battle_turndata["actiontype"] == "Offence":
            message_colour = colour["red"]

            #default text size
            size = "small"
            if "dmg" in action:
                message_colour = colour[battle_turndata["actionelement"]]
                battle_turndata["crit"] = False
                battle_turndata["weak"] = False
                basedmg = action["dmg"]

                damage = int(basedmg * ((self.stats["STR"]+self.stats["bonuses"]["STR"])/100))
                print("Before: " + str(damage))

                #Apply elemental dmg bonuses
                additional_damage_multiplier = 100
                if str(battle_turndata["actionelement"]) + " DMG" in self.stats:
                    additional_damage_multiplier += self.stats[str(battle_turndata["actionelement"]) + " DMG"]
                if str(battle_turndata["actionelement"]) + " DMG" in self.stats["bonuses"]:
                    additional_damage_multiplier += self.stats["bonuses"][str(battle_turndata["actionelement"]) + " DMG"]
                if "All DMG" in self.stats:
                    additional_damage_multiplier += self.stats["All DMG"]
                if "All DMG" in self.stats["bonuses"]:
                    additional_damage_multiplier += self.stats["bonuses"]["All DMG"]

                #Manage crits
                if random.randint(1,100) <= self.stats["CRIT"]+self.stats["bonuses"]["CRIT"] and damage > 0:
                    additional_damage_multiplier += self.stats["CRIT DMG"]+self.stats["bonuses"]["CRIT DMG"]
                    battle_turndata["critamount"] += 1
                    battle_turndata["crit"] = True
                #Manage weakness. Bonus is fixed amount
                if battle_turndata["actionelement"] in target["weakness"] and damage > 0:
                    additional_damage_multiplier += 50
                    battle_turndata["weakamount"] += 1
                    battle_turndata["weak"] = True

                damage = int(damage * (additional_damage_multiplier/100))
                #Damage reduction via RES
                damage -= int(damage * (target["RES"]+target["bonuses"]["RES"])/100)

                if damage < 0:  damage = 0
                else:   damage = int(damage)
                print("After: " + str(damage))


                #END OF DMG CALCULATION


                #Play sounds. Different sound based on crit hit
                sounds = {"Singularity" : "hit_sing.wav", "Fire" : "hit_fire.wav", "Water" : "hit_water.wav", "Wind" : "hit_wind.wav", }
                sounds_crit = {"Singularity" : "hit_sing.wav","Fire" : "hit_firecrit.wav", "Water" : "hit_watercrit.wav", "Wind" : "hit_windcrit.wav", }
                if battle_turndata["crit"] or battle_turndata["weak"]:    sound = sounds_crit[battle_turndata["actionelement"]]
                else:   sound = sounds[battle_turndata["actionelement"]]

                if battle_turndata["crit"] or battle_turndata["weak"]:  fontsize = "large"
                else:   fontsize = "dmgmed"

            
                    
                #Deal dmg
                battle_turndata["hit"] += 1
                battle_turndata["totaldmg"] += damage
                #Projectiles
                #Player's
                if self.stats["name"] in player_party:
                    actorxy = [self.rect.x+self.rect.width,self.rect.y+(self.rect.height/2)]
                    targetxy = [random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width),random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)]
                else:
                    actorxy = [self.rect.x-self.rect.width,self.rect.y+(self.rect.height/2)]
                    targetxy = [random.randint(player.rect.x,player.rect.x+player.rect.width),random.randint(player.rect.y,player.rect.y+player.rect.height)]
                
                if battle_turndata["crit"] or battle_turndata["weak"]: battle_projectile(actorxy,targetxy,self.img_proj[battle_turndata["actionelement"]+"_crit"])
                else:   battle_projectile(actorxy,targetxy,self.img_proj[battle_turndata["actionelement"]])
                #Damage text
                battle_damagetext(targetxy[0], targetxy[1]+2,str(damage), colour["grey"],fontsize)
                battle_damagetext(targetxy[0], targetxy[1],str(damage), colour[battle_turndata["actionelement"]],fontsize)
                if battle_turndata["weak"]:
                    battle_damagetext(targetxy[0]-screen_mult(screen_width,0), targetxy[1]+2+screen_mult(screen_height,20),"WEAK!", colour["grey"],"dmgsmall")
                    battle_damagetext(targetxy[0]-screen_mult(screen_width,0), targetxy[1]+screen_mult(screen_height,20),"WEAK!", colour[battle_turndata["actionelement"]],"dmgsmall")



                #Decrease hp
                target = battle_changehp(target, -damage, sound)

                #Change conditions
                if self.stats["HP"] <= 0: battle_turndata["actorcondition"] = "Defeated"
                elif self.stats["HP"]/(self.stats["MHP"]+self.stats["bonuses"]["MHP"]) <= 30:    battle_turndata["actorcondition"] = "Critical"
                else:   battle_turndata["actorcondition"] = "Normal"
                if target["HP"] <= 0: battle_turndata["targetcondition"] = "Defeated"
                elif target["HP"]/(target["MHP"]+target["bonuses"]["MHP"]) <= 30:    battle_turndata["targetcondition"] = "Critical"
                else:   battle_turndata["targetcondition"] = "Normal"


            #Apply debuff if attack has one
            if battle_turndata["actioninflict"] != "None":
                if self.stats["name"] in player_party:
                    x,y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Debuff", x,y,target)
                else:
                    x,y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Debuff", x,y,target)
                
        elif battle_turndata["actiontype"] == "Defence":#Cast move on self
            #Healing
            if "heal" in action:
                amount = int((action["heal"] * ((self.stats["MHP"]+self.stats["bonuses"]["MHP"])/100)))
                if self.stats["name"] == target["name"]:
                    battle_damagetext(self.rect.x+(self.rect.width/2), self.rect.y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                    self.stats = battle_changehp(self.stats, amount,"heal.wav")
                elif target["name"] in player_party:
                    battle_damagetext(400, screen_height/2,str(amount), colour[battle_turndata["actionelement"]],"medium")
                    target = battle_changehp(target, amount,"heal.wav")
            #Apply buff
            if battle_turndata["actioninflict"] != "None":
                if self.stats["name"] == target["name"]:
                    x,y = random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height)
                    self.stats = battle_applybuffs(battle_turndata["actioninflict"],2, "Buff", x,y,self.stats)
                elif target["name"] in player_party:
                    x,y = screen_mult(screen_width,400), (screen_height/(len(player_party)+1)) * (player_party.index(target["name"])+1)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,target)
        elif battle_turndata["actiontype"] == "Party" and self.stats["name"] in player_party:#Cast move on party member
            for member in player_party:
                if (self.stats["name"] == member and self.stats["HP"] <= 0) or (battle_characters[member]["HP"] <= 0):
                    continue#Do no include downed members
                #Healing
                if "heal" in battle_turndata["action"]:
                    amount = int((action["heal"] * ((self.stats["MHP"]+self.stats["bonuses"]["MHP"])/100)))
                    if self.stats["name"] == member:
                        battle_damagetext(self.rect.x+(self.rect.width/2), self.rect.y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                        self.stats = battle_changehp(self.stats, amount,"heal.wav")
                    else:
                        x,y = screen_mult(screen_width,400), (screen_height/(len(player_party)+1)) * (player_party.index(member)+1)
                        battle_damagetext(x, y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                        battle_characters[member] = battle_changehp(battle_characters[member], amount,"heal.wav")
                #Apply buff
                if battle_turndata["actioninflict"] != "None":
                    if self.stats["name"] == member:
                        x,y = random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height)
                        self.stats = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,self.stats)
                    else:
                        x,y = screen_mult(screen_width,400), (screen_height/(len(player_party)+1)) * (player_party.index(member)+1)
                        battle_characters[member] = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,battle_characters[member])
            
        #Update bonuses
        self.stats["bonuses"] = battle_updatestats(self.stats,target,battle_turndata)
        target["bonuses"] = battle_updatestats(target,self.stats,battle_turndata)
        return battle_turndata,target
            

    def update(self):
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    #image display
    #(methods must have "self" as a minimum)
    def draw(self, x, y):
        self.rect.center = (x,y)
        display.blit(self.image, self.rect)
        
    def switch(self,new_name,player_party):
        global abilities
        global party
        global battle_characters
        #Player exclusive.
        flag = False
        for person in battle_characters:
            if person == self.stats["name"]:
                battle_characters[person] = self.stats
            elif person == new_name:            
                self.stats = battle_characters[person]
                flag = True

        #Character not found, cannot switch
        if flag == False:
            return
        
        self.status = "turn"
        abilities = battle_createability(self.stats["moves"])
        party = battle_createparty(player_party)
        
        
        self.image_list = {
            "turn" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/turn.png").convert_alpha(),
            "idle" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png").convert_alpha(),
            "dead" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/hurt.png").convert_alpha(),
            "hurt" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/hurt.png").convert_alpha(),
            "move" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/move.png").convert_alpha(),
            "ready" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/ready.png").convert_alpha()
        
                           }
        
        #size = 1
        #self.image = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)



class ProgressBar():
    def __init__(self,width, height,direction="horizontal"):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.direction = direction

    def draw(self, x,y,value, maxvalue, mouse_pos,col,show_percent=True):
        self.x = x
        self.y = y
        #update with new "value"
        self.value = int(value)
        self.maxvalue = int(maxvalue)
        #calculate percentage
        percent = int((self.value / self.maxvalue) * 100)

        #Makes sure fill rectange does not exceed limit
        if percent >= 100:
            percent = 100
        elif percent <= 0:
            percent = 0
            if self.value > 0:
                percent = 1
        
        if self.direction == "horizontal":
            if show_percent: draw_text(str(percent) + "%", fonts["small"], colour[col], x + self.width+2, y-3, False)#Display percentage
            pygame.draw.rect(display, colour["grey"], (x, y, self.width, self.height))
            pygame.draw.rect(display, colour[col], (x, y, (percent/100)*self.width, self.height))
            #Outline
            pygame.draw.rect(display, colour[col], (x-1, y-1, self.width+1, self.height+1), 1)

            #Display exact values when hovering with mouse
            if (mouse_pos[0] >= x and mouse_pos[0] <= self.width+x) and (mouse_pos[1] >= y and mouse_pos[1] <= y+self.height):
                draw_text("(" + str(self.value) + "/" + str(int(self.maxvalue)) + ")", fonts["small"], colour["white"],mouse_pos[0],mouse_pos[1], False)
        elif self.direction == "vigour":
            if show_percent: draw_text(str(percent) + "%", fonts["small"], colour[col], x-3, y+ self.height+2, False)
            pygame.draw.rect(display, colour[col], (x, y, self.width, (percent/100)*self.height))

            #Display exact values when hovering with mouse
            if (mouse_pos[0] >= x and mouse_pos[0] <= self.width+x) and (mouse_pos[1] >= y and mouse_pos[1] <= y+self.height):
                draw_text("(" + str(self.value) + "/" + str(int(self.maxvalue)) + ")", fonts["small"], colour["white"],mouse_pos[0],mouse_pos[1], False)



def myMixer(decision,direction):
  global myMixerSwitch
  decision = str(decision)
  #Direction is a float from -1.0 to 1.0. 0 makes sound normal
  L, R = 1.0, 1.0
  if direction != 0:
      if direction > 0:
          L -= direction
      elif direction < 0:
          R += direction
  
  if decision == "":
    return
  elif ".wav" in decision:
    try:
      #Create sound channel instance and play the sound
      channel = pygame.mixer.Sound("snd/" + str(decision)).play()
      #Set volume according to direction
      channel.set_volume(L,R)
    except Exception as e:
      print("Cannot play sound '" + str(decision) + "':\n" + str(e))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, value, colour, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image_original = fonts[size].render(value, True, colour)
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.center = (self.x+self.rect.width/2, self.y+self.rect.height/2)
        #to control how long to make text exist for
        self.counter = 0
        self.alpha = self.image.get_alpha()
        self.scale = screen_mult(screen_diag,500)
        if size == "large":
            self.scale += int(self.scale/2)
            self.counter = -framesrate/2
        self.scale_original = self.scale
        
    def update(self):
        #decrease y cord (move text up)
        self.counter += 1
        #Moves 3 times slower
        if self.counter % 2 == 0:
            self.y -= 1
        if self.scale > 100:
            self.scale -= int(int((self.scale_original*20)/framesrate))
            if self.scale > 0:
                self.image = pygame.transform.scale(self.image, (int(self.rect.width*(self.scale/100)),int(self.rect.height*(self.scale/100))))
        else:
            self.image = self.image_original

        self.image.set_alpha(self.alpha)
            
        self.rect.center = (self.x-(self.image.get_rect()).width/2, self.y-(self.image.get_rect().height/2))

        #Kill after 2 seconds
        if self.counter > framesrate*2:
            self.kill()
        elif self.counter > framesrate:
            self.alpha -= int(255/framesrate)*2


def battle_damagetext(x,y, message, message_colour, message_size):
    #random.randint(target.rect.x,target.rect.x+target.rect.width), random.randint(target.rect.y,target.rect.y+target.rect.height)
    damage_text = DamageText(x,y, message, message_colour,message_size)
    damage_text_group.add(damage_text)

class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_x = target_x
        self.target_y =target_y
        self.speed = int(screen_mult(screen_width,8000)/framesrate)
        #0.3 second limit
        self.limit = framesrate/4

        #Rotate image
        if self.rect.center[0] > self.target_x:
            self.image = pygame.transform.rotate(self.image,180)
    def update(self):
        self.limit -= 1
        self.rect.center = move_to_point(self.rect.center[0],self.rect.center[1],self.target_x,self.target_y,self.speed)[0],move_to_point(self.rect.center[0],self.rect.center[1],self.target_x,self.target_y,self.speed)[1]
        display.blit(self.image, self.rect)

        if ((self.target_x >= self.rect.x and self.target_x <= self.rect.x + self.rect.width) and (self.target_y >= self.rect.y and self.target_y <= self.rect.y + self.rect.height)) or self.limit <= 0:
            self.kill()

def battle_projectile(actor, target, image):
    projectile = Projectile(image, actor[0],actor[1],target[0],target[1])
    projectile_group.add(projectile)

class NormalText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts["small"].render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Battle_invisCircle():#Invisible moving circle. For circular animation of UI
    def __init__(self,centre_x,centre_y,radius):
        self.centre_x, self.centre_y = centre_x, centre_y
        self.radius = radius
        self.angle = 0
        self.angular_velocity = 1
        self.line_width = 1
        self.colour = (0,0,0,0)
        self.top_x, self.top_y = 0,0
        
    def update(self,spd):
        if spd == "":
            self.angular_velocity = 2
        else:
            self.angular_velocity = spd
        # Update the angle
        self.angle += (self.angular_velocity/framesrate)*100
        # Convert the angle to radians
        radians = math.radians(self.angle)
        # Calculate the position of the top point
        self.top_x = int(self.centre_x + self.radius * math.cos(radians))
        self.top_y = int(self.centre_y + self.radius * math.sin(radians))

    def draw(self):
        # Draw the circle
        pygame.draw.circle(screen, self.colour, (self.centre_x, self.centre_y), self.radius, self.line_width)

def get_fusion(fusion):
  #First 6 fusions are basic
  #Last 4 are complex and open new playstyles

  #Fusion = {Effects : [], Desc : ""}
  #Effect = {Conditions : [], Stat : "", Amount : 0}
  #Condition = {Type1 : "TurnData"/"Stats", Stat1 : data[turn]/MHP, Amount1 : 0, Type2 : "TurnData"/"Stats", Stat2 : data[turn]/MHP, Amount2 : 0, Comparison : ">"/"=="/etc}

  #Algorithm runs through every CONDITION of EFFECT. If all CONDITIONs are true, EFFECT is enabled and performed (Amount is added to Stat).
  #Effects can have multiple Conditions, and Fusions can have multiple Effects.
  #As algorithm runs through Fusion, a Description is tabulated.


  newfusions = {
      "Wind Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT", "Num" : 8}]},
      "Wind Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 16}]},
      "Wind Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 10}]},
      "Wind Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT", "Num" : 16}]},
      "Wind Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 32}]},
      "Wind Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 20}]},
      "Wind Type 07" : {"Effects" : [{"Cond" : "Crit", "Stat" : "Buff", "Num" : "Focused"}]},#Landing crit grants Focused buff
      "Wind Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 30}, {"Cond" : "Actor HP higher", "Stat" : "CRIT DMG", "Num" : 30}]},#+35 crit dmg if hp higher than target. +35 crit dmg.
      "Wind Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 25},{"Cond" : "Crit", "Stat" : "Wind DMG", "Num" : 25}]},#+50% wind dmg. Landing crit gives +50% wind dmg
      "Prototype: GALE" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 25},{"Cond" : "HP 60% higher", "Stat" : "CRIT", "Num" : 20}, {"Cond" : "HP 60% higher", "Stat" : "CRIT DMG", "Num" : 40},{"Cond" : "HP 60% lower", "Stat" : "CRIT", "Num" : 40},{"Cond" : "HP 60% lower", "Stat" : "CRIT DMG", "Num" : 20},{"Cond" : "Critical condition", "Stat" : "CRIT", "Num" : 20},{"Cond" : "Critical condition", "Stat" : "CRIT DMG", "Num" : 80}]},

      "Fire Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "MHP", "Num" : 20}]},
      "Fire Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 10}]},
      "Fire Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Fire DMG", "Num" : 10}]},
      "Fire Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "MHP", "Num" : 40}]},
      "Fire Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 20}]},
      "Fire Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Fire DMG", "Num" : 20}]},
      "Fire Type 07" : {"Effects" : [{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Blaze Shield"}]},#Taking hits grants Blaze Shield buff, extra mhp
      "Fire Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 30},{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Concentrated"}, {"Cond" : "Take hit", "Stat" : "Debuff", "Num" : "Vulnerable"}]},#+60 str. Grants concentrate to self and Vulnerable to opponent when taking hits.
      "Fire Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Buff", "Num" : "Pyroclastic Charge"}]},#Every point of Max HP increases Fire DMG bonus by 0.05%
      "Prototype: BLZE" : {"Effects" : [{"Cond" : "", "Stat" : "MHP", "Num" : 40},{"Cond" : "HP 60% lower", "Stat" : "Buff", "Num" : "Pyroclastic Charge"}, {"Cond" : "Critical condition", "Stat" : "Buff", "Num" : "Pyroclastic Surge"}]},#Every point of Max HP increases Fire DMG bonus by 0.05%, double the effect in critical condition
      
      "Water Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 5}]},
      "Water Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "AGG", "Num" : 5}]},
      "Water Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 10}]},
      "Water Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10}]},
      "Water Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "AGG", "Num" : 10}]},
      "Water Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 20}]},
      "Water Type 07" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10},{"Cond" : "", "Stat" : "AGG", "Num" : 10}, {"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Invulnerable"}, {"Cond" : "Take hit", "Stat" : "Debuff", "Num" : "Drained"}]},#RES +20. Grants invulnerable to self and drained to target when taking hit
      "Water Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 45}, {"Cond" : "Actor HP higher", "Stat" : "Water DMG", "Num" : 45}]},#+60 phys dmg. +20 if hp higher than opponent
      "Water Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 30},{"Cond" : "", "Stat" : "Buff", "Num" : "Inspired"}]},#+50% water dmg. Inspired: every point of RES gives 2% Water DMG.
      "Prototype: AQUA" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10},{"Cond" : "", "Stat" : "AGG", "Num" : 10},{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Awakened"},{"Cond" : "Critical condition", "Stat" : "Buff", "Num" : "Awakened One"}]}#Taking hits grants Awakaned: 50% water dmg + 10 RES. Awakened One: all bonuses increased by 50%.

      ,"Prototype: STAR" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 30},{"Cond" : "Not critical condition", "Stat" : "Buff", "Num" : "Half Moon"},{"Cond" : "Critical condition", "Stat" : "Buff", "Num" : "Full Moon"}]}
        }
      
  newoutput = ["","",""]
  desc = ""
  if fusion not in newfusions:
      return newoutput
  else:
      newoutput[0] = fusion


      conditions = {
          "Critical condition" : "When in Critical Condition",
          "Not critical condition" : "When not in Critical Condition",
          "Actor HP higher" : "When HP is higher than opponent's",
          "Target HP higher" : "When HP is lower than opponent's",
          "HP 60% higher" : "When above 60% HP",
          "HP 60% lower" : "When below 60% HP",
          "Crit" : "When landing a CRIT",
          "Take crit" : "When taking a CRIT hit",
          "Hit" : "When landing an attack",
          "Take hit" : "When hit by an attack",
          #No condition
          "" : ""}

      #Conditions and their effects.
      conditions_output = {}
      #Conditions and their effect description.
      conditions_outputdesc = {}

      #For every effect in Fusion
      for effect in newfusions[fusion]["Effects"]:
          if effect["Cond"] not in conditions_output:
              #Adds conditions
              conditions_output[effect["Cond"]] = {"Buff" : [], "Debuff" : []}
              conditions_outputdesc[effect["Cond"]] = []

          #Adds effect for condition + desc
          if effect["Stat"] != "Buff" and effect["Stat"] != "Debuff":
              conditions_output[effect["Cond"]][effect["Stat"]] = effect["Num"]
              message=effect["Stat"] + " increased by " + str(effect["Num"])
              if effect["Stat"] == "MHP" or effect["Stat"] == "STR" or effect["Stat"] == "Fire DMG" or effect["Stat"] == "Water DMG" or effect["Stat"] == "Wind DMG" or effect["Stat"] == "All DMG" or effect["Stat"] == "ER":
                  message += "%"
              conditions_outputdesc[effect["Cond"]].append(message)
          elif effect["Stat"] == "Buff":
              conditions_output[effect["Cond"]]["Buff"].append(effect["Num"])
              conditions_outputdesc[effect["Cond"]].append("Gain the '" + str(effect["Num"]) + "' buff")
          elif effect["Stat"] == "Debuff":
              conditions_output[effect["Cond"]]["Debuff"].append(effect["Num"])
              conditions_outputdesc[effect["Cond"]].append("Apply the '" + str(effect["Num"]) + "' debuff on opponent")


      for cond in conditions_output:
          #Removes buff/debuff section if no buff/debuff effects
          if len(conditions_output[cond]["Buff"]) == 0:
              conditions_output[cond].pop("Buff")
          if len(conditions_output[cond]["Debuff"]) == 0:
              conditions_output[cond].pop("Debuff")

      #Formulates description
      for cond in conditions_outputdesc:
          if cond != "":    desc += conditions[cond] + ", "
          for effect in conditions_outputdesc[cond]:
              desc += effect
              if effect == conditions_outputdesc[cond][-1]: desc += ". "
              else: desc += " and "
          desc += "# "


  newoutput[1] = desc
  newoutput[2] = conditions_output

  #e.g output = ["Wind Type 01", Conditions+Effect descs, Conditions+Effects]
  return newoutput

def get_enemies(option):
  global battle_characters
  global player_party
  #Enemy names:
  #Elemental, Fighter, Guardian, Sentinel
  enemies = [

    {"name" : "Wind Elemental","id": "1", "LVL" : 1, "turns" : 2,"MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 1, "CRIT" : 30, "CRIT DMG" : 50, "fusion" : "Wind Type 01", "moves" : {"Garudyne":0}, "weakness" : "Fire"},
    {"name" : "Wind Elemental","id": "2", "LVL" : 5, "turns" : 2,"MHP" : 1100, "HP" : 1200, "STR" : 100, "RES" : 2, "CRIT" : 30, "CRIT DMG" : 50, "fusion" : "Wind Type 02", "moves" : {"Garudyne":0, "Focus":0}, "weakness" : "Fire"},
    {"name" : "Wind Elemental","id": "3", "LVL" : 10, "turns" : 2,"MHP" : 1200, "HP" : 1400, "STR" : 100, "RES" : 3, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 03", "moves" : {"Garudyne":0, "Wind Boost":0}, "weakness" : "Fire"},
    {"name" : "Wind Fighter","id": "4", "LVL" : 15, "turns" : 2,"MHP" : 1300, "HP" : 1600, "STR" : 100, "RES" : 4, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 04", "moves" : {"Garudyne":0, "Overhype":0, "Focus":0}, "weakness" : "Fire"},
    {"name" : "Wind Fighter","id": "5", "LVL" : 20, "turns" : 2,"MHP" : 1400, "HP" : 1800, "STR" : 100, "RES" : 5, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 05", "moves" : {"Focus":0, "Garudyne" : 0}, "weakness" : "Fire"},
    {"name" : "Wind Fighter","id": "6", "LVL" : 25, "turns" : 2,"MHP" : 1500, "HP" : 2000, "STR" : 100, "RES" : 6, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 06", "moves" : {"Wrath Tempest":0}, "weakness" : "Fire"},
    {"name" : "Wind Guardian","id": "7", "LVL" : 30, "turns" : 2,"MHP" : 1600, "HP" : 2200, "STR" : 100, "RES" : 7, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 07", "moves" : {"Overhype":0, "Garudyne":0}, "weakness" : "Fire"},
    {"name" : "Wind Guardian","id": "8", "LVL" : 35, "turns" : 2,"MHP" : 1800, "HP" : 2400, "STR" : 100, "RES" : 8, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 08", "moves" : {"Focus":0, "Garudyne":0}, "weakness" : "Fire"},
    {"name" : "Wind Sentinel","id": "9", "LVL" : 40, "turns" : 3,"MHP" : 2000, "HP" : 2600, "STR" : 100, "RES" : 9, "CRIT" : 30,"CRIT DMG" : 50, "fusion" : "Wind Type 09", "moves" : {"Wrath Tempest":0, "Garudyne":0}, "weakness" : "Fire"},
    {"name" : "Kaze","id": "10", "LVL" : 45, "turns" : 3,"MHP" : 2500, "HP" : 2500, "STR" : 100, "RES" : 10, "CRIT" : 30,"CRIT DMG" : 50,  "fusion" : "Prototype: GALE", "moves" : {"Wind Boost":0,"Wrath Tempest":0,"Cyclone":0}, "weakness" : "Fire"},

    {"name" : "Fire Elemental","id": "11", "LVL" : 1,"turns" : 2, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 1, "CRIT" : 2,"CRIT DMG" : 50, "fusion" : "Fire Type 01", "moves" : {"Agi":0, "Overgrow":0}, "weakness" : "Water"},
    {"name" : "Fire Elemental","id": "12", "LVL" : 5,"turns" : 2, "MHP" : 1100, "HP" : 1100, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "fusion" : "Fire Type 02", "moves" : {"Agi":0, "Concentrate":0}, "weakness" : "Water"},
    {"name" : "Fire Elemental","id": "13", "LVL" : 10,"turns" : 2, "MHP" : 1200, "HP" : 1200, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "fusion" : "Fire Type 03", "moves" : {"Fire Boost":0, "Agi":0}, "weakness" : "Water"},
    {"name" : "Fire Fighter","id": "14", "LVL" : 15,"turns" : 2, "MHP" : 1300, "HP" : 1300, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "fusion" : "Fire Type 04", "moves" : {"Agilao":0, "Overgrow":0, "Diarama" : 0}, "weakness" : "Water"},
    {"name" : "Fire Fighter","id": "15", "LVL" : 20,"turns" : 2, "MHP" : 1400, "HP" : 1400, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "fusion" : "Fire Type 05", "moves" : {"Concentrate":0, "Fire Dance" : 0}, "weakness" : "Water"},
    {"name" : "Fire Fighter","id": "16", "LVL" : 25,"turns" : 2, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "fusion" : "Fire Type 06", "moves" : {"Burning Hell":0}, "weakness" : "Water"},
    {"name" : "Fire Guardian","id": "17", "LVL" : 30,"turns" : 2, "MHP" : 1600, "HP" : 1600, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50,"fusion" : "Fire Type 07", "moves" : {"Diarama":0, "Agidyne" : 0}, "weakness" : "Water"},
    {"name" : "Fire Guardian","id": "18", "LVL" : 35,"turns" : 2, "MHP" : 1800, "HP" : 1800, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "fusion" : "Fire Type 08", "moves" : {"Fire Boost":0, "Agibarion":0}, "weakness" : "Water"},
    {"name" : "Fire Sentinel","id": "19", "LVL" : 40,"turns" : 3, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "fusion" : "Fire Type 09", "moves" : {"Burning Hell":0, "Fire Dance":0}, "weakness" : "Water"},
    {"name" : "Hi", "LVL" : 45,"id": "20", "MHP" : 3000,"turns" : 3, "HP" : 2500, "STR" : 2500, "RES" : 10, "CRIT" : 20,"CRIT DMG" : 50, "fusion" : "Prototype: BLZE", "moves" : {"Fire Boost":0,'Debilitate': 0, "Burning Hell" : 0}, "weakness" : "Water"},

    {"name" : "Water Elemental","id": "21", "LVL" : 1,"turns" : 2, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 10, "CRIT" : 2,"CRIT DMG" : 50, "fusion" :"Water Type 01", "moves" : {"Resist":0, "Bufu":0}, "weakness" : "Wind"},
    {"name" : "Water Elemental","id": "22", "LVL" : 5,"turns" : 2, "MHP" : 1100, "HP" : 1100, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "fusion" : "Water Type 02", "moves" : {"Charge" : 0,"Megi":0}, "weakness" : "Wind"},
    {"name" : "Water Elemental","id": "23", "LVL" : 10,"turns" : 2, "MHP" : 1200, "HP" : 1200, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "fusion" : "Water Type 03", "moves" : {"Water Boost":0, "Rush":0}, "weakness" : "Wind"},
    {"name" : "Water Fighter","id": "24", "LVL" : 15,"turns" : 2, "MHP" : 1300, "HP" : 1300, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "fusion" : "Water Type 04", "moves" : {"Bufula":0, "Resist":0}, "weakness" : "Wind"},
    {"name" : "Water Fighter","id": "25", "LVL" : 20,"turns" : 2, "MHP" : 1400, "HP" : 1400, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "fusion" : "Water Type 05", "moves" : {"Megido":0, "Charge":0}, "weakness" : "Wind"},
    {"name" : "Water Fighter","id": "26", "LVL" : 25,"turns" : 2, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "fusion" : "Water Type 06", "moves" : {"Thalassic Calamity":0, "Concentrate":0}, "weakness" : "Wind"},
    {"name" : "Water Guardian","id": "27", "LVL" : 30,"turns" : 2, "MHP" : 1600, "HP" : 1600, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50, "fusion" : "Water Type 07", "moves" : {"Thalassic Calamity":0, "Inspire":0}, "weakness" : "Wind"},
    {"name" : "Water Guardian","id": "28", "LVL" : 35,"turns" : 2, "MHP" : 1800, "HP" : 1800, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "fusion" : "Water Type 08", "moves" : {"Bufudyne":0, "Megidola":0},"weakness" : "Wind"},
    {"name" : "Water Sentinel","id": "29", "LVL" : 40,"turns" : 3, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "fusion" : "Water Type 09", "moves" : {"Bufubarion":0, "Water Boost":0,"Debilitate":0}, "weakness" : "Wind"},
    {"name" : "Mizu", "LVL" : 45,"id": "30", "MHP" : 2500,"turns" : 3, "HP" : 2500, "STR" : 100, "RES" : 10, "CRIT" : 20, "CRIT DMG" : 50, "fusion" : "Prototype: AQUA", "moves" : {"Water Boost":0, "Thalassic Calamity":0, "Bufubarion" : 0},"weakness" : "Wind"}
     ]

  if option == "all":#all enemies
      return enemies
  elif option == "any":#random enemy
      return random.choice(enemies)
  else:
      for e in enemies:#search for specific enemy
          if option == e["id"]:
              return e
              break
      return enemies[0]#return first enemy if desired is not found

def battle_charmslookup(request):
    #WIP
    #Set bonuses
    sets = {
        "Fire Emblem" : {
            "2pc" : [{"Cond" : "", "Stat" : "MHP", "Num" : 20}],
            "4pc" : [{"Cond" : "HP 60% lower", "Stat" : "Fire DMG", "Num" : 30}]},
        "Water Emblem" : {
            "2pc" : [{"Cond" : "", "Stat" : "RES", "Num" : 10}],
            "4pc" : [{"Cond" : "HP 60% higher", "Stat" : "AGG", "Num" : 20},{"Cond" : "Take hit", "Stat" : "Buff", "Num" : ""}]},
        "Wind Emblem" : {
            "2pc" : [{"Cond" : "", "Stat" : "CRIT", "Num" : 10}],
            "4pc" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 30}]},
        "Star Emblem" : {
            "2pc" : [{"Cond" : "", "Stat" : "All DMG", "Num" : 10}],
            "4pc" : [{"Cond" : "HP 60% higher", "Stat" : "All DMG", "Num" : 30}]}}

    #Generate [request amount] random charms
    if request != "":
        count = request
        charms = []
        stats = {
                 "Fire DMG" : 5,
                 "Water DMG" : 5,
                 "Wind DMG" : 5,
                 "All DMG" : 5,
                 "CRIT DMG" : 10,
                 "CRIT" : 5,
                 "MHP" : 10,
                 "STR" : 10,
                 "RES" : 3}
        
        rarities = {"1" : "common", "2" : "rare", "3" : "legend"}

        while count > 0:
            stat = random.choice(list(stats))
            stat_num = stats[stat]
            #rarity = random.randint(1,3)
            rarity = 3
            set_type = random.choice(
                ["Power"#, "Fire", "Wind", "Water", "Star", "Focus", "Hyper", "Blaze", "Strength", "Shield"
                 ]
            )
            
            new_charm = {
                "set" : set_type + " Emblem",
                "img" : "charm_"+str(set_type).lower(),
                "stat" : stat,
                "amount" : int(stat_num*rarity),
                "rarity" : rarities[str(rarity)]}
                
            
            
            #Descriptions
            new_charm["desc"] = "+" + str(new_charm["amount"])
            if new_charm["stat"] == "MHP" or new_charm["stat"] == "STR":
                new_charm["desc"] += "%"
            new_charm["desc"] += " " + str(new_charm["stat"])

            charms.append(new_charm)
            count -= 1

        return charms

def charms_eq_check(ID):
    global player_characters
    result = ""

    for char in player_characters:
        if str(ID) in player_characters[char]["charms"]:
            result = char
            break

    return result

def move_stats(multiplier, lvl):
    #Increases move strength based on level
    return int(multiplier+((multiplier*0.15)*(lvl-1)))

def battle_moveslookup(move, lvl=1):
  #"Name : [BaseDMG, Range of hits, Type Offence/Defence/Heal, Buff/Debuff infliction, Element, Unique attribute]"

  #THESE NEED TO BE REWORKED
  all_moves = {
                  #Healing
                  "Diarama" : [20, [0,0], "Defence", "None","Heal",""]
                  ,"SPECIAL: Shining Arrows" : [50, [8,0], "Offence", "None","Singularity",""]
                  #Water
                  ,"Bufu" : [50, [1,0], "Offence", "None","Water",""]
                  ,"Bufula" : [80, [1,0], "Offence", "None","Water",""]
                  ,"Bufudyne" : [100, [1,0], "Offence", "None","Water",""]
                  ,"Bufubarion" : [120, [1,0], "Offence", "None","Water",""]
                  ,"Thalassic Calamity" : [66, [3,0], "Offence", "None","Water",""]
                  ,"Striking Tide" : [20,[10,0], "Offence", "None","Water",""]
                  ,"SPECIAL: Hyperflood Abrasion" : [320,[1,0], "Offence", "None","Water",""]
                  #Fire
                  ,"Agi" : [50, [1,0], "Offence", "None","Fire",""]
                  ,"Agilao" : [80, [1,0], "Offence", "None","Fire",""]
                  ,"Agidyne" : [100, [1,0], "Offence", "None","Fire",""]
                  ,"Agibarion" : [120, [1,0], "Offence", "None","Fire",""]
                  ,"Fire Dance" : [66, [3,0], "Offence", "None","Fire",""]
                  ,"Burning Hell" : [200, [1,0], "Offence", "None","Fire",""]
                  ,"SPECIAL: Cataclysm" : [32,[10,0], "Offence", "None","Fire",""]
                  #Wind
                  ,"Garu" : [50, [1,0], "Offence", "None","Wind",""]
                  ,"Garula" : [80, [1,0], "Offence", "None","Wind",""]
                  ,"Garudyne" : [100, [1,0], "Offence", "None","Wind",""]
                  ,"Garubarion" : [120,[1,0], "Offence", "None","Wind",""]
                  ,"Cyclone" : [25,[8,0], "Offence", "None","Wind",""]
                  ,"Wrath Tempest" : [100,[2,0], "Offence", "None","Wind",""]
                  ,"SPECIAL: Eye of the Storm" : [320,[1,0], "Offence", "None","Wind",""]
                   #Singularity      
                  ,"SPECIAL: Tenman Crescent Moon" : [45,[10,0], "Offence", "None","Singularity",""]
                  #Support
                  , "Debilitate" : [0, [0,0], "Offence", "Vulnerable","Debuff","Decreases opponent's RES"]
                  , "Taunt" : [0, [0,0], "Defence", "Taunt","Buff","Draws enemy attention"]
                  , "Concentrate" : [0, [0,0], "Defence", "Concentrated","Buff","Increases All DMG"]
                  , "Wind Boost" : [0, [0,0], "Defence", "Wind Boost","Buff","Increases Wind DMG"]
                  , "Fire Boost" : [0, [0,0], "Defence", "Fire Boost","Buff","Increases Fire DMG"]
                  , "Water Boost" : [0, [0,0], "Defence", "Water Boost","Buff","Increases Water DMG"]
                  , "Focus" : [0, [0,0], "Defence", "Focused","Buff","Increases CRIT Rate"]
                  , "Overhype" : [0, [0,0], "Defence", "Hyped","Buff","Increases CRIT DMG"]
                  , "Overgrow" : [0, [0,0], "Defence", "Overgrown","Buff","Increases Max HP"]
                  , "Awaken" : [0, [0,0], "Defence", "Awakened","Buff","Increases All DMG based on RES"]
                  , "Awaken II" : [0, [0,0], "Defence", "Awakened One","Buff","Increases All DMG based on RES"]
                  , "Blaze Shield" : [0, [0,0], "Defence", "Blaze Shield","Buff","Increases Max HP"]
                  , "Pyroclastic Charge" : [0, [0,0], "Defence", "Pyroclastic Charge","Buff","Increases Fire DMG based on Max HP"]
                  , "Pyroclastic Surge" : [0, [0,0], "Defence", "Pyroclastic Surge","Buff","Increases Fire DMG based on Max HP"]
                  , "Inspire" : [0, [0,0], "Defence", "Inspired","Buff","Increases Water DMG based on RES"]
                  ,"Drain Energy" : [0, [0,0], "Offence", "Drained","Debuff","Decreases opponent's All DMG"]
                  ,"Resist" : [0, [0,0], "Defence", "Invulnerable","Buff","Increases RES"]
                  ,"Defend" : [0, [0,0], "Defence", "Defending","Buff","Increases RES"]    
                  ,"SPECIAL: Burning Bones" : [0,[0,0], "Offence", "Burning Bones","Debuff","Shreds opponent's RES"]    
                  ,"SPECIAL: Total Focus" : [0,[0,0], "Defence", "Total Focus","Buff","Guaranteed Critical Hits"]   
                  ,"SPECIAL: March Forward" : [0,[0,0], "Party", "March!","Buff","Increases STR of all allies"]
                  ,"SPECIAL: Ultimate Defence" : [0,[0,0], "Defence", "Ultimate Defence","Buff","Heavily increases RES"]
                  ,"SPECIAL: Eternal Endurance" : [0,[0,0], "Party", "Endure","Buff","Heavily increases RES of all allies"]
                  ,"SPECIAL: Rivers in the Desert" : [300,[0,0], "Party", "None","Heal",""]
                  #Items
                  ,"Bead" : [300, [0,0], "Defence", "None","Heal",""]
                  ,"Healing Orb" : [100, [0,0], "Defence", "None","Heal",""]
                  ,"Hydro Bomb" : [90, [1,0], "Offence", "None","Water",""]
                  ,"Molotov" : [90, [1,0], "Offence", "None","Fire",""]
                  ,"Flashbang" : [90, [1,0], "Offence", "None","Wind",""]
                  }
  #THIS IS THE NEW FORMAT. Properties, img, dmg, description
  #Minor, Medium, Major, Massive
  all_moves = {
      "Skip" : {"prop" : ["Defence"], "img" : "skip","cost" : 0},
      "SPECIAL: March Forward" : {"prop" : ["Party", "Buff", "SPECIAL"], "img" : "special", "inflict" : "March!","cost" : 0},
      "Taunt" : {"prop" : ["Defence", "Buff", "Skill"], "img" : "buff", "inflict" : "Taunt","cost" : 40},
      "Target" : {"prop" : ["Offence", "Debuff", "Skill"], "img" : "debuff", "inflict" : "Targeted","cost" : 40},
      "Focus" : {"prop" : ["Defence", "Buff", "Skill"], "img" : "buff", "inflict" : "Focused","cost" : 40},
      "Overhype" : {"prop" : ["Defence", "Buff", "Skill"], "img" : "buff", "inflict" : "Hyped","cost" : 40},
      "Wind Boost" : {"prop" : ["Defence", "Buff", "Skill"], "img" : "buff", "inflict" : "Wind Boost","cost" : 40},
      "Debilitate" : {"prop" : ["Offence", "Debuff", "Skill"], "img" : "debuff", "inflict" : "Vulnerable","cost" : 40},
      "SPECIAL: Ultimate Defence" : {"prop" : ["Defence", "Buff", "SPECIAL"], "img" : "special", "inflict" : "Ultimate Defence","cost" : 0},
      "SPECIAL: Total Focus" : {"prop" : ["Defence", "Buff", "SPECIAL"], "img" : "special", "inflict" : "Total Focus","cost" : 0},
      "SPECIAL: Eternal Endurance" : {"prop" : ["Party", "Buff", "SPECIAL"], "img" : "special", "inflict" : "Endure","cost" : 0},
      "SPECIAL: Life's Garden" : {"prop" : ["Party", "Heal", "SPECIAL"], "img" : "special", "heal" : 40,"cost" : 0},#Healing scales off Max HP
      "Diarama" : {"prop" : ["Defence", "Heal", "Skill"], "img" : "heal", "heal" : 35,"cost" : 40},#Healing scales off Max HP
      "Mediarama" : {"prop" : ["Party", "Heal", "Skill"], "img" : "heal", "heal" : 20,"cost" : 40},#Healing scales off Max HP
      "Dia" : {"prop" : ["Defence", "Heal", "Basic"], "img" : "heal", "heal" : 15,"cost" : 20},#Healing scales off Max HP

      "Garudyne" : {"prop" : ["Offence", "Wind", "Basic"], "img" : "wind_1s", "dmg" : 50,"cost" : 20},#Damage scales off STR
      "Cyclone": {"prop" : ["Offence", "Wind", "Skill"], "img" : "wind_mg", "dmg" : 25, "hits" : 8,"cost" : 40},
      "Wrath Tempest": {"prop" : ["Offence", "Wind", "Skill"], "img" : "wind_mg", "dmg" : 70, "hits" : 3,"cost" : 40},
      "Wind Blades": {"prop" : ["Offence", "Wind", "Basic"], "img" : "wind_mg", "dmg" : 10, "hits" : 8,"cost" : 20},
      "Garubarion": {"prop" : ["Offence", "Wind", "Skill"], "img" : "wind_mg", "dmg" : 100, "hits" : 2,"cost" : 40},
      "SPECIAL: Eye of the Storm": {"prop" : ["Offence", "Wind", "SPECIAL"], "img" : "special", "dmg" : 40, "hits" : 8,"cost" : 0},
      "Bufudyne": {"prop" : ["Offence", "Water", "Basic"], "img" : "water_1s", "dmg" : 50,"cost" : 20},
      "Striking Tide": {"prop" : ["Offence", "Water", "Skill"], "img" : "water_mg", "dmg" : 20, "hits" : 10,"cost" : 40},
      "Bufubarion": {"prop" : ["Offence", "Water", "Skill"], "img" : "water_1g", "dmg" : 200,"cost" : 40},
      "SPECIAL: Thalassic Calamity": {"prop" : ["Offence", "Water", "SPECIAL"], "img" : "special", "dmg" : 32, "hits" : 10,"cost" : 0},
      "Agidyne": {"prop" : ["Offence", "Fire", "Basic"], "img" : "fire_1s", "dmg" : 50,"cost" : 20},
      "Fire Dance": {"prop" : ["Offence", "Fire", "Skill"], "img" : "fire_mg", "dmg" : 66, "hits" : 3,"cost" : 40},
      "Agibarion": {"prop" : ["Offence", "Fire", "Skill"], "img" : "fire_1g", "dmg" : 200,"cost" : 40},
      "SPECIAL: Burning Hell": {"prop" : ["Offence", "Fire", "SPECIAL"], "img" : "special", "dmg" : 320,"cost" : 0}
  }
  all_moves_desc = { #s = Small desc. b = Big desc0
      "Skip" : {"s" : "End this turn", "b" : "End this turn"},
      "Taunt" : {"s" : "Draws opponent's attention", "b" : "Draws enemy attention by increasing AGG"},
      "Target" : {"s" : "Increases opponent's AGG", "b" : "Enemy is targeting this person"},
      "Focus" : {"s" : "Increases CRIT", "b" : "Increases CRIT Rate"},
      "SPECIAL: Ultimate Defence" : {"s" : "Heavily increases RES", "b" : "Heavily increases RES of self"},
      "SPECIAL: Eternal Endurance" : {"s" : "Increases RES of party", "b" : "Increases all allies' RES"},
      "SPECIAL: Total Focus" : {"s" : "Guaranteed critical hits", "b" : "Increases CRIT Rate by 100%"},
      "Overhype" : {"s" : "Increases CRIT DMG", "b" : "Increases CRIT DMG"},
      "Wind Boost" : {"s" : "Increases Wind DMG", "b" : "Increases Wind DMG"},
      "SPECIAL: March Forward" : {"s" : "All out attack", "b" : "Increases all party members' STR"},
      "Debilitate" : {"s" : "Reduce opponent's RES", "b" : "Make the opponent take more DMG by reducing their RES"},
      "SPECIAL: Life's Garden" : {"s" : "Suffer no more", "b" : "Heals " + str(move_stats(all_moves["SPECIAL: Life's Garden"]["heal"],lvl)) + "% of one's Max HP to all allies"},
      "Diarama" : {"s" : "Heals medium HP", "b" : "Heals " + str(move_stats(all_moves["Diarama"]["heal"],lvl)) + "% of one's Max HP to target ally"},
      "Mediarama" : {"s" : "Heals medium HP to party", "b" : "Heals " + str(move_stats(all_moves["Mediarama"]["heal"],lvl)) + "% of one's Max HP to all allies"},
      "Dia" : {"s" : "Heals some HP", "b" : "Heals " + str(move_stats(all_moves["Dia"]["heal"],lvl)) + "% of one's Max HP to target ally"},

      "Garudyne" : {"s":"Deals medium Wind DMG", "b" : "Deals " + str(move_stats(all_moves["Garudyne"]["dmg"],lvl)) + "% Wind DMG to a single target enemy"},
      "Cyclone" : {"s":"Deals minor Wind DMG x8", "b" : "Deals " + str(move_stats(all_moves["Cyclone"]["dmg"],lvl)) + "% Wind DMG to a single target enemy 8 times"},
      "Wrath Tempest" : {"s":"Deals medium Wind DMG x3", "b" : "Deals " + str(move_stats(all_moves["Wrath Tempest"]["dmg"],lvl)) + "% Wind DMG to a single target enemy 3 times"},
      "Wind Blades" : {"s":"Deals minor Wind DMG x10", "b" : "Deals " + str(move_stats(all_moves["Wind Blades"]["dmg"],lvl)) + "% Wind DMG to a single target enemy 10 times"},
      "Garubarion" : {"s":"Deals medium Wind DMG x2", "b" : "Deals " + str(move_stats(all_moves["Garubarion"]["dmg"],lvl)) + "% Wind DMG to a single target enemy 2 times"},
      "SPECIAL: Eye of the Storm" : {"s":"'I venture forth to hunt'", "b" : "Deals " + str(move_stats(all_moves["SPECIAL: Eye of the Storm"]["dmg"],lvl)) + "% Wind DMG to a single target enemy 8 times"},

      "Bufudyne" : {"s":"Deals medium Water DMG", "b" : "Deals " + str(move_stats(all_moves["Bufudyne"]["dmg"],lvl)) + "% Water DMG to a single target enemy"},
      "Striking Tide" : {"s":"Deals minor Water DMG x10", "b" : "Deals " + str(move_stats(all_moves["Striking Tide"]["dmg"],lvl)) + "% Water DMG to a single target enemy across multiple hits"},
      "Bufubarion" : {"s":"Deals major Water DMG", "b" : "Deals " + str(move_stats(all_moves["Bufubarion"]["dmg"],lvl)) + "% Water DMG to a single target enemy"},
      "SPECIAL: Thalassic Calamity" : {"s":"The seas are ablaze", "b" : "Deals " + str(move_stats(all_moves["SPECIAL: Thalassic Calamity"]["dmg"],lvl)) + "% Water DMG to a single target enemy across multiple hits"},

      "Agidyne" : {"s":"Deals medium Fire DMG", "b" : "Deals " + str(move_stats(all_moves["Agidyne"]["dmg"],lvl)) + "% Fire DMG to a single target enemy"},
      "Fire Dance" : {"s":"Deals medium Fire DMG x3", "b" : "Deals " + str(move_stats(all_moves["Fire Dance"]["dmg"],lvl)) + "% Fire DMG to a single target enemy across multiple hits"},
      "Agibarion" : {"s":"Deals major Fire DMG", "b" : "Deals " + str(move_stats(all_moves["Agibarion"]["dmg"],lvl)) + "% Fire DMG to a single target enemy"},
      "SPECIAL: Burning Hell" : {"s":"Until everything burns to ashes!", "b" : "Deals " + str(move_stats(all_moves["SPECIAL: Burning Hell"]["dmg"],lvl)) + "% Fire DMG to a single target enemy"},
  }

  #Finds move and adds the desc to output
  output = {}
  if move in all_moves:
      output = all_moves[move]
      output["desc"] = all_moves_desc[move]
      return output
  elif move == "all":
      return all_moves
  else:
      #Either move not found OR switching to another character
    return {"prop" : [],"img":"","desc":{"s" : "Switch character","b":"Switch character"},"dmg" : 0,"cost" : 0}

def battle_applybuffs(buff, buffamount, bufftype, x,y,target):
    global battle_characters
    global player
    
    #Do not need to return anything because Object content is changed
    #If buff already in list, add onto it. Otherwise create and add onto it.
    if buff in target[bufftype.lower()]:
        target[bufftype.lower()][buff] += buffamount
        battle_damagetext(x,y,str(buff) + " +"+str(buffamount)+"!", colour[bufftype],"small")
    else:
        target[bufftype.lower()][buff] = buffamount
        if target["name"] == player.stats["name"]:  direction = -0.5
        elif target["name"] in battle_characters: direction = -0.9
        else:   direction = 0.5
        myMixer("hit_" + str(bufftype.lower()) + ".wav",direction)
        battle_damagetext(x,y,str(buff) + " +"+str(buffamount)+"!", colour[bufftype],"dmgsmall")

    return target



def battle_changehp(target, amount, sound):
    global player_party
    #Do not need to return anything because Object content is changed

    #Play sound effect
    if target["name"] in player_party:
        direction = -0.5
    else:
        direction = 0.5
    myMixer(sound,direction)

    
    target["HP"] += amount
    if target["HP"] >= target["MHP"]:
        target["HP"] = target["MHP"]
    elif target["HP"] < 0:
        target["HP"] = 0

    return target



def battle_removebuffs(buffs):
  remove = []
  for i in buffs:
    buffs[i] -= 1
    if buffs[i] <= 0:
      remove.append(str(i))
      
  for i in remove:
    buffs.pop(str(i))

  return buffs

def battle_movecd(moves):
  for i in moves:
    if i != "":
        moves[i] = True

  return moves

def battle_bonuscheck(actor,target,data,bonus_values):
    global party
    global player_charms

    #Create bonuses dict if they dont have one
    if "bonuses" not in actor:  actor["bonuses"] = bonus_values
    if "bonuses" not in target: target["bonuses"] = bonus_values

    #Assign coords of actor and target
    if actor["name"] == player.stats["name"]:
        actor_x,actor_y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)
        target_x,target_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        bonus_values["ER"] = 0
    elif actor["name"] in player_party:
        actor_x,actor_y = 450, party[actor["name"]]["button"].rect.y+50
        target_x,target_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        bonus_values["ER"] = 0
    else:
        actor_x,actor_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        target_x,target_y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)


    #Add bonuses from charms
    if actor["name"] in battle_characters:
        for charm in player_characters[actor["name"]]["charms"]:
            charm_stats = player_charms[charm]
            if charm_stats["stat"] in bonus_values:
                bonus_values[str(charm_stats["stat"])] += charm_stats["amount"]

    #Fusion. 0=Name,1=Desc,2=Conditions and Bonuses
    fusion = get_fusion(actor["fusion"])
    for cond in fusion[2]:
        grant_bonus = False
        
        if cond == "Critical condition" and int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100) <= 30:  grant_bonus = True
        elif cond == "Not critical condition" and int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100) > 30:  grant_bonus = True
        elif cond == "Actor HP higher" and int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100) > int((target["HP"]/(target["MHP"]+target["bonuses"]["MHP"]))*100):  grant_bonus = True
        elif cond == "Target HP higher" and int((target["HP"]/(target["MHP"]+target["bonuses"]["MHP"]))*100) > int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100):  grant_bonus = True
        elif cond == "HP 60% higher" and int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100) > 60:  grant_bonus = True
        elif cond == "HP 60% lower" and int((actor["HP"]/(actor["MHP"]+actor["bonuses"]["MHP"]))*100) < 60:  grant_bonus = True
        elif cond == "Crit" and data["critamount"] > 0 and data["turn"] == actor["name"]:  grant_bonus = True
        elif cond == "Take crit" and data["critamount"] > 0 and data["turn"] == target["name"]:  grant_bonus = True
        elif cond == "Hit" and data["hit"]>0 and data["turn"] == actor["name"]:  grant_bonus = True
        elif cond == "Take hit" and data["hit"]>0 and data["turn"] == target["name"]:  grant_bonus = True
        elif cond == "":    grant_bonus = True

        if grant_bonus:
            for bonus in fusion[2][cond]:
                if bonus != "Buff" and bonus != "Debuff":
                    bonus_values[bonus] += fusion[2][cond][bonus]
                elif bonus == "Buff" and fusion[2][cond][bonus][0] not in actor["buff"]:
                    battle_applybuffs(fusion[2][cond][bonus][0], 3, "Buff", actor_x,actor_y,actor)
                elif bonus == "Debuff" and fusion[2][cond][bonus][0] not in target["debuff"]:
                    battle_applybuffs(fusion[2][cond][bonus][0], 3, "Debuff", target_x,target_y,target)


    #Updates stats that act as percentage increase rather than flat increase
    bonus_values["MHP"] = actor["MHP"] * (bonus_values["MHP"]/100)
    bonus_values["STR"] += actor["STR"] * (bonus_values["STR"]/100)

    actor["bonuses"] = bonus_values


    #Buffs and Debuffs
    for buff in actor["buff"]:
        info = get_buff(actor,target,buff)
        if info[1] != None:
            bonus_values[info[1]["Stat"]] += info[1]["Value"]
    for buff in actor["debuff"]:
        info = get_buff(actor,target,buff)
        if info[1] != None:
            bonus_values[info[1]["Stat"]] += info[1]["Value"]



    #Converting all to int
    for stat in bonus_values:
        bonus_values[stat] = int(bonus_values[stat])

    return bonus_values
        
def get_buff(actor, target, buff):
    #Name,data,description
    output = [buff, {},"desc"]
    #buff is the Buff to search for and return the corrosponding value of in output variable
    buffs = {
        "Debilitate" : {"Type":"Offence", "Buff" : "Vulnerable", "Stat" : "RES", "Value" : -20},
        "Target" : {"Type":"Offence", "Buff" : "Targeted", "Stat" : "AGG", "Value" : 100},
        "Taunt" : {"Type":"Defence", "Buff" : "Taunt", "Stat" : "AGG", "Value" : 20},
        "Concentrate" : {"Type":"Defence", "Buff" : "Concentrated", "Stat" : "All DMG", "Value": 20},
        "SPECIAL: March Forward" : {"Type":"Defence", "Buff" : "March!", "Stat" : "STR", "Value": 50},
        "Wind Boost" : {"Type":"Defence", "Buff" : "Wind Boost", "Stat" : "Wind DMG", "Value": 40},
        "Fire Boost" : {"Type":"Defence", "Buff" : "Fire Boost", "Stat" : "Fire DMG", "Value": 40},
        "Water Boost" : {"Type":"Defence", "Buff" : "Water Boost", "Stat" : "Water DMG", "Value": 40},
        "Drain Energy" : {"Type":"Offence", "Buff" : "Drained", "Stat" : "All DMG", "Value": -20},
        "Resist" : {"Type":"Defence", "Buff" : "Invulnerable", "Stat" : "RES", "Value":  20},
        "Defend" : {"Type":"Defence", "Buff" : "Defending", "Stat" : "RES", "Value":  10},
        "SPECIAL: Burning Bones" : {"Type":"Offence", "Buff" : "Burning Bones", "Stat" : "RES", "Value":  -50},
        "SPECIAL: Total Focus" : {"Type":"Defence", "Buff" : "Total Focus", "Stat" : "CRIT", "Value":  100},
        "SPECIAL: Ultimate Defence" : {"Type":"Defence", "Buff" : "Ultimate Defence", "Stat" : "RES", "Value":  50},
        "SPECIAL: Eternal Endurance" : {"Type":"Defence", "Buff" : "Endure", "Stat" : "RES", "Value":  25},
        "Focus" : {"Type":"Defence", "Buff" : "Focused", "Stat" : "CRIT", "Value" : 20},
        "Overhype" : {"Type":"Defence", "Buff" : "Hyped", "Stat" : "CRIT DMG", "Value" : 40},
        "Overgrow" : {"Type":"Defence", "Buff" : "Overgrown", "Stat" : "MHP", "Value" :  int((actor["MHP"]) * 0.2)},
        "Awaken" : {"Type":"Defence", "Buff" : "Awakened", "Stat" : "Water DMG", "Value" : int((actor["RES"]+actor["bonuses"]["RES"]) * 2)},
        "Awaken II" : {"Type":"Defence", "Buff" : "Awakened One", "Stat" : "Water DMG", "Value" : int((actor["RES"]+actor["bonuses"]["RES"]) * 3)},
        "Blaze Shield" : {"Type":"Defence", "Buff" : "Blaze Shield", "Stat" : "MHP", "Value" : int((actor["MHP"]) * 0.6)},
        "Pyroclastic Charge" : {"Type":"Defence", "Buff" : "Pyroclastic Charge", "Stat" : "Fire DMG", "Value" : int((actor["MHP"]+actor["bonuses"]["MHP"]) * 0.03)},
        "Pyroclastic Surge" : {"Type":"Defence", "Buff" : "Pyroclastic Surge", "Stat" : "Fire DMG", "Value" : int((actor["MHP"]+actor["bonuses"]["MHP"]) * 0.06)},
        "Inspire" : {"Type":"Defence", "Buff" : "Inspired", "Stat" : "Water DMG", "Value" : int((actor["RES"]+actor["bonuses"]["RES"]) * 2)},
        "Half Moon" : {"Type":"Defence", "Buff" : "Half Moon", "Stat" : "All DMG", "Value" : int((actor["STR"]+actor["bonuses"]["STR"]) * 0.3)},
        "Full Moon" : {"Type":"Defence", "Buff" : "Full Moon", "Stat" : "All DMG", "Value" : int((actor["STR"]+actor["bonuses"]["STR"]) * 0.6)}
        }

    for i in buffs:
        if i == buff or buff in buffs[i]["Buff"]:
            output[1] = buffs[i]
            #Make description
            output[2] = ""
            if buffs[i]["Value"] > 0:   output[2] += "Increases"
            else:   output[2] += "Decreases"
            output[2] += " " + str(buffs[i]["Stat"]) + " by " + str(buffs[i]["Value"])
            if buffs[i]["Stat"] == "CRIT DMG" or buffs[i]["Stat"] == "Fire DMG" or buffs[i]["Stat"] == "Water DMG" or buffs[i]["Stat"] == "Wind DMG" or buffs[i]["Stat"] == "All DMG":
                output[2] += "%."
            else:
                output[2] += "."
            break

    return output

def battle_energy(amount,er,eg,meg):
    #Base amount, multiplied by Energy recharge
    amount = int(amount*(er/100))

    #Cannot exceed max limit
    if amount + eg >= meg:
        eg = meg
    else:
        eg += amount

    #Return new energy
    return eg

def battle_createability(moves):
    #Creating buttons. Screen, width, height, image, size x, size y
    abilities = {}
    x_value = 0
    size = 90
    keys = {"1" : pygame.K_q,"2" : pygame.K_w,"3" : pygame.K_e,"4" : pygame.K_r}
    count = 1
    for ability in moves:
        #Add the Button attribute to ability
        abilities[ability] = {
            "button" : button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), pygame.image.load("img/Other/"+ str(battle_moveslookup(ability)["img"]) + ".png").convert_alpha(), screen_mult(screen_width,size),screen_mult(screen_height,size),keys[str(count)])}
        #Used for spacing out abilities on screen
        x_value += screen_mult(screen_width,size+10)
        count+=1
    #abilities["Skip"] = {"button" :button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), img_skip, screen_mult(screen_width,size),screen_mult(screen_height,size))}
    

    return abilities

def battle_createparty(members):
    global img_party
    party_images(members)
    #Creating buttons. Screen, width, height, image, size x, size y
    party = {}
    y_value = screen_height/(len(members)+1)
    size = screen_mult(screen_diag,100)
    keys = {"1" : pygame.K_1,"2" : pygame.K_2,"3" : pygame.K_3}
    count = 1
    for member in members:
        #Add the Button attribute to ability
        party[member] = {
            "button" : button.Button(display, screen_mult(screen_width,50), y_value, img_party[member]["icon"], size,size,keys[str(count)])}
        party[member]["hp"] = ProgressBar(party[member]["button"].rect.width,screen_mult(screen_height,5))
        party[member]["eg"] = ProgressBar(party[member]["button"].rect.width,screen_mult(screen_height,5))
        #Used for spacing out abilities on screen
        y_value += (screen_height/(len(members)+1))-(party[member]["button"].rect.height/2)
        count += 1

    return party

def party_images(party):
    global img_party
    img_party = {}
    for member in party:
        img_party[member] = {
        "icon" : pygame.image.load("img/Char/" + str(member) + "/icon.png").convert_alpha(),
        "turn" : pygame.image.load("img/Char/" + str(member) + "/icon_turn.png").convert_alpha(),
        "spec" : pygame.image.load("img/Char/" + str(member) + "/icon_spec.png").convert_alpha(),
        "hurt" : pygame.image.load("img/Char/" + str(member) + "/icon_hurt.png").convert_alpha()
            }

def battle_viewmember(member,background): # Not in use
    global player
    global battle_characters
    global inviscircle

    running = True

    #Decrease music volume
    pygame.mixer.music.set_volume(0.1)

    bg = pygame.transform.gaussian_blur(background,20)
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    scale = 0.5
    img = pygame.image.load("img/Char/" + str(member["name"]) + "/portrait.png")
    img_rect = img.get_rect()
    member_portrait = pygame.transform.scale(img,(screen_mult(screen_width,int(img_rect.width*scale)),screen_mult(screen_height,int(img_rect.height*scale))))
    
    while running:
        #clock tick
        clock.tick(framesrate)
        
        display.blit(bg,(0,0))

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        display.blit(member_portrait,(screen_mult(screen_width,100),screen_mult(screen_height,200)))

        #For events happening in the pygame
        for event in pygame.event.get():
            #If window X clicked
            if event.type == pygame.QUIT:
                terminate()

            #If left mouse button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("left click")
                #Right mouse button
                if event.button == 3:
                    print("right click")
                    running = False
                
        screen.blit(display,(0,0))
        pygame.display.update()
        
def char_stats(stat,lvl):#Increases by 20%
    multiplier = 0.2
    return int(stat+(((stat*multiplier)*lvl)-stat*multiplier))

def battle_system(player_party,enemy_stats,bg,bgm):
    global player
    global enemy
    global player_characters
    global inviscircle
    global player_hp
    global player_eg
    global enemy_hp
    global damage_text_group
    global projectile_group
    global abilities
    global party
    global img_buffs
    global img_bonus
    global battle_characters
    #Classes must be declared outside of main function

    #Keyboard input
    keys = {
        "1" : pygame.K_1,
        "2" : pygame.K_2,
        "3" : pygame.K_3,
        "q" : pygame.K_q,
        "w" : pygame.K_w,
        "e" : pygame.K_e,
        "r" : pygame.K_r,
        "escape" : pygame.K_ESCAPE,
        "space" : pygame.K_SPACE
    }

    #AGG target
    icon_target = pygame.transform.scale(pygame.image.load("img/Other/target.png"),(screen_mult(screen_width,30),screen_mult(screen_height,30))).convert_alpha()
    img_buffs = {
        "Vulnerable" : pygame.image.load("img/Other/buff_vulnerable.png").convert_alpha(),
        "Taunt" : pygame.image.load("img/Other/buff_taunt.png").convert_alpha(),
        "Targeted" : pygame.image.load("img/Other/buff_taunt.png").convert_alpha(),
        "Concentrated" : pygame.image.load("img/Other/buff_concentrated.png").convert_alpha(),
        "Charged" : pygame.image.load("img/Other/buff_charged.png").convert_alpha(),
        "Wind Boost" : pygame.image.load("img/Other/icon_bonus_wind.png").convert_alpha(),
        "Fire Boost" : pygame.image.load("img/Other/icon_bonus_fire.png").convert_alpha(),
        "Water Boost" : pygame.image.load("img/Other/icon_bonus_water.png").convert_alpha(),
        "Drained" : pygame.image.load("img/Other/buff_drained.png").convert_alpha(),
        "Invulnerable" : pygame.image.load("img/Other/buff_invulnerable.png").convert_alpha(),
        "Defending" : pygame.image.load("img/Other/buff_invulnerable.png").convert_alpha(),
        "Burning Bones" : pygame.image.load("img/Other/buff_burnbones.png").convert_alpha(),
        "Total Focus" : pygame.image.load("img/Other/buff_totalfocus.png").convert_alpha(),
        "Ultimate Defence" : pygame.image.load("img/Other/buff_ultdefence.png").convert_alpha(),
        "Focused" : pygame.image.load("img/Other/buff_focused.png").convert_alpha(),
        "Hyped" : pygame.image.load("img/Other/buff_hyped.png").convert_alpha(),
        "Overgrown" : pygame.image.load("img/Other/buff_overgrown.png").convert_alpha(),
        "Awakened" : pygame.image.load("img/Other/buff_awakened.png").convert_alpha(),
        "Awakened One" : pygame.image.load("img/Other/buff_awakenedone.png").convert_alpha(),
        "Blaze Shield" : pygame.image.load("img/Other/buff_blazeshield.png").convert_alpha(),
        "March!" : pygame.image.load("img/Other/buff_march.png").convert_alpha(),
        "Endure" : pygame.image.load("img/Other/buff_endure.png").convert_alpha(),
        "Blaze Shield" : pygame.image.load("img/Other/buff_blazeshield.png").convert_alpha(),
        "Pyroclastic Charge" : pygame.image.load("img/Other/buff_pyrocharge.png").convert_alpha(),
        "Pyroclastic Surge" : pygame.image.load("img/Other/buff_pyrosurge.png").convert_alpha(),
        "Inspired" : pygame.image.load("img/Other/buff_inspired.png").convert_alpha(),
        "Half Moon" : pygame.image.load("img/Other/buff_halfmoon.png").convert_alpha(),
        "Full Moon" : pygame.image.load("img/Other/buff_fullmoon.png").convert_alpha()
        }
    img_bonus = {
        "CRIT" : pygame.image.load("img/Other/icon_bonus_crit.png").convert_alpha(),
        "CRIT DMG" : pygame.image.load("img/Other/icon_bonus_critdmg.png").convert_alpha(),
        "Fire DMG" : pygame.image.load("img/Other/icon_bonus_fire.png").convert_alpha(),
        "Water DMG" : pygame.image.load("img/Other/icon_bonus_water.png").convert_alpha(),
        "Wind DMG" : pygame.image.load("img/Other/icon_bonus_wind.png").convert_alpha(),
        "MHP" : pygame.image.load("img/Other/icon_bonus_hp.png").convert_alpha(),
        "All DMG" : pygame.image.load("img/Other/icon_bonus_dmg.png").convert_alpha(),
        "STR" : pygame.image.load("img/Other/icon_bonus_str.png").convert_alpha(),
        "RES" : pygame.image.load("img/Other/icon_bonus_res.png").convert_alpha(),
        "ER" : pygame.image.load("img/Other/icon_bonus_er.png").convert_alpha(),
        "AGG" : pygame.image.load("img/Other/icon_bonus_agg.png").convert_alpha()}
    
    #Add cooldowns on moves
    for member in player_party:
        #Temporary stats for this battle
        battle_characters[member] = {
            "name" : str(member),
            "element" : characters[member]["element"],
            "weakness" : characters[member]["weakness"],
            "fusion" : characters[member]["fusion"],
            "MHP" : char_stats(characters[member]["MHP"],player_characters[member]["LVL"]),
            "HP" : player_characters[member]["HP"],
            "STR" : char_stats(characters[member]["STR"],player_characters[member]["LVL"]),
            "RES" : char_stats(characters[member]["RES"],player_characters[member]["LVL"]),
            "CRIT" : char_stats(characters[member]["CRIT"],player_characters[member]["LVL"]),
            "CRIT DMG" : char_stats(characters[member]["CRIT DMG"],player_characters[member]["LVL"]),
            "ER" : 100,
            "EG" : player_characters[member]["EG"],
            "MEG" : 100,
            "AGG" : characters[member]["AGG"],
            "buff" : {},
            "debuff" : {},
        }
        newdict = {}
        for move in characters[member]["moves"]:
            newdict[move] = True
        battle_characters[member]["moves"] = newdict

    enemy_stats = {
            "name" : enemy_stats["name"],
            "LVL" : enemy_stats["LVL"],
            "id" : enemy_stats["id"],
            "turns" : enemy_stats["turns"],
            "weakness" : enemy_stats["weakness"],
            "fusion" : enemy_stats["fusion"],
            "MHP" : char_stats(enemy_stats["MHP"],enemy_stats["LVL"]),
            "HP" : 0,
            "STR" : char_stats(enemy_stats["STR"],enemy_stats["LVL"]),
            "RES" : char_stats(enemy_stats["RES"],enemy_stats["LVL"]),
            "CRIT" : char_stats(enemy_stats["CRIT"],enemy_stats["LVL"]),
            "CRIT DMG" : char_stats(enemy_stats["CRIT DMG"],enemy_stats["LVL"]),
            "moves" : enemy_stats["moves"],
            "buff" : {},
            "debuff" : {},
        }
    #Adjust to difficulty
    modes = {"Normal" : 1, "Hard" : 1.5,"Maddening" : 2}
    enemy_stats["turns"] = int(enemy_stats["turns"]*modes[difficulty])
    enemy_stats["MHP"] = int(enemy_stats["MHP"]*modes[difficulty])
    enemy_stats["HP"] = enemy_stats["MHP"]
    enemy_stats["STR"] = int(enemy_stats["STR"]*modes[difficulty])
    enemy_stats["RES"] = int(enemy_stats["RES"]*modes[difficulty])
    enemy_stats["CRIT"] = int(enemy_stats["CRIT"]*modes[difficulty])
    enemy_stats["HP"] = enemy_stats["MHP"]
    
    #Damage text
    damage_text_group = pygame.sprite.Group()
    #Projectiles
    projectile_group = pygame.sprite.Group()

    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    #Create fighter classes
    player = Fighter(screen_width/4, int(screen_height/2),battle_characters[player_party[0]])
    enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)
    enemy_turns = 0
    

    #Create progressbars. Arguements are width and height
    size_x, size_y = screen_mult(screen_width,100),screen_mult(screen_height,10)
    player_hp = ProgressBar(size_x,size_y)
    player_eg = ProgressBar(size_x,size_y)
    enemy_hp = ProgressBar(screen_width/4,screen_mult(screen_height,20))
    vigour_bar = ProgressBar(screen_mult(screen_width,50),screen_height-screen_mult(screen_height,360),"vigour")

    #Vigour values
    vigour = {"current" : 100, "max" : 100, "red" : 0,"transition" : 0}

    #Ability and Party buttons
    abilities = battle_createability(player.stats["moves"])
    party = battle_createparty(player_party)

    #Add "bonuses" element to combatents stats temporarily for this battle
    battle_turndata = {
                         "action" : "",
                         "actionelement" : "",
                         "actiontype" : "",
                         "actioninflict" : "",
                         "actor" : player,
                         "target" : enemy,
                         "turn" : player.stats["name"],
                         "totaldmg" : 0,
                         "crit" : False,
                         "critamount" : 0,
                         "hit" : 0,
                         "heal" : 0,
                         "actorcondition" : "",
                         "targetcondition" : ""}

    for member in player_party:
        #Trigger is when character HP is full. If character has a MHP bonus, maintain full health accordingly
        trigger = False
        if battle_characters[member]["HP"] == battle_characters[member]["MHP"]: trigger = True

        battle_characters[member]["bonuses"] = battle_updatestats(battle_characters[member],enemy_stats,battle_turndata)
        if trigger == True:  battle_characters[member]["HP"] = int(battle_characters[member]["MHP"] + battle_characters[member]["bonuses"]["MHP"])

    enemy_stats["bonuses"] = battle_updatestats(enemy_stats,battle_characters[player_party[0]],battle_turndata)
    enemy_stats["HP"] = int(enemy_stats["MHP"] + enemy_stats["bonuses"]["MHP"])

    player.stats = battle_characters[player_party[0]]
    enemy.stats = enemy_stats

    player.status = "turn"
    cooldown = framesrate
    battle_action = "player"
    selected = ""
    screen_shake = 0
    enemy_shake = 0
    combo_shake = 0
    combo = {"hits" : 0, "dmg" : 0}
    hits = 0
    maxhits = 0

    #player button transition
    #point = current offset pixels, max = offset starting point pixels, spd = pixel offset reduction per frame
    buttonshift_speed = int(framesrate*0.1)#0.1s
    buttonshift_party = {"max" : screen_mult(screen_width,500)}
    buttonshift_party["point"] = buttonshift_party["max"]
    buttonshift_party["spd"] = int(buttonshift_party["max"]/buttonshift_speed)
    buttonshift_moves = {"max" : screen_mult(screen_width,300)}
    buttonshift_moves["point"] = buttonshift_moves["max"]
    buttonshift_moves["spd"] = int(buttonshift_moves["max"]/buttonshift_speed)

    #actions. [move, target]
    action = ["",""]

    #Determines rating for after battle
    battle_data = {
        "dmg_done" : 0,
        "dmg_moves" : 0,
        "highestcombo" : combo,
        "dmg_take" : 0,
        "dmg_overkill" : 0,
        "dmg_weak" : 0,
        #Dmg amplified
        "dmg_effe" : 0,
        #Dmg efficiency. Uses dmg_moves and dmg_done in calc
        "dmg_effi" : 0,
        "turn_count" : 0,
        "result" : "",
        "energy" : {},#energy generated by who
        "vigour" : {}#vigour used by who
        }

    for member in player_party:#add members to relevant data
        battle_data["energy"][member] = 0
        battle_data["vigour"][member] = 0

    #Calculating total party MHP to determine music to play
    battle_music(bgm)
    
    #Running loop. 1 Loop = 1 Frame
    running = ""
    while running == "":
        #clock tick
        clock.tick(framesrate)

        #Change rainbow colour
        colour_rainbowcycle()

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Record keys pressed this frame
        keys_pressed=[]
        keyboard = pygame.key.get_pressed()
        for k in keys:
            if keyboard[keys[k]]:
                keys_pressed.append(keys[k])

        #Update invis circle effect
        if (player.stats["HP"]/player.stats["MHP"])*100 <= 30:
            inviscircle.update(3)
            if random.randint(1,200) == 1:  screen_shake = framesrate/10
        elif battle_action == "Victory!" or battle_action == "Defeat!":
            inviscircle.update(0)
        else:
            inviscircle.update(2)

        #Display images
        draw_background(bg,"circle")


        #Display players
        if battle_action == "player" and selected == "":
            player.status = "idle"
        elif battle_action == "player" and selected != "" and action[0] == "":
            player.status = "ready"
        player.update()
        x,y = mouse_hovereffect(screen_width/3, int(screen_height/2)-int(player.rect.height/5),"circle")
        player.draw(x,y)

        #Add enemy shake
        if enemy_shake > 0:
            enemy_shake -= 1
            shake_x, shake_y = image_shake(15)
        else:   shake_x, shake_y = 0,0
        if enemy.stats["HP"] > 0:
            enemy.update()
            x,y = mouse_hovereffect(screen_width-(screen_width/4),int(screen_height/2)-int(enemy.rect.height/5),"circle")
            enemy.draw(x+shake_x,y+shake_y)


        #Buttons transitions
        if battle_action == "player":
            if buttonshift_party["point"] >= 0 and buttonshift_party["point"] > buttonshift_party["spd"]:
                buttonshift_party["point"] -= buttonshift_party["spd"]
            else:   buttonshift_party["point"] = 0
            if buttonshift_moves["point"] >= 0 and buttonshift_moves["point"] > buttonshift_moves["spd"]:
                buttonshift_moves["point"] -= buttonshift_moves["spd"]
            else:   buttonshift_moves["point"] = 0

        #Top and bottom borders for effect
            #Black
        size = screen_mult(screen_height,180)
        box3 = pygame.Rect(0, 0, screen_width, size)
        pygame.draw.rect(display, colour["black"], box3)
        box4 = pygame.Rect(0, screen_height-size, screen_width, size)
        pygame.draw.rect(display, colour["black"], box4)
        
        #Update coords for battle status display and main colours
        if (battle_action == "player" and action[0] == "") or battle_action == "Victory!":
            x = player.rect.x
            y = player.rect.y
            if "SPECIAL" in selected:   myColour = colour["rainbowcycle"]
            else:   myColour = colour[player.stats["element"]]
        elif battle_action == "enemy" or battle_action == "Defeat!":
            x = enemy.rect.x
            y = enemy.rect.y
            myColour = colour["red"]
        elif action[0] != "":#Action being done
            x = (screen_width/2.5)
            y = screen_height/4
            if "SPECIAL" in battle_turndata["action"]:   myColour = colour["rainbowcycle"]
            else:   myColour = colour["white"]
        else:
            x = (screen_width/2.5)
            y = screen_height/4
            myColour = colour["white"]
            
        #Coloured borders
        size = screen_mult(screen_height,20)
        box = pygame.Rect(0, 0, screen_width, size)
        pygame.draw.rect(display, myColour, box)
        box2 = pygame.Rect(0, screen_height-size, screen_width, size)
        pygame.draw.rect(display, myColour, box2)

        #display battle status
        #draw_text(str(battle_action).upper(), fonts["verylarge"], myColour, x, y-100, True)
        #display selected ability
        weak = ""#Additional text at the end of message to denote weakness
        if selected != "":
            x,y = (screen_width/2)-screen_mult(screen_width,60),screen_height - (screen_height/3)
            #adjust size
            if "SPECIAL" in selected:
                text_output = selected[9:]
            else: text_output = selected
            x -= screen_mult(screen_width,52*len(text_output))

            #adjust x based on actor+text length
            #print(battle_action, action[0])
            if action[0] != "" and battle_action=="neutral" and action[0] != "Switch" and action[0] != "Skip":#action being done aka battle_neutral
                if get_element(battle_moveslookup(action[0])["prop"]) == action[1]["weakness"]:#Display WEAK if striking a weakness
                    weak = " (WEAK!)"
            elif battle_action == "player":
                #x -= screen_mult(screen_width,200)
                if get_element(battle_moveslookup(selected)["prop"]) == enemy.stats["weakness"]:
                    weak = " (WEAK!)"
            elif battle_action == "enemy":
                #x += screen_mult(screen_width,200)
                if get_element(battle_moveslookup(selected)["prop"]) == player.stats["weakness"]:
                    weak = " (WEAK!)"

            draw_text(str(text_output).upper(), fonts["battlemove"], myColour, x, y + screen_mult(screen_height,142), False,100)#Transparent
            draw_text(str(battle_moveslookup(selected)["desc"]["s"]).upper() + str(weak), fonts["dmgmed"], myColour, x+screen_mult(screen_width,52*len(selected)), y + screen_mult(screen_height,300), False)
        
            
        #Combo metre. Also shakes
        if (combo["hits"] > 0 and player.status != "idle" and player.status != "hurt" and player.status != "dead") or (combo["hits"] > 0 and player.status == "idle" and battle_action == "player"):
            if combo_shake > 0:
                myColour = colour["red"]
                combo_shake -= 1
                shake_x, shake_y = image_shake(10)
            elif combo["hits"] > 20:
                myColour = colour["rainbowcycle"]
                shake_x, shake_y = image_shake(2)
            else:
                myColour = colour["white"]
                shake_x, shake_y = 0,0
            x, y = mouse_hovereffect(screen_mult(screen_width,200)+(screen_width/2),screen_height/4,"circle")
            draw_text(str(combo["hits"]) + " HITS!", fonts["large"], colour["grey"], x-shake_x+2, y-shake_y+2, False)#Grey outline text
            draw_text(str(combo["dmg"]) + " TOTAL DMG", fonts["dmgsmall"], colour["grey"], x+shake_x+2, y +shake_y+2+screen_mult(screen_height,80), False)#Grey outline text
            draw_text(str(combo["hits"]) + " HITS!", fonts["large"], myColour, x+shake_x, y+shake_y, False)
            draw_text(str(combo["dmg"]) + " TOTAL DMG", fonts["dmgsmall"], myColour, x-shake_x, y -shake_y+screen_mult(screen_height,80), False)
        

        #Player and enemy health bars
        battle_draw_health(player,player_hp, mouse_pos)
        battle_draw_enemyhealth(enemy,enemy_hp, mouse_pos)

        #projectiles
        projectile_group.update()
        projectile_group.draw(display)

        #Finding member with highest aggro
        highest_agg = player_party[0]#this variable is member name
        for member in player_party:
            if battle_characters[member]["AGG"]+battle_characters[member]["bonuses"]["AGG"] > battle_characters[highest_agg]["AGG"]+battle_characters[highest_agg]["bonuses"]["AGG"]:
                highest_agg = member
        

        if battle_action == "player" and action[0] == "":
            #ABILITY BUTTONS
            #For spacing between buttons
            x_value = screen_mult(screen_width,50)
            for move in player.stats["moves"]:
                if "SPECIAL" in battle_moveslookup(move)["prop"]:
                    special = True
                else:
                    special = False
                if special and player.stats["EG"] != player.stats["MEG"]:
                    continue
                elif special and player.stats["EG"] == player.stats["MEG"]:
                    myColour = "rainbowcycle"
                else:
                    myColour = player.stats["element"]
                #Display the ability button
                x,y = mouse_hovereffect(player.x + x_value, screen_height - (screen_height/4)+buttonshift_moves["point"],"circle")
                ability_clicked = abilities[move]["button"].draw(x,y,"",keys_pressed) #(Returns True if button is pressed)
                x_value += screen_mult(screen_width,100)
                #Display cooldown TRUE, otherwise display READY
                if player.stats["moves"][move] == False:
                    pygame.draw.circle(display, colour["white"], (abilities[move]["button"].rect.center[0], abilities[move]["button"].rect.center[1]),abilities[move]["button"].rect.width/2, 5)
                    draw_text("X", fonts["dmgsmall"], colour["white"], abilities[move]["button"].rect.center[0]-screen_mult(screen_width,10), abilities[move]["button"].rect.center[1]-screen_mult(screen_height,22), False)
                elif special:
                    pygame.draw.circle(display, colour["rainbowcycle"], (abilities[move]["button"].rect.center[0], abilities[move]["button"].rect.center[1]),abilities[move]["button"].rect.width/2, 5)

                #Display ability descriptionif mouse hovering over ability button
                if abilities[move]["button"].hover() == True and selected == "" and battle_action == "player":
                    if player.stats["moves"][move] == True:
                        pygame.draw.circle(display, colour["green"], (abilities[move]["button"].rect.center[0]-1, abilities[move]["button"].rect.center[1]-1),abilities[move]["button"].rect.width/2, 5)
                        draw_text(str(move.upper())+ " # -" + str(battle_moveslookup(move)["desc"]["s"]), fonts["small"], colour["green"], abilities[move]["button"].rect.x, abilities[move]["button"].rect.y + abilities[move]["button"].rect.height + screen_mult(screen_height,5), True)
                    else:
                        draw_text(str(move.upper())+ " (Already used) # -" + str(battle_moveslookup(move)["desc"]["s"]), fonts["small"], colour["white"], abilities[move]["button"].rect.x, abilities[move]["button"].rect.y + abilities[move]["button"].rect.height + screen_mult(screen_height,5), True)

        
                #If button pressed + Player's turn = Can select ability.
                if ability_clicked and selected != move:
                    myMixer("menu_text.wav",0)
                    selected = str(move)
                    break
                #If ability already selected and they click button again and have enough vigour, perform ability on self/enemy. DOES NOT INCLUDE SWITCH or SKIP
                elif ability_clicked and selected == move:
                    if vigour["current"] >= battle_moveslookup(move)["cost"]:
                        myMixer("menu_enter.wav",0)

                        #Deciding target depending on type of action
                        actiontype = get_element(battle_moveslookup(selected)["prop"])
                        if "Fire" == actiontype or "Water" == actiontype or "Wind" == actiontype or "Singularity" == actiontype or "Debuff" == actiontype:
                            action = [selected,enemy.stats]
                        elif "Heal" == actiontype or "Buff" == actiontype:
                            action = [selected,player.stats]

                        #Check if move has multiple hits
                        hits = battle_moveslookup(action[0])
                        if "hits" in hits:
                            hits = hits["hits"]
                        else: hits = 1
                        maxhits = hits
                        cooldown = 0
                        break
                    else:
                        myMixer("menu_invalid.wav",0)
                        screen_shake = framesrate/10
                        vigour["red"] = framesrate/10

                #Draw outline over selected ability
                if move == selected and battle_action == "player":
                    if special:   myColour = colour["rainbowcycle"]
                    else:   myColour = colour[player.stats["element"]]
                    pygame.draw.circle(display, myColour, (abilities[move]["button"].rect.center[0]-1, abilities[move]["button"].rect.center[1]-1),abilities[move]["button"].rect.width/2, 5)
                    draw_text("READY", fonts["small"], colour["grey"], abilities[move]["button"].rect.topleft[0]+screen_mult(screen_width,3), abilities[move]["button"].rect.center[1]-screen_mult(screen_height,10)+2, False)
                    draw_text("READY", fonts["small"], myColour, abilities[move]["button"].rect.topleft[0]+screen_mult(screen_width,3), abilities[move]["button"].rect.center[1]-screen_mult(screen_height,10), False)


            #Display skip button at the end. NOT IN USE
            # x,y = mouse_hovereffect(player.x + x_value, screen_height - (screen_height/4)+buttonshift_moves["point"],"circle")
            # skip_clicked = abilities["Skip"]["button"].draw(x,y,"")
            # if skip_clicked:
            #     myMixer("menu_back.wav",0)
            #     selected = "Skip"
            #     action = ["Skip",player.stats]
            #Display desc if hovering over Skip button
            # if abilities["Skip"]["button"].hover() and selected == "" and battle_action == "player":
            #         draw_text("Skip turn", fonts["small"], colour["green"], abilities["Skip"]["button"].rect.x, abilities["Skip"]["button"].rect.y + abilities["Skip"]["button"].rect.width, True)

            #TURN COUNT/VIGOUR
            myColour = "menu"
            if vigour["red"] > 0:
                myColour = "red"
                vigour["red"] -= 1
            if vigour["transition"] < 100:
                myColour = "white"
                vigour["transition"] += int((5/framesrate)*100)
            if vigour["transition"] > 100:#not elif because of above statement
                vigour["transition"] = 100

            vigour_bar.draw(0,screen_mult(screen_height,180),vigour["max"],vigour["max"],[0,0],"grey",False)
            if selected == "" or "SPECIAL" in selected:
                #Vigour bar
                vigour_bar.draw(0,screen_mult(screen_height,180),int(vigour["current"]*(vigour["transition"]/100)),vigour["max"],[0,0],myColour,False)
                #Text
                text_surface = pygame.transform.rotate(fonts["large"].render("VIGOUR", True, colour[myColour]),-90)
                text_surface.set_alpha(100)
                display.blit(text_surface, (screen_mult(screen_width,30), screen_mult(screen_height,180)))
                #Value
                text_surface = pygame.transform.rotate(fonts["dmgmed"].render(str(int(vigour["current"]*(vigour["transition"]/100))), True, colour[myColour]),-90)
                display.blit(text_surface, (screen_mult(screen_width,40), screen_mult(screen_height,320)))
            elif selected != "Skip" and selected != "Switch":
                cost = battle_moveslookup(selected)["cost"]
                blink = int(mouse_hovereffect(10,10,"circle")[1])
                #if weak != "":  cost = int(cost/2)
                #Vigour bar current
                vigour_bar.draw(0,screen_mult(screen_height,180),vigour["current"]-cost+blink,vigour["max"],[0,0],myColour,False)
                #Text
                text_surface = pygame.transform.rotate(fonts["large"].render("VIGOUR" + str(weak), True, colour[myColour]),-90)
                text_surface.set_alpha(100)
                display.blit(text_surface, (screen_mult(screen_width,30), screen_mult(screen_height,180)))
                #Value
                text_surface = pygame.transform.rotate(fonts["dmgmed"].render(str(vigour["current"]) + " -> " + str(vigour["current"]-cost), True, colour[myColour]),-90)
                display.blit(text_surface, (screen_mult(screen_width,40), screen_mult(screen_height,270)))



            #PARTY MEMBER BUTTONS
            y_value = screen_height/(len(party)+1)

            for member in player_party:
                #Establish x and y
                x,y = mouse_hovereffect(screen_mult(screen_width,200)-buttonshift_party["point"], y_value,"circle")
                if member == player.stats["name"]:  x += screen_mult(screen_width,20)
                elif party[member]["button"].hover() and battle_characters[member]["HP"] > 0:   x+= screen_mult(screen_width,20)
                #Grey box background
                pygame.draw.rect(display, colour["grey"], (party[member]["button"].rect.x-1, party[member]["button"].rect.y-1, party[member]["button"].rect.width+1, party[member]["button"].rect.height+1))

                #HP and EG bars
                spacing = screen_mult(screen_height,15)
                party[member]["hp"].draw(x,y+party[member]["button"].rect.height+screen_mult(screen_height,6),battle_characters[member]["HP"],battle_characters[member]["MHP"]+battle_characters[member]["bonuses"]["MHP"],mouse_pos,"green",False)
                if battle_characters[member]["EG"] == battle_characters[member]["MEG"]:   party[member]["eg"].draw(x,y+party[member]["button"].rect.height+spacing,battle_characters[member]["EG"],battle_characters[member]["MEG"],mouse_pos,"rainbowcycle",False)
                else:   party[member]["eg"].draw(x,y+party[member]["button"].rect.height+spacing,battle_characters[member]["EG"],battle_characters[member]["MEG"],mouse_pos,battle_characters[member]["element"],False)

                battle_draw_equips(battle_characters[member],enemy.stats,x,y+party[member]["button"].rect.height+screen_mult(screen_height,25))
                
                #Change outline colour and image depending on conditions
                if battle_characters[member]["HP"] <= 0:
                    myColour = colour["red"]
                    icon = img_party[member]["hurt"].convert()
                    icon.set_alpha(128)
                elif battle_characters[member]["EG"] == battle_characters[member]["MEG"]:
                    myColour = colour["rainbowcycle"]
                    icon = img_party[member]["spec"]
                elif member == player.stats["name"]:
                    myColour = colour["white"]
                    icon = img_party[member]["turn"]
                elif party[member]["button"].hover() and int((battle_characters[member]["HP"]/battle_characters[member]["MHP"])*100) <= 30:
                    myColour = colour["green"]
                    icon = img_party[member]["hurt"]
                elif party[member]["button"].hover():
                    myColour = colour["green"]
                    icon = img_party[member]["turn"]
                elif int((battle_characters[member]["HP"]/battle_characters[member]["MHP"])*100) <= 30:
                    myColour = colour["red"]
                    icon = img_party[member]["hurt"]
                else:
                    myColour = colour[characters[member]["element"]]
                    icon = img_party[member]["icon"]

                #Main img
                member_clicked = party[member]["button"].draw(x,y,icon,keys_pressed) #(Returns True if button is pressed)
                y_value += (screen_height/(len(party)+1))-(party[member]["button"].rect.height/2)

                #Draw outline over the icon
                pygame.draw.rect(display, myColour, (party[member]["button"].rect.x-1, party[member]["button"].rect.y-1, party[member]["button"].rect.width+1, party[member]["button"].rect.height+1), 4)

                #UNUSED
                #battle_viewmember(battle_characters[player_party[0]],display)
                info = battle_moveslookup(selected)
                if member_clicked and selected == "":#Switch to character
                    if battle_characters[member]["HP"] > 0 and cooldown <= 0 and member != player.stats["name"]:
                        selected = member
                    elif cooldown <= 0:
                        myMixer("menu_invalid.wav",0)
                        screen_shake = framesrate/10
                elif member_clicked and selected != "" and info["cost"] <= vigour["current"] and battle_characters[member]["HP"] > 0 and ("Heal" in info["prop"] or "Defence" in info["prop"] or "Party" in info["prop"]):#Cast move on party member
                    action = [selected, battle_characters[member]]
                    hits=1
                    maxhits=hits
                    cooldown = 0
                elif party[member]["button"].hover():#View stats when hovering mouse over party member
                    x,y = mouse_hovereffect(party[member]["button"].rect.x+party[member]["button"].rect.width+screen_mult(screen_width,30),party[member]["button"].rect.y,"circle")
                    battle_draw_stats(battle_characters[member],x,y,myColour)
                elif member == highest_agg:#Display target icon on person with highest aggro
                    display.blit(icon_target,(party[member]["button"].rect.x+party[member]["button"].rect.width + screen_mult(screen_width,5),party[member]["button"].rect.y))

            #Display fusion and buffs/debuffs if hovering over Character
            if player.rect.collidepoint(mouse_pos) and selected == "":
                pygame.mouse.set_visible(False)
                draw_text(str(player.stats["fusion"].upper()) + " # " + get_fusion(player.stats["fusion"])[1], fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
            elif enemy.rect.collidepoint(mouse_pos) and selected == "":
                pygame.mouse.set_visible(False)
                draw_text(str(enemy.stats["fusion"].upper()) + " # " + str(get_fusion(enemy.stats["fusion"])[1]), fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
            else:
               pygame.mouse.set_visible(True)
                
            #SWITCH FUNCTION. Hits = 1 so that it performs the move
            if selected in player_party:
                action = [selected,battle_characters[selected]]
                #Transition variables
                buttonshift_party["point"] = buttonshift_party["max"]
                buttonshift_moves["point"] = buttonshift_moves["max"]
                vigour["transition"] = 0
                maxhits = 1

        elif battle_action == "enemy":
            if selected == "":
                #Enemy AI
                selected = "Skip"

                #List of all moves off cooldown
                enemy_moves = []
                for move in enemy.stats["moves"]:
                    if enemy.stats["moves"][move] == True:
                        enemy_moves.append(move)
                if len(enemy_moves) > 0:
                        selected = random.choice(enemy_moves)
                        #Target member with highest aggro.
                        if random.randint(1,100) > 50+(battle_characters[highest_agg]["AGG"]-100) and battle_characters[highest_agg]["HP"] > 0:
                            action[1] = battle_characters[highest_agg]
                        else:
                            while True:
                                chosen = random.choice(player_party)
                                action[1] = battle_characters[chosen]
                                if action[1]["HP"] > 0:
                                    break
                        #Check if move has multiple hits

                        hits = battle_moveslookup(selected)
                        if "hits" in hits:
                            hits = hits["hits"]
                        else: hits = 1
                        maxhits = hits


        #cooldown makes turns not instant/1 frame long
        if cooldown > 0:
            cooldown -= 1
        if cooldown <= 0:
            cooldown = 0
            #Allows combatents to perform actions
            if battle_action == "player" and player.stats["HP"] > 0 and action[0] != "":
                #Set variables
                player.status = "move"

                #Perform move
                if hits > 0 or action[0] == "Skip" or action[0] in player_party:
                    if action[1]["name"] == enemy.stats["name"]:
                        battle_turndata,enemy.stats = player.move(action[0], action[1],player_party)
                    elif action[1]["name"] == player.stats["name"]:
                        battle_turndata,player.stats = player.move(action[0], action[1],player_party)
                    elif action[1]["name"] in player_party:
                        battle_turndata,battle_characters[action[1]["name"]] = player.move(action[0], action[1],player_party)

                    #Changing combatent condition based on HP
                    if enemy.stats["HP"] <= 0:
                        enemy.condition = "Defeated"
                        enemy.status = "dead"
                    elif enemy.stats["HP"]/enemy.stats["MHP"] <= 30:
                        enemy.condition = "Critical"
                    else:
                        enemy.condition = "Normal"
                    if player.stats["HP"] <= 0:
                        player.condition = "Defeated"
                        player.status = "dead"
                    elif player.stats["HP"]/player.stats["MHP"] <= 30:
                        player.condition = "Critical"
                    else:
                        player.condition = "Normal"

                    #Hitting opponent changes their pose + starts/adds to combo
                    if battle_turndata["hit"] > 0:
                        enemy_shake = framesrate/10
                        if int((battle_turndata["totaldmg"]/battle_turndata["target"]["MHP"])*100) >= 5:
                            enemy.status = "hurt"
                        combo_shake = framesrate/5
                        combo["hits"] += battle_turndata["hit"]
                        combo["dmg"] += battle_turndata["totaldmg"]

                    #Neutral cooldown
                    if maxhits == 1:
                        cooldown = (framesrate*2)
                    elif maxhits != 0:
                        cooldown = int((framesrate*2)/maxhits)

                    hits -= 1

                if hits <= 0:
                    #Changes battle state when hits are finished
                    battle_action = "neutral"

                    #Energy charge. Player exclusive
                    #Player acts, party gets energy
                    if "Basic" in battle_turndata["action"]["prop"] or "Skill" in battle_turndata["action"]["prop"]:
                        if "Basic" in battle_turndata["action"]["prop"]:    energy = 5
                        elif "Skill" in battle_turndata["action"]["prop"]:  energy = 10
                        e = battle_energy(energy,player.stats["ER"]+player.stats["bonuses"]["ER"],player.stats["EG"],player.stats["MEG"])
                        battle_data["energy"][player.stats["name"]] += e - battle_characters[player.stats["name"]]["EG"]
                        battle_characters[player.stats["name"]]["EG"] = e

                        for member in player_party:
                            e = battle_energy(energy,battle_characters[member]["ER"]+battle_characters[member]["bonuses"]["ER"],battle_characters[member]["EG"],battle_characters[member]["MEG"])
                            battle_data["energy"][member] += e - battle_characters[member]["EG"]
                            battle_characters[member]["EG"] = e

                    #Consume vigour
                    if "Skip" == action[0]:
                        vigour["current"]= 0
                    elif "SPECIAL" not in action[0] and action[0] not in player_party:#if not SPECIAL or switch button
                        c = battle_moveslookup(action[0])["cost"]
                        vigour["current"] -= c
                        battle_data["vigour"][player.stats["name"]] += c
                    elif "SPECIAL" in action[0]:
                        player.stats["EG"] = 0
                    #Restore enemy turns
                    if vigour["current"] <= 0:
                        enemy_turns = enemy.stats["turns"]
                    player.status = "turn"

                    #Neutral cooldown
                    cooldown = int(framesrate*2)
                
            elif battle_action == "enemy" and enemy.stats["HP"] > 0:
                #Increases cooldown if action completed
                if selected != "Skip":   enemy.stats["moves"][selected] = False
                #Set variables
                enemy.status = "move"
                battle_action = "neutral"

                if "Offence" in battle_moveslookup(selected)["prop"]:
                    #Targets random alive party member
                    action[0] = selected
                        
                    if action[1]["name"] == player.stats["name"]:
                        battle_turndata,player.stats = enemy.move(action[0], action[1],player_party)
                    else:
                        battle_turndata,battle_characters[action[1]["name"]] = enemy.move(action[0], action[1],player_party)

                    #Enemy lands hit: character hit gets energy
                    energy = 5
                    if action[1]["weakness"] in battle_moveslookup(action[0])["prop"]: energy = energy * 2
                    e = battle_energy(energy,battle_characters[action[1]["name"]]["ER"]+battle_characters[action[1]["name"]]["bonuses"]["ER"],battle_characters[action[1]["name"]]["EG"],battle_characters[action[1]["name"]]["MEG"])
                    battle_data["energy"][action[1]["name"]] += e - battle_characters[action[1]["name"]]["EG"]
                    battle_characters[action[1]["name"]]["EG"] = e
                else:
                    action = [selected,enemy.stats]
                    battle_turndata,enemy.stats = enemy.move(action[0], action[1],player_party)
                    


                #Changing combatent condition based on HP
                if player.stats["HP"] <= 0:
                    player.condition = "Defeated"
                    player.status = "dead"
                    player.stats["EG"] = 0
                elif player.stats["HP"]/player.stats["MHP"] <= 30:
                    player.condition = "Critical"
                else:
                    player.condition = "Normal"
                if enemy.stats["HP"] <= 0:
                    enemy.condition = "Defeated"
                    enemy.status = "dead"
                elif enemy.stats["HP"]/enemy.stats["MHP"] <= 30:
                    enemy.condition = "Critical"
                else:
                    enemy.condition = "Normal"

                #Screen shake and pose change
                if battle_turndata["hit"] > 0:
                    screen_shake = framesrate/10
                    if int((battle_turndata["totaldmg"]/battle_turndata["target"]["MHP"])*100) >= 10:
                        player.status = "hurt"


                cooldown = int(framesrate*2)
            
                
            elif battle_action == "neutral":
                hits = 0
                maxhits = 0
                #Determines what happens after action completed
                
                #End of battle
                end = ""
                if battle_turndata["actor"].stats["HP"] <= 0 and battle_turndata["actor"].stats["name"] == player.stats["name"] or battle_turndata["target"]["HP"] <= 0 and battle_turndata["target"]["name"] == player.stats["name"]:
                    count = 0
                    #Counts how many members have fallen
                    for member in player_party:
                        if battle_characters[member]["HP"] <= 0:
                            count += 1
                        else:
                            #If a member is alive, switch to them
                            battle_turndata,battle_characters[member] = player.move(member, battle_characters[member],player_party)
                            break
                    #If all have fallen, the battle is lost
                    if count == len(player_party):
                        end = "Defeat!"
                elif battle_turndata["actor"].stats["HP"] <= 0 and battle_turndata["actor"].stats["name"] == enemy.stats["name"] or battle_turndata["target"]["HP"] <= 0 and battle_turndata["target"]["name"] == enemy.stats["name"]:
                    end = "Victory!"
                    battle_music("End")

                if end != "":
                    battle_action = end
                    if end == "Defeat!":
                        player.status = "dead"
                    elif end == "Victory!":
                        player.status = "turn"
                    battle_music("End")
                    battle_action = end

                    
                #Player turn
                elif vigour["current"] > 0:
                    #Removes enemy move CD
                    enemy.stats["moves"] = battle_movecd(enemy.stats["moves"])

                    if battle_turndata["actor"].stats["name"] == enemy.stats["name"]:
                        for member in player_party:
                            if member != player.stats["name"]:
                                battle_characters[member]["buff"] = battle_removebuffs(battle_characters[member]["buff"])
                                battle_characters[member]["debuff"] = battle_removebuffs(battle_characters[member]["debuff"])
                            else:
                                player.stats["buff"] = battle_removebuffs(player.stats["buff"])
                                player.stats["debuff"] = battle_removebuffs(player.stats["debuff"])
                        
                    myMixer("menu_turn.wav",0)
                    player.status = "turn"
                    enemy.status = "idle"
                    battle_action = "player"
                #Enemy turn
                elif enemy_turns > 0:
                    enemy_turns -= 1

                    if battle_turndata["actor"].stats["name"] in player_party:
                        enemy.stats["buff"] = battle_removebuffs(enemy.stats["buff"])
                        enemy.stats["debuff"] = battle_removebuffs(enemy.stats["debuff"])
                    
                    player.status = "idle"
                    enemy.status = "turn"
                    battle_action = "enemy"

                    if enemy_turns <= 0:
                        #Restores vigour to player
                        vigour["current"] = vigour["max"]
                        buttonshift_party["point"] = buttonshift_party["max"]
                        buttonshift_moves["point"] = buttonshift_moves["max"]
                        vigour["transition"] = 0
                        combo = {"hits" : 0, "dmg" : 0}

                if action[0] in player_party:#switch button has less button cd
                    cooldown = framesrate*0.1
                else:
                    cooldown = (framesrate*2)#This stops combatents from acting immediately, after being able to
                selected = ""
                action=["",""]

        print("\n" * 200,battle_action)

        #For events happening in the pygame
        for event in pygame.event.get():
            #If window X clicked
            if event.type == pygame.QUIT:
                terminate()

            #Skip cooldown
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cooldown = 0
                #Right mouse button
                if event.button == 3 and battle_action == "player" and selected != "":
                    selected = ""
                    myMixer("menu_back.wav",0)
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    cooldown = 0
                #Right mouse button
                if event.key == 27 and battle_action == "player" and selected != "":
                    selected = ""
                    myMixer("menu_back.wav",0)


        #damage text
        damage_text_group.update()
        damage_text_group.draw(display)

        display_offset = [0,0]
        if screen_shake>0:
            screen_shake -= 1
            if battle_action == "player":   intensity = 2
            else: intensity = int((battle_turndata["totaldmg"]/battle_turndata["target"]["MHP"])*10)*3
            display_offset = image_shake(intensity)
        else:
            screen_shake = 0
                
        screen.blit(display,display_offset)
        pygame.display.update()

        if cooldown <= 0 and (battle_action == "Victory!" or battle_action == "Defeat!"):
            running = "end"
            battle_data["result"] = battle_action

    del img_buffs
    del img_bonus

    for member in player_party:
        player_characters[member]["EG"] = battle_characters[member]["EG"]
        player_characters[member]["HP"] = battle_characters[member]["HP"]

    return battle_data


def battle_startend(player_party,enemy_stats="any",bg="Battle_1",bgm="streaked"):
    global player_characters
    global difficulty
    enemy_stats = get_enemies(enemy_stats)

    #Initiate battle
    result = battle_system(player_party,enemy_stats,bg,bgm)

    #Reformatting stats after battle
    for member in player_party:

        #Fix current HP
        if player_characters[member]["HP"] <= 0:
            player_characters[member]["HP"] = char_stats(characters[member]["MHP"],player_characters[member]["LVL"])
        elif player_characters[member]["HP"] > char_stats(characters[member]["MHP"],player_characters[member]["LVL"]):
            player_characters[member]["HP"] = char_stats(characters[member]["MHP"],player_characters[member]["LVL"])

    return result

def menu_party_character(member):
    global player_characters
    global player_party
    global player_charms

    if member not in player_characters:
        return "", {}

    img = pygame.image.load("img/Char/" + str(member) + "/portrait.png").convert_alpha()
    img_rect = img.get_rect()
    img_scale = screen_mult(screen_diag,60)/100
    img = pygame.transform.scale(img, (int(img_rect.width*img_scale),int(img_rect.height*img_scale)))

    stat_desc = {
        "element" : "Specialised elemental type",
        "STR" : "Base attack strength",
        "RES" : "Resistance against damage",
        "MHP" : "Amount of maximum health points",
        "ER" : "Rate of Energy Recharge",
        "CRIT" : "Likelihood of landing Critical hits",
        "CRIT DMG" : "Damage bonus gained from Critical hits",
        "Fire DMG" : "Damage bonus gained from Fire hits",
        "Wind DMG" : "Damage bonus gained from Wind hits",
        "Water DMG" : "Damage bonus gained from Water hits",
        "All DMG" : "Damage bonus gained from all hits"
        }
        
    stats = {}
    fusion = get_fusion(characters[member]["fusion"])
    for stat in characters[member]:
        #Base value
        value = characters[member][stat]
        if type(value) == int:
            value = char_stats(value,player_characters[member]["LVL"])
        bonus = 0

        #Adds onto base value using charms and fusion
        for charm in player_characters[member]["charms"]:
            if player_charms[charm]["stat"] == stat:
                bonus += player_charms[charm]["amount"]

        if "" in fusion[2]: #(bonus stat without condition)
            if stat in fusion[2][""]:
                bonus += fusion[2][""][stat]
        
        
        if stat in stat_desc:
            if stat == "MHP" and bonus > 0:   bonus = int(value * (bonus/100))
            stats[stat] = {}
            if bonus > 0:
                stats[stat]["stat"] = (str(stat).upper() + ": " + str(value+bonus)) + " (+" + str(bonus) + ")"
            else:
                stats[stat]["stat"] = (str(stat).upper() + ": " + str(value))
            stats[stat]["desc"] = stat_desc[stat]

    return img, stats

def menu_party_buttons():
    global player_characters
    global player_party
    button_party = {}
    button_char = {}
    button_back = button.Button(display,screen_mult(screen_width,5),screen_mult(screen_height,5),pygame.image.load("img/UI/menu_back.png").convert_alpha(),screen_mult(screen_width,60),screen_mult(screen_height,60))
    
    button_width, button_height = screen_mult(screen_width,100),screen_mult(screen_height,100)
    offset = 10

    #Party member buttons
    x, y_value = screen_mult(screen_width,30), screen_height/(len(player_party)+1)
    for member in player_party:
        if player_characters[member]["unlock"] == True:
            button_party[member] = {
                "button" : button.Button(display,x+offset,y_value+offset,pygame.image.load("img/Char/" + str(member) + "/icon_spec.png").convert_alpha(),button_width-int(offset*1.5),button_height-int(offset*1.5)),
                "bg" : pygame.image.load("img/UI/party_" + str(characters[member]["element"]).lower() + "_bg.png").convert_alpha(),
                "border" : pygame.image.load("img/UI/party_" + str(characters[member]["element"]).lower() + ".png").convert_alpha()}
            button_party[member]["bg"] = pygame.transform.scale(button_party[member]["bg"],(button_width-int(offset/5),button_height-int(offset/5)))
            button_party[member]["border"] = pygame.transform.scale(button_party[member]["border"],(button_width,button_height))

            y_value += (screen_height/(len(player_party)+1)) - button_height/2

    #All character buttons
    x_value = x+button_width+x
    basecount = 6 #Character per row
    y_value = screen_height/((len(player_characters)+1/basecount))
    count = basecount+1
    for member in player_characters:
        if member in player_party or player_characters[member]["unlock"] == False:
            continue
        if count > basecount:
            count = 1
            x_value = x+button_width+x
            y_value += button_height + screen_mult(screen_height,30)
        button_char[member] = {
            "button" : button.Button(display,x_value+offset,y_value+offset,pygame.image.load("img/Char/" + str(member) + "/icon.png").convert_alpha(),button_width-int(offset*1.5),button_height-int(offset*1.5)),
            "bg" : pygame.image.load("img/UI/party_" + str(characters[member]["element"]).lower() + "_bg.png").convert_alpha(),
            "border" : pygame.image.load("img/UI/char_" + str(characters[member]["element"]).lower() + ".png").convert_alpha()}
        button_char[member]["bg"] = pygame.transform.scale(button_char[member]["bg"],(button_width-int(offset/5),button_height-int(offset/5)))
        button_char[member]["border"] = pygame.transform.scale(button_char[member]["border"],(button_width,button_height))

        x_value += button_width+screen_mult(screen_width,30)
        count += 1

    return button_party, button_char, button_back, offset

def menu_party_equipment(character,option):
    global player_characters
    global player_charms
    
    button_width, button_height = screen_mult(screen_width,100),screen_mult(screen_height,100)
    
    if option == "moves":
        moves_allowed = 4
        button_mv_eq = {}        
        button_mv_all = {}

        #Equipped moves
        x, y_value = screen_mult(screen_width,30), screen_height/(moves_allowed+1)
        for move in characters[character]["moves"]:
            move_stats = battle_moveslookup(move)
            button_mv_eq[move] = {
                "button" : button.Button(display,x,y_value,pygame.image.load("img/Other/" + str(move_stats["img"]) + ".png").convert_alpha(),button_width,button_height),
                "stats" : move_stats}

            y_value += (screen_height/(moves_allowed+1)) - button_height/2


        return button_mv_eq, button_mv_all

    elif option == "charms":
        charms_allowed = 4
        button_ch_eq = {}        
        button_ch_all = {}

        #Equipped charms
        x, y_value = screen_mult(screen_width,30), screen_height/(charms_allowed+1)
        for charm in player_characters[character]["charms"]:
            charm_stats = player_charms[charm]
            button_ch_eq[charm] = {
                "button" : button.Button(display,x,y_value,pygame.image.load("img/Other/" + str(charm_stats["img"]) + ".png").convert_alpha(),button_width,button_height),
                "stats" : charm_stats,
                "bg" : pygame.transform.scale(pygame.image.load("img/Other/bg_" + str(charm_stats["rarity"]) + ".png").convert_alpha(),(button_width,button_height))}

            y_value += (screen_height/(charms_allowed+1)) - button_height/2
            
        #All charm buttons
        button_width, button_height = screen_mult(screen_width,70),screen_mult(screen_height,70)
        x_value = x+button_width+x
        basecount = 8  #Charms per row
        y_value = screen_mult(screen_height,80)
        count = basecount+1
        for charm in player_charms:
            charm_stats = player_charms[charm]
            if charms_eq_check(charm) != "":
                continue
            if count > basecount:
                count = 1
                x_value = x+button_width+x+x
                y_value += button_height + screen_mult(screen_height,30)
            button_ch_all[charm] = {
                "button" : button.Button(display,x_value,y_value,pygame.image.load("img/Other/" + str(charm_stats["img"]) + ".png").convert_alpha(),button_width,button_height),
                "stats" : charm_stats,
                "bg" : pygame.transform.scale(pygame.image.load("img/Other/bg_" + str(charm_stats["rarity"]) + ".png").convert_alpha(),(button_width,button_height))
                }

            x_value += button_width+screen_mult(screen_width,30)
            count += 1

        return button_ch_eq, button_ch_all
    elif option == "fusion":
        return None, None
    

def menu_party(message):
    global player_characters
    global player_party
    global inviscircle

    base_message = message
    button_party, button_char, button_back, offset = menu_party_buttons()
    max_partysize = 3

    #Black box
    black_box_alpha = 255
    black_box = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA) #SRCALPHA enables transparency

    #Exclaimation mark
    exclaim = pygame.transform.scale(pygame.image.load("img/UI/exclaim.png").convert_alpha(),(20,30))

    #Equipment buttons
    y_value = 0
    x,y = screen_width/2 + screen_mult(screen_width,200), screen_height-(screen_height/4)-screen_mult(screen_height,10)
    button_width, button_height = screen_mult(screen_width,210),screen_mult(screen_height,50)
    options = ["about","moves","charms","fusion"]
    button_equip = {}
    for option in options:
        button_equip[option] = {
                "button" : button.Button(display,x,y+y_value,pygame.image.load("img/UI/mainmenu_button.png").convert_alpha(),button_width,button_height),
                "icon" : pygame.image.load("img/UI/party_" + str(option) + ".png").convert_alpha()}
        button_equip[option]["icon"] = pygame.transform.scale(button_equip[option]["icon"], (button_equip[option]["button"].rect.height-screen_mult(screen_width,10),button_equip[option]["button"].rect.height-screen_mult(screen_height,10)))
        y_value += button_height + screen_mult(screen_height,10)

    #Equip/Swap/Remove button
    button_eq = button.Button(display,screen_mult(screen_width,35),screen_mult(screen_height,850),pygame.image.load("img/UI/party_eqbutton.png").convert_alpha(),screen_mult(screen_width,90),screen_mult(screen_height,30))

    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))


    selected = ""
    selected_eq = ""
    menu = "characters"
    button_equipment, button_equipment_all = "", ""
    bg_left = pygame.image.load("img/background/menu_party_bg.png").convert_alpha()
    bg_left = pygame.transform.scale(bg_left,(int(screen_width/2),int(screen_height)))
    bg_right = pygame.image.load("img/background/menu_party_char.png").convert_alpha()
    bg_right = pygame.transform.scale(bg_right,(int(screen_width/2),int(screen_height)))
    bar = pygame.image.load("img/UI/levelup_bar.png").convert_alpha()
    bar = pygame.transform.scale(bar,(int(screen_width/2),int(screen_height/4)))

    char_img, char_stats = "", {}
    
    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False,
            "right_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True
                elif event.button == 3 and selected != "" and menu == "characters":
                    controls["right_click"] = True
                    myMixer("menu_back.wav",0)
                    selected = ""
                    message = "Organise party"
                    char_img, char_stats = "", {}
                elif event.button == 3 and selected != "" and menu != "characters" and selected_eq != "":
                    controls["right_click"] = True
                    myMixer("menu_back.wav",0)
                    selected_eq = ""
                    message = ""
                
        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()
        display.fill(colour["grey"])

        #Update invis circle
        inviscircle.update(5)

        #Backgrounds
        display.blit(bg_left,(0,0))
        display.blit(bg_right,(screen_width/2,0))

        #Top left border
        box = pygame.Rect(0, 0, screen_width/2, screen_mult(screen_height,170))
        pygame.draw.rect(display, colour["black"], box)
        #Bottom left border
        box = pygame.Rect(0, screen_height-screen_mult(screen_height,120), screen_width/2, screen_mult(screen_height,120))
        pygame.draw.rect(display, colour["black"], box)

        size = screen_mult(screen_height,120)
        #Top right border
        box = pygame.Rect(screen_width/2, 0, screen_width/2, size)
        pygame.draw.rect(display, colour["black"], box)
        #Bottom right border
        box = pygame.Rect(screen_width/2, screen_height-size, screen_width/2, size)
        pygame.draw.rect(display, colour["black"], box)
        
        #Middle line
        box = pygame.Rect((screen_width/2)-screen_mult(screen_width,5), 0, screen_mult(screen_width,10), screen_height)
        pygame.draw.rect(display, colour["black"], box)


        #Manage buttons
        text_hover = ""
        if menu == "characters":
            switch = False
            draw_text("PARTY", fonts["dmgsmall"], colour["menu"], screen_mult(screen_width,35), screen_mult(screen_height,180), False)
            for option in button_party:
                #display party buttons
                display.blit(button_party[option]["bg"], [button_party[option]["button"].rect.x-offset+2, button_party[option]["button"].rect.y-offset+2]) 
                clicked = button_party[option]["button"].draw("","","")
                display.blit(button_party[option]["border"], [button_party[option]["button"].rect.x-offset, button_party[option]["button"].rect.y-offset])

                #Outline if seleted
                if option == selected:
                    pygame.draw.rect(display, colour[characters[option]["element"]], (button_party[option]["button"].rect.x-offset+2, button_party[option]["button"].rect.y-offset+2, button_party[option]["button"].rect.width+offset+2, button_party[option]["button"].rect.height+offset+2), screen_mult(screen_width,5))
                elif button_party[option]["button"].hover():
                    pygame.draw.rect(display, colour["white"], (button_party[option]["button"].rect.x-offset+2, button_party[option]["button"].rect.y-offset+2, button_party[option]["button"].rect.width+offset+2, button_party[option]["button"].rect.height+offset+2), screen_mult(screen_width,5))
                    if selected not in button_party and selected != "":
                        draw_text("SWAP", fonts["small"], colour["menu"], button_party[option]["button"].rect.x+15, button_party[option]["button"].rect.y+button_party[option]["button"].rect.height+5, False)
                    else:
                        draw_text(str(option).upper() + " • LVL " + str(player_characters[option]["LVL"]), fonts["small"], colour[characters[option]["element"]], button_party[option]["button"].rect.x-15, button_party[option]["button"].rect.y+button_party[option]["button"].rect.height+5, False)

                #Swap characters
                if clicked and selected != "" and selected != option and selected not in button_party and controls["left_click"]:
                    message = str(selected) + " joined the party!"
                    if len(player_party) < max_partysize:
                        player_party.append(selected)
                    else:
                        player_party[player_party.index(option)] = selected
                    selected = ""
                    switch = True
                    button_party, button_char, button_back, offset = menu_party_buttons()
                    char_img, char_stats = "", {}
                    myMixer("menu_1more.wav",-0.5)
                #Select character
                elif clicked and controls["left_click"]:
                    selected = option
                    char_img, char_stats = menu_party_character(option)
                    myMixer("menu_text.wav",-0.5)
                    
                
            for option in button_char:
                #display character buttons  
                display.blit(button_char[option]["bg"], [button_char[option]["button"].rect.x-offset+2, button_char[option]["button"].rect.y-offset+2])
                clicked = button_char[option]["button"].draw("","","")
                display.blit(button_char[option]["border"], [button_char[option]["button"].rect.x-offset, button_char[option]["button"].rect.y-offset])

                #Outline if selected
                if option == selected:
                    pygame.draw.rect(display, colour[characters[option]["element"]], (button_char[option]["button"].rect.x-offset+2, button_char[option]["button"].rect.y-offset+2, button_char[option]["button"].rect.width+offset+2, button_char[option]["button"].rect.height+offset+2), screen_mult(screen_width,5))
                elif button_char[option]["button"].hover():
                    pygame.draw.rect(display, colour["white"], (button_char[option]["button"].rect.x-offset+2, button_char[option]["button"].rect.y-offset+2, button_char[option]["button"].rect.width+offset+2, button_char[option]["button"].rect.height+offset+2), screen_mult(screen_width,5))
                    if selected not in button_char and selected != "":
                        draw_text("SWAP", fonts["small"], colour["menu"], button_char[option]["button"].rect.x+screen_mult(screen_width,15), button_char[option]["button"].rect.y+button_char[option]["button"].rect.height+5, False)
                    else:
                        draw_text(str(option).upper() + " • LVL " + str(player_characters[option]["LVL"]), fonts["small"], colour[characters[option]["element"]], button_char[option]["button"].rect.x-10, button_char[option]["button"].rect.y+button_char[option]["button"].rect.height+5, False)

                #Swap characters
                if clicked and selected != "" and switch == False and selected != option and selected in button_party and option not in button_party and controls["left_click"]:
                    message = str(option) + " joined the party!"
                    if len(player_party) < max_partysize:
                        player_party.append(option
                                            )
                    else:
                        player_party[player_party.index(selected)] = option
                    selected = ""
                    button_party, button_char, button_back, offset = menu_party_buttons()
                    char_img, char_stats = "", {}
                    myMixer("menu_1more.wav",-0.5)
                #Select character
                elif clicked and controls["left_click"] and switch == False:
                    selected = option
                    char_img, char_stats = menu_party_character(option)
                    myMixer("menu_text.wav",-0.3)
                    
        elif menu == "moves" and selected != "":
            text_hover = ""
            switch = False
            #EQUIPPED MOVE
            for move in button_equipment: 
                clicked = button_equipment[move]["button"].draw("","","")
                
                #Outline if seleted
                if move == selected_eq:
                    pygame.draw.circle(display, colour["white"], (button_equipment[move]["button"].rect.center[0]-2, button_equipment[move]["button"].rect.center[1]-2), button_equipment[move]["button"].rect.width/2,7)
                elif button_equipment[move]["button"].hover():
                    pygame.draw.circle(display, colour["green"], (button_equipment[move]["button"].rect.center[0]-2, button_equipment[move]["button"].rect.center[1]-2), button_equipment[move]["button"].rect.width/2,7)
                    #Move name
                    text_hover = str(move) + " # # " + str(button_equipment[move]["stats"]["desc"]["b"] + " # ")

                #Select move
                if clicked and controls["left_click"] and switch == False:
                    selected_eq = move
                    message = button_equipment[move]["stats"]["desc"]["b"]
                    myMixer("menu_text.wav",-0.5)

            draw_text(text_hover, fonts["small"], colour["menu"], mouse_pos[0], mouse_pos[1], True)
                    
        elif menu == "about" and selected != "":
            switch = False
            text_hover = ""
            #EQUIPPED WEAPON
            clicked = button_equipment["button"].draw("","","")
            #Outline if seleted
            if button_equipment["stats"]["name"] == selected_eq:
                pygame.draw.rect(display, colour["white"], (button_equipment["button"].rect.x-2, button_equipment["button"].rect.y-2, button_equipment["button"].rect.width+2, button_equipment["button"].rect.height+2), 5)
            elif button_equipment["button"].hover():
                pygame.draw.rect(display, colour["green"], (button_equipment["button"].rect.x-2, button_equipment["button"].rect.y-2, button_equipment["button"].rect.width+2, button_equipment["button"].rect.height+2), 5)
                text_hover = button_equipment["desc"]

            if clicked and controls["left_click"]:
                selected_eq = button_equipment["stats"]["name"]
                message = "Selected: " + str(selected_eq)
                myMixer("menu_text.wav",-0.5)

            draw_text(text_hover, fonts["small"], colour["menu"], mouse_pos[0], mouse_pos[1], True)
        elif menu == "charms":
            #Variable "charm" is an ID for a charm.
            charms_allowed = 4
            text_hover = ""
            switch = False
            #EQUIPPED CHARM
            for charm in button_equipment:
                display.blit(button_equipment[charm]["bg"], [button_equipment[charm]["button"].rect.x, button_equipment[charm]["button"].rect.y]) 
                clicked = button_equipment[charm]["button"].draw("","","")
                
                #Outline if seleted
                if charm == selected_eq:
                    pygame.draw.rect(display, colour["white"], (button_equipment[charm]["button"].rect.x-2, button_equipment[charm]["button"].rect.y-2, button_equipment[charm]["button"].rect.width+2, button_equipment[charm]["button"].rect.height+2), 5)
                    #Remove button
                    button_eq.scale(screen_mult(screen_width,90),screen_mult(screen_height,30))
                    remove = button_eq.draw(button_equipment[charm]["button"].rect.x+2,button_equipment[charm]["button"].rect.y+button_equipment[charm]["button"].rect.height+2,"")
                    if button_eq.hover():
                        col = colour[characters[selected]["element"]]
                    else:
                        col = colour["menu"]
                    draw_text("REMOVE", fonts["small"], colour["grey"], button_eq.rect.x+screen_mult(screen_width,8)+2, button_eq.rect.y+screen_mult(screen_height,5)+2, False)
                    draw_text("REMOVE", fonts["small"], col, button_eq.rect.x+screen_mult(screen_width,8), button_eq.rect.y+screen_mult(screen_height,5), False)

                    if remove:
                        player_characters[selected]["charms"].remove(selected_eq)
                        selected_eq = ""
                        char_stats = menu_party_character(selected)[1]
                        button_equipment, button_equipment_all = menu_party_equipment(selected,menu)
                        myMixer("menu_back.wav",-0.5)
                        message = "Removed: " + str(player_charms[charm]["set"])
                elif button_equipment[charm]["button"].hover():
                    pygame.draw.rect(display, colour["green"], (button_equipment[charm]["button"].rect.x-2, button_equipment[charm]["button"].rect.y-2, button_equipment[charm]["button"].rect.width+2, button_equipment[charm]["button"].rect.height+2), 5)
                    #charm name
                    if selected_eq != charm and selected_eq != "":
                        draw_text("SWAP", fonts["small"], colour["menu"], button_equipment[charm]["button"].rect.x+screen_mult(screen_width,15), button_equipment[charm]["button"].rect.y+button_equipment[charm]["button"].rect.height+5, False)
                    text_hover = str(button_equipment[charm]["stats"]["set"]) + " # # +" + str(button_equipment[charm]["stats"]["amount"]) + " " + str(button_equipment[charm]["stats"]["stat"])
                    
                #Swap charm
                if clicked and selected_eq != "" and selected_eq in button_equipment_all and controls["left_click"]:
                    message = "Equipped '" + str(player_charms[selected_eq]["set"]) + "'!"
                    if len(player_characters[selected]["charms"]) >= charms_allowed:
                        #Swap charms
                        player_characters[selected]["charms"][player_characters[selected]["charms"].index(charm)] = selected_eq
                    else:
                        #Add charm to equipment if less than 4 equipped
                        player_characters[selected]["charms"].append(selected_eq)
                    selected_eq = ""
                    switch = True
                    char_stats = menu_party_character(selected)[1]
                    button_equipment, button_equipment_all = menu_party_equipment(selected,menu)
                    myMixer("equip_charm.wav",-0.5)
                #Select charm
                if clicked and controls["left_click"] and switch == False:
                    selected_eq = charm
                    message = player_charms[charm]["set"]
                    myMixer("menu_text.wav",-0.5)

            #ALL CHARMS
            for charm in button_equipment_all:
                display.blit(button_equipment_all[charm]["bg"], [button_equipment_all[charm]["button"].rect.x, button_equipment_all[charm]["button"].rect.y]) 
                clicked = button_equipment_all[charm]["button"].draw("","","")
                
                #Outline if selected
                if charm == selected_eq:
                    pygame.draw.rect(display, colour["white"], (button_equipment_all[charm]["button"].rect.x-2, button_equipment_all[charm]["button"].rect.y-2, button_equipment_all[charm]["button"].rect.width+2, button_equipment_all[charm]["button"].rect.height+2), 5)
                    #Add button
                    if len(player_characters[selected]["charms"]) < charms_allowed:
                        button_eq.scale(screen_mult(screen_width,50),screen_mult(screen_height,27))
                        add = button_eq.draw(button_equipment_all[charm]["button"].rect.x+screen_mult(screen_width,7),button_equipment_all[charm]["button"].rect.y+button_equipment_all[charm]["button"].rect.height+2,"")
                        if button_eq.hover():
                            col = colour[characters[selected]["element"]]
                        else:
                            col = colour["menu"]
                        draw_text("ADD", fonts["small"], colour["grey"], button_eq.rect.x+screen_mult(screen_width,7)+2, button_eq.rect.y+screen_mult(screen_height,4)+2, False)
                        draw_text("ADD", fonts["small"], col, button_eq.rect.x+screen_mult(screen_width,7), button_eq.rect.y+screen_mult(screen_height,4), False)

                        if add:
                            player_characters[selected]["charms"].append(selected_eq)
                            selected_eq = ""
                            char_stats = menu_party_character(selected)[1]
                            button_equipment, button_equipment_all = menu_party_equipment(selected,menu)
                            myMixer("equip_charm.wav",-0.5)
                            message = "Equipped: " + str(player_charms[charm]["set"])
                elif button_equipment_all[charm]["button"].hover():
                    pygame.draw.rect(display, colour["green"], (button_equipment_all[charm]["button"].rect.x-2, button_equipment_all[charm]["button"].rect.y-2, button_equipment_all[charm]["button"].rect.width+2, button_equipment_all[charm]["button"].rect.height+2), 5)
                    if selected_eq not in button_equipment_all and selected_eq != "":
                        draw_text("SWAP", fonts["small"], colour["menu"], button_equipment_all[charm]["button"].rect.x+screen_mult(screen_width,15), button_equipment_all[charm]["button"].rect.y+button_equipment_all[charm]["button"].rect.height+5, False)
                    text_hover = str(button_equipment_all[charm]["stats"]["set"]) + " # # +" + str(button_equipment_all[charm]["stats"]["amount"]) + " " + str(button_equipment_all[charm]["stats"]["stat"] + " # ")
                    
                #Swap charm
                if clicked and switch == False and selected_eq != "" and selected_eq in button_equipment and controls["left_click"]:
                    message = "Equipped '" + str(player_charms[charm]["set"]) + "'!"
                    if len(player_characters[selected]["charms"]) >= 4:
                        player_characters[selected]["charms"][player_characters[selected]["charms"].index(selected_eq)] = charm
                    else:
                        player_characters[selected]["charms"].append(charm)
                    selected_eq = ""
                    char_stats = menu_party_character(selected)[1]
                    button_equipment, button_equipment_all = menu_party_equipment(selected,menu)
                    myMixer("equip_charm.wav",-0.5)
                #Select charm
                elif clicked and controls["left_click"] and switch == False:
                    selected_eq = charm
                    message = "Selected: " + str(player_charms[charm]["set"])
                    myMixer("menu_text.wav",-0.5)

            #Add/Remove button
            #Selected charm is equipped
            if selected_eq in button_equipment:
                clicked = button_eq.draw("","","")
                if button_eq.hover():
                    col = colour[characters[selected]["element"]]
                else:
                    col = colour["menu"]
                draw_text("REMOVE", fonts["small"], colour["grey"], button_eq.rect.x+screen_mult(screen_width,7)+2, button_eq.rect.y+screen_mult(screen_height,4)+2, False)
                draw_text("REMOVE", fonts["small"], col, button_eq.rect.x+screen_mult(screen_width,7), button_eq.rect.y+screen_mult(screen_height,4), False)

                if clicked:
                    player_characters[selected]["charms"].remove(selected_eq)
                    selected_eq = ""
                    char_stats = menu_party_character(selected)[1]
                    button_equipment, button_equipment_all = menu_party_equipment(selected,menu)
                    myMixer("menu_back.wav",-0.5)
                    message = "Removed: " + str(player_charms[charm]["set"])

            draw_text(str(text_hover), fonts["small"], colour["menu"], mouse_pos[0], mouse_pos[1], True)


        if text_hover != "":
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

        #Character img and stats
        if char_img != "" and len(char_stats) > 0:
            #Top right border
            size = screen_mult(screen_height,20)
            box = pygame.Rect(screen_width/2, 0, screen_width/2, size)
            pygame.draw.rect(display, colour[characters[selected]["element"]], box)
            #Bottom right border
            box = pygame.Rect(screen_width/2, screen_height-size, screen_width/2, size)
            pygame.draw.rect(display, colour[characters[selected]["element"]], box)
            
            x,y = (screen_width/2,screen_height-(screen_height/4)-screen_mult(screen_height,30))
            #Character image. Only move the y axis with inviscircle. Makes sure image is centred
            img_rect = char_img.get_rect()
            img_x, img_y = int((screen_width*0.75)-(img_rect.width/2)),screen_mult(screen_height,50)
            display.blit(char_img, (img_x,mouse_hovereffect(img_x,img_y,"circle")[1]))
            #Stats bar
            display.blit(bar,(x,y))
            #Character equips
            hover = False
            for equip in button_equip:
                clicked = button_equip[equip]["button"].draw("","","") and controls["left_click"]

                myColour = colour["white"]
                icon_x = button_equip[equip]["button"].rect.x+screen_mult(screen_width,20)
                #Display equipment descriptions if hovering over the button
                if button_equip[equip]["button"].hover():
                    desc = ""
                    if equip == "about":
                        desc = "This is the character's information"
                    elif equip == "moves":
                        for move in characters[selected]["moves"]:
                            desc += str(move) + " # "
                    elif equip == "charms":
                        for charm in player_characters[selected]["charms"]:
                            desc += str(player_charms[charm]["set"]) + " - " + str(player_charms[charm]["desc"]) + " # "
                    elif equip == "fusion":
                        desc = str(characters[selected]["fusion"]).upper() + " # # " + str(get_fusion(characters[selected]["fusion"])[1])
                    hover = True
                    icon_x += screen_mult(screen_width,5)
                    draw_text(str(desc), fonts["small"], colour["menu"], button_equip[equip]["button"].rect.x+screen_mult(screen_width,210),y+screen_mult(screen_height,30), True)
                    myColour = colour[characters[selected]["element"]]
                
                if clicked and menu != equip:
                    hover = True
                    myMixer("menu_text.wav",0.3)
                    myColour = colour["white"]
                    #Open corrosponding menu
                    menu = equip
                    message = ""
                    selected_eq = ""
                    button_equipment, button_equipment_all = menu_party_equipment(selected,equip)
                elif clicked and menu == equip:
                    hover = True
                    myMixer("menu_back.wav",0.3)
                    myColour = colour["white"]
                    #Back to character menu
                    menu = "characters"
                    button_equipment, button_equipment_all = "",""
                elif clicked == False and menu == equip:
                    myColour = colour[characters[selected]["element"]]
                    
                #Exclaimation mark if incomplete equipment
                if (equip == "moves" and len(characters[selected]["moves"]) < 4) or (equip == "charms" and len(player_characters[selected]["charms"]) < 4):
                    display.blit(exclaim, (button_equip[equip]["button"].rect.x+screen_mult(screen_width,140),button_equip[equip]["button"].rect.y+screen_mult(screen_height,8)))
                #Display equipment button itself
                display.blit(button_equip[equip]["icon"], (icon_x,button_equip[equip]["button"].rect.y+screen_mult(screen_height,5)))
                draw_text(str(equip).upper(), fonts["small"], myColour, button_equip[equip]["button"].rect.x+screen_mult(screen_width,62),button_equip[equip]["button"].rect.y+button_equip[equip]["button"].rect.height/3, False)

                
            #Character name text
            draw_text(str(characters[selected]["name"]) + " • LVL " + str(player_characters[selected]["LVL"]), fonts["verylarge"], colour["black"], screen_width/2+screen_mult(screen_width,60)+3, screen_height-(screen_height/3)-screen_mult(screen_height,45)+3, False)
            draw_text(str(characters[selected]["name"]) + " • LVL " + str(player_characters[selected]["LVL"]), fonts["verylarge"], colour[characters[selected]["element"]], screen_width/2+screen_mult(screen_width,60), screen_height-(screen_height/3)-screen_mult(screen_height,45), False)
            if hover == False:
                y_value = 0
                y+= screen_mult(screen_height,15)
                x+= screen_mult(screen_width,400)
                for stat in char_stats:
                    draw_text(char_stats[stat]["stat"], fonts["small"], colour["menu"], x, y, False)
                    #Display desc if hovering over stat
                    if mouse_pos[0] <= x+screen_mult(screen_width,100) and mouse_pos[0] >= x and mouse_pos[1] <= y+screen_mult(screen_height,20) and mouse_pos[1] >= y:
                        draw_text(char_stats[stat]["desc"], fonts["small"], colour["menu"], mouse_pos[0], mouse_pos[1]-screen_mult(screen_height,20), True)
                    y += screen_mult(screen_height,20)

        #Back button
        if button_back.hover():
            draw_text("Back", fonts["small"], colour["green"], button_back.rect.x+button_back.rect.width+2,button_back.rect.y+button_back.rect.height/3, False)
        if button_back.draw("","","") and controls["left_click"]:
            #Return to character screen if pressed back on another screen
            if menu != "characters":
                menu = "characters"
                message = "Organise party"
                selected_eq = ""
            else:
                running = "back"
            myMixer("menu_back.wav",0)

        #Message text
        x,y = screen_mult(screen_width,30),screen_height-screen_mult(screen_height,120)
        draw_text(str(message), fonts["medium"], colour["menu"], x, y, False)

        #Title text
        x,y = screen_mult(screen_width,150), screen_mult(screen_height,30)
        draw_text(str(menu).upper(), fonts["verylarge"], colour["menu"], x, y, True)

        #Initial fade in
        if black_box_alpha > 0:
            black_box.fill((0, 0, 0, black_box_alpha))
            display.blit(black_box, (0,0))

            black_box_alpha -= int(255/(framesrate/2))
                

        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)

    if running == "back":
        return player_party

def menu_options(message):
    global inviscircle
    global player_characters
    global framesrate
    global difficulty
    global screen_height
    global screen_width
    global screen_diag
    global display
    global screen
    global fonts

    base_message = message
    #Available options
    options = {
        "Difficulty" : {"desc" : "Difficulty set to: " + str(difficulty)},
        "Framerate" : {"desc" : "Framerate set to: " + str(framesrate)},
        "Resolution" : {"desc" : "Resolution set to: (" + str(screen_width) + "x" + str(screen_height) + ")"},
        #"Reset" : {"desc" : "Revert characters to LVL 1"},
        "Back" : {"desc" : "Back to Main Menu"}}

    #Create buttons from options
    y_value = screen_height/(len(options)+1)
    button_width = screen_mult(screen_width,420)
    button_height = screen_mult(screen_height,70)
    for option in options:
        options[option]["button"] = button.Button(display,0,y_value,pygame.image.load("img/UI/mainmenu_button.png").convert_alpha(),button_width,button_height)
        y_value += (screen_height/(len(options)+1)) - button_height/2
        options[option]["hovering"] = False

    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    
    selected = ""
    
    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True
                
        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Update invis circle
        inviscircle.update("")
        #Display images
        draw_background("menu_options","circle")

        #Top and bottom borders for effect
        #Black
        box_size = screen_mult(screen_height,180)
        box1 = pygame.Rect(0, 0, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box1)
        box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box2)

        #Title text
        x,y = screen_mult(screen_width,30), screen_mult(screen_height,30)
        draw_text("OPTIONS", fonts["title"], colour["menu"], x, y, False)
    

        #Display buttons
        y_value = screen_height/(len(options)+1)+button_height/2
        message = base_message
        for option in options:
            x,y = -screen_mult(screen_width,50),y_value
            clicked = options[option]["button"].draw(x,y,"")

            #Draw outline if hovering
            if options[option]["button"].hover():
                myColour = colour["white"]
                x_value = screen_mult(screen_width,100)
                message = options[option]["desc"]
                if options[option]["hovering"] == False:
                    options[option]["hovering"] = True
                    myMixer("menu_tap.wav",-0.5)
            else:
                myColour = colour["menu"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False
                
            if clicked and controls["left_click"]:
                running = option
                x_value = screen_mult(screen_width,120)
                
            #Button text
            draw_text(str(option).upper(), fonts["medium"], myColour, x+x_value, y+screen_mult(screen_height,5), False)
            y_value += (screen_height/(len(options)+1)) - button_height/2

        #Message text
        x,y = screen_mult(screen_width,30),screen_height-screen_mult(screen_height,170)
        draw_text(str(message), fonts["medium"], colour["menu"], x, y, False)


        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)
            

    myMixer("menu_text.wav",-0.5)


    #NOT IN USE because i must rework stats dictionaries
    if running == "Reset":
        for member in player_characters:
            player_characters[member]["LVL"] = 1
            player_characters[member]["EXP"] = 0
            player_characters[member]["MEXP"] = 500
            player_characters[member]["MHP"] = 1000
            player_characters[member]["HP"] = player_characters[member]["MHP"]
            player_characters[member]["STR"] = 0
            player_characters[member]["RES"] = 0
            player_characters[member]["ER"] = 100
            player_characters[member]["EG"] = 0
            player_characters[member]["AGG"] = 100 #Aggression
            player_characters[member]["DEF"] = 0 #Shields
            player_characters[member]["CRIT"] = 5
            player_characters[member]["CRIT DMG"] = 50
            player_characters[member]["Fire DMG"] = 0
            player_characters[member]["Water DMG"] = 0
            player_characters[member]["Wind DMG"] = 0
            player_characters[member]["moves"] = ["Attack"]
            player_characters[member]["charms"] = []
            #For formatting old stats
##            newlist = []
##            for charm in player_characters[member]["charms"]:
##                newlist.append(charm)
##            player_characters[member]["charms"] = newlist
##            newlist = []
##            for move in player_characters[member]["moves"]:
##                newlist.append(move)
##            player_characters[member]["moves"] = newlist
##            player_characters[member]["fusion"] = player_characters[member]["fusion"][0]

        
##        file = open("savedatapy.py","w")
##        file.write("player_characters=" + str(player_characters))
##        file.close()
            
        time.sleep(1)
        myMixer("hit_debuff.wav",0)
        message = "All characters reset."

    elif running == "Framerate":
        frames = [120,90,60,30]
        framesrate = frames[frames.index(framesrate)-1]

        myMixer("setting.wav",0)
        message = "Framerate set to: " + str(framesrate)
    elif running == "Resolution":
        wid = [2560,1920,1280]
        hei = [1440,1080,720]
        screen_width = wid[wid.index(screen_width)-1]
        screen_height = hei[hei.index(screen_height)-1]
        screen_diag = int(diagonal(screen_width,screen_height))
        screen = pygame.display.set_mode((screen_width,screen_height))
        display = pygame.Surface((screen_width,screen_height))
        fonts = init_font(screen_diag)

        myMixer("setting.wav",0)
        message = "Resolution set to: " + str(screen_width) + "x" + str(screen_height)

    elif running == "Difficulty":
        modes = ["Maddening", "Hard", "Normal"]
        difficulty = modes[modes.index(difficulty)-1]
        myMixer("setting.wav",0)
        message = "Difficulty set to: " + str(difficulty)
        
    elif running == "Back":
        myMixer("menu_back.wav",0)
        
        return

    menu_options(message)

def screen_mult(screen_value, value):
    global screen_width
    global screen_height
    global screen_diag
    base_res = [1920,1080]#standard
    
    if screen_value == screen_width:
        return int((value/base_res[0])*screen_value)
    elif screen_value == screen_height:
        return int((value/base_res[1])*screen_value)
    elif screen_value == screen_diag:
        base_diag = diagonal(base_res[0],base_res[1])
        return int((value/base_diag)*screen_value)
    else:
        return value

def menu_main(message):
    global old_player_characters
    global player_characters
    global player_party
    global inviscircle
    global version

    base_message = message
    exp_cost = 3

    #Black box
    black_box_alpha = 255
    black_box = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA) #SRCALPHA enables transparency
    
    #Available options
    options = {
        "Fight" : {"desc" : "Start a battle!", "unlock" : True},
        #"Endless" : {"desc" : "Test your might. (Coming soon)"},
        "Train" : {"desc" : "Earn EXP (Cost: " + str(exp_cost) + " GOLD)", "unlock": (player_inventory["Gold"] >= exp_cost)},#Turned off for now
        "Party" : {"desc" : "Organise party", "unlock" : True},
        "Save" : {"desc" : "Save the game", "unlock" : False},
        "Options" : {"desc" : "Change preferences", "unlock" : True},
        "Quit" : {"desc" : "Leave the game", "unlock" : True}}

    #Create buttons from options
    y_value = screen_height/(len(options)+1)
    button_width = screen_mult(screen_width,420)
    button_height = screen_mult(screen_height,70)
    for option in options:
        options[option]["button"] = button.Button(display,0,y_value,pygame.image.load("img/UI/mainmenu_button.png"),button_width,button_height)
        y_value += (screen_height/(len(options)+1)) - button_height/2
        options[option]["hovering"] = False

    #Shop button. [0] is normal button and [1] is button when hovering
    shop_image = [pygame.image.load("img/UI/shop_icon1.png"),pygame.image.load("img/UI/shop_icon2.png")]
    size = 1.5
    shop_button = button.Button(display,screen_width-(screen_width/4),screen_height-(screen_width/5),shop_image[0],int(screen_mult(screen_width,284*size)),int(screen_mult(screen_height,82*size)))

    money_bg = pygame.transform.scale(pygame.image.load("img/UI/mainmenu_money.png"),(shop_button.rect.width,screen_mult(screen_height,40)))
    money_size = screen_mult(screen_width,30)
    money_gold = pygame.transform.scale(pygame.image.load("img/UI/gold.png"),(money_size,money_size))

    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    
    selected = ""
    
    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True
                
        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Update invis circle
        inviscircle.update("")
        #Display images
        draw_background("menu_main","circle")

        #Top and bottom borders for effect
        #Black
        box_size = screen_mult(screen_height,180)
        box1 = pygame.Rect(0, 0, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box1)
        box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box2)

        #Title text
        x,y = screen_mult(screen_width,30), screen_mult(screen_height,30)
        draw_text("WHIMS OF FATE", fonts["title"], colour["grey"], x+2, y+2, False)
        draw_text("by Navee " + str(version), fonts["dmgsmall"], colour["grey"], x+screen_mult(screen_width,1110)+2, y+screen_mult(screen_height,75)+2, False)
        draw_text("WHIMS OF FATE", fonts["title"], colour["menu"], x, y, False)
        draw_text("by Navee " + str(version), fonts["dmgsmall"], colour["menu"], x+screen_mult(screen_width,1110), y+screen_mult(screen_width,75), False)
    

        #Display buttons
        y_value = screen_height/(len(options)+1)+button_height/1.5
        message = base_message
        for option in options:
            x,y = -screen_mult(screen_width,50),y_value
            clicked = options[option]["button"].draw(x,y,"")

            #Draw outline if hovering
            if options[option]["button"].hover() and options[option]["unlock"] == True:
                myColour = colour["white"]
                x_value = screen_mult(screen_width,100)
                message = options[option]["desc"]
                if options[option]["hovering"] == False:
                    options[option]["hovering"] = True
                    myMixer("menu_tap.wav",-0.5)
            elif options[option]["unlock"] == False:
                myColour = colour["grey"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False
            else:
                myColour = colour["menu"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False
    
            if clicked and controls["left_click"] and options[option]["unlock"]:
                running = option
                x_value = screen_mult(screen_width,120)
                if option == "Save":    message = "Saving..."
                elif option == "Quit":    message = "Thanks for Playing!"
                
            #Button text
            draw_text(str(option).upper(), fonts["medium"], myColour, x+x_value, y+screen_mult(screen_height,5), False)
            y_value += (screen_height/(len(options)+1)) - button_height/2

        #Shop button
        #Change img if hovering
        x,y = shop_button.rect.x+(shop_button.rect.width/5),shop_button.rect.y+(shop_button.rect.height/10)
        if shop_button.hover() and controls["left_click"] == False:
            clicked_shop = shop_button.draw(shop_button.rect.x,shop_button.rect.y,shop_image[1])
            draw_text("SHOP", fonts["verylarge"], colour["Singularity"], x-screen_mult(screen_width,20),y-screen_mult(screen_height,15), False)
            message = "Buy equipment"
        else:
            clicked_shop = shop_button.draw(shop_button.rect.x,shop_button.rect.y,shop_image[0])
            draw_text("SHOP", fonts["large"], colour["white"], x,y, False)
        #Currencies under main shop button
        x,y = shop_button.rect.x,shop_button.rect.y+shop_button.rect.height+screen_mult(screen_height,10)
        display.blit(money_bg,(x,y))
        display.blit(money_gold,(x+screen_mult(screen_width,40),y+screen_mult(screen_height,5)))
        draw_text(str(player_inventory["Gold"]), fonts["small"], colour["Singularity"], x+screen_mult(screen_width,80),y+screen_mult(screen_height,12), True)

        if clicked_shop and controls["left_click"]:
            running = "Shop"

        #Message text
        x,y = screen_mult(screen_width,30),screen_height-screen_mult(screen_height,170)
        draw_text(str(message), fonts["medium"], colour["menu"], x, y, False)

        #Initial fade in
        if black_box_alpha > 0:
            black_box.fill((0, 0, 0, black_box_alpha))
            display.blit(black_box, (0,0))

            black_box_alpha -= int(255/(framesrate/2))


        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)
            
    if running == "Fight" and len(player_party) > 0:
        myMixer("menu_text.wav",-0.5)
        menu_world("Select a World")
        pygame.mixer.music.set_volume(0.2)
        message = "Welcome back."
        
    elif running == "Party":
        myMixer("menu_text.wav",-0.5)
        pygame.mixer.music.set_volume(0.1)
        menu_party(options["Party"]["desc"])
        pygame.mixer.music.set_volume(0.2)
        message = "Welcome back."

    elif running == "Options":
        myMixer("menu_text.wav",-0.5)
        pygame.mixer.music.set_volume(0.1)
        menu_options(options["Options"]["desc"])
        pygame.mixer.music.set_volume(0.2)
        message = "Welcome back."
        
    elif running == "Train" and player_inventory["Gold"] >= exp_cost:
        player_inventory["Gold"] -= exp_cost
        myMixer("menu_text.wav",-0.5)
        pygame.mixer.music.fadeout(300)
        exp = 3000
        distribution = {}
        for member in player_party:
            distribution[member] = 100
        battle_result("Training Results", {"EXP" : exp},distribution)
        myMixer("menu_back.wav",0)
        pygame.mixer.music.load("snd/radar.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=99)
        message = str(exp_cost) + " GOLD consumed."

    elif running == "Shop":
        myMixer("menu_shop.wav",0.7)
        costs_gold = 3
        if player_inventory["Gold"] >= costs_gold:
            player_inventory["Gold"] -= costs_gold
            new_charm = battle_charmslookup(1)[0]
            num = "1"
            while num in player_charms:
                num = str(random.randint(1,999))
            player_charms[num] = new_charm
            message = str(costs_gold) + " GOLD consumed -> " + str(new_charm["set"]) + "."
            myMixer("menu_1more.wav",0.8)
        else:
            message = str(costs_gold) + " GOLD needed to buy Charm!"
            myMixer("menu_invalid.wav",0.8)
        
    elif running == "Save":
        myMixer("menu_text.wav",-0.5)
        snd = ""
        time.sleep(1)
        try:
            #Saving data
            with open("savedata.csv", "w") as csv_file:
                    fieldnames = []
                    for stat in player_characters[list(player_characters)[0]]:
                        fieldnames.append(stat)
                        
                    writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
                    writer.writeheader()

                    for player in player_characters:
                        writer.writerow(player_characters[player])
            old_player_characters = player_characters
            snd = "menu_1more.wav"
            message = "Data saved successfully!"
        except Exception as e:
            snd = "menu_invalid.wav"
            message = "Save failed: # " + str(e)
        myMixer(snd,0)
    elif running == "Quit":
        myMixer("menu_text.wav",-0.5)
        pygame.mixer.music.fadeout(300)
        time.sleep(1)
        myMixer("menu_back.wav",0)
        
        terminate()
    else:
        myMixer("menu_invalid.wav",0)
        

    menu_main(message)

def menu_world(message):
    global old_player_characters
    global player_characters
    global worlds
    global player_worlds
    global player_party
    global inviscircle
    global version

    base_message = message

    #Available options
    options = {
        "World 1" : {"desc" : "Enter World 1", "bg" : "Battle_2"},
        "World 2" : {"desc" : "Enter World 2", "bg" : "Battle_3"},
        "World 3" : {"desc" : "Enter World 3", "bg" : "Battle_1"}
    }
    for world in options:
        options[world]["unlock"] = False
        for floor in worlds[world]:
            if worlds[world][floor]["id"] in player_worlds["Available"]:
                options[world]["unlock"] = True
                break
    options["Return"] = {"desc" : "Return to Main Menu", "unlock" : True}


    #Create buttons from options
    y_value = screen_height/(len(options)+1)
    button_width = screen_mult(screen_width,420)
    button_height = screen_mult(screen_height,70)
    for option in options:
        options[option]["button"] = button.Button(display,0,y_value,pygame.image.load("img/UI/mainmenu_button.png"),button_width,button_height)
        y_value += (screen_height/(len(options)+1)) - button_height/2
        options[option]["hovering"] = False
    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))


    selected = ""

    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Update invis circle
        inviscircle.update("")
        #Display images
        flag = False
        for world in options:
            if options[world]["hovering"] and world != "Return":
                draw_background("Battle_5pre","circle")
                x,y = screen_width/3,screen_height/4
                w,h = screen_mult(screen_width,1000),screen_mult(screen_height,562)
                display.blit(pygame.transform.scale(background[str(options[world]["bg"])+"pre"],(w,h)),(x,y))
                pygame.draw.rect(display, colour["white"], (x-5, y-5, w+5, h+5), 5)
                flag = True
                break
        if flag == False:   draw_background("Battle_5","circle")

        #Top and bottom borders for effect
        #Black
        box_size = screen_mult(screen_height,180)
        box1 = pygame.Rect(0, 0, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box1)
        box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box2)

        #Title text
        x,y = screen_mult(screen_width,30), screen_mult(screen_height,30)
        draw_text("WORLD SELECT", fonts["title"], colour["grey"], x+2, y+2, False)
        draw_text("WORLD SELECT", fonts["title"], colour["menu"], x, y, False)

        #Display buttons
        y_value = screen_height/(len(options)+1)+button_height/1.5
        message = base_message
        for option in options:
            x,y = -screen_mult(screen_width,50),y_value
            clicked = options[option]["button"].draw(x,y,"")

            #Draw outline if hovering
            if options[option]["button"].hover() and (options[option]["unlock"] == True or option == "Return"):#Can hover if level high enough or return button
                myColour = colour["white"]
                x_value = screen_mult(screen_width,100)
                message = options[option]["desc"]
                if options[option]["hovering"] == False:
                    options[option]["hovering"] = True
                    myMixer("menu_tap.wav",-0.5)
            elif options[option]["unlock"] == False and option != "Return":
                myColour = colour["grey"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False
            else:
                myColour = colour["menu"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False

            if clicked and controls["left_click"] and (options[option]["unlock"] == True or option=="Return"):
                running = option
                x_value = screen_mult(screen_width,120)

            #Button text
            draw_text(str(option).upper(), fonts["medium"], myColour, x+x_value, y+screen_mult(screen_height,5), False)
            y_value += (screen_height/(len(options)+1)) - button_height/2

        #Message text
        x,y = screen_mult(screen_width,30),screen_height-screen_mult(screen_height,170)
        draw_text(str(message), fonts["medium"], colour["menu"], x, y, False)


        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)

    if running in worlds and options[running]["unlock"] == True:
        myMixer("menu_text.wav",-0.5)
        menu_floor("Select a Floor",running,options[running]["bg"])#Enter world
        myMixer("menu_back.wav",0)
    elif running == "Return":
        myMixer("menu_text.wav",-0.5)
        myMixer("menu_back.wav",0)
        return


    menu_world(message)

def menu_floor(message,world_num,bg):
    global old_player_characters
    global player_characters
    global player_party
    global inviscircle
    global version

    base_message = message

    #Available options
    options = {}
    for floor in worlds[world_num]:
        options[floor] = {"desc" : "Enter Battle (" + str(floor) + ")", "Enemies" : worlds[world_num][floor]["Enemies"], "rank" : "", "Rewards" : worlds[world_num][floor]["Rewards"]}
    for floor in options:
        if worlds[world_num][floor]["id"] in player_worlds["Available"]:
            options[floor]["unlock"] = True
            e = {}#Dict full of enemy info such as Lvl, img
            for enemy in options[floor]["Enemies"]:
                info = get_enemies(str(enemy))
                e[str(enemy)] = {"LVL" : info["LVL"],"img" : pygame.image.load("img/Char/"+str(info["name"])+"/idle.png")}
                e[str(enemy)]["rect"] = e[str(enemy)]["img"].get_rect()
                scale = screen_mult(screen_diag,100)#percentage
                e[str(enemy)]["img"] = pygame.transform.scale(e[str(enemy)]["img"],((int(e[str(enemy)]["rect"].width*scale)/100),int((e[str(enemy)]["rect"].height*scale)/100)))
                e[str(enemy)]["rect"] = e[str(enemy)]["img"].get_rect()
            options[floor]["Enemies"] = e


        else:
            options[floor]["unlock"] = False
    options["Return"] =  {"desc" : "Return to Main Menu", "unlock" : False, "rank" : ""}


    #Create buttons from options
    y_value = screen_height/(len(options)+1)
    button_width = screen_mult(screen_width,420)
    button_height = screen_mult(screen_height,70)
    for option in options:
        options[option]["button"] = button.Button(display,0,y_value,pygame.image.load("img/UI/mainmenu_button.png"),button_width,button_height)
        y_value += (screen_height/(len(options)+1)) - button_height/2
        options[option]["hovering"] = False

    for floor in options:
        if floor != "Return":
            if worlds[world_num][floor]["id"] in player_worlds["Available"]:
                options[floor]["rank"] = pygame.transform.scale(pygame.image.load("img/UI/"+str(player_worlds["Available"][worlds[world_num][floor]["id"]])+".png"),(screen_mult(screen_width,button_height),screen_mult(screen_height,button_height))).convert_alpha()


    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    #Character images
    party_members = {}
    scale = screen_mult(screen_diag,100)#percentage
    for member in player_party:
        rect1 = pygame.image.load("img/Char/"+str(member)+"/idle.png").get_rect()
        rect2 = pygame.image.load("img/Char/"+str(member)+"/turn.png").get_rect()
        party_members[member] = {
            "1" : pygame.transform.scale(pygame.image.load("img/Char/"+str(member)+"/idle.png"),(int((rect1.width*scale)/100),int((rect1.height*scale)/100))),
            "2" : pygame.transform.scale(pygame.image.load("img/Char/"+str(member)+"/turn.png"),(int((rect2.width*scale)/100),int((rect2.height*scale)/100))),
            "rect1" : rect1,
            "rect2" : rect2}

    #Reward images
    reward_img = {
        "scale": screen_mult(screen_diag,60),
        "GOLD" : pygame.image.load("img/UI/gold.png"),
        "EXP" : pygame.image.load("img/UI/exp.png")}
    for floor in options:
        if floor == "Return":   continue
        if "Character" in options[floor]["Rewards"]:
            reward_img[options[floor]["Rewards"]["Character"]] = pygame.image.load("img/Char/"+str(options[floor]["Rewards"]["Character"])+"/icon.png")
    for r in reward_img:#Scale all images
        if r == "scale":    continue
        reward_img[r] = pygame.transform.scale(reward_img[r],(reward_img["scale"],reward_img["scale"]))

    scale = screen_mult(screen_diag,100)#percentage
    for member in player_party:
        rect1 = pygame.image.load("img/Char/"+str(member)+"/idle.png").get_rect()
        rect2 = pygame.image.load("img/Char/"+str(member)+"/turn.png").get_rect()
        party_members[member] = {
            "1" : pygame.transform.scale(pygame.image.load("img/Char/"+str(member)+"/idle.png"),(int((rect1.width*scale)/100),int((rect1.height*scale)/100))),
            "2" : pygame.transform.scale(pygame.image.load("img/Char/"+str(member)+"/turn.png"),(int((rect2.width*scale)/100),int((rect2.height*scale)/100))),
            "rect1" : rect1,
            "rect2" : rect2}

    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Update invis circle
        inviscircle.update("")
        #Display images
        draw_background("Battle_5pre","circle")


        #Top and bottom borders for effect
        #Black
        box_size = screen_mult(screen_height,180)
        box1 = pygame.Rect(0, 0, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box1)
        box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box2)

        #Title text
        x,y = screen_mult(screen_width,30), screen_mult(screen_height,30)
        draw_text("LEVEL SELECT", fonts["title"], colour["grey"], x+2, y+2, False)
        draw_text("LEVEL SELECT", fonts["title"], colour["menu"], x, y, False)

        #Display buttons
        y_value = screen_height/(len(options)+1)+button_height/1.5
        message = base_message
        hover = False
        for option in options:
            x,y = -screen_mult(screen_width,50),y_value
            clicked = options[option]["button"].draw(x,y,"")
            if options[option]["rank"] != "":
                display.blit(options[option]["rank"], (x+options[option]["button"].rect.width-(options[option]["button"].rect.height),y-(options[option]["button"].rect.height*0.3)))

            #Draw outline if hovering
            if options[option]["button"].hover() and (options[option]["unlock"] == True or option == "Return"):#FIX
                myColour = colour["white"]
                hover = True
                x_value = screen_mult(screen_width,100)
                message = options[option]["desc"]
                if options[option]["hovering"] == False:
                    options[option]["hovering"] = True
                    myMixer("menu_tap.wav",-0.5)
            elif options[option]["unlock"] == False and option != "Return":
                myColour = colour["grey"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False
            else:
                myColour = colour["menu"]
                x_value = screen_mult(screen_width,80)
                options[option]["hovering"] = False

            if clicked and controls["left_click"] and (options[option]["unlock"] == True or option=="Return"):
                running = option
                x_value = screen_mult(screen_width,120)

            #Button text
            draw_text(str(option).upper(), fonts["medium"], myColour, x+x_value, y+screen_mult(screen_height,5), False)
            y_value += (screen_height/(len(options)+1)) - button_height/2

        #Display smaller screen with floor info
        text = ""
        e_num = 0
        p_num = 0
        col="white"
        for option in options:
            if options[option]["hovering"] and option != "Return":
                e_num = 0
                for e in options[option]["Enemies"]:
                    e_num += options[option]["Enemies"][e]["LVL"]
                e_num = int(e_num/len(options[option]["Enemies"]))
                text = "Recommended LVL: " + str(e_num)
                p_num = 0
                for member in player_party:
                    p_num += player_characters[member]["LVL"]
                p_num = int(p_num/len(player_party))
                if p_num < e_num:
                    col = "red"
                break
        x,y = screen_width/3-screen_mult(screen_width,200),screen_height/4-screen_mult(screen_height,14)
        w,h = screen_mult(screen_width,1050),screen_mult(screen_height,590)
        display.blit(pygame.transform.scale(background[bg+"pre"],(w,h)),(x,y))
        pygame.draw.rect(display, colour["white"], (x-5, y-5, w+5, h+5), 5)
        draw_text(str(text).upper(), fonts["large"], colour["grey"], x+2+(w*0.15), y+2+(h*0.1), False)
        draw_text(str(text).upper(), fonts["large"], colour[col], x+(w*0.15), y+(h*0.1), False)
        for option in options:#Display enemies for the floor
            if options[option]["hovering"] == True and options[option]["unlock"] == True:
                x_value = 0
                for e in options[option]["Enemies"]:
                    col = "white"
                    if options[option]["Enemies"][e]["LVL"] > p_num:
                        col = "red"
                    display.blit(options[option]["Enemies"][e]["img"],(x+x_value+(w*0.6),y+(h*0.8)-options[option]["Enemies"][e]["rect"].height))
                    draw_text(str(options[option]["Enemies"][e]["LVL"]), fonts["medium"], colour["grey"], x+x_value+(w*0.6)+2, y+(h*0.65)+2, False)
                    draw_text(str(options[option]["Enemies"][e]["LVL"]), fonts["medium"], colour[col], x+x_value+(w*0.6), y+(h*0.65), False)
                    x_value += options[option]["Enemies"][e]["rect"].width*0.8
        #Display party characters
        x_value = 0
        for member in party_members:

            if running in worlds[world_num]:#Change pose is battle starts
                num = "2"
            else:
                num = "1"
            col = "white"
            if hover:
                if player_characters[member]["LVL"] >= e_num:
                    col = "green"
                elif p_num >= e_num:
                    col = "white"
                elif player_characters[member]["LVL"] < e_num:
                    col = "red"
            display.blit(party_members[member][num],(x+x_value+(w*0.1),y+(h*0.8)-party_members[member]["rect" + str(num)].height))
            draw_text(str(player_characters[member]["LVL"]), fonts["medium"], colour["grey"], x+x_value+(w*0.1)+screen_mult(screen_width,12), y+(h*0.65)+2, False)
            draw_text(str(player_characters[member]["LVL"]), fonts["medium"], colour[col], x+x_value+(w*0.1)+screen_mult(screen_width,10), y+(h*0.65), False)
            x_value += party_members[member]["rect" + str(num)].width*0.8

        #REWARDS
        y_value = reward_img["scale"]
        for option in options:
            if options[option]["hovering"] == True and options[option]["unlock"] == True:
                pygame.draw.rect(display, colour["black"],
                                 (x+w+screen_mult(screen_width,15), y,
                                 screen_mult(screen_width,400), (len(options[option]["Rewards"])*reward_img["scale"])+reward_img["scale"]+10))
                pygame.draw.rect(display, colour["white"],
                                 (x+w+screen_mult(screen_width,15), y,
                                 screen_mult(screen_width,400), (len(options[option]["Rewards"])*reward_img["scale"])+reward_img["scale"]+10), 5)
                draw_text("Rewards:", fonts["medium"], colour["grey"], x+w+screen_mult(screen_width,20)+2, y, False)
                draw_text("Rewards:", fonts["medium"], colour["menu"], x+w+screen_mult(screen_width,20), y, False)

                for r in options[option]["Rewards"]:
                    if r == "Character":    display.blit(reward_img[options[option]["Rewards"][r]],(x+w+screen_mult(screen_width,20),y+y_value))
                    else:   display.blit(reward_img[r],(x+w+screen_mult(screen_width,20),y+y_value))
                    draw_text(str(r) + ": " + str(options[option]["Rewards"][r]), fonts["medium"], colour["grey"], x+w+screen_mult(screen_width,20)+reward_img["scale"]+2, y+y_value-2, False)
                    draw_text(str(r) + ": " + str(options[option]["Rewards"][r]), fonts["medium"], colour["Singularity"], x+w+screen_mult(screen_width,20)+reward_img["scale"], y+y_value-2, False)
                    y_value += int(reward_img["scale"]+(reward_img["scale"]*0.1))


        #Message text
        x,y = screen_mult(screen_width,30),screen_height-screen_mult(screen_height,170)
        draw_text(str(message), fonts["medium"], colour["menu"], x, y, False)


        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)

    if running in worlds[world_num] and len(player_party) > 0:
        myMixer("menu_text.wav",-0.5)
        myMixer("battle_start.wav",0)
        pygame.mixer.music.fadeout(300)
        time.sleep(2)
        results = []
        for e in worlds[world_num][running]["Enemies"]:
            results.append(battle_startend(player_party,e,bg,worlds[world_num][running]["bgm"]))
            print(results)
            pygame.mixer.music.load("snd/radar.wav")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=99)
        myMixer("menu_back.wav",0)

        result = "Victory!"
        for r in results:
            if r["result"] == "Defeat!":
                result = "Defeat!"
                break

        message = "Welcome back."
        if "Defeat!" in result:
            message += " That was rough."
        elif "Victory!" in result:
            eg = {}
            highest_eg = ["",0]#Record highest generated energy to choose mvp
            distribution = {}#Distributing EXP according to performance
            vigour = 0#To choose rank for this level. 400vigour ~ 100%enemy hp for S+

            for member in player_party:
                distribution[member] = 0
                eg[member] = 0
            for r in results:
                for member in player_party:
                    distribution[member] += r["vigour"][member] + r["energy"][member]
                    eg[member] += r["energy"][member]
                    vigour += r["vigour"][member]

            #Rank calculation
            score = vigour/len(results)#average per battle
            levels = 0
            for e in options[running]["Enemies"]:
                levels += options[running]["Enemies"][e]["LVL"]
            ranking = {"rank_4" : char_stats(100,levels),"rank_3" : char_stats(200,levels),"rank_2" : char_stats(400,levels)}#S+,S,A,B
            rank = "rank_1"#B by default
            for r in ranking:
                if score <= ranking[r]:
                    rank = r
                    break

            #Choose mvp
            for member in eg:
                if eg[member] > highest_eg[1]:
                    highest_eg = [member,eg[member]]

            rewards = worlds[world_num][running]["Rewards"]
            battle_result("Battle Results",rewards,distribution,{"mvp":highest_eg[0]},rank)

            player_inventory["Wins"] += 1
            player_worlds["Floor"] += 1
            player_worlds["Available"][worlds[world_num][running]["id"]] = str(rank)
            if player_worlds["Floor"] >= len(worlds[world_num]):
                player_worlds["Floor"] = 1
                player_worlds["World"] += 1#Risky. Inconsistent data can occur
            if str(int(worlds[world_num][running]["id"])+1) not in player_worlds["Available"]:#If floor above is locked then unlock it
                player_worlds["Available"][str(int(worlds[world_num][running]["id"])+1)] = "rank_0"
            message += " Ez clap."
    elif running == "Return":
        myMixer("menu_text.wav",-0.5)
        myMixer("menu_back.wav",0)
        return


    menu_floor(message,world_num,bg)

def battle_result_character(player_party,mvp):
    output = {}
    x_value = 0
    for member in player_party:
        output[str(member)] = {"img" : "","x" : 0,"rect" : "","bar" : "","mvp" : False}
        if mvp != "" and mvp == member:
            img = pygame.image.load("img/Char/" + str(member) + "/icon_spec.png").convert_alpha()
            output[str(member)]["mvp"] = True
        else:
            img = pygame.image.load("img/Char/" + str(member) + "/icon.png").convert_alpha()
        img_rect = img.get_rect()
        img_scale = screen_mult(screen_diag,200)
        img = pygame.transform.scale(img, (img_scale,img_scale))
        output[str(member)]["bar"] = ProgressBar(img_scale,img_scale/10,"horizontal")
        output[str(member)]["img"] = img
        output[str(member)]["rect"] = output[str(member)]["img"].get_rect()
        output[str(member)]["x"] = x_value

        x_value += int(img_scale+(img_scale/10))

    return output



def battle_result(message,rewards,distribution,data={},rank=""):
    global player_characters
    global worlds
    global player_party
    global player_inventory

    if "GOLD" in rewards:
        player_inventory["Gold"] += rewards["GOLD"]
    if "Character" in rewards:
        player_characters[rewards["Character"]]["unlock"] = True

    #Creating average for distribution
    total = 0
    for member in distribution:
        total += distribution[member]
    for member in distribution:
        distribution[member] = distribution[member]/total#multiplier
        distribution[member] = int(rewards["EXP"]*distribution[member])
        if distribution[member] <= 0:
            distribution[member] = 1

    print(distribution)
     #Create invisible circle effect object
    size = screen_mult(screen_diag,100)
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))
    button_continue = button.Button(display, screen_width-size-screen_mult(screen_width,50), screen_height-size-screen_mult(screen_height,50), img_skip, size,size)
    mvp_size = screen_mult(screen_diag,80)
    mvp_star = pygame.transform.scale(pygame.image.load("img/UI/star.png").convert_alpha(),(mvp_size,mvp_size))
    mvp = ""
    if "mvp" in data:
        mvp = data["mvp"]
    if rank != "":
        rank = pygame.transform.scale(pygame.image.load("img/UI/" + str(rank) + ".png").convert_alpha(),(screen_mult(screen_diag,200),screen_mult(screen_diag,200)))

    char_ui = battle_result_character(player_party,mvp)
    char_count = 0
    char_exp = {"name" : player_party[char_count],"exp" : distribution[player_party[char_count]]}
    lvl_font_size = screen_mult(screen_diag,80)
    lvl_font = pygame.font.SysFont("Franklin Gothic Medium Cond", lvl_font_size)
    lvl_sfont = pygame.font.SysFont("Franklin Gothic Medium Cond", 30)
    spd = 1/framesrate
    frames = 0
    shake = 0
    shake_y = 0

    running = ""
    while running == "":
        # Handle events
        controls = {
            "left_click" : False
            }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    controls["left_click"] = True

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        if shake > 0:
            shake_y = image_shake(shake)[1]#Shake coords
            shake -= 1#Shake duration
        else:
            shake_y = 0
            shake = 0

        #Update invis circle
        inviscircle.update("")
        #Display images
        draw_background("Battle_5","circle")

        #Top and bottom borders for effect
        #Black
        box_size = screen_mult(screen_height,180)
        box1 = pygame.Rect(0, 0, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box1)
        box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
        pygame.draw.rect(display, colour["black"], box2)

        #Title text
        x,y = int(screen_width*0.05), screen_mult(screen_height,30)
        draw_text(str(message.upper()), fonts["title"], colour["grey"], x+4, y+2, False)
        draw_text(str(message.upper()), fonts["title"], colour["menu"], x, y, False)


        x,y = int(screen_width*0.1),int(screen_height/3)
        if rank != "":#Display rank
            display.blit(rank,(int(screen_width*0.5),y))

        for member in char_ui:#BACKGROUND BOX
            offset = screen_mult(screen_diag,20)
            pygame.draw.rect(display, colour["black"], (x-offset, y-offset, (char_ui[member]["rect"].width+offset)*len(player_party)+screen_mult(screen_width,10), char_ui[member]["rect"].height+screen_mult(screen_height,100)))#Box
            pygame.draw.rect(display, colour["white"], (x-offset, y-offset, (char_ui[member]["rect"].width+offset)*len(player_party)+screen_mult(screen_width,10), char_ui[member]["rect"].height+screen_mult(screen_height,100)),screen_mult(screen_diag,5))#Box
            break
        for member in char_ui:#MAIN CHARACTER BOXES
            s = 0
            if char_exp["name"] == member and shake > 0:
                s = shake_y
            pygame.draw.rect(display, colour["grey"], (x+char_ui[member]["x"], y, char_ui[member]["rect"].width, char_ui[member]["rect"].height))#Box
            display.blit(char_ui[member]["img"],(x+char_ui[member]["x"],y))#Character image
            pygame.draw.rect(display, colour[characters[member]["element"]], (x+char_ui[member]["x"]-10, y-10, char_ui[member]["rect"].width+10, char_ui[member]["rect"].height+10), 10)#Box Outline
            if char_ui[member]["mvp"]:
                display.blit(mvp_star,(x+char_ui[member]["x"]-screen_mult(screen_width,30),y-screen_mult(screen_height,30)))#MVP Star

            draw_text(str(player_characters[member]["LVL"]), lvl_font, colour["black"],x+char_ui[member]["x"]+8+s,y+char_ui[member]["rect"].height-lvl_font_size+2, False)#LVL text
            draw_text(str(player_characters[member]["LVL"]), lvl_font, colour["white"],x+char_ui[member]["x"]+5+s,y+char_ui[member]["rect"].height-lvl_font_size+2, False)
            if player_party.index(member) <= char_count:
                num = distribution[member]
                if member == char_exp["name"]:
                    num -= char_exp["exp"]
                draw_text("+" + str(num) + " EXP", lvl_sfont, colour["white"],x+char_ui[member]["x"]+5,y+char_ui[member]["rect"].height+screen_mult(screen_height,30), False)#EXP Text
            char_ui[member]["bar"].draw(x+char_ui[member]["x"],y+char_ui[member]["rect"].height+5,player_characters[member]["EXP"],char_stats(BASE_MEXP,player_characters[member]["LVL"]),mouse_pos,"white",False)#Progress bar

        if char_exp["exp"] > 0 and player_characters[char_exp["name"]]["LVL"] < 40:
            #Add exp
            tosubtract = (int(distribution[player_party[char_count]] * spd))
            if tosubtract <= 0:     tosubtract = 1
            if char_exp["exp"] > tosubtract:
                #earning exp
                player_characters[char_exp["name"]]["EXP"] += int(distribution[player_party[char_count]] * spd)#add
                char_exp["exp"] -= tosubtract#subtract remaining exp
                if frames == int(framesrate*0.05):
                    myMixer("exp.wav",0)
            else:
                player_characters[char_exp["name"]]["EXP"] += char_exp["exp"]
                char_exp["exp"] = 0
                myMixer("exp_final.wav",0)
            if char_exp["exp"] == 0 and char_count != len(player_party)-1:
                char_count+=1
                char_exp = {"name" : player_party[char_count],"exp" : distribution[player_party[char_count]]}
                spd = 1/framesrate

            if player_characters[char_exp["name"]]["EXP"] >= char_stats(BASE_MEXP,player_characters[char_exp["name"]]["LVL"]):
                #level up!
                myMixer("menu_1more.wav",0)
                shake = 15
                player_characters[char_exp["name"]]["EXP"] = 0
                player_characters[char_exp["name"]]["LVL"] += 1

                if player_characters[char_exp["name"]]["LVL"] >= 40:
                    player_characters[char_exp["name"]]["EXP"] = char_stats(BASE_MEXP,40)
                    char_exp["exp"] = 0

                player_characters[char_exp["name"]]["HP"] = char_stats(characters[char_exp["name"]]["MHP"],player_characters[char_exp["name"]]["LVL"])

        #Continue button
        x,y = mouse_hovereffect(screen_width-size-screen_mult(screen_width,50), screen_height-size-screen_mult(screen_height,50),"mouse")
        if char_count+1 == len(char_ui) and char_exp["exp"] == 0:
            if button_continue.draw(x,y,img_skip):
                running = "continue"
            elif button_continue.hover():
                pygame.draw.rect(display, colour["white"], (x-1, y-1, size+1, size+1), 5)

        screen.blit(display,(0,0))
        pygame.display.update()

        #clock tick
        clock.tick(framesrate)
        frames += 1
        if frames > int(framesrate*0.05):
            frames = 0


def terminate():
    #Terminate
    pygame.quit()
    quit()

#Main program
print("\n" * 200)

global fonts
fonts = init_font(screen_diag)
    
global player_party
player_party = ["Seliph"]

global player_charms
player_charms = {}
charms = battle_charmslookup(2)
ID = 1
for i in charms:
    player_charms[str(ID)] = i
    ID += 1

global player_inventory
player_inventory = {"Gold" : 30, "Wins" : 0}

global difficulty
difficulty = "Normal"
            
pygame.mixer.music.load("snd/radar.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=99)
time.sleep(0.3)
menu_main("")
    
terminate()
