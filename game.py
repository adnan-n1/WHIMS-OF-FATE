import pygame
import random
import time
import button

#Change print statements for battle_passives into visual effects



pygame.init()
#framerate
clock = pygame.time.Clock()
framesrate = 120

#game window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Battle")

#fonts
fonts={"small":pygame.font.SysFont("Time New Roman", 26),
       "dmgsmall":pygame.font.SysFont("Time New Roman", 39),
       "medium":pygame.font.SysFont("Time New Roman", 58),
       "large":pygame.font.SysFont("Time New Roman", 84)}
colour = {"red" : (255, 0, 0), "green" : (0, 255, 0), "white" : (255,255,255), "black" : (0,0,0),
          "Fire" : (247, 65, 15), "Water" : (10, 86, 240), "Wind" : (48, 242, 129), "Physical" : (200, 200, 200)}

#images

#image loaded
background = pygame.image.load("img/Background/background.png").convert_alpha()
img_sword = pygame.image.load("img/Other/icon_sword.png")
img_lunge = pygame.image.load("img/Other/icon_lunge.png")
img_whip = pygame.image.load("img/Other/icon_whip.png")
img_skip = pygame.image.load("img/Other/icon_skip.png")
img_heal = pygame.image.load("img/Other/icon_heal.png")


#image display
def draw_background():
    screen.blit(background, (0,0))

def draw_stats():
    for person in combatents:
        draw_text(str(person.stats["name"]) + " HP:", fonts["small"], colour["green"], person.x, person.y+100)
        draw_text(str(person.stats["HP"]) + " " + str(person.status), fonts["small"], colour["green"], person.x, person.y+120)

def draw_text(text,font,colour,x,y):
    img = font.render(text, True, colour)
    screen.blit(img, (x ,y))

def draw_bar(x, y, value, maxvalue):
    ProgressBar(x,y,value,maxvalue).draw()

#combatents

class Fighter():
    def __init__(self, x, y, stats):
        self.status = "idle"
        self.stats = stats
        self.x = x
        self.y = y
        self.condition = "Normal"

        self.alive = True
        
        #image loaded, and its scale is changeable
        self.image_list = {
            "turn" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/turn.png"),
            "idle" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png"),
            "dead" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png"),
            "move" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/move.png")
                           }
        
        #size = 1
        #self.image = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        

    def move(self, action, target):
        #Functions acts as "Battle neutral"
        self.status = "move"
        message = ""
        message_colour = colour["white"]

        action = battle_moveslookup(action)

        #Contains all data of the current Turn
        battle_turndata = {
                     "action" : str(action[0]),
                     "actionelement" : action[5],
                     "turn" : self.stats["name"],
                     "totaldmg" : 0,
                     "crit" : 0,
                     "hit" : 0,
                     "heal" : 0,
                     "inflictself" : False,
                     "inflictopp" : False,
                     "actorcondition" : "",
                     "targetcondition" : ""}

        if self.stats["HP"] <= 0: battle_turndata["actorcondition"] = "Defeated"
        elif self.stats["HP"]/self.stats["MHP"] <= 30:    battle_turndata["actorcondition"] = "Critical"
        else:   battle_turndata["actorcondition"] = "Normal"
        if target.stats["HP"] <= 0: battle_turndata["targetcondition"] = "Defeated"
        elif target.stats["HP"]/target.stats["MHP"] <= 30:    battle_turndata["targetcondition"] = "Critical"
        else:   battle_turndata["targetcondition"] = "Normal"

        #Calculate dmg/healing/etc
        basehits = 1
        hits = basehits
        if action[0] == "Skip":
            message_colour = colour["white"]
            message = "Skipped"
            damage_text = DamageText(self.rect.centerx, self.rect.y, str(message), message_colour,"medium")
            damage_text_group.add(damage_text)
        elif action[3] == "Offence":
            message_colour = colour["red"]

            if action[0] != "":
                basedmg = action[1]
                hits = action[2]
            else:
                basedmg = 0
                hits = 0

            #default text size
            size = "small"
            while hits > 0:
                message_colour = colour[battle_turndata["actionelement"]]
                hits -= 1
                battle_turndata["hit"] += 1
                
                damage = int(basedmg * (self.stats["STR"]/100))
                damage += int(battle_dmgbonus(damage, self.stats, target.stats,battle_turndata))
                damage -= int(damage * target.stats["RES"]/100)
                damage += int(battle_dmgreduc(damage, self.stats, target.stats,battle_turndata))

                if damage < 0:  damage = 0

                
                #Manage crits
                crit = False
                if battle_dmgcrit(self.stats,target.stats,battle_turndata) <= self.stats["CRIT"] and damage > 0 and (battle_turndata["actionelement"] == "Physical" or battle_turndata["actionelement"] == "Wind"):
                    damage += battle_dmgcritbonus(damage, self.stats,target.stats,battle_turndata)
                    battle_turndata["crit"] += 1
                    crit = True
                if battle_turndata["actionelement"] in target.stats["weakness"] and damage > 0:
                    damage += battle_dmgcritbonus(damage, self.stats,target.stats,battle_turndata)
                    battle_turndata["crit"] += 1
                    crit = True

                #Deal dmg
                battle_turndata["hit"] += 1
                target.stats["HP"] -= damage
                if target.stats["HP"] <= 0:
                    target.stats["HP"] = 0
                    target.alive = False
                    target.status = "dead"

                #Changing combatent condition based on HP
                if self.stats["HP"] <= 0: self.condition = "Defeated"
                elif self.stats["HP"]/self.stats["MHP"] <= 30:    self.condition = "Critical"
                else:   self.condition = "Normal"
                if target.stats["HP"] <= 0: target.condition = "Defeated"
                elif target.stats["HP"]/target.stats["MHP"] <= 30:    target.condition = "Critical"
                else:   target.condition = "Normal"

                self.stats = battle_passive(self.stats,target.stats,battle_turndata)
                target.stats = battle_passive(target.stats,self.stats,battle_turndata)

                message = str(damage)

                if crit:  size = "medium"
                else:   size = "dmgsmall"
                damage_text = DamageText(random.randint(target.rect.x,target.rect.x+target.rect.width), random.randint(target.rect.y,target.rect.y+target.rect.height), str(message), message_colour,size)
                damage_text_group.add(damage_text)
                
        elif action[3] == "Defence":
            message_colour = colour["green"]

            healing = int(action[1])

            self.stats["HP"] += healing
            if self.stats["HP"] > self.stats["MHP"]: self.stats["HP"] = self.stats["MHP"]

            message = "+" + str(healing)
            
            if action == "Skip":
                message_colour = colour["white"]
                message = "Skipped"

            damage_text = DamageText(target.rect.centerx, target.rect.y, str(message), message_colour, "medium")
            damage_text_group.add(damage_text)
            


    def update(self):
        self.image = self.image_list[str(self.status)]

    #image display
    #(methods must have "self" as a minimum)
    def draw(self):
        screen.blit(self.image, self.rect)

