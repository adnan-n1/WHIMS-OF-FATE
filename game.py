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

#Create way more moves, SPECIALS, new fusion type physical (Power Type 01)?
#General balancing between enemy stats and increased stats when level up




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
        if stat != "name" and stat != "element" and stat != "weakness" and stat != "weapontype" and stat != "fusion"and stat != "weapon":
            #Reformatting data since they're all stored as strings 
            player_characters[member][stat] = ast.literal_eval(player_characters[member][stat])

print(player_characters)

#List of all the playable characters and their base stats. Needs reworking. First 3 already done
characters = {
    'Byleth': {'name': 'Byleth', 'weapon': 'Catalyst', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Wind Type 09', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Morgan': {'name': 'Morgan', 'weapon': 'Resistance Blade', 'element': 'Water', 'MHP': 250, 'STR': 115, 'RES': 6, 'CRIT': 4, 'CRIT DMG': 14, 'MEG': 100, 'fusion': 'Prototype: AQUA', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 120},
    'Claude': {'name': 'Claude', 'weapon': 'Bow', 'element': 'Fire', 'MHP': 210, 'STR': 115, 'RES': 4, 'CRIT': 14, 'CRIT DMG': 22, 'MEG': 100, 'fusion': 'Fire Type 07', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},

    'Alm': {'name': 'Alm', 'weapon': 'Wind Bow', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Wind Type 08', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Dimitri': {'name': 'Dimitri', 'weapon': 'Hyper Blade', 'element': 'Water', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Water Type 08', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Lilina': {'name': 'Lilina', 'weapon': 'Catalyst', 'element': 'Fire', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Fire Type 08', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Hilda': {'name': 'Hilda', 'weapon': 'Blade', 'element': 'Fire', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Fire Type 09', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Lucina': {'name': 'Lucina', 'weapon': 'Blade', 'element': 'Water', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Water Type 09', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Ninian': {'name': 'Ninian', 'weapon': 'Focus Catalyst', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Prototype: GALE', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Shez': {'name': 'Shez', 'weapon': 'Health Blade', 'element': 'Fire', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Prototype: BLZE', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Anna': {'name': 'Anna', 'weapon': 'Bow', 'element': 'Fire', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Fire Type 06', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Knight': {'name': 'Knight', 'weapon': 'Blade', 'element': 'Water', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Water Type 07', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Kris': {'name': 'Kris', 'weapon': 'Blade', 'element': 'Water', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Water Type 06', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Lyn': {'name': 'Lyn', 'weapon': 'Blade', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Wind Type 07', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Mia': {'name': 'Mia', 'weapon': 'Blade', 'element': 'Fire', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Fire Type 05', 'moves': ['Agidyne', "Fire Dance", "Burning Hell"], 'weakness': 'Water', 'AGG': 100},
    'Reginn': {'name': 'Reginn', 'weapon': 'Blade', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Wind Type 06', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Seliph': {'name': 'Seliph', 'weapon': 'Blade', 'element': 'Water', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Water Type 05', 'moves': ['Bufudyne',"Striking Tide", "Thalassic Calamity"], 'weakness': 'Wind', 'AGG': 100},
    'Sothe': {'name': 'Sothe', 'weapon': 'Blade', 'element': 'Wind', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Wind Type 05', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'Fire', 'AGG': 100},
    'Alear': {'name': 'Alear', 'weapon': 'Star Blade', 'element': 'Singularity', 'MHP': 230, 'STR': 125, 'RES': 2, 'CRIT': 9, 'CRIT DMG': 30, 'MEG': 100, 'fusion': 'Prototype: STAR', 'moves': ['Garudyne',"Cyclone", "Eye of the Storm"], 'weakness': 'None', 'AGG': 100,}
}

player_characters = {
    "Byleth" : {"name" : "Byleth", "LVL" : 5, "EXP" : 1,"HP" : 230, "charms" : []},
    "Claude" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 210, "charms" : []},
    "Dimitri" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Lilina" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Hilda" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Lucina" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Ninian" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Shez" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Anna" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Knight" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Kris" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Lyn" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Mia" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Reginn" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Seliph" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Sothe" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Alear" : {"name" : "Claude", "LVL" : 3, "EXP" : 1,"HP" : 230, "charms" : []},
    "Morgan" : {"name" : "Morgan", "LVL" : 1, "EXP" : 1,"HP" : 250, "charms" : []}
}

BASE_MEXP = 500

battle_characters = {}

#OLD
##player_characters = {'Alm': {'name': 'Alm', 'weapon': {'type': 'Bow', 'str': 100, 'stat': 'Wind DMG', 'amount': 15, 'name': 'Wind Bow', 'desc': 'STR: 100. Increases Wind DMG by 15.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT DMG Charm I': {'stat': 'CRIT DMG', 'amount': 25, 'name': 'CRIT DMG Charm I', 'desc': 'Increases CRIT DMG by 25.'}}, 'fusion': ['Wind Type 08', "CRIT DMG increased by 35. # When HP is higher than opponent's, CRIT DMG increased by 35. # "], 'moves': {'Attack': 0, 'Cyclone': 0, 'Garudyne': 0, 'SPECIAL: Eye of the Storm': 0, 'Focus': 0, 'Dia': 0}, 'weakness': 'Fire', 'weapontype': 'Bow'},
##                  'Dimitri': {'name': 'Dimitri', 'weapon': {'type': 'Blade', 'str': 100, 'stat': 'CRIT DMG', 'amount': 20, 'name': 'Hyper Blade', 'desc': 'STR: 100. Increases CRIT DMG by 20.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}, 'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Water Type 08', "Physical DMG increased by 80%. # When HP is higher than opponent's, Physical DMG increased by 40%. # "], 'moves': {'Attack': 0, 'Overgrow': 0, 'Awaken II': 0, 'Charge': 0, 'Dia': 0, 'Diarama': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Lilina': {'name': 'Lilina', 'weapon': {'type': 'Catalyst', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Catalyst', 'desc': 'STR: 100.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}, 'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Fire Type 08', "STR increased by 60%. # When hit by an attack, Gain the 'Concentrate' buff and Apply the 'Vulnerable' debuff on opponent. # "], 'moves': {'Attack': 0, 'Agidyne': 0, 'Fire Dance': 0, 'SPECIAL: Cataclysm': 0, 'Concentrate': 0, 'Dia': 0}, 'weakness': 'Water', 'weapontype': 'Catalyst'},
##                  'Byleth': {'name': 'Byleth', 'weapon': {'type': 'Catalyst', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Catalyst', 'desc': 'STR: 100.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT DMG Charm I': {'stat': 'CRIT DMG', 'amount': 25, 'name': 'CRIT DMG Charm I', 'desc': 'Increases CRIT DMG by 25.'}, 'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Wind Type 09', 'Wind DMG increased by 50%. # When landing a CRIT, Wind DMG increased by 50%. # '], 'moves': {'Attack': 0, 'Cyclone': 0, 'Garubarion': 0, 'SPECIAL: Eye of the Storm': 0, 'Overhype': 0, 'Dia': 0}, 'weakness': 'Fire', 'weapontype': 'Catalyst'},
##                  'Hilda': {'name': 'Hilda', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'HP Charm I': {'stat': 'MHP', 'amount': 20, 'name': 'HP Charm I', 'desc': 'Increases MHP by 20%.'}, 'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}}, 'fusion': ['Fire Type 09', "Gain the 'Pyroclastic Charge' buff. # "], 'moves': {'Attack': 0, 'Fire Dance': 0, 'Agibarion': 0, 'SPECIAL: Cataclysm': 0, 'Dia': 0}, 'weakness': 'Water', 'weapontype': 'Blade'},
##                  'Lucina': {'name': 'Lucina', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'RES Charm I': {'stat': 'RES', 'amount': 10, 'name': 'RES Charm I', 'desc': 'Increases RES by 10.'}}, 'fusion': ['Water Type 09', "Water DMG increased by 50% and Gain the 'Inspired' buff. # "], 'moves': {'Attack': 0, 'Striking Tide': 0, 'Bufubarion': 0, 'SPECIAL: Hyperflood Abrasion': 0, 'Debilitate': 0, 'Dia': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Morgan': {'name': 'Morgan', 'weapon': {'type': 'Blade', 'str': 100, 'stat': 'RES', 'amount': 10, 'name': 'Resistance Blade', 'desc': 'STR: 100. Increases RES by 10.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'RES Charm I': {'stat': 'RES', 'amount': 10, 'name': 'RES Charm I', 'desc': 'Increases RES by 10.'}}, 'fusion': ['Prototype: AQUA', "RES increased by 10. # When hit by an attack, Gain the 'Awakened' buff. # When in Critical Condition, Gain the 'Awakened One' buff. # "], 'moves': {'Attack': 0, 'Thalassic Calamity': 0, 'Striking Tide': 0, 'SPECIAL: Hyperflood Abrasion': 0, 'Water Boost': 0, 'Dia': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Claude': {'name': 'Claude', 'weapon': {'type': 'Bow', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Bow', 'desc': 'STR: 100.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'HP Charm I': {'stat': 'MHP', 'amount': 20, 'name': 'HP Charm I', 'desc': 'Increases MHP by 20%.'}}, 'fusion': ['Fire Type 07', "When hit by an attack, Gain the 'Blaze Shield' buff. # "], 'moves': {'Attack': 0, 'Agibarion': 0, 'Fire Dance': 0, 'SPECIAL: Cataclysm': 0, 'Fire Boost': 0, 'Dia': 0}, 'weakness': 'Water', 'weapontype': 'Bow'},
##                  'Ninian': {'name': 'Ninian', 'weapon': {'type': 'Catalyst', 'str': 100, 'stat': 'CRIT', 'amount': 10, 'name': 'Focus Catalyst', 'desc': 'STR: 100. Increases CRIT by 10.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT DMG Charm I': {'stat': 'CRIT DMG', 'amount': 25, 'name': 'CRIT DMG Charm I', 'desc': 'Increases CRIT DMG by 25.'}}, 'fusion': ['Prototype: GALE', 'Wind DMG increased by 20%. # When above 60% HP, CRIT increased by 20 and CRIT DMG increased by 100. # When below 60% HP, CRIT increased by 40 and CRIT DMG increased by 50. # When in Critical Condition, CRIT increased by 20 and CRIT DMG increased by 100. # '], 'moves': {'Attack': 0, 'Garubarion': 0, 'Wrath Tempest': 0, 'SPECIAL: Eye of the Storm': 0, 'Concentrate': 0, 'Wind Boost': 0, 'Dia': 0}, 'weakness': 'Fire', 'weapontype': 'Catalyst'},
##                  'Shez': {'name': 'Shez', 'weapon': {'type': 'Blade', 'str': 100, 'stat': 'MHP', 'amount': 20, 'name': 'Health Blade', 'desc': 'STR: 100. Increases MHP by 20%.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'HP Charm I': {'stat': 'MHP', 'amount': 20, 'name': 'HP Charm I', 'desc': 'Increases MHP by 20%.'}}, 'fusion': ['Prototype: BLZE', "MHP increased by 20%. # When below 60% HP, Gain the 'Pyroclastic Charge' buff. # When in Critical Condition, Gain the 'Pyroclastic Surge' buff. # "], 'moves': {'Attack': 0, 'Burning Hell': 0, 'Fire Dance': 0, 'SPECIAL: Cataclysm': 0, 'Dia': 0, 'Pyroclastic Charge': 0}, 'weakness': 'Water', 'weapontype': 'Blade'},
##                  'Anna': {'name': 'Anna', 'weapon': {'type': 'Bow', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Bow', 'desc': 'STR: 100.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}}, 'fusion': ['Fire Type 06', 'Fire DMG increased by 50%. # '], 'moves': {'Attack': 0, 'Agidyne': 0, 'Concentrate': 0, 'SPECIAL: Cataclysm': 0}, 'weakness': 'Water', 'weapontype': 'Bow'},
##                  'Knight': {'name': 'Knight', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'RES Charm I': {'stat': 'RES', 'amount': 10, 'name': 'RES Charm I', 'desc': 'Increases RES by 10.'}}, 'fusion': ['Water Type 07', "RES increased by 20. # When hit by an attack, Gain the 'Invulnerable' buff and Apply the 'Drained' debuff on opponent. # "], 'moves': {'Attack': 0, 'Bufudyne': 0, 'SPECIAL: Hyperflood Abrasion': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Kris': {'name': 'Kris', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'ER Charm I': {'stat': 'ER', 'amount': 40, 'name': 'ER Charm I', 'desc': 'Increases ER by 40.'}}, 'fusion': ['Water Type 06', 'Water DMG increased by 50%. # '], 'moves': {'Attack': 0, 'Bufudyne': 0, 'Rush': 0, 'SPECIAL: Hyperflood Abrasion': 0, 'Water Boost': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Lyn': {'name': 'Lyn', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Wind Type 07', "When landing a CRIT, Gain the 'Focused' buff. # "], 'moves': {'Attack': 0, 'Garudyne': 0, 'Wrath Tempest': 0, 'SPECIAL: Eye of the Storm': 0, 'Overhype': 0}, 'weakness': 'Fire', 'weapontype': 'Blade'},
##                  'Mia': {'name': 'Mia', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}}, 'fusion': ['Fire Type 05', 'STR increased by 60%. # '], 'moves': {'Attack': 0, 'Agilao': 0, 'Agi': 0, 'SPECIAL: Cataclysm': 0, 'Fire Boost': 0, 'Concentrate': 0}, 'weakness': 'Water', 'weapontype': 'Blade'},
##                  'Reginn': {'name': 'Reginn', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Wind Type 06', 'Wind DMG increased by 50%. # '], 'moves': {'Attack': 0, 'Garudyne': 0, 'Cyclone': 0, 'SPECIAL: Eye of the Storm': 0, 'Wind Boost': 0, 'Concentrate': 0}, 'weakness': 'Fire', 'weapontype': 'Blade'},
##                  'Seliph': {'name': 'Seliph', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'STR Charm I': {'stat': 'STR', 'amount': 30, 'name': 'STR Charm I', 'desc': 'Increases STR by 30%.'}}, 'fusion': ['Water Type 05', 'Physical DMG increased by 80%. # '], 'moves': {'Attack': 0, 'Megido': 0, 'Thousand Slaps': 0, 'SPECIAL: Shining Arrows': 0, 'Charge': 0, 'Debilitate': 0}, 'weakness': 'Wind', 'weapontype': 'Blade'},
##                  'Sothe': {'name': 'Sothe', 'weapon': {'type': 'Blade', 'str': 100, 'stat': '', 'amount': 0, 'name': 'Blade', 'desc': 'STR: 100.'}, 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'CRIT Charm I': {'stat': 'CRIT', 'amount': 5, 'name': 'CRIT Charm I', 'desc': 'Increases CRIT by 5.'}}, 'fusion': ['Wind Type 05', 'CRIT DMG increased by 40. # '], 'moves': {'Attack': 0, 'Garula': 0, 'Garu': 0, 'SPECIAL: Eye of the Storm': 0, 'Wind Boost': 0, 'Concentrate': 0}, 'weakness': 'Fire', 'weapontype': 'Blade'},
##                  'Alear': {'name': 'Alear', 'weapon': {'type': 'Blade', 'str': 100, 'stat': 'All DMG', 'amount': 15, 'name': 'Star Blade', 'desc': 'STR: 100. Increases All DMG by 15.'}, 'element': 'Singularity', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': {'All DMG Charm I': {'stat': 'All DMG', 'amount': 5, 'name': 'All DMG Charm I', 'desc': 'Increases All DMG by 5.'}}, 'fusion': ['Prototype: STAR', "All DMG increased by 60%. # When not in Critical Condition, Gain the 'Half Moon' buff. # When in Critical Condition, Gain the 'Full Moon' buff. # "], 'moves': {'Attack': 0, 'Cyclone': 0, 'Burning Hell': 0, 'Striking Tide': 0, 'SPECIAL: Tenman Crescent Moon': 0, 'Concentrate': 0}, 'weakness': 'None', 'weapontype': 'Blade'}}

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#framerate
clock = pygame.time.Clock()
global framesrate
framesrate = 60

#game window
global screen_width
global screen_height
screen_width = 1280
screen_height = 720
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
          "Fire" : (247, 65, 15), "Water" : (10, 86, 240), "Wind" : (48, 242, 129), "Physical" : (200, 200, 200),"Singularity" : (252, 228, 104),
          "Buff" : (66, 135, 245), "Debuff" : (162, 78, 222), "Heal" : (0, 255, 0)}

#images

#image loaded
background = {
    "menu_main" : pygame.image.load("img/Background/menu_main.png").convert_alpha(),
    "Battle_1" : pygame.image.load("img/Background/battle_1.png").convert_alpha(),
    "Battle_2" : pygame.image.load("img/Background/battle_2.png").convert_alpha(),
    "Battle_3" : pygame.image.load("img/Background/battle_3.png").convert_alpha(),
    "Battle_4" : pygame.image.load("img/Background/battle_4.png").convert_alpha(),
    "Battle_spec" : pygame.image.load("img/Background/battle_5.png").convert_alpha(),
    "Battle_chall" : pygame.image.load("img/Background/battle_6.png").convert_alpha(),
    "Battle_final" : pygame.image.load("img/Background/battle_7.png").convert_alpha(),
    "menu_options" : pygame.image.load("img/Background/menu_options.png").convert_alpha(),
    "Levelup" : pygame.image.load("img/Background/Levelup.png").convert_alpha()
    }

img_skip = pygame.image.load("img/Other/icon_skip.png").convert_alpha()



img_weapon = {
    "Blade" : {
        "Common" : pygame.image.load("img/Other/blade_1.png"),
        "Rare" : pygame.image.load("img/Other/blade_3.png"),
        "Legend" : pygame.image.load("img/Other/blade_4.png")},
    "Bow" : {
        "Common" : pygame.image.load("img/Other/range_1.png"),
        "Rare" : pygame.image.load("img/Other/range_3.png"),
        "Legend" : pygame.image.load("img/Other/range_4.png")},
    "Catalyst" : {
        "Common" : pygame.image.load("img/Other/catalyst_1.png"),
        "Rare" : pygame.image.load("img/Other/catalyst_3.png"),
        "Legend" : pygame.image.load("img/Other/catalyst_4.png")}
    }



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

    #WEAPON
    if "weapon" in person:
        weapon_stats = battle_weaponslookup(person["weapon"])
        image = pygame.transform.scale(img_weapon[weapon_stats["type"]][weapon_stats["rarity"]],(size,size)).convert()
        display.blit(image, (x,y))
        pygame.draw.rect(display, colour["white"], (x, y, size+2, size+2), 2)
        if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
            message = str(person["weapon"]) + ": " + str(weapon_stats["desc"])
            myColour = "white"
        x += size + screen_mult(screen_width,10)

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
    
    symbols = {"MHP" : "","AGG" : "","ER" : "%", "CRIT" : "", "CRIT DMG" : "%", "Physical DMG" : "%","Fire DMG" : "%",  "Water DMG" : "%",  "Wind DMG" : "%",  "RES" : "",  "STR" : "", "All DMG" : "%"}
            
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
        if info.lower() != "charms" and info.lower() != "fusion" and info.lower() != "drops" and info.lower() != "moves" and info.lower() != "bonuses":
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
    battle_draw_bonus(person.stats["bonuses"],x,y+rect_height+screen_mult(screen_height,5))
    
    #Display player charms
    if person.stats["name"] == player.stats["name"]:
        battle_draw_equips(player.stats,enemy.stats,x,y+rect_height+screen_mult(screen_height,40))
    elif person.stats["name"] == enemy.stats["name"]:
        battle_draw_equips(enemy.stats,player.stats,x,y+rect_height+screen_mult(screen_height,40))

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

def draw_text(text,font,textcolour,x,y, includebox):
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
        display.blit(text_surface, (x, line_y + y))
        line_y += text_surface.get_height()
        
    #img = font.render(text, True, colour)
    #screen.blit(img, (x ,y))

def battle_music(hp1, hp2, startend):
    if startend == "Start":
        if hp2 >= 4500:
            track = "streaked.wav"
        elif hp2 >= hp1:
            track = "streaked.wav"
        else:
            track = "streaked.wav"
        pygame.mixer.music.load("snd/" + str(track))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=99)
    elif startend == "End":   pygame.mixer.music.fadeout(3000)

def mouse_hovereffect(x,y,option):
    global inviscircle
    if option == "mouse":   mouse_x, mouse_y = pygame.mouse.get_pos()
    elif option == "circle":    mouse_x,mouse_y = inviscircle.top_x,inviscircle.top_y
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
    bonus_values = {"MHP" : 0,"CRIT" : 0, "CRIT DMG" : 0, "STR" : 0, "RES" : 0, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, "AGG" : 0}
    newstats = battle_bonuscheck(actor,target,battle_turndata,bonus_values)

    return newstats


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
            "move" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/move.png").convert_alpha()
                           }
        #Player has extra img
        if self.stats["name"] in battle_characters:
            self.image_list["ready"] = pygame.image.load("img/Char/" + str(self.stats["name"]) + "/ready.png").convert_alpha()
        
        #size = 1
        #self.image = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        

    def move(self, action, target,player_party):
        global damage_text_group
        
        #Damage text reset
        damage_text_group = pygame.sprite.Group()
        #Functions acts as "Battle neutral"
        self.status = "move"
        message = ""
        message_colour = colour["white"]
        
        action_name = action
        action = battle_moveslookup(action)
        print(action)

        the_elements = ["Fire", "Water", "Wind", "Physical","Singularity","Buff","Debuff","Heal"]
        actionelement = "None"
        for e in the_elements:
            if e in action["prop"]:
                actionelement = e
                break
        the_types = ["Offence", "Defence"]
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
                     "actioninflict" : "None",
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
        hits = 1
        if action_name == "Skip":
            message_colour = colour["white"]
            battle_damagetext(random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height), action_name, message_colour,"medium")
        elif action_name in player_party:
            self.switch(player_party[player_party.index(action_name)],player_party)
            myMixer("partyswitch.wav",-0.5)
            return battle_turndata,target
        elif battle_turndata["actiontype"] == "Offence":
            #Projectiles
            img_proj = {
                "Physical" : pygame.image.load("img/Effects/proj_phys.png").convert_alpha(),
                "Physical_crit" : pygame.image.load("img/Effects/proj_phys_crit.png").convert_alpha(),
                "Fire" : pygame.image.load("img/Effects/proj_fire.png").convert_alpha(),
                "Fire_crit" : pygame.image.load("img/Effects/proj_fire_crit.png").convert_alpha(),
                "Wind" : pygame.image.load("img/Effects/proj_wind.png").convert_alpha(),
                "Wind_crit" : pygame.image.load("img/Effects/proj_wind_crit.png").convert_alpha(),
                "Water" : pygame.image.load("img/Effects/proj_water.png").convert_alpha(),
                "Water_crit" : pygame.image.load("img/Effects/proj_water_crit.png").convert_alpha(),
                "Singularity" : pygame.image.load("img/Effects/proj_sing.png").convert_alpha(),
                "Singularity_crit" : pygame.image.load("img/Effects/proj_sing_crit.png").convert_alpha()
                }
            message_colour = colour["red"]

            if battle_turndata["action"] != "":
                print(action)
                basedmg = action["dmg"]
                if "hits" in action["prop"]:
                    hits = action["hits"]
                else:
                    hits = 1
            else:
                basedmg = 0
                hits = 0

            print(hits)

            #default text size
            size = "small"
            while hits > 0:
                message_colour = colour[battle_turndata["actionelement"]]
                hits -= 1
                battle_turndata["crit"] = False
                battle_turndata["weak"] = False

                damage = int(basedmg * ((self.stats["STR"]+self.stats["bonuses"]["STR"])/100))
                additional_damage_multiplier = 100
                #Apply elemental/physical dmg bonuses
                if str(battle_turndata["actionelement"]) + " DMG" in self.stats and str(battle_turndata["actionelement"]) + " DMG" in self.stats["bonuses"]:
                    additional_damage_multiplier += self.stats["bonuses"][str(battle_turndata["actionelement"]) + " DMG"]+self.stats[str(battle_turndata["actionelement"]) + " DMG"]
                if "All DMG" in self.stats and "All DMG" in self.stats["bonuses"]:
                    additional_damage_multiplier += self.stats["bonuses"]["All DMG"]+self.stats["All DMG"]     
                
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


                #END OF DMG CALCULATION


                #Play sounds. Different sound based on crit hit
                sounds = {"Physical" : "hit_physical.wav","Singularity" : "hit_sing.wav", "Fire" : "hit_fire.wav", "Water" : "hit_water.wav", "Wind" : "hit_wind.wav", }
                sounds_crit = {"Physical" : "hit_physicalcrit.wav", "Singularity" : "hit_sing.wav","Fire" : "hit_firecrit.wav", "Water" : "hit_watercrit.wav", "Wind" : "hit_windcrit.wav", }
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
                    actorxy = [self.rect.x+self.rect.width,random.randint(self.rect.y,self.rect.y+self.rect.height)]
                    targetxy = [random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.height),random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)]
                else:
                    actorxy = [self.rect.x+self.rect.width,random.randint(self.rect.y,self.rect.y+self.rect.height)]
                    targetxy = [random.randint(player.rect.x,player.rect.x+player.rect.height),random.randint(player.rect.y,player.rect.y+player.rect.height)]
                
                if battle_turndata["crit"] or battle_turndata["weak"]: battle_projectile(actorxy,targetxy,img_proj[battle_turndata["actionelement"]+"_crit"])
                else:   battle_projectile(actorxy,targetxy,img_proj[battle_turndata["actionelement"]])
                #Damage text
                battle_damagetext(targetxy[0], targetxy[1]+2,str(damage), colour["grey"],fontsize)
                battle_damagetext(targetxy[0], targetxy[1],str(damage), colour[battle_turndata["actionelement"]],fontsize)


                #Decrease hp
                target = battle_changehp(target, -damage, sound)

                
                #Enemy lands hit: character hit gets energy
                if "EG" in target:
                    energy = 2
                    if battle_turndata["weak"]: energy = energy * 2
                    target["EG"] = battle_energy(energy,target["ER"]+target["bonuses"]["ER"],target["EG"],target["MEG"])

                #Change conditions
                if self.stats["HP"] <= 0: battle_turndata["actorcondition"] = "Defeated"
                elif self.stats["HP"]/(self.stats["MHP"]+self.stats["bonuses"]["MHP"]) <= 30:    battle_turndata["actorcondition"] = "Critical"
                else:   battle_turndata["actorcondition"] = "Normal"
                if target["HP"] <= 0: battle_turndata["targetcondition"] = "Defeated"
                elif target["HP"]/(target["MHP"]+target["bonuses"]["MHP"]) <= 30:    battle_turndata["targetcondition"] = "Critical"
                else:   battle_turndata["targetcondition"] = "Normal"

                #Update bonuses
                self.stats["bonuses"] = battle_updatestats(self.stats,target,battle_turndata)
                target["bonuses"] = battle_updatestats(target,self.stats,battle_turndata)
                


            #Apply debuff if attack has one
            if battle_turndata["actioninflict"] != "None":
                if self.stats["name"] in player_party:
                    x,y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Debuff", x,y,target)
                else:
                    x,y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Debuff", x,y,target)
                
        elif battle_turndata["actiontype"] == "Defence":
            #Healing
            if "dmg" in action:
                amount = int((action["dmg"] * ((self.stats["STR"]+self.stats["bonuses"]["STR"])/100)) * 4)
                if self.stats["name"] == target["name"]:
                    battle_damagetext(self.rect.x+(self.rect.width/2), self.rect.y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                    self.stats = battle_changehp(self.stats, amount,"heal.wav")
                elif target["name"] in player_party:
                    battle_damagetext(200, screen_height/2,str(amount), colour[battle_turndata["actionelement"]],"medium")
                    target = battle_changehp(target, amount,"heal.wav")
            #Apply buff
            if battle_turndata["actioninflict"] != "None":
                if self.stats["name"] == target["name"]:
                    x,y = random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height)
                    self.stats = battle_applybuffs(battle_turndata["actioninflict"],2, "Buff", x,y,self.stats)
                elif target["name"] in player_party:
                    x,y = screen_mult(screen_width,250), (screen_height/(len(player_party)+1)) * (player_party.index(target["name"])+1)
                    target = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,target)
        elif battle_turndata["actiontype"] == "Party" and self.stats["name"] in player_party:
            for member in player_party:
                #Healing
                if action["dmg"] != 0:
                    amount = int((action["dmg"] * ((self.stats["STR"]+self.stats["bonuses"]["STR"])/100)) * 4)
                    if self.stats["name"] == member:
                        battle_damagetext(self.rect.x+(self.rect.width/2), self.rect.y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                        self.stats = battle_changehp(self.stats, amount,"heal.wav")
                    else:
                        x,y = screen_mult(screen_width,250), (screen_height/(len(player_party)+1)) * (player_party.index(member)+1)
                        battle_damagetext(x, y,str(amount), colour[battle_turndata["actionelement"]],"medium")
                        battle_characters[member] = battle_changehp(battle_characters[member], amount,"heal.wav")
                #Apply buff
                if battle_turndata["actioninflict"] != "None":
                    if self.stats["name"] == member:
                        x,y = random.randint(self.rect.x,self.rect.x+self.rect.width), random.randint(self.rect.y,self.rect.y+self.rect.height)
                        self.stats = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,self.stats)
                    else:
                        x,y = screen_mult(screen_width,250), (screen_height/(len(player_party)+1)) * (player_party.index(member)+1)
                        battle_characters[member] = battle_applybuffs(battle_turndata["actioninflict"], 2, "Buff", x,y,battle_characters[member])
            

        #Energy charge. Player exclusive
        #Player acts hit, party gets energy
        if "EG" in self.stats and "SPECIAL" not in battle_turndata["action"]:
            #Base regen rate
            energy = 3
            if battle_turndata["weak"] or battle_turndata["action"] == "Skip": energy = energy * 2
            
            battle_characters[self.stats["name"]]["EG"] = battle_energy(energy,self.stats["ER"]+self.stats["bonuses"]["ER"],self.stats["EG"],self.stats["MEG"])
            for member in player_party:
                battle_characters[member]["EG"] = battle_energy(energy,battle_characters[member]["ER"]+battle_characters[member]["bonuses"]["ER"],battle_characters[member]["EG"],battle_characters[member]["MEG"])
        
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
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def draw(self, x,y,value, maxvalue, mouse_pos,col):
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
        

        draw_text(str(percent) + "%", fonts["small"], colour[col], x + self.width+2, y-3, False)
        pygame.draw.rect(display, colour["grey"], (x, y, self.width, self.height))
        pygame.draw.rect(display, colour[col], (x, y, (percent/100)*self.width, self.height))
        #Outline
        pygame.draw.rect(display, colour[col], (x-1, y-1, self.width+1, self.height+1), 1)

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

class Battle_invisCircle():
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
        self.angle += self.angular_velocity * (80/framesrate)
        # Convert the angle to radians
        radians = math.radians(self.angle)
        # Calculate the position of the top point
        self.top_x = self.centre_x + self.radius * math.cos(radians)
        self.top_y = self.centre_y + self.radius * math.sin(radians)

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
      "Water Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 15}]},
      "Water Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 10}]},
      "Water Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10}]},
      "Water Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 30}]},
      "Water Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 20}]},
      "Water Type 07" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10},{"Cond" : "", "Stat" : "AGG", "Num" : 10}, {"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Invulnerable"}, {"Cond" : "Take hit", "Stat" : "Debuff", "Num" : "Drained"}]},#RES +20. Grants invulnerable to self and drained to target when taking hit
      "Water Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 45}, {"Cond" : "Actor HP higher", "Stat" : "Physical DMG", "Num" : 45}]},#+60 phys dmg. +20 if hp higher than opponent
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
              if effect["Stat"] == "MHP" or effect["Stat"] == "STR" or effect["Stat"] == "Physical DMG" or effect["Stat"] == "Fire DMG" or effect["Stat"] == "Water DMG" or effect["Stat"] == "Wind DMG" or effect["Stat"] == "All DMG" or effect["Stat"] == "ER":
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

    {"name" : "Wind Elemental", "LVL" : 1, "MHP" : 500, "HP" : 500, "STR" : 25, "RES" : 1, "CRIT" : 30, "CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 01", "moves" : {"Thousand Slaps":0, "Garu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Garu", "Thousand Slaps"], "Fusion Cards" : ["Wind Type 01"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 5, "MHP" : 1000, "HP" : 1000, "STR" : 50, "RES" : 2, "CRIT" : 30, "CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,"buff" : {}, "debuff" : {}, "fusion" : "Wind Type 02", "moves" : {"Thousand Slaps":0, "Focus":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Garu", "Focus"], "Fusion Cards" : ["Wind Type 02"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 10, "MHP" : 1500, "HP" : 1500, "STR" : 75, "RES" : 3, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 03", "moves" : {"Garu":0, "Wind Boost":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Garu", "Wind Boost"], "Fusion Cards" : ["Wind Type 03"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 15, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 4, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 04", "moves" : {"Garula":0, "Overhype":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Garula", "Overhype"], "Fusion Cards" : ["Wind Type 04"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 20, "MHP" : 2500, "HP" : 2500, "STR" : 125, "RES" : 5, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 05", "moves" : {"Focus":0, "Cyclone" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Focus","Cyclone"], "Fusion Cards" : ["Wind Type 05"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 25, "MHP" : 3000, "HP" : 3000, "STR" : 150, "RES" : 6, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,"buff" : {}, "debuff" : {}, "fusion" : "Wind Type 06", "moves" : {"Wrath Tempest":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["SPECIAL: Eye of the Storm"], "Fusion Cards" : ["Wind Type 06"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 30, "MHP" : 3500, "HP" : 3500, "STR" : 175, "RES" : 7, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {},"debuff" : {}, "fusion" : "Wind Type 07", "moves" : {"Overhype":0, "Garudyne":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Garudyne", "Overhype"], "Fusion Cards" : ["Wind Type 07"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 35, "MHP" : 4000, "HP" : 4000, "STR" : 200, "RES" : 8, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 08", "moves" : {"Focus":0, "Garubarion":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Garubarion", "Focus"], "Fusion Cards" : ["Wind Type 08"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Sentinel", "LVL" : 40, "MHP" : 4500, "HP" : 4500, "STR" : 225, "RES" : 9, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Wind Type 09", "moves" : {"Wrath Tempest":0, "Cyclone":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Cyclone", "Wrath Tempest"], "Fusion Cards" : ["Wind Type 09"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Kaze", "LVL" : 45, "MHP" : 30000, "HP" : 30000, "STR" : 100, "RES" : 10, "CRIT" : 30,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Prototype: GALE", "moves" : {"Wind Boost":0,"Wrath Tempest":0,"Cyclone":0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Cyclone","Wind Boost","Wrath Tempest"], "Fusion Cards" : ["Prototype: GALE"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Fire Elemental", "LVL" : 1, "MHP" : 500, "HP" : 500, "STR" : 100, "RES" : 1, "CRIT" : 2,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 01", "moves" : {"Agi":0, "Overgrow":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Agi", "Overgrow"], "Fusion Cards" : ["Fire Type 01"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 5, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,"buff" : {}, "debuff" : {}, "fusion" : "Fire Type 02", "moves" : {"Agi":0, "Concentrate":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Agi", "Concentrate"], "Fusion Cards" : ["Fire Type 02"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 10, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 03", "moves" : {"Fire Boost":0, "Agi":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Agi", "Fire Boost"], "Fusion Cards" : ["Fire Type 03"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 15, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 04", "moves" : {"Agilao":0, "Overgrow":0, "Diarama" : 0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Agilao","Diarama"], "Fusion Cards" : ["Fire Type 04"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 20, "MHP" : 2500, "HP" : 2500, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 05", "moves" : {"Concentrate":0, "Fire Dance" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Concentrate", "Agilao"], "Support Items" : ["Molotov"], "Fusion Cards" : ["Fire Type 05"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 25, "MHP" : 3000, "HP" : 3000, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 06", "moves" : {"Burning Hell":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["SPECIAL: Cataclysm", "Agilao"], "Fusion Cards" : ["Fire Type 06"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 30, "MHP" : 3500, "HP" : 3500, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 07", "moves" : {"Diarama":0, "Agidyne" : 0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Diarama", "Agidyne"], "Fusion Cards" : ["Fire Type 07"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 35, "MHP" : 4000, "HP" : 4000, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 08", "moves" : {"Fire Boost":0, "Agibarion":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Agibarion","Fire Boost"], "Fusion Cards" : ["Fire Type 08"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Sentinel", "LVL" : 40, "MHP" : 4500, "HP" : 4500, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Fire Type 09", "moves" : {"Burning Hell":0, "Fire Dance":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Burning Hell", "Fire Dance"], "Fusion Cards" : ["Fire Type 09"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Hi", "LVL" : 45, "MHP" : 30000, "HP" : 30000, "STR" : 100, "RES" : 10, "CRIT" : 20,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Prototype: BLZE", "moves" : {"Fire Boost":0,'Debilitate': 0, "Burning Hell" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Burning Hell", "Fire Dance"], "Fusion Cards" : ["Prototype: BLZE"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Water Elemental", "LVL" : 1, "MHP" : 500, "HP" : 500, "STR" : 100, "RES" : 10, "CRIT" : 2,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" :"Water Type 01", "moves" : {"Resist":0, "Bufu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Resist","Bufu"], "Fusion Cards" : ["Water Type 01"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 5, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Water Type 02", "moves" : {"Charge" : 0,"Megi":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Charge", "Megido"], "Fusion Cards" : ["Water Type 02"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 10, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Water Type 03", "moves" : {"Water Boost":0, "Rush":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Water Boost","Rush"], "Fusion Cards" : ["Water Type 03"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 15, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Water Type 04", "moves" : {"Bufula":0, "Resist":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Bufula","Resist"], "Fusion Cards" : ["Water Type 04"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 20, "MHP" : 2500, "HP" : 2500, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Water Type 05", "moves" : {"Megido":0, "Charge":0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Charge"], "Fusion Cards" : ["Water Type 05"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 25, "MHP" : 3000, "HP" : 3000, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Water Type 06", "moves" : {"Thalassic Calamity":0, "Concentrate":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["SPECIAL: Hyperflood Abrasion"], "Fusion Cards" : ["Water Type 06"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 30, "MHP" : 3500, "HP" : 3500, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,   "buff" : {}, "debuff" : {}, "fusion" : "Water Type 07", "moves" : {"Thalassic Calamity":0, "Inspire":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Thalassic Calamity","Inspire"], "Fusion Cards" : ["Water Type 07"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 35, "MHP" : 4000, "HP" : 4000, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Water Type 08", "moves" : {"Bufudyne":0, "Megidola":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Megidola","Bufudyne"], "Fusion Cards" : ["Water Type 08"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Sentinel", "LVL" : 40, "MHP" : 4500, "HP" : 4500, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0,  "buff" : {}, "debuff" : {}, "fusion" : "Water Type 09", "moves" : {"Bufubarion":0, "Water Boost":0,"Debilitate":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Debilitate","Bufubarion"], "Fusion Cards" : ["Water Type 09"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Mizu", "LVL" : 45, "MHP" : 30000, "HP" : 30000, "STR" : 100, "RES" : 10, "CRIT" : 20, "CRIT DMG" : 50, "Physical DMG" : 0, "Fire DMG" : 0, "Water DMG" : 0, "Wind DMG" : 0, "All DMG" : 0, "buff" : {}, "debuff" : {}, "fusion" : "Prototype: AQUA", "moves" : {"Water Boost":0, "Thalassic Calamity":0, "Bufubarion" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Thalassic Calamity","Bufubarion"], "Fusion Cards" : ["Prototype: AQUA"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"}
     ]

  if option == "all":
      return enemies
  elif option != "rng":
      for e in enemies:
          if option == e["name"]:
              return e
              break
      return None
  

  elements = ["Wind", "Water", "Fire"]
  element = random.choice(elements)
  #Average lvl of party
  lvl = 0
  for member in player_party:
      lvl += player_characters[member]["LVL"]
  lvl = int(lvl/len(player_party))

  myEnemy = {"LVL" : random.randint(lvl+5,lvl+10), "MHP" : 500}
  myEnemy["MHP"] += myEnemy["LVL"] * 125
  myEnemy["HP"] = myEnemy["MHP"]
  myEnemy["STR"] = 100
  myEnemy["RES"] = myEnemy["LVL"]
  if myEnemy["RES"] >= 50:
      myEnemy["RES"] = 50
  myEnemy["CRIT"] = 20
  myEnemy["CRIT DMG"] = 50
  myEnemy["Physical DMG"] = 0
  myEnemy["Fire DMG"] = 0
  myEnemy["Water DMG"] = 0
  myEnemy["Wind DMG"] = 0
  myEnemy["All DMG"] = 0
  myEnemy["buff"] = {}
  myEnemy["debuff"] = {}
  myEnemy["weakness"] = elements[elements.index(element)-1]
  
  #Fusion
  count = random.randint(1,10)
  fusion = ""
  if count == 10:
      if element == "Wind":
          fusion = "Prototype: GALE"
      elif element == "Fire":
          fusion = "Prototype: BLZE"
      elif element == "Water":
          fusion = "Prototype: AQUA"
  else:
      fusion = str(element) + " Type 0" + str(count)
  myEnemy["fusion"] = fusion

  #Name
  name = ""
  if myEnemy["LVL"] >= 45:
      if element == "Fire":
          myEnemy["name"] = "Hi"
      elif element == "Wind":
          myEnemy["name"] = "Kaze"
      elif element == "Water":
          myEnemy["name"] = "Mizu"
      myEnemy["MHP"] = 30000
      myEnemy["HP"] = myEnemy["MHP"]
  elif myEnemy["LVL"] >= 40:
      myEnemy["name"] = str(element) + " Sentinel"
  elif myEnemy["LVL"] >= 30:
      myEnemy["name"] = str(element) + " Guardian"
  elif myEnemy["LVL"] >= 15:
      myEnemy["name"] = str(element) + " Fighter"
  else:
      myEnemy["name"] = str(element) + " Elemental"

  #Moves
  moves = battle_moveslookup("all")
  myEnemy["moves"] = {}
  count = 0
  buffs = 0
  while count < 5:
      move = random.choice(list(moves))
      if moves[move][4] == element:
          myEnemy["moves"][move] = 0
          count += 1
      elif (moves[move][4] == "Buff" or moves[move][4] == "Debuff") and buffs < 1:
          myEnemy["moves"][move] = 0
          count += 1
          buffs += 1

  #Drops
  myEnemy["drops"] = {"EXP" : int(myEnemy["LVL"]*100), "Gold" : random.choice([1,2]), "Iron" : random.choice([10,30])}

  return myEnemy

def battle_weaponslookup(weapon):
    global img_weapon
    #Procedurally generated weapons
    all_weapons = {}
    bonuses = {
        "Strength" : {"stat" : "STR", "amount" : 20, "rarity" : "Common"},
        "Resistance" : {"stat" : "RES", "amount" : 5, "rarity" : "Common"},
        "Health" : {"stat" : "MHP", "amount" : 20, "rarity" : "Common"},
        "Focus" : {"stat" : "CRIT", "amount" : 8, "rarity" : "Rare"},
        "Hyper" : {"stat" : "CRIT DMG", "amount" : 16, "rarity" : "Rare"},
        "Physical" : {"stat" : "Physical DMG", "amount" : 20, "rarity" : "Rare"},
        "Fire" : {"stat" : "Fire DMG", "amount" : 15, "rarity" : "Rare"},
        "Water" : {"stat" : "Water DMG", "amount" : 15, "rarity" : "Rare"},
        "Wind" : {"stat" : "Wind DMG", "amount" : 15, "rarity" : "Rare"},
        "Star" : {"stat" : "All DMG", "amount" : 10, "rarity" : "Legend"}
        }
    types = ["Blade", "Bow", "Catalyst"]
    for wp_type in types:
        #Basic weapons
        all_weapons[wp_type] = {"type" : wp_type, "str" : 100, "stat" : "", "amount" : 0, "rarity" : "Common"}
        #All other weapons
        for bonus in bonuses:
            all_weapons[str(bonus) + " " + str(wp_type)] = {
                 "type" : wp_type,
                 "str" : 100,
                 "stat" : str(bonuses[bonus]["stat"]),
                 "amount" : bonuses[bonus]["amount"],
                 "rarity" : bonuses[bonus]["rarity"]}

    name = weapon
    if weapon in all_weapons: weapon = all_weapons[weapon]
    elif weapon == "all":   return all_weapons
    else:   return {"name" : name, "stat" : "???", "str" : 50, "amount" : 0, "desc" : "", "type" : ""}

    weapon["name"] = name
    weapon["desc"] = "STR: " + str(weapon["str"])
    if weapon["stat"] != "":    weapon["desc"] += ". Increases " + str(weapon["stat"]) + " by " + str(weapon["amount"])
    if weapon["stat"] == "MHP" or weapon["stat"] == "STR": weapon["desc"] += "%"
    weapon["desc"] += "."

    return weapon

def battle_charmslookup(request):
    #WIP
    #Set bonuses
    sets = {
        "Power Emblem" : {
            "2pc" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 30}],
            "4pc" : [{"Cond" : "HP 60% higher", "Stat" : "Physical DMG", "Num" : 30}]},
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
            "4pc" : [{"Cond" : "HP 60% higher", "Stat" : "Physical DMG", "Num" : 30}]}}

    #Generate [request amount] random charms
    if request != "":
        count = request
        charms = []
        stats = {"Physical DMG" : 10,
                 "Fire DMG" : 5,
                 "Water DMG" : 5,
                 "Wind DMG" : 5,
                 "All DMG" : 5,
                 "CRIT DMG" : 10,
                 "CRIT" : 5,
                 "MHP" : 10,
                 "ER" : 10,
                 "STR" : 10,
                 "RES" : 3,
                 "AGG" : 3}
        
        rarities = {"1" : "common", "2" : "rare", "3" : "legend"}

        while count > 0:
            stat = random.choice(list(stats))
            stat_num = stats[stat]
            rarity = random.randint(1,3)
            set_type = random.choice(["Power", "Fire", "Wind", "Water", "Star", "Focus", "Hyper", "Blaze", "Energy", "Strength", "Shield"])
            
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
    return int(multiplier+((multiplier*0.15)*lvl))

def battle_moveslookup(move, lvl=1):
  #Light, Weak, Medium, Heavy, Severe, Colossal
  #"Name : [BaseDMG, Range of hits, Type Offence/Defence/Heal, Buff/Debuff infliction, Element, Unique attribute]"

  #THESE NEED TO BE REWORKED
  all_moves = {
                  #Healing
                  "Diarama" : [20, [0,0], "Defence", "None","Heal",""]
                  #Physical
                  , "Attack" : [50, [1,0], "Offence", "None","Physical",""]
                  ,"Lunge" : [60, [1,0], "Offence", "None","Physical","High Critical rate"]
                  ,"Megi" : [80, [1,0], "Offence", "None","Physical",""]
                  ,"Megido" : [100, [1,0], "Offence", "None","Physical",""]
                  ,"Megidola" : [120, [1,0], "Offence", "None","Physical",""]
                  ,"SPECIAL: Shining Arrows" : [50, [8,0], "Offence", "None","Physical",""]
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
                  , "Charge" : [0, [0,0], "Defence", "Charged","Buff","Increases Physical DMG"]
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
  all_moves = {
      "Skip" : {"prop" : ["Defence"], "img" : "skip"},

      "Garudyne" : {"prop" : ["Offence", "Wind", "Basic"], "img" : "wind_1s", "dmg" : 100},
      "Cyclone": {"prop" : ["Offence", "Wind", "Skill"], "img" : "wind_mg", "dmg" : 240, "hits" : 8},
      "Eye of the Storm": {"prop" : ["Offence", "Wind", "SPECIAL"], "img" : "special", "dmg" : 432, "hits" : 8},
      "Bufudyne": {"prop" : ["Offence", "Water", "Basic"], "img" : "water_1s", "dmg" : 100},
      "Striking Tide": {"prop" : ["Offence", "Water", "Skill"], "img" : "water_mg", "dmg" : 24, "hits" : 10},
      "Thalassic Calamity": {"prop" : ["Offence", "Water", "SPECIAL"], "img" : "special", "dmg" : 43, "hits" : 10},
      "Agidyne": {"prop" : ["Offence", "Fire", "Basic"], "img" : "fire_1s", "dmg" : 100},
      "Fire Dance": {"prop" : ["Offence", "Fire", "Skill"], "img" : "fire_mg", "dmg" : 80, "hits" : 3},
      "Burning Hell": {"prop" : ["Offence", "Fire", "SPECIAL"], "img" : "special", "dmg" : 420}
  }
  all_moves_desc = { #s = Small desc. b = Big desc0
      "Skip" : {"s" : "End this turn", "b" : "End this turn"},

      "Garudyne" : {"s":"Deals medium Wind DMG", "b" : "Deals " + str(move_stats(all_moves["Garudyne"]["dmg"],lvl)) + "% Wind DMG to a single target enemy"},
      "Cyclone" : {"s":"Deals strong Wind DMG", "b" : "Deals " + str(move_stats(all_moves["Cyclone"]["dmg"],lvl)) + "% Wind DMG to a single target enemy across multiple hits"},
      "Eye of the Storm" : {"s":"Deals extreme Wind DMG", "b" : "Deals " + str(move_stats(all_moves["Eye of the Storm"]["dmg"],lvl)) + "% Wind DMG to a single target enemy across multiple hits"},

      "Bufudyne" : {"s":"Deals medium Water DMG", "b" : "Deals " + str(move_stats(all_moves["Bufudyne"]["dmg"],lvl)) + "% Water DMG to a single target enemy"},
      "Striking Tide" : {"s":"Deals strong Water DMG", "b" : "Deals " + str(move_stats(all_moves["Striking Tide"]["dmg"],lvl)) + "% Water DMG to a single target enemy across multiple hits"},
      "Thalassic Calamity" : {"s":"Deals extreme Water DMG", "b" : "Deals " + str(move_stats(all_moves["Thalassic Calamity"]["dmg"],lvl)) + "% Water DMG to a single target enemy across multiple hits"},

      "Agidyne" : {"s":"Deals medium Fire DMG", "b" : "Deals " + str(move_stats(all_moves["Agidyne"]["dmg"],lvl)) + "% Fire DMG to a single target enemy"},
      "Fire Dance" : {"s":"Deals strong Fire DMG", "b" : "Deals " + str(move_stats(all_moves["Fire Dance"]["dmg"],lvl)) + "% Fire DMG to a single target enemy across multiple hits"},
      "Burning Hell" : {"s":"Deals extreme Fire DMG", "b" : "Deals " + str(move_stats(all_moves["Burning Hell"]["dmg"],lvl)) + "% Fire DMG to a single target enemy"},
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
    return {"prop" : [],"img":"","desc":{"s" : "Switch character","b":"Switch character"},"dmg" : 0}

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
    
    if "bonuses" not in actor:  actor["bonuses"] = bonus_values
    if "bonuses" not in target: target["bonuses"] = bonus_values

    #Assign coords of actor and target
    if actor["name"] == player.stats["name"]:
        actor_x,actor_y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)
        target_x,target_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        bonus_values["ER"] = 0
    elif actor["name"] in player_party:
        actor_x,actor_y = party[actor["name"]]["button"].rect.x +200, party[actor["name"]]["button"].rect.y+50
        target_x,target_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        bonus_values["ER"] = 0
    else:
        actor_x,actor_y = random.randint(enemy.rect.x,enemy.rect.x+enemy.rect.width), random.randint(enemy.rect.y,enemy.rect.y+enemy.rect.height)
        target_x,target_y = random.randint(player.rect.x,player.rect.x+player.rect.width), random.randint(player.rect.y,player.rect.y+player.rect.height)


    #Add bonuses from charms and weapon
    if actor["name"] in battle_characters:
        for charm in player_characters[actor["name"]]["charms"]:
            charm_stats = player_charms[charm]
            if charm_stats["stat"] in bonus_values:
                bonus_values[str(charm_stats["stat"])] += charm_stats["amount"]
            
        weapon_stats = battle_weaponslookup(characters[actor["name"]]["weapon"])
        if weapon_stats["stat"] in bonus_values:
            bonus_values[str(weapon_stats["stat"])] += weapon_stats["amount"]

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
    if actor["name"] in battle_characters:
        bonus_values["STR"] = battle_weaponslookup(characters[actor["name"]]["weapon"])["str"] * (bonus_values["STR"]/100)
    else:
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

    print(bonus_values)
    return bonus_values
        
def get_buff(actor, target, buff):
    #Name,data,description
    output = [buff, {},"desc"]
    #buff is the Buff to search for and return the corrosponding value of in output variable
    buffs = {
        "Debilitate" : {"Type":"Offence", "Buff" : "Vulnerable", "Stat" : "RES", "Value" : -20},
        "Taunt" : {"Type":"Defence", "Buff" : "Taunt", "Stat" : "AGG", "Value" : 20},
        "Concentrate" : {"Type":"Defence", "Buff" : "Concentrated", "Stat" : "All DMG", "Value": 20},
        "Charge" : {"Type":"Defence", "Buff" : "Charged", "Stat" : "Physical DMG", "Value": 60},
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
            if buffs[i]["Stat"] == "CRIT DMG" or buffs[i]["Stat"] == "Physical DMG" or buffs[i]["Stat"] == "Fire DMG" or buffs[i]["Stat"] == "Water DMG" or buffs[i]["Stat"] == "Wind DMG" or buffs[i]["Stat"] == "All DMG":
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
    for ability in moves:
        print(ability)
        #Add the Button attribute to ability
        abilities[ability] = {
            "button" : button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), pygame.image.load("img/Other/"+ str(battle_moveslookup(ability)["img"]) + ".png").convert_alpha(), screen_mult(screen_width,70),screen_mult(screen_height,70))}
        #Used for spacing out abilities on screen
        x_value += screen_mult(screen_width,80)
    abilities["Skip"] = {"button" :button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), img_skip, screen_mult(screen_width,70),screen_mult(screen_height,70))}
    

    return abilities

def battle_createparty(members):
    global img_party
    party_images(members)
    #Creating buttons. Screen, width, height, image, size x, size y
    party = {}
    y_value = screen_height/(len(members)+1)
    size = screen_mult(screen_diag,100)
    for member in members:
        #Add the Button attribute to ability
        party[member] = {
            "button" : button.Button(display, screen_mult(screen_width,50), y_value, img_party[member]["icon"], size,size)}
        party[member]["hp"] = ProgressBar(party[member]["button"].rect.width,screen_mult(screen_height,5))
        party[member]["eg"] = ProgressBar(party[member]["button"].rect.width,screen_mult(screen_height,5))
        #Used for spacing out abilities on screen
        y_value += (screen_height/(len(members)+1))-(party[member]["button"].rect.height/2)

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

def battle_playerturn(player_turn, request):
    #Format of request = "move","weak","check"
    #Format of player_turn = [turn0,turn0,turn0,turn0]
    result = ""

    #Takes turn away
    if request == "move":
        count = 0
        for i in player_turn:
            if i != "turn0":
                break
            else:
                count += 1
        player_turn[count] = "turn0"
        result = player_turn

    #Replaces current turn with "1more"
    elif request == "weak":
        count = 0
        flag = False
        for i in player_turn:
            if i == "turn1":
                flag = True
                player_turn[count] = "turn2"
                break
            else:
                count += 1

        #If no regular turns found, remove "1more" turn
        if flag == False:
            player_turn = battle_playerturn(player_turn, "move")
            
        result = player_turn

    #Checks if its the player's turn, looking at the turn count
    elif request == "check":
        result = ("turn1" in player_turn or "turn2" in player_turn)

    #Restores turns
    elif request == "default":
        result = ["turn1","turn1","turn1","turn1"]

    return result

def battle_viewmember(member,background):
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
        
def char_stats(stat,lvl):
    return int(stat+((stat*0.1)*lvl))

def battle_system(player_party,enemy_stats):
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

    bg = "Battle_" + str(random.randint(1,4))

    #AGG target
    icon_target = pygame.transform.scale(pygame.image.load("img/Other/target.png"),(screen_mult(screen_width,30),screen_mult(screen_height,30))).convert_alpha()

    img_buffs = {
        "Vulnerable" : pygame.image.load("img/Other/buff_vulnerable.png").convert_alpha(),
        "Taunt" : pygame.image.load("img/Other/buff_taunt.png").convert_alpha(),
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
        "Physical DMG" : pygame.image.load("img/Other/icon_bonus_phys.png").convert_alpha(),
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
            "EG" : 0,
            "MEG" : 100,
            "AGG" : characters[member]["AGG"],
            "buff" : {},
            "debuff" : {},
        }
        newdict = {}
        for move in characters[member]["moves"]:
            newdict[move] = True
        battle_characters[member]["moves"] = newdict
    
    #Damage text
    damage_text_group = pygame.sprite.Group()
    #Projectiles
    projectile_group = pygame.sprite.Group()

    #Create invisible circle effect object
    inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2))

    #Create fighter classes
    player = Fighter(screen_width/4, int(screen_height/2),battle_characters[player_party[0]])
    enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)
    

    #Create progressbars. Arguements are width and height
    size_x, size_y = screen_mult(screen_width,100),screen_mult(screen_height,10)
    player_hp = ProgressBar(size_x,size_y)
    player_eg = ProgressBar(size_x,size_y)
    enemy_hp = ProgressBar(size_x,size_y)
    enemy_hp_old = ProgressBar(size_x,size_y)

    #Ability and Party buttons
    abilities = battle_createability(player.stats["moves"])
    party = battle_createparty(player_party)

    #Player Turn Count
    player_turn = ["turn1","turn1","turn1","turn1"]
    player_turnimg = {
        "turn0" : pygame.image.load("img/UI/turn0.png").convert_alpha(),
        "turn1" : pygame.image.load("img/UI/turn1.png").convert_alpha(),
        "turn2" : pygame.image.load("img/UI/turn2.png").convert_alpha()}

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
        battle_characters[member]["STR"] += battle_weaponslookup(characters[member]["weapon"])["str"]

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
        "turn_owner" : 0,
        }

    #Calculating total party MHP to determine music to play
    hp = 0
    for member in player_party:
        hp += battle_characters[member]["MHP"]
    battle_music(hp, enemy.stats["MHP"], "Start")
    
    #Running loop. 1 Loop = 1 Frame
    running = ""
    while running == "":
        #clock tick
        clock.tick(framesrate)

        #Change rainbow colour
        colour_rainbowcycle()

        #gets mouse position
        mouse_pos = pygame.mouse.get_pos()

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
        elif battle_action == "player" and selected != "":
            player.status = "ready"
        player.update()
        x,y = mouse_hovereffect(screen_width/4, int(screen_height/2)-int(player.rect.height/5),"circle")
        player.draw(x,y)

        #Add enemy shake
        if enemy_shake > 0:
            enemy_shake -= 1
            shake_x, shake_y = image_shake(int((battle_turndata["totaldmg"]/2000)*40))
        else:   shake_x, shake_y = 0,0
        if enemy.stats["HP"] > 0:
            enemy.update()
            x,y = mouse_hovereffect(screen_width-(screen_width/4),int(screen_height/2)-int(enemy.rect.height/5),"circle")
            enemy.draw(x+shake_x,y+shake_y)

        #Top and bottom borders for effect
            #Black
        size = screen_mult(screen_height,180)
        box3 = pygame.Rect(0, 0, screen_width, size)
        pygame.draw.rect(display, colour["black"], box3)
        box4 = pygame.Rect(0, screen_height-size, screen_width, size)
        pygame.draw.rect(display, colour["black"], box4)
        
        #Update coords for battle status display and main colours
        if battle_action == "player" or battle_action == "Victory!":
            x = player.rect.x
            y = player.rect.y
            if "SPECIAL" in selected:   myColour = colour["rainbowcycle"]
            else:   myColour = colour[player.stats["element"]]
        elif battle_action == "enemy" or battle_action == "Defeat!":
            x = enemy.rect.x
            y = enemy.rect.y
            myColour = colour["red"]
        elif battle_action == "neutral":
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
        x,y = mouse_hovereffect(x,y,"circle")
        #draw_text(str(battle_action).upper(), fonts["verylarge"], myColour, x, y-100, True)
        #display selected ability
        if selected != "":
            x,y = mouse_hovereffect(x,screen_height - (screen_height/4),"circle")
            draw_text(str(selected).upper(), fonts["large"], myColour, x, y + screen_mult(screen_height,80), True)
            draw_text(str(battle_moveslookup(selected)["desc"]["s"]).upper(), fonts["dmgsmall"], myColour, x, y + screen_mult(screen_height,170), True)
        
            
        #Combo metre. Also shakes
        if (combo["hits"] > 1 and player.status != "idle" and player.status != "hurt" and player.status != "dead") or (combo["hits"] > 1 and player.status == "idle" and battle_action == "player"):
            if combo_shake > 0:
                myColour = colour["red"]
                combo_shake -= 1
                shake_x, shake_y = image_shake(8)
            elif combo["hits"] > 20:
                myColour = colour["rainbowcycle"]
                shake_x, shake_y = image_shake(1)
            else:
                myColour = colour["white"]
                shake_x, shake_y = 0,0
            x, y = mouse_hovereffect(screen_width/3,screen_height/5,"circle")
            draw_text(str(combo["hits"]) + " HITS!", fonts["large"], myColour, x+shake_x, y+shake_y, True)
            draw_text(str(combo["dmg"]) + " TOTAL DMG", fonts["dmgsmall"], myColour, x-shake_x, y -shake_y+screen_mult(screen_height,90), True)
        

        #Player and enemy health bars
        battle_draw_health(player,player_hp, mouse_pos)
        battle_draw_health(enemy,enemy_hp, mouse_pos)

        #projectiles
        projectile_group.update()
        projectile_group.draw(display)

        #actions. [move, target]
        action = ["",""]
        
        

        if battle_action == "player":
            #ABILITY BUTTONS
            #For spacing between buttons
            x_value = -screen_mult(screen_width,120)
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
                x,y = mouse_hovereffect(player.x + x_value, screen_height - (screen_height/4),"circle")
                ability_clicked = abilities[move]["button"].draw(x,y,"") #(Returns True if button is pressed)
                x_value += screen_mult(screen_width,80)
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

        
                #If button pressed + Ability cooldown 0 + Player's turn = Can select and perform ability.
                if ability_clicked and selected != move:
                    if player.stats["moves"][move] == True:
                        myMixer("menu_text.wav",0)
                        selected = str(move)
                        break
                    else:
                        myMixer("menu_invalid.wav",0)
                        screen_shake = framesrate/10
                #If ability already selected and they click button again, perform ability on self/enemy. DOES NOT INCLUDE SWITCH AND SKIP
                elif ability_clicked and selected == move:
                    if player.stats["moves"][move] == True:
                        myMixer("menu_enter.wav",0)

                        actiontype = battle_moveslookup(selected)["prop"]
                        the_elements = ["Fire", "Water", "Wind", "Physical", "Singularity", "Debuff", "Buff", "Heal"]
                        for e in the_elements:
                            if e in actiontype:
                                actiontype = e
                                break

                        if "Fire" in battle_moveslookup(selected)["prop"] or "Water" in battle_moveslookup(selected)["prop"] or "Wind" in battle_moveslookup(selected)["prop"] or "Singularity" in battle_moveslookup(selected)["prop"] or "debuff" in battle_moveslookup(selected)["prop"]:
                            action = [selected,enemy.stats]
                        elif "Heal" in battle_moveslookup(selected)["prop"] or "Buff" in battle_moveslookup(selected)["prop"]:
                            action = [selected,player.stats]
                        break
                    else:
                        myMixer("menu_invalid.wav",0)
                        screen_shake = framesrate/10

                #Draw outline over selected ability
                if move == selected and battle_action == "player":
                    if special:   myColour = colour["rainbowcycle"]
                    else:   myColour = colour[player.stats["element"]]
                    pygame.draw.circle(display, myColour, (abilities[move]["button"].rect.center[0]-1, abilities[move]["button"].rect.center[1]-1),abilities[move]["button"].rect.width/2, 5)
                    draw_text("READY", fonts["small"], colour["grey"], abilities[move]["button"].rect.topleft[0]+screen_mult(screen_width,3), abilities[move]["button"].rect.center[1]-screen_mult(screen_height,10)+2, False)
                    draw_text("READY", fonts["small"], myColour, abilities[move]["button"].rect.topleft[0]+screen_mult(screen_width,3), abilities[move]["button"].rect.center[1]-screen_mult(screen_height,10), False)


            #Display skip button at the end
            x,y = mouse_hovereffect(player.x + x_value, screen_height - (screen_height/4),"circle")
            skip_clicked = abilities["Skip"]["button"].draw(x,y,"")
            if skip_clicked:
                myMixer("menu_back.wav",0)              
                selected = "Skip"
            #Display desc if hovering over Skip button
            if abilities["Skip"]["button"].hover() and selected == "" and battle_action == "player":
                    draw_text("Skip turn", fonts["small"], colour["green"], abilities["Skip"]["button"].rect.x, abilities["Skip"]["button"].rect.y + abilities["Skip"]["button"].rect.width, True)
            x_value += screen_mult(screen_width,80)

            #TURN COUNT
            x,y = mouse_hovereffect(screen_mult(screen_width,500), screen_mult(screen_height,225),"circle")
            spacing = screen_mult(screen_width,45)
            draw_text("TURN COUNT", fonts["franksmall"], colour["Fire"], x-(spacing*3), y - screen_mult(screen_height,25), False)
            for turn in player_turn:
                display.blit(player_turnimg[turn],(x,y))
                x -= spacing


            #PARTY MEMBER BUTTONS
            y_value = screen_height/(len(party)+1)
            highest_agg = player_party[0]
            for member in player_party:
                if battle_characters[member]["AGG"] > battle_characters[highest_agg]["AGG"]:
                    highest_agg = member
            for member in player_party:
                #Establish x and y
                x,y = mouse_hovereffect(screen_mult(screen_width,50), y_value,"circle")
                if member == player.stats["name"]:  x += screen_mult(screen_width,20)
                elif party[member]["button"].hover() and battle_characters[member]["HP"] > 0:   x+= screen_mult(screen_width,20)
                #Grey box background
                pygame.draw.rect(display, colour["grey"], (party[member]["button"].rect.x-1, party[member]["button"].rect.y-1, party[member]["button"].rect.width+1, party[member]["button"].rect.height+1))

                #HP and EG bars
                spacing = screen_mult(screen_height,15)
                party[member]["hp"].draw(x,y+party[member]["button"].rect.height+screen_mult(screen_height,6),battle_characters[member]["HP"],battle_characters[member]["MHP"]+battle_characters[member]["bonuses"]["MHP"],mouse_pos,"green")
                if battle_characters[member]["EG"] == battle_characters[member]["MEG"]:   party[member]["eg"].draw(x,y+party[member]["button"].rect.height+spacing,battle_characters[member]["EG"],battle_characters[member]["MEG"],mouse_pos,"rainbowcycle")
                else:   party[member]["eg"].draw(x,y+party[member]["button"].rect.height+spacing,battle_characters[member]["EG"],battle_characters[member]["MEG"],mouse_pos,battle_characters[member]["element"])

                
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
                member_clicked = party[member]["button"].draw(x,y,icon) #(Returns True if button is pressed)
                y_value += (screen_height/(len(party)+1))-(party[member]["button"].rect.height/2)

                #Draw outline over the icon
                pygame.draw.rect(display, myColour, (party[member]["button"].rect.x-1, party[member]["button"].rect.y-1, party[member]["button"].rect.width+1, party[member]["button"].rect.height+1), 4)

                #UNUSED
                #battle_viewmember(battle_characters[player_party[0]],display)

                if member_clicked and selected == "":
                    if battle_characters[member]["HP"] > 0 and cooldown <= 0 and member != player.stats["name"]:
                        selected = member
                    elif cooldown <= 0:
                        myMixer("menu_invalid.wav",0)
                        screen_shake = framesrate/10
                elif member_clicked and selected != "" and ("Heal" in battle_moveslookup(selected) or "Buff" in battle_moveslookup(selected)):
                    action = [selected, battle_characters[member]]
                elif party[member]["button"].hover():
                    x,y = mouse_hovereffect(party[member]["button"].rect.x+party[member]["button"].rect.width+screen_mult(screen_width,30),party[member]["button"].rect.y,"circle")
                    battle_draw_stats(battle_characters[member],x,y,myColour)
                elif member == highest_agg:
                    display.blit(icon_target,(party[member]["button"].rect.x+party[member]["button"].rect.width + screen_mult(screen_width,10),party[member]["button"].rect.y))


            #Display fusion and buffs/debuffs if hovering over Character
            if player.rect.collidepoint(mouse_pos) and selected == "":
                pygame.mouse.set_visible(False)
                draw_text(str(player.stats["fusion"].upper()) + " # " + get_fusion(player.stats["fusion"])[1], fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
            elif enemy.rect.collidepoint(mouse_pos) and selected == "":
                pygame.mouse.set_visible(False)
                draw_text(str(enemy.stats["fusion"].upper()) + " # " + str(get_fusion(enemy.stats["fusion"])[1]), fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
            else:
               pygame.mouse.set_visible(True)
                
            #SWITCH AND SKIP FUNCTION
            if selected == "Skip":
                action = [selected,player.stats]
            elif selected in player_party:
                action = [selected,battle_characters[selected]]

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


        #cooldown makes turns not instant/1 frame long
        cooldown -= 1
        if cooldown <= 0:
            #Allows combatents to perform actions
            if battle_action == "player" and player.stats["HP"] > 0 and action[0] != "":
                #Set variables
                battle_action = "neutral"
                player.status = "move"

                #Perform move
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
                
                #Increases cooldown if action completed
                if "SPECIAL" not in action[0] and action[0] not in player_party:
                    if action[0] in player.stats["moves"]:
                        player.stats["moves"][action[0]] = False
                    if battle_turndata["weakamount"] > 0:
                        player_turn = battle_playerturn(player_turn,"weak")
                    elif action[0] == "Skip":
                        player_turn = ["turn0","turn0","turn0","turn0"]
                    else:
                        player_turn = battle_playerturn(player_turn,"move")
                
                #Hitting opponent changes their pose + starts/adds to combo
                if battle_turndata["hit"] > 0:
                    enemy_shake = framesrate/10
                    if int((battle_turndata["totaldmg"]/battle_turndata["target"]["MHP"])*100) >= 5:
                        enemy.status = "hurt"
                    combo_shake = framesrate/10
                    combo["hits"] += battle_turndata["hit"]
                    combo["dmg"] += battle_turndata["totaldmg"]

                #Neutral cooldown
                cooldown = framesrate
                
            elif battle_action == "enemy" and enemy.stats["HP"] > 0:
                #Increases cooldown if action completed
                if selected != "Skip":   enemy.stats["moves"][selected] = False
                #Set variables
                enemy.status = "move"
                battle_action = "neutral"

                if "Offence" in battle_moveslookup(selected)["prop"]:
                    #Targets random alive party member
                    action[0] = selected
                    while True:
                        action[1] = battle_characters[random.choice(player_party)]
                        if action[1]["HP"] > 0:
                            break

                    #Changes target to party member with the highest Aggro. 10% chance to ignore this rule.
                    if random.randint(1,10) != 1:
                        for member in player_party:
                            if battle_characters[member]["HP"] > 0:
                                if member != player.stats["name"]:
                                    if battle_characters[member]["AGG"]+battle_characters[member]["bonuses"]["AGG"] > action[1]["AGG"]+action[1]["bonuses"]["AGG"]:
                                        action[1] = battle_characters[member]
                                else:
                                    if player.stats["AGG"]+player.stats["bonuses"]["AGG"] > action[1]["AGG"]+action[1]["bonuses"]["AGG"]:
                                        action[1] = player.stats
                        
                    if action[1]["name"] == player.stats["name"]:
                        battle_turndata,player.stats = enemy.move(action[0], action[1],player_party)
                    else:
                        battle_turndata,battle_characters[action[1]["name"]] = enemy.move(action[0], action[1],player_party)
                else:
                    action = [selected,enemy.stats]
                    battle_turndata,enemy.stats = enemy.move(action[0], action[1],player_party)
                    


                #Changing combatent condition based on HP
                if player.stats["HP"] <= 0:
                    player.condition = "Defeated"
                    player.status = "dead"
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

                #Restores player turns
                if battle_turndata["weakamount"] <= 0:
                    player_turn = battle_playerturn(player_turn,"default")
                    
                cooldown = framesrate
            
                
            elif battle_action == "neutral":
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
                    battle_music(hp, enemy.stats["MHP"], "End")

                if end != "":
                    battle_action = end
                    if end == "Defeat!":
                        player.status = "dead"
                    elif end == "Victory!":
                        player.status = "turn"
                    battle_music(hp, enemy.stats["MHP"], "End")
                    battle_action = end

                    
                #Player turn
                elif (battle_playerturn(player_turn,"check") == True):
                    #Removes enemy move CD
                    enemy.stats["moves"] = battle_movecd(enemy.stats["moves"])

                    if battle_turndata["actor"].stats["name"] == enemy.stats["name"]:
                        player.stats["buff"] = battle_removebuffs(player.stats["buff"])
                        player.stats["debuff"] = battle_removebuffs(player.stats["debuff"])
                        
                    if battle_turndata["critamount"] > 0:
                        myMixer("menu_1more.wav",0)
                    else:
                        myMixer("menu_turn.wav",0)
                    player.status = "turn"
                    enemy.status = "idle"
                    battle_action = "player"
                #Enemy turn
                elif (battle_playerturn(player_turn,"check") == False):
                    #Removes Player move CD
                    for member in player_party:
                        if player.stats["name"] != member:
                            battle_characters[member]["moves"] = battle_movecd(battle_characters[member]["moves"])
                        else:
                            player.stats["moves"] = battle_movecd(player.stats["moves"])
                    if battle_turndata["actor"].stats["name"] in player_party:
                        enemy.stats["buff"] = battle_removebuffs(enemy.stats["buff"])
                        enemy.stats["debuff"] = battle_removebuffs(enemy.stats["debuff"])
                    
                    player.status = "idle"
                    enemy.status = "turn"
                    battle_action = "enemy"
                    combo = {"hits" : 0, "dmg" : 0}
                    
                selected = ""
                cooldown = framesrate
     


        #For events happening in the pygame
        for event in pygame.event.get():
            #If window X clicked
            if event.type == pygame.QUIT:
                terminate()

            #If left mouse button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cooldown = 0
                #Right mouse button
                if event.button == 3 and battle_action == "player" and selected != "":
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
            running = battle_action

    del img_buffs
    del img_bonus

    return running

def levelup_draw_stats(name,stats, x,y):
    #"stats" means the old stats before level up
    message = ""
    message_bonus = ""
    for info in stats:

        #Stats before level up
        if info == "STR":
            message += str(info) + ": " + str(battle_weaponslookup(characters[name]["weapon"])["str"]+stats[info]) + " # "
        else:
            message += str(info) + ": " + str(stats[info]) + " # "

        #Stat increases
        if char_stats(characters[name][info],player_characters[name]["LVL"]) != stats[info]:
            message_bonus += " +" + str(int(char_stats(characters[name][info],player_characters[name]["LVL"])-stats[info])) + "! # "
        else:
            message_bonus += " # "

    #Darker text behind main
    #Dark
    draw_text(str(message), fonts["franksmall"], colour["grey"], x+1, y+1, False)
    draw_text(str(message_bonus), fonts["franksmall"], colour["grey"], x+screen_mult(screen_width,200)+1, y+1, False)
    #Main
    draw_text(str(message), fonts["franksmall"], colour["white"], x, y, False)
    draw_text(str(message_bonus), fonts["franksmall"], colour["Singularity"], x+screen_mult(screen_width,200), y, False)

def menu_levelup(name, exp,message):
  global player_characters
  global characters
  global BASE_MEXP
  baseexp = exp
  stats = {
      "MHP" : char_stats(characters[name]["MHP"],player_characters[name]["LVL"]),
      "STR" : char_stats(characters[name]["STR"],player_characters[name]["LVL"]),
      "RES" : char_stats(characters[name]["RES"],player_characters[name]["LVL"]),
      "CRIT" : char_stats(characters[name]["CRIT"],player_characters[name]["LVL"]),
      "CRIT DMG" : char_stats(characters[name]["CRIT DMG"],player_characters[name]["LVL"])
      }

  if player_characters[name]["LVL"] >= 40:
      exp = 0


  exp_bar = ProgressBar(screen_mult(screen_width,200),screen_mult(screen_height,15))
  #Size of continue button
  size = screen_mult(screen_diag,100)
  button_continue = button.Button(display, screen_width-size-screen_mult(screen_width,50), screen_height-size-screen_mult(screen_height,50), img_skip, size,size)
  levelup_bar = pygame.transform.scale(pygame.image.load("img/UI/levelup_bar.png"),(screen_mult(screen_width,900),screen_mult(screen_height,110))).convert_alpha()
  levelup_box = pygame.transform.scale(pygame.image.load("img/UI/levelup_box.png"),(screen_mult(screen_width,410),screen_mult(screen_height,650))).convert_alpha()
  portrait = pygame.image.load("img/Char/" + str(name) + "/portrait.png").convert_alpha()
  rect = portrait.get_rect()
  scale =0.8
  portrait = pygame.transform.scale(portrait, (screen_mult(screen_width,rect.width*scale),screen_mult(screen_height,rect.height*scale)))
    
  #Character shake effect
  shake = 0
  skip = False
  #spd is the % of exp to add per frame
  spd = 0.04

  running = ""
  cooldown = 0
  while running == "":
    cooldown -= 1
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
            
    #gets mouse position
    mouse_pos = pygame.mouse.get_pos()
    #Display images
    draw_background("Levelup","mouse")

    #Top and bottom borders for effect
        #Black
    box_size = screen_mult(screen_height,180)
    box1 = pygame.Rect(0, 0, screen_width, box_size)
    pygame.draw.rect(display, colour["black"], box1)
    box2 = pygame.Rect(0, screen_height-box_size, screen_width, box_size)
    pygame.draw.rect(display, colour["black"], box2)

    #Level up bar
    x,y = mouse_hovereffect(0,screen_height/2-screen_mult(screen_height,100),"mouse")
    display.blit(levelup_bar,(x,y))
    draw_text(str(message).upper(), fonts["large"], colour["white"], x+screen_mult(screen_width,300), y+screen_mult(screen_height,10), False)

    #Character image
    if shake > 0:
        shake -= 1
        shake_x,shake_y = image_shake(2)
    else:
        shake = 0
        shake_x,shake_y = 0,0
    x,y = mouse_hovereffect(screen_mult(screen_width,1500)-portrait.get_rect().width/2,screen_mult(screen_height,50),"mouse")
    display.blit(portrait,(x+shake_x,y+shake_y))

    #Level up box
    x,y = mouse_hovereffect(screen_width/2.5,screen_mult(screen_height,170),"mouse")
    display.blit(levelup_box,(x,y))
    #Name on box
    draw_text(name.upper(), fonts["dmgsmall"], colour["grey"], x+screen_mult(screen_width,160)+1, y+screen_mult(screen_height,80)+1, False)
    draw_text(name.upper(), fonts["dmgsmall"], colour[characters[name]["element"]], x+screen_mult(screen_width,160), y+screen_mult(screen_height,80), False)
    #EXP bar under name on box
    exp_bar.draw(x+screen_mult(screen_width,110),y+screen_mult(screen_height,125),player_characters[name]["EXP"],char_stats(BASE_MEXP,player_characters[name]["LVL"]),mouse_pos,characters[name]["element"])
    draw_text("LVL" + str(player_characters[name]["LVL"]) + " • " + str(player_characters[name]["EXP"]) + "/" + str(char_stats(BASE_MEXP,player_characters[name]["LVL"])) + "EXP", fonts["small"], colour["grey"], x+screen_mult(screen_width,140), y+screen_mult(screen_height,125)+exp_bar.height, False)
    #Stats on box
    levelup_draw_stats(name,stats,x+screen_mult(screen_width,50),y+screen_mult(screen_height,190))
    
    if exp > 0 and player_characters[name]["LVL"] < 40:
        
        #Add exp
        if exp > (int(baseexp * spd)):
            #earning exp
            player_characters[name]["EXP"] += int(baseexp * spd)
            exp -= int(baseexp * spd)
            myMixer("exp.wav",0)
        else:
            player_characters[name]["EXP"] += exp
            exp = 0
            myMixer("exp_final.wav",0)

        if player_characters[name]["EXP"] >= char_stats(BASE_MEXP,player_characters[name]["LVL"]):
            #level up!
            #myMixer("menu_1more.wav",0)
            player_characters[name]["EXP"] = 0
            player_characters[name]["LVL"] += 1
            shake = framesrate/20

            if player_characters[name]["LVL"] >= 40:
                player_characters[name]["EXP"] = char_stats(BASE_MEXP,40)
                exp = 0

            #bonuses["MHP"] += 25
            #for i in range(int(len(rates)/2)):
            #    rng = random.randint(1,100)
            #    for stat in rates:
            #        if rng > rates[stat]:
            #            rng = stat
            #            break
                    
            #    bonuses[rng] += 2
            
            player_characters[name]["HP"] = char_stats(characters[name]["MHP"],player_characters[name]["LVL"])


    #EXP earned
    draw_text("Earned +" + str(exp) + " EXP", fonts["dmgsmall"], colour["white"], x+screen_mult(screen_width,100)+1, y+screen_mult(screen_height,400)+1, False)
    draw_text("Earned +" + str(exp) + " EXP", fonts["dmgsmall"], colour["grey"], x+screen_mult(screen_width,100), y+screen_mult(screen_height,400), False)

    #Continue button
    x,y = mouse_hovereffect(screen_width-size-screen_mult(screen_width,50), screen_height-size-screen_mult(screen_height,50),"mouse")
    if exp == 0:
        if button_continue.draw(x,y,img_skip):
            running = "continue"
        elif button_continue.hover():
            pygame.draw.rect(display, colour["white"], (x-1, y-1, size+1, size+1), 5)
        

    screen.blit(display,(0,0))
    pygame.display.update()

    #clock tick
    clock.tick(framesrate)

  myMixer("menu_enter.wav",0)


def battle_startend(player_party):
    global player_characters
    global difficulty
    #Choose enemy
    enemy_stats = random.choice(get_enemies("all"))

    #Adjust to difficulty
    modes = {"Normal" : 1, "Hard" : 1.5,"Maddening" : 2}
    enemy_stats["MHP"] = int(enemy_stats["MHP"]*modes[difficulty])
    enemy_stats["HP"] = enemy_stats["MHP"]
    enemy_stats["STR"] = int(enemy_stats["STR"]*modes[difficulty])
    enemy_stats["RES"] = int(enemy_stats["RES"]*modes[difficulty])
    enemy_stats["CRIT"] = int(enemy_stats["CRIT"]*modes[difficulty])
    enemy_stats["drops"]["EXP"] = int(enemy_stats["drops"]["EXP"]*(modes[difficulty]+0.1))
    enemy_stats["drops"]["Gold"] = int(1*(modes[difficulty]+0.1))
    enemy_stats["drops"]["Iron"] = int(10*(modes[difficulty]+0.1))
    enemy_stats["moves"] = {"Agidyne" : 1}

    #Initiate battle
    result = battle_system(player_party,enemy_stats)

    #Reformatting stats after battle
    for member in player_party:
        #Remove bonuses element
        #if "bonuses" in player_characters[member]:  player_characters[member].pop("bonuses")

        #Cut gained Energy in half
        #if player_characters[member]["EG"] > 2: player_characters[member]["EG"] = int(player_characters[member]["EG"]/2)

        #Remove cooldowns on moves
        #newlist = []
        #for move in player_characters[member]["moves"]:
        #    player_characters[member]["moves"][move] = 0
        #    newlist.append(move)
        #player_characters[member]["moves"] = newlist

        #Remove buffs and debuffs
        #player_characters[member]["buff"] = {}
        #player_characters[member]["debuff"] = {}
        #Fix current HP
        if player_characters[member]["HP"] <= 0:
            player_characters[member]["HP"] = char_stats(characters[member]["MHP"],player_characters[member]["LVL"])
        elif player_characters[member]["HP"] > char_stats(characters[member]["MHP"],player_characters[member]["LVL"]):
            player_characters[member]["HP"] = char_stats(characters[member]["MHP"],player_characters[member]["LVL"])
        #Bring STR back down to 0
        #player_characters[member]["STR"] -= battle_weaponslookup(player_characters[member]["weapon"])["str"]

    #All members earn exp if win
    if result == "Victory!":
        player_inventory["Wins"] += 1
        player_inventory["Gold"] += enemy_stats["drops"]["Gold"]
        player_inventory["Iron"] += enemy_stats["drops"]["Iron"]
        for member in player_party:
            menu_levelup(member, int(enemy_stats["drops"]["EXP"]/len(player_party)), "Victory!")

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
        "Physical DMG" : "Damage bonus gained from Physical hits",
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
        if stat == "STR":   value += battle_weaponslookup(characters[member]["weapon"])["str"]
        bonus = 0

        #Adds onto base value using charms, weapon and fusion
        for charm in player_characters[member]["charms"]:
            if player_charms[charm]["stat"] == stat:
                bonus += player_charms[charm]["amount"]
                
        if battle_weaponslookup(characters[member]["weapon"])["stat"] == stat:
            bonus += battle_weaponslookup(characters[member]["weapon"])["amount"]
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
        if member in player_party:
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
    global player_weapons
    global player_charms
    
    button_width, button_height = screen_mult(screen_width,100),screen_mult(screen_height,100)

    if option == "weapon":
        weapon_stats = battle_weaponslookup(characters[character]["weapon"])
        x, y = screen_mult(screen_width,30), screen_height/2 - button_height
        button_wp_eq = {
            "button" : button.Button(display,x,y,img_weapon[weapon_stats["type"]][weapon_stats["rarity"]],button_width,button_height)     ,
            "stats" : weapon_stats,
            "desc" : str(characters[character]["weapon"]).upper() + " # # " + str(weapon_stats["desc"])}
        button_wp_all = {}

        return button_wp_eq, button_wp_all
    
    elif option == "moves":
        moves_allowed = 4
        button_mv_eq = {}        
        button_mv_all = {}
        #button.Button(display,x,y,img_weapon[characters[character]["weapon"]["name"]],button_width,button_height)

        #Equipped moves
        x, y_value = screen_mult(screen_width,30), screen_height/(moves_allowed+1)
        for move in characters[character]["moves"]:
            move_stats = battle_moveslookup(move)
            print(move_stats)
            button_mv_eq[move] = {
                "button" : button.Button(display,x,y_value,pygame.image.load("img/Other/" + str(move_stats["img"]) + ".png").convert_alpha(),button_width,button_height),
                "stats" : move_stats}

            y_value += (screen_height/(moves_allowed+1)) - button_height/2


        return button_mv_eq, button_mv_all

    elif option == "charms":
        charms_allowed = 4
        button_ch_eq = {}        
        button_ch_all = {}
        #button.Button(display,x,y,img_weapon[characters[character]["weapon"]["name"]],button_width,button_height)

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
    global player_weapons
    global inviscircle

    base_message = message
    button_party, button_char, button_back, offset = menu_party_buttons()
    max_partysize = 4

    #Black box
    black_box_alpha = 255
    black_box = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA) #SRCALPHA enables transparency

    #Exclaimation mark
    exclaim = pygame.transform.scale(pygame.image.load("img/UI/exclaim.png").convert_alpha(),(20,30))

    #Equipment buttons
    y_value = 0
    x,y = screen_width/2 + screen_mult(screen_width,200), screen_height-(screen_height/4)-screen_mult(screen_height,10)
    button_width, button_height = screen_mult(screen_width,210),screen_mult(screen_height,50)
    options = ["weapon","moves","charms","fusion"]
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
                    
        elif menu == "weapon" and selected != "":
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
            
        elif menu == "fusion":
            print("")

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
                    if equip == "weapon":
                        desc = str(characters[selected]["weapon"]).upper() + " # # " + str(battle_weaponslookup(characters[selected]["weapon"])["desc"])
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
        #player_characters={'Alm': {'name': 'Alm', 'weapon': 'Wind Bow', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Wind Type 08', 'moves': ['Attack', 'Cyclone', 'Garudyne', 'SPECIAL: Eye of the Storm', 'Focus', 'Dia'], 'weakness': 'Fire'}, 'Dimitri': {'name': 'Dimitri', 'weapon': 'Hyper Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Water Type 08', 'moves': ['Attack', 'Overgrow', 'Awaken II', 'Charge', 'Dia', 'Diarama'], 'weakness': 'Wind'}, 'Lilina': {'name': 'Lilina', 'weapon': 'Catalyst', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Fire Type 08', 'moves': ['Attack', 'Agidyne', 'Fire Dance', 'SPECIAL: Cataclysm', 'Concentrate', 'Dia'], 'weakness': 'Water'}, 'Byleth': {'name': 'Byleth', 'weapon': 'Catalyst', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Wind Type 09', 'moves': ['Attack', 'Cyclone', 'Garubarion', 'SPECIAL: Eye of the Storm', 'Overhype', 'Dia'], 'weakness': 'Fire'}, 'Hilda': {'name': 'Hilda', 'weapon': 'Blade', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Fire Type 09', 'moves': ['Attack', 'Fire Dance', 'Agibarion', 'SPECIAL: Cataclysm', 'Dia'], 'weakness': 'Water'}, 'Lucina': {'name': 'Lucina', 'weapon': 'Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Water Type 09', 'moves': ['Attack', 'Striking Tide', 'Bufubarion', 'SPECIAL: Hyperflood Abrasion', 'Debilitate', 'Dia'], 'weakness': 'Wind'}, 'Morgan': {'name': 'Morgan', 'weapon': 'Resistance Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Prototype: AQUA', 'moves': ['Attack', 'Thalassic Calamity', 'Striking Tide', 'SPECIAL: Hyperflood Abrasion', 'Water Boost', 'Dia'], 'weakness': 'Wind'}, 'Claude': {'name': 'Claude', 'weapon': 'Bow', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Fire Type 07', 'moves': ['Attack', 'Agibarion', 'Fire Dance', 'SPECIAL: Cataclysm', 'Fire Boost', 'Dia'], 'weakness': 'Water'}, 'Ninian': {'name': 'Ninian', 'weapon': 'Focus Catalyst', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Prototype: GALE', 'moves': ['Attack', 'Garubarion', 'Wrath Tempest', 'SPECIAL: Eye of the Storm', 'Concentrate', 'Wind Boost', 'Dia'], 'weakness': 'Fire'}, 'Shez': {'name': 'Shez', 'weapon': 'Health Blade', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Prototype: BLZE', 'moves': ['Attack', 'Burning Hell', 'Fire Dance', 'SPECIAL: Cataclysm', 'Dia', 'Pyroclastic Charge'], 'weakness': 'Water'}, 'Anna': {'name': 'Anna', 'weapon': 'Bow', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Fire Type 06', 'moves': ['Attack', 'Agidyne', 'Concentrate', 'SPECIAL: Cataclysm'], 'weakness': 'Water'}, 'Knight': {'name': 'Knight', 'weapon': 'Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Water Type 07', 'moves': ['Attack', 'Bufudyne', 'SPECIAL: Hyperflood Abrasion'], 'weakness': 'Wind'}, 'Kris': {'name': 'Kris', 'weapon': 'Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Water Type 06', 'moves': ['Attack', 'Bufudyne', 'Rush', 'SPECIAL: Hyperflood Abrasion', 'Water Boost'], 'weakness': 'Wind'}, 'Lyn': {'name': 'Lyn', 'weapon': 'Blade', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Wind Type 07', 'moves': ['Attack', 'Garudyne', 'Wrath Tempest', 'SPECIAL: Eye of the Storm', 'Overhype'], 'weakness': 'Fire'}, 'Mia': {'name': 'Mia', 'weapon': 'Blade', 'element': 'Fire', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Fire Type 05', 'moves': ['Attack', 'Agilao', 'Agi', 'SPECIAL: Cataclysm', 'Fire Boost', 'Concentrate'], 'weakness': 'Water'}, 'Reginn': {'name': 'Reginn', 'weapon': 'Blade', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Wind Type 06', 'moves': ['Attack', 'Garudyne', 'Cyclone', 'SPECIAL: Eye of the Storm', 'Wind Boost', 'Concentrate'], 'weakness': 'Fire'}, 'Seliph': {'name': 'Seliph', 'weapon': 'Blade', 'element': 'Water', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Water Type 05', 'moves': ['Attack', 'Megido', 'Thousand Slaps', 'SPECIAL: Shining Arrows', 'Charge', 'Debilitate'], 'weakness': 'Wind'}, 'Sothe': {'name': 'Sothe', 'weapon': 'Blade', 'element': 'Wind', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Wind Type 05', 'moves': ['Attack', 'Garula', 'Garu', 'SPECIAL: Eye of the Storm', 'Wind Boost', 'Concentrate'], 'weakness': 'Fire'}, 'Alear': {'name': 'Alear', 'weapon': 'Star Blade', 'element': 'Singularity', 'LVL': 1, 'MEXP': 500, 'EXP': 0, 'MHP': 500, 'HP': 500, 'STR': 0, 'RES': 0, 'CRIT': 5, 'CRIT DMG': 50, 'ER': 100, 'EG': 0, 'MEG': 100, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0, 'buff': {}, 'debuff': {}, 'charms': [], 'fusion': 'Prototype: STAR', 'moves': ['Attack', 'Cyclone', 'Burning Hell', 'Striking Tide', 'SPECIAL: Tenman Crescent Moon', 'Concentrate'], 'weakness': 'None'}}
        
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
            player_characters[member]["Physical DMG"] = 0
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
##            player_characters[member]["weapon"] = player_characters[member]["weapon"]["name"]
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
    base_res = [1920,1080]
    
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

    base_message = message
    exp_cost = 3

    #Black box
    black_box_alpha = 255
    black_box = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA) #SRCALPHA enables transparency
    
    #Available options
    options = {
        "Fight" : {"desc" : "Start a battle!"},
        "Train" : {"desc" : "Earn EXP (Cost: " + str(exp_cost) + " GOLD)"},
        "Party" : {"desc" : "Organise party"},
        "Save" : {"desc" : "Save the game"},
        "Options" : {"desc" : "Change preferences"},
        "Quit" : {"desc" : "Leave the game"}}

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
    money_iron = pygame.transform.scale(pygame.image.load("img/UI/iron.png"),(money_size,money_size))

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
        draw_text("by Navee", fonts["dmgsmall"], colour["grey"], x+screen_mult(screen_width,1110)+2, y+screen_mult(screen_height,75)+2, False)
        draw_text("WHIMS OF FATE", fonts["title"], colour["menu"], x, y, False)
        draw_text("by Navee", fonts["dmgsmall"], colour["menu"], x+screen_mult(screen_width,1110), y+screen_mult(screen_width,75), False)
    

        #Display buttons
        y_value = screen_height/(len(options)+1)+button_height/1.5
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
                if option == "Save":    message = "Saving..."
                elif option == "Fight":    message = "Prepare for Battle!"
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
        display.blit(money_iron,(x+screen_mult(screen_width,200),y+screen_mult(screen_height,5)))
        draw_text(str(player_inventory["Iron"]), fonts["small"], colour["Physical"], x+screen_mult(screen_width,240),y+screen_mult(screen_height,12), True)
        
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
        myMixer("battle_start.wav",0)
        pygame.mixer.music.fadeout(300)
        time.sleep(2)
        result = battle_startend(player_party)
        pygame.mixer.music.load("snd/radar.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=99)
        myMixer("menu_back.wav",0)
        
        message = "Welcome back."
        if result == "Defeat!":    message += " That was rough."
        elif result == "Victory!":    message += " Ez clap."
        
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
        exp = 10000
        for member in player_party:
            menu_levelup(member, int(exp/len(player_party)),"+" + str(exp) + "EXP")
        myMixer("menu_back.wav",0)
        pygame.mixer.music.load("snd/radar.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=99)
        message = str(exp_cost) + " GOLD consumed."

    elif running == "Shop":
        myMixer("menu_shop.wav",0.7)
        costs_iron = 10
        costs_gold = 1
        if player_inventory["Iron"] >= costs_iron:
            player_inventory["Iron"] -= costs_iron
            new_charm = battle_charmslookup(1)[0]
            num = "1"
            while num in player_charms:
                num = str(random.randint(1,999))
            player_charms[num] = new_charm
            message = str(costs_iron) + " IRON consumed -> " + str(new_charm["set"]) + "."
            myMixer("menu_1more.wav",0.8)
        elif player_inventory["Gold"] >= costs_gold:
            player_inventory["Gold"] -= costs_gold
            new_charm = battle_charmslookup(1)[0]
            num = "1"
            while num in player_charms:
                num = str(random.randint(1,999))
            player_charms[num] = new_charm
            message = str(costs_gold) + " GOLD consumed -> " + str(new_charm["set"]) + "."
            myMixer("menu_1more.wav",0.8)
        else:
            message = str(costs_gold) + " GOLD/" + str(costs_iron) + " IRON needed to buy Charm!"
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

def terminate():
    #Terminate
    pygame.quit()
    quit()

#Main program
print("\n" * 200)

global fonts
fonts = init_font(screen_diag)
    
global player_party
player_party = ["Byleth"]

global player_weapons
player_weapons = {}
for weapon in battle_weaponslookup("all"):
    if weapon in player_weapons:
        player_weapons[weapon] += 1
    else:
        player_weapons[weapon] = 1


global player_charms
player_charms = {}
charms = battle_charmslookup(2)
ID = 1
for i in charms:
    print(str(i) + "\n")
    player_charms[str(ID)] = i
    ID += 1

global player_inventory
player_inventory = {"Gold" : 99, "Iron" : 0, "Wins" : 0}

global difficulty
difficulty = "Normal"
            
pygame.mixer.music.load("snd/radar.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=99)
time.sleep(0.3)
menu_main("")
    
terminate()





    