class ProgressBar():
    def __init__(self, x, y, value, maxvalue):
        self.x =x
        self.y = y
        self.value = value
        self.maxvalue = maxvalue

    def draw(self, value):
        #update with new "value"
        self.value = value
        #calculate percentage
        percent = (self.value / self.maxvalue) * 100
        if percent <= 0:    percent = 0
        
        pygame.draw.rect(screen, colour["red"], (self.x, self.y, 100, 10))
        pygame.draw.rect(screen, colour["green"], (self.x, self.y, percent, 10))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, value, colour, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts[size].render(value, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #to control how long to make text float for
        self.counter = 0

    def update(self):
        #move text up
        #decrease y cord
        self.counter += 1
        if self.counter % 3 == 0:
            self.rect.y -= 1
        if self.counter > framesrate:
            self.kill()

class NormalText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts["small"].render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
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

    {"name" : "Hi", "LVL" : 45, "MHP" : 5000, "HP" : 5000, "STR" : 300, "RES" : 10, "CRIT" : 20, "EVA" : 75, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: BLZE", "Use the might of BLZE, gaining the power to ignite cataclysms: Landing hits drains 5% HP from self. When below 50% Max HP, All damage increased by 20% Max HP. Damage bonuses gained is doubled when in Critical condition"], "moves" : {"Concentrate":0,'Burning Hell': 0, "Fire Dance" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Burning Hell", "Fire Dance"], "Fusion Cards" : ["Prototype: BLZE"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

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

def battle_moveslookup(move):
  #Light, Weak, Medium, Heavy, Severe, Colossal
  #"Name : [BaseDMG, Range of hits, Type Offence/Defence/Heal, Buff/Debuff infliction, Element, Unique attribute]"
  all_moves = {"Nothing" : [0, [0,0], "Other", "None","",""]
                  #Healing
                  ,"Dia" : [100, [0,0], "Defence", "None","Heal",""]
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
                  ,"Fire Dance" : [83, [3,0], "Offence", "None","Fire",""]
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
                  ,"Bead" : [300, [0,0], "Defence", "None","",""]
                  ,"Healing Orb" : [100, [0,0], "Defence", "Heal","",""]
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
    moves[i] -= 1
    if moves[i] <= 0:
      moves[i] = 0

  return moves

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

def battle_passive(actor,target,data):
    #Change print statements

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

damage_text_group = pygame.sprite.Group()

#Main storage for player stats
player_stats = {'name': 'Byleth',
                      'weapon': 'Gold Sword',
                      'LVL': 40, 'MEXP': 100, 'EXP': 0,
                      'MHP': 2250,'HP': 2250,
                      'STR': 225, 'RES': 9, 'CRIT': 30, 'EVA': 45,
                      'buff': {}, 'debuff': {},
                      "charms" : [],
                      'fusion': ["Wind Type 09", "CRIT damage increased by 75%"],
                      'moves': {"Attack" : 0,"Cyclone":0, "Garubarion":0,"Dia" : 0},
                      "weakness" : "Fire"}
#Temporary stats for this battle
player = Fighter(screen_width/4, int(screen_height/2),player_stats)

enemy_stats = random.choice(get_enemies())
enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)




#Creating buttons. Screen, width, height, image, size x, size y
images = {"Physical" : img_sword, "Fire" : img_whip, "Water" : img_lunge, "Wind" : img_sword, "Heal" : img_heal}
abilities = {}
x_value = 0
for ability in player.stats["moves"]:
    #Add the Button attribute to ability
    abilities[ability] = {
        "button" : button.Button(screen, (screen_width/5) + x_value, screen_height - (screen_height/4), images[battle_moveslookup(ability)[5]], 70,70),
        "image" : images[battle_moveslookup(ability)[5]]}
    #Used for spacing out abilities on screen
    x_value += 80
abilities["Skip"] = {"button" :button.Button(screen, (screen_width/5) + x_value, screen_height - (screen_height/4), img_skip, 70,70),
                     "image" : img_skip}


            

#Create progressbars
player_hp = ProgressBar(player.x,player.y+140,player.stats["HP"],player.stats["MHP"])
enemy_hp = ProgressBar(enemy.x,enemy.y+140,enemy.stats["HP"],enemy.stats["MHP"])

combatents = [player, enemy]
player.status = "turn"
cooldown = 60

clicked = False

battle_action = "player"
selected = ""

#Running loop
running = True
while running:
    #clock tick
    clock.tick(framesrate)

    #Display images
    draw_background()

    if player.alive:
        player.update()
        player.draw()

    if enemy.alive:
        enemy.update()
        enemy.draw()

    #display battle status
    draw_text(str(battle_action).upper(), fonts["large"], colour["white"], screen_width/2, int(0 + screen_height/4))
    #display selected ability
    draw_text(str(selected).upper(), fonts["large"], colour["white"], (screen_width/5), screen_height - (screen_height/4) + 70)

    draw_stats()
    player_hp.draw(player.stats["HP"])
    enemy_hp.draw(enemy.stats["HP"])

    #damage text
    damage_text_group.update()
    damage_text_group.draw(screen)


    #actions
    action = ""
    
    
    #gets mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_img = None
    pygame.mouse.set_visible(True)
    
    for move in player.stats["moves"]:
        ability_clicked = abilities[move]["button"].draw() #(Returns True if button is pressed)
        skip_clicked = abilities["Skip"]["button"].draw()
        #Display cooldown if > 0, otherwise display READY
        if player.stats["moves"][move] > 0:    draw_text("CD: " + str(player.stats["moves"][move]), fonts["small"], colour["green"], abilities[move]["button"].rect.topleft[0], abilities[move]["button"].rect.topleft[1])
        else:   draw_text("READY", fonts["small"], colour["green"], abilities[move]["button"].rect.topleft[0], abilities[move]["button"].rect.topleft[1])

        #If button pressed + Ability cooldown 0 + Player's turn
        if ability_clicked and battle_action == "player":
            if player.stats["moves"][move] <= 0:                    
                selected = str(move)
                break
        elif skip_clicked and battle_action == "player":              
            selected = "Skip"
            break

    #Display description if hovering over Ability
    for move in player.stats["moves"]:
        if abilities[move]["button"].hover() == True and selected == "" and battle_action == "player":
            draw_text(str(move.upper()), fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            draw_text("   - " + str(battle_moveslookup(move)[7]), fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 20)

    #Display skip if hovering over Skip button
    if abilities["Skip"]["button"].hover() and selected == "" and battle_action == "player":
            draw_text("Skip turn", fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    #Display fusion if hovering over Character
    if player.rect.collidepoint(mouse_pos) and battle_action == "player" and selected == "":
        draw_text(str(player.stats["fusion"][0].upper()), fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        draw_text("   - " + str(player.stats["fusion"][1]), fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 20)
    if enemy.rect.collidepoint(mouse_pos) and battle_action == "player" and selected == "":
        draw_text(str(enemy.stats["fusion"][0].upper()), fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        draw_text("   - " + str(enemy.stats["fusion"][1]), fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 20)
        
    if selected != "Skip" and selected != "":
        #hide mouse
        pygame.mouse.set_visible(False)
        screen.blit(abilities[selected]["image"], mouse_pos)
        
    #Conditions to perform action (mouse on enemy, its your turn, ability selected, etc. Some conditions to not apply to some moves.)
    if enemy.rect.collidepoint(mouse_pos) and player.status == "turn" and selected != "" and battle_moveslookup(selected)[3] == "Offence":
        draw_text("CONFIRM?", fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 20)
        if clicked:
            action = selected
            selected = ""
    elif player.rect.collidepoint(mouse_pos) and player.status == "turn" and selected != "" and battle_moveslookup(selected)[3] == "Defence":
        draw_text("CONFIRM?", fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 20)
        if clicked:
            action = selected
            selected = ""
    elif selected == "Skip":
        action = selected
        selected = ""

    #cooldown makes turns not instant/1 frame long
    cooldown -= 1
    if cooldown <= 0:
        #Allows combatents to perform actions
        if battle_action == "player" and player.alive and action != "":
            player.status = "move"
            if battle_moveslookup(action)[3] == "Offence":    player.move(action, enemy)
            elif battle_moveslookup(action)[3] == "Defence":    player.move(action, player)
            else:   player.move(action, enemy)
            #Increases cooldown if action completed
            if action != "Skip":   player.stats["moves"][action] = 5
            battle_action = "neutral"
            cooldown = framesrate
        elif battle_action == "enemy" and enemy.alive:
            #Enemy AI
            action = ""
            limit = random.randint(1,len(enemy.stats["moves"]))
            for move in enemy.stats["moves"]:
                action = move
                limit -= 1
                if limit <= 0:  break
            if enemy.stats["moves"][action] > 0:    action = "Skip"
            
            enemy.status = "move"
            if battle_moveslookup(action)[3] == "Offence":    enemy.move(action, player)
            elif battle_moveslookup(action)[3] == "Defence":    enemy.move(action, enemy)
            else:   enemy.move(action, player)
            battle_action = "neutral"
            cooldown = framesrate
        
            
        elif battle_action == "neutral":
            #Detects action completion ("move"). Passes over turn
            if player.status == "move" and enemy.alive:
                enemy.status = "turn"
                player.status = "idle"
                battle_action = "enemy"
            elif enemy.status == "move" and player.alive:
                player.status = "turn"
                enemy.status = "idle"
                battle_action = "player"

            #Decrease Player and Enemy CD
            player.stats["moves"] = battle_movecd(player.stats["moves"])
            enemy.stats["moves"] = battle_movecd(enemy.stats["moves"])

            #Decreases buff/debuff duration
            if len(player.stats["buff"]) > 0 or len(player.stats["debuff"]) > 0:
                player.stats["buff"] = battle_removebuffs(player.stats["buff"])
                player.stats["debuff"] = battle_removebuffs(player.stats["debuff"])
            if len(enemy.stats["buff"]) > 0 or len(enemy.stats["debuff"]) > 0:
                enemy.stats["buff"] = battle_removebuffs(enemy.stats["buff"])
                enemy.stats["debuff"] = battle_removebuffs(enemy.stats["debuff"])
                
            #Determines battle outcome
            if not enemy.alive:
                battle_action = "Victory!"
            if not player.alive:
                battle_action = "Defeat!"
            cooldown = framesrate



    #For events happening in the pygame
    for event in pygame.event.get():
        #If window X clicked
        if event.type == pygame.QUIT:
            running = False

        #If mouse button clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            enemy_stats = random.choice(get_enemies())
            enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)
            enemy_hp = ProgressBar(enemy.x,enemy.y+140,enemy.stats["HP"],enemy.stats["MHP"])
            player_stats = {'name': 'Byleth',
                      'weapon': 'Gold Sword',
                      'LVL': 40, 'MEXP': 100, 'EXP': 0,
                      'MHP': 2250,'HP': 2250,
                      'STR': 225, 'RES': 9, 'CRIT': 30, 'EVA': 45,
                      'buff': {}, 'debuff': {},
                      "charms" : [],
                      'fusion': ["Wind Type 09", "CRIT damage increased by 75%"],
                      'moves': {"Attack" : 0,"Cyclone":0, "Garubarion":0,"Dia" : 0},
                      "weakness" : "Fire"}
            player = Fighter(screen_width/4, int(screen_height/2),player_stats)
            player_hp = ProgressBar(player.x,player.y+140,player.stats["HP"],player.stats["MHP"])
            player.status = "turn"
            enemy.status = "idle"
            combatents = [player, enemy]
            battle_action = "player"

            

    pygame.display.update()
#Terminate
if running == False:
    pygame.quit()
    quit()
