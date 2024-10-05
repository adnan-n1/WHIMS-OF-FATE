import pygame
import random
import time
import button
import math

#Make controls more efficient ln 1523
#Display mini descs on left of screen each turn in the form of list
#Add other menus


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#framerate
clock = pygame.time.Clock()
framesrate = 165

#game window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Greatest Battle")
pygame.display.set_icon(pygame.image.load("img/icon.png"))

display = pygame.Surface((screen_width,screen_height))

#fonts
fonts={"small":pygame.font.SysFont("", 26),
       "dmgsmall":pygame.font.SysFont("Franklin Gothic Medium Cond", 39),
       "medium":pygame.font.SysFont("Franklin Gothic Medium Cond", 58),
       "large":pygame.font.SysFont("Franklin Gothic Medium Cond", 84),
       "verylarge":pygame.font.SysFont("Franklin Gothic Medium Cond", 110)}

#For rainbow colour
# Set the increment or decrement value for each color channel
incr = [2, 2, 2]

# Set the upper and lower bounds for each color channel
upper_bound = [255, 255, 255]
lower_bound = [0, 50, 0]
#All colours
colour = {"red" : (255, 0, 0), "green" : (0, 255, 0), "white" : (255,255,255), "black" : (0,0,0),"grey" : (100,100,100), "rainbowcycle" : (255,0,0),
          "Fire" : (247, 65, 15), "Water" : (10, 86, 240), "Wind" : (48, 242, 129), "Physical" : (200, 200, 200),
          "Buff" : (66, 135, 245), "Debuff" : (162, 78, 222), "Heal" : (0, 255, 0)}

#images

#image loaded
background = pygame.image.load("img/Background/background.png").convert_alpha()
img_physical = pygame.image.load("img/Other/icon_physical.png")
img_fire = pygame.image.load("img/Other/icon_fire.png")
img_water = pygame.image.load("img/Other/icon_water.png")
img_wind = pygame.image.load("img/Other/icon_wind.png")
img_skip = pygame.image.load("img/Other/icon_skip.png")
img_heal = pygame.image.load("img/Other/icon_heal.png")
img_buff = pygame.image.load("img/Other/icon_buff.png")
img_debuff = pygame.image.load("img/Other/icon_debuff.png")

img_charm = {
    "CRIT" : pygame.image.load("img/Other/icon_charm_crit.png"),
    "CRIT DMG" : pygame.image.load("img/Other/icon_charm_critdmg.png"),
    "Physical DMG" : pygame.image.load("img/Other/icon_charm_phys.png"),
    "Elemental DMG" : pygame.image.load("img/Other/icon_charm_elem.png"),
    "MHP" : pygame.image.load("img/Other/icon_charm_hp.png"),
    "DMG" : pygame.image.load("img/Other/icon_charm_dmg.png"),
    "ER" : pygame.image.load("img/Other/icon_charm_er.png")}

img_bonus = {
    "CRIT" : pygame.image.load("img/Other/icon_bonus_crit.png"),
    "CRIT DMG" : pygame.image.load("img/Other/icon_bonus_critdmg.png"),
    "Physical" : pygame.image.load("img/Other/icon_bonus_phys.png"),
    "Fire" : pygame.image.load("img/Other/icon_bonus_fire.png"),
    "Water" : pygame.image.load("img/Other/icon_bonus_water.png"),
    "Wind" : pygame.image.load("img/Other/icon_bonus_wind.png"),
    "MHP" : pygame.image.load("img/Other/icon_bonus_hp.png"),
    "All" : pygame.image.load("img/Other/icon_bonus_dmg.png"),
    "STR" : pygame.image.load("img/Other/icon_bonus_str.png"),
    "RES" : pygame.image.load("img/Other/icon_bonus_res.png"),
    "ER" : pygame.image.load("img/Other/icon_charm_er.png")}

img_proj = {
    "Physical" : pygame.image.load("img/Effects/proj_phys.png"),
    "Physical_crit" : pygame.image.load("img/Effects/proj_phys_crit.png"),
    "Fire" : pygame.image.load("img/Effects/proj_fire.png"),
    "Fire_crit" : pygame.image.load("img/Effects/proj_fire_crit.png"),
    "Wind" : pygame.image.load("img/Effects/proj_wind.png"),
    "Wind_crit" : pygame.image.load("img/Effects/proj_wind_crit.png"),
    "Water" : pygame.image.load("img/Effects/proj_water.png"),
    "Water_crit" : pygame.image.load("img/Effects/proj_water_crit.png"),
    "Abyss" : pygame.image.load("img/Effects/proj_abyss.png"),
    "Abyss_crit" : pygame.image.load("img/Effects/proj_abyss_crit.png")
    }
    


#background display
def draw_background():
    x,y = mouse_hovereffect(0,0)
    display.blit(background, (x,y))

def move_to_point(current_x, current_y, target_x, target_y, speed):
  #Calculate the distance to the target point
  distance = math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2)

  #Calculate the direction to the target point
  angle = math.atan2(target_y - current_y, target_x - current_x)

  #Calculate the velocity in the x and y directions
  vel_x = math.cos(angle) * speed
  vel_y = math.sin(angle) * speed

  #Move the object to the target point
  current_x += vel_x
  current_y += vel_y

  return current_x, current_y

def draw_charms(myCharms, mouse_pos, x, y):
    #Charms 30x30, 10 pixels spacing in y
    #Increases when new Charm in list
    x_value = 0
    #Width and Height
    size = 20
    #x and y are x and y of Charm
    for charm in myCharms:
        charmtype = myCharms[charm]["stat"]
        image = pygame.transform.scale(img_charm[charmtype],(size,size)).convert()
        display.blit(image, (x,y))
        if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
            draw_text(myCharms[charm]["desc"], fonts["small"], colour["green"],x,y+size, False)
        x_value += 40
        x += size + 10

def draw_bonus(myBonuses, mouse_pos, x, y):
    elemental = myBonuses["EDMG"]
    #Bonuses 30x30, 10 pixels spacing in y
    #Increases when new Bonus in list
    #Width and Height
    size = 20
    #x and y are that of Bonus
    
    symbols = {"MHP" : "","ER" : "%", "CRIT" : "", "CRIT DMG" : "%", "Physical" : "%","Fire" : "%",  "Water" : "%",  "Wind" : "%",  "RES" : "",  "STR" : "", "All" : "%"}
            
    for bonus in myBonuses:
        if bonus != "EDMG" and myBonuses[bonus] != 0:
            if myBonuses[bonus] > 0:    symbol = "+"
            else:   symbol = ""
            image = pygame.transform.scale(img_bonus[bonus],(size,size)).convert()
            display.blit(image, (x,y))
            #Outline
            if symbol == "+": pygame.draw.rect(display, colour["Buff"], (x-2, y-2, size+2, size+2), 2)
            elif symbol == "": pygame.draw.rect(display, colour["Debuff"], (x-2, y-2, size+2, size+2), 2)

            if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
                draw_text(str(bonus) + " " + str(symbol) + str(myBonuses[bonus]) + str(symbols[bonus]), fonts["small"], colour["green"],x,y+size, False)
            x += size + 10
    for bonus in elemental:
        if elemental[bonus] != 0:
            if elemental[bonus] > 0:    symbol = "+"
            else:   symbol = ""
            image = pygame.transform.scale(img_bonus[bonus],(size,size)).convert()
            display.blit(image, (x,y))
            #Outline
            if symbol == "+": pygame.draw.rect(display, colour["Buff"], (x-2, y-2, size+2, size+2), 2)
            elif symbol == "": pygame.draw.rect(display, colour["Debuff"], (x-2, y-2, size+2, size+2), 2)
            
            if (mouse_pos[0] >= x and mouse_pos[0] <= x+size) and (mouse_pos[1] >= y and mouse_pos[1] <= y+size):
                draw_text(str(bonus) + " DMG " + str(symbol) + str(elemental[bonus]) + str(symbols[bonus]), fonts["small"], colour["green"],x,y+size, False)
            x += size + 10
        
def draw_stats(person, x, y):
    message = ""
    for info in person.stats:
        if info.lower() != "charms" and info.lower() != "fusion" and info.lower() != "drops" and info.lower() != "moves":
            output = person.stats[info]
            if info in person.bonuses and info != "EDMG":  output += person.bonuses[info]
            if info == "EDMG":
                edmg_dict = {}
                for stat in person.stats["EDMG"]:
                    edmg_dict[stat] = person.stats["EDMG"][stat] + person.bonuses["EDMG"][stat]
                output = edmg_dict
            output = str(info.upper()) + ": " + str(output)
            message += str(output) + " # "

    draw_text(str(message), fonts["small"], colour["white"], x, y, True)

def draw_health(person, healthbar, mouse_pos):
    x = person.rect.x
    y = person.rect.y+person.rect.height+10
    x,y = mouse_hovereffect(x,y)

    #If person is the player
    if "EG" in person.stats:
        rect_width, rect_height = 150,70
        myColour = "green"
    else:
        rect_width, rect_height = 150,40
        myColour = "red"
    
    #Outline width makes box slightly wider to not cover text
    outline_width = 3
    box = pygame.Rect(x-outline_width, y-outline_width, rect_width+outline_width, rect_height+outline_width)
    #Main box
    pygame.draw.rect(display, colour["grey"], box)
    #Outline
    pygame.draw.rect(display, colour[myColour], (x-outline_width, y-outline_width, rect_width+outline_width, rect_height+outline_width), 3)

    #Healthbars
    draw_text(str(person.stats["name"]), fonts["small"], colour[myColour], x+3, y+3, False)
    healthbar.draw(x+3,y+22,person.stats["HP"],person.stats["MHP"]+person.bonuses["MHP"],mouse_pos,myColour)
    if "EG" in person.stats:
        if person.stats["EG"] == person.stats["MEG"]:   player_eg.draw(x+3,y+44,person.stats["EG"],person.stats["MEG"],mouse_pos,"rainbowcycle")
        else:   player_eg.draw(x+3,y+44,person.stats["EG"],person.stats["MEG"],mouse_pos,"Buff")

    #Display stat bonuses
    draw_bonus(person.bonuses,mouse_pos,x,y+rect_height+5)
    
    #Display player charms
    if person.stats["name"] == player.stats["name"]:
        draw_charms(person.stats["charms"],mouse_pos,x,y+rect_height+40)

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
        text_width, text_height = font.size(longest_line.upper())
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
        if hp1 >= hp2:
            track = random.choice(["battle.wav","battle_vocal.wav"])
            pygame.mixer.music.load("snd/battle_vocal.wav")
        else:
            track = random.choice(["boss.wav","boss_vocal.wav","tears.wav"])
            pygame.mixer.music.load("snd/" + str(track))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=99)
    elif startend == "End":   pygame.mixer.music.fadeout(3000)

def mouse_hovereffect(x,y):
    #mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x,mouse_y = inviscircle.top_x,inviscircle.top_y
    spd = -0.005
    
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

def battle_updatestats(stats, oppstats, battle_turndata):
    newstats = battle_bonuscheck(stats,oppstats,battle_turndata)
    
    #Add bonuses from charms
    if stats["name"] == player_stats["name"]:
        for charm in stats["charms"]:
            newstats[str(stats["charms"][charm]["stat"])] += stats["charms"][charm]["amount"]

    #MHP Acts as percent rather than flat number. This converts to flat number
    newstats["MHP"] = int((stats["MHP"] * (newstats["MHP"]/100)))


    return newstats


class Fighter():
    def __init__(self, x,y,statistics):
        self.status = "idle"
        self.stats = statistics
        self.x = x
        self.y = y
        self.condition = "Normal"
        self.bonuses ={"MHP" : 0, "CRIT" : 0, "CRIT DMG" : 0, "STR" : 0, "RES" : 0, "EDMG":{'Physical': 0, 'Fire': 0, 'Water': 0, 'Wind': 0, 'All': 0}}
        if self.stats["name"] == player_stats["name"]:  self.bonuses["ER"] = 0
        #Actual bonues values added onto normal stats
        

        self.alive = True
        
        #image loaded, and its scale is changeable
        self.image_list = {
            "turn" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/turn.png"),
            "idle" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png"),
            "dead" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/idle.png"),
            "hurt" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/hurt.png"),
            "move" : pygame.image.load("img/Char/" + str(self.stats["name"]) + "/move.png")
                           }
        
        #size = 1
        #self.image = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        self.image = self.image_list[str(self.status)]
        #rect used for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        

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
                     "actiontype" : action[3],
                     "actioninflict" : action[4],
                     "actor" : self,
                     "target" : target,
                     "turn" : self.stats["name"],
                     "totaldmg" : 0,
                     "crit" : False,
                     "critamount" : 0,
                     "hit" : 0,
                     "heal" : 0,
                     "actorcondition" : "",
                     "targetcondition" : ""}
        
        #For stats
        self.bonuses = battle_updatestats(self.stats,target.stats,battle_turndata)
##        for stat in self.stats:
##            if stat != "EDMG" and stat in self.bonuses: self.stats[stat] += self.bonuses[stat]     
##        for stat in self.stats["EDMG"]:
##            self.stats["EDMG"][stat] += self.bonuses["EDMG"][stat]

        target.bonuses = battle_updatestats(target.stats,self.stats,battle_turndata)
##        for stat in target.stats:
##            if stat != "EDMG" and stat in target.bonuses: target.stats[stat] += target.bonuses[stat]
##        for stat in target.stats["EDMG"]:
##            target.stats["EDMG"][stat] += target.bonuses["EDMG"][stat]

        

        if self.stats["HP"] <= 0: battle_turndata["actorcondition"] = "Defeated"
        elif self.stats["HP"]/(self.stats["MHP"]+self.bonuses["MHP"]) <= 30:    battle_turndata["actorcondition"] = "Critical"
        else:   battle_turndata["actorcondition"] = "Normal"
        if target.stats["HP"] <= 0: battle_turndata["targetcondition"] = "Defeated"
        elif target.stats["HP"]/(target.stats["MHP"]+target.bonuses["MHP"]) <= 30:    battle_turndata["targetcondition"] = "Critical"
        else:   battle_turndata["targetcondition"] = "Normal"

        if "EG" in self.stats and "SPECIAL" in battle_turndata["action"]:
            self.stats["EG"] = 0

        #Calculate dmg/healing/etc
        hits = 1
        if action[0] == "Skip":
            message_colour = colour["white"]
            message = "Skipped"
            battle_damagetext(self, str(message), message_colour,"medium")
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
                battle_turndata["crit"] = False
                battle_turndata["hit"] += 1

                damage = int(basedmg * ((self.stats["STR"]+self.bonuses["STR"])/100))
                additional_damage = 0
                #Apply elemental/physical dmg bonuses
                additional_damage += (((self.bonuses["EDMG"][battle_turndata["actionelement"]]+self.stats["EDMG"][battle_turndata["actionelement"]])/100)*damage) + (((self.bonuses["EDMG"]["All"]+self.stats["EDMG"]["All"])/100)*damage)
                additional_damage -= int(damage * (target.stats["RES"]+target.bonuses["RES"])/100)

                if damage < 0:  damage = 0
                else:   damage = int(damage)

              
                
                #Manage crits
                critdmg = ((self.stats["CRIT DMG"]+self.bonuses["CRIT DMG"])/100)*damage
                if random.randint(1,100) <= self.stats["CRIT"]+self.bonuses["CRIT"] and damage > 0:
                    additional_damage += critdmg
                    battle_turndata["critamount"] += 1
                    battle_turndata["crit"] = True
                if battle_turndata["actionelement"] in target.stats["weakness"] and damage > 0:
                    additional_damage += damage * 0.5
                    battle_turndata["critamount"] += 1
                    battle_turndata["crit"] = True

                #Play sounds. Different sound based on crit hit
                sounds = {"Physical" : "hit_physical.wav", "Fire" : "hit_fire.wav", "Water" : "hit_water.wav", "Wind" : "hit_wind.wav", }
                sounds_crit = {"Physical" : "hit_physicalcrit.wav", "Fire" : "hit_firecrit.wav", "Water" : "hit_watercrit.wav", "Wind" : "hit_windcrit.wav", }
                if battle_turndata["crit"]:    sound = sounds_crit[battle_turndata["actionelement"]]
                else:   sound = sounds[battle_turndata["actionelement"]]

                if battle_turndata["crit"]:  fontsize = "medium"
                else:   fontsize = "dmgsmall"
                    
                #Deal dmg
                damage = int(damage + additional_damage)
                battle_turndata["hit"] += 1
                battle_turndata["totaldmg"] += damage
                #Projectiles
                if battle_turndata["crit"]: battle_projectile(self,target,img_proj[battle_turndata["actionelement"]+"_crit"])
                else:   battle_projectile(self,target,img_proj[battle_turndata["actionelement"]])
                #Change hp
                battle_changehp(target, damage, battle_turndata["actionelement"], sound, False,fontsize)

                #Energy charge. Player exclusive
                #Player lands crit: 2 times damage used for EG calc
                if "EG" in self.stats and battle_turndata["crit"] and "SPECIAL" not in battle_turndata["action"]:
                    self.stats["EG"] = battle_energy(target.stats["MHP"],damage*2,self.stats["ER"],self.stats["EG"],self.stats["MEG"])
                #Enemy lands crit: 4 times less damage used for EG calc
                elif "EG" in target.stats and battle_turndata["crit"]:
                    target.stats["EG"] = battle_energy(target.stats["MHP"],damage/2,target.stats["ER"],target.stats["EG"],target.stats["MEG"])
                
                #Passives
                #self.stats = battle_passive(self,target,battle_turndata)
                #target.stats = battle_passive(target,self,battle_turndata)

                #Update bonuses
                self.bonuses = battle_updatestats(self.stats,target.stats,battle_turndata)
                target.bonuses = battle_updatestats(target.stats,self.stats,battle_turndata)
                


            #Apply debuff
            if action[4] != "None":
                battle_applybuffs(action[4], 3, "Debuff", target)
                
        elif action[3] == "Defence":
            #Healing
            if action[1] != 0:
                battle_changehp(self, int(action[1] * ((self.stats["STR"]+self.bonuses["STR"])/100)), battle_turndata["actionelement"], "heal.wav", False,"medium")
            #Apply buff
            if action[4] != "None":
                battle_applybuffs(action[4], 3, "Buff", self)


        #Return the results of this turn to Battle_Neutral
        #Update stats (Using buffs/ passives/ charms/ etc)
##        for stat in self.stats:
##            if stat != "EDMG" and stat in self.bonuses: self.stats[stat] -= self.bonuses[stat]
##        for stat in self.stats["EDMG"]:
##            self.stats["EDMG"][stat] -= self.bonuses["EDMG"][stat]
##
##        for stat in target.stats:
##            if stat != "EDMG" and stat in target.bonuses: target.stats[stat] -= target.bonuses[stat]
##        for stat in target.stats["EDMG"]:
##            target.stats["EDMG"][stat] -= target.bonuses["EDMG"][stat]

        #Decreases buff/debuff duration
        self.stats["buff"] = battle_removebuffs(self.stats["buff"])
        self.stats["debuff"] = battle_removebuffs(self.stats["debuff"])
        
        return battle_turndata
            

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
        
        if percent <= 0:
            percent = 0
            if self.value > 0:
                percent = 1
        
        if percent <= 30:
            myColour = "red"
        else:
            myColour = col

        draw_text(str(percent) + "%", fonts["small"], colour[myColour], x + self.width+2, y-3, False)
        pygame.draw.rect(display, colour["grey"], (x, y, self.width, self.height))
        pygame.draw.rect(display, colour[col], (x, y, percent, self.height))
        #Outline
        pygame.draw.rect(display, colour[col], (x-1, y-1, self.width+1, self.height+1), 1)

        #Display exact values when hovering with mouse
        if (mouse_pos[0] >= x and mouse_pos[0] <= self.width+x) and (mouse_pos[1] >= y and mouse_pos[1] <= y+self.height):
            draw_text("(" + str(self.value) + "/" + str(int(self.maxvalue)) + ")", fonts["small"], colour[myColour],mouse_pos[0],mouse_pos[1], False)



def myMixer(decision):
  global myMixerSwitch
  decision = str(decision)
  
  if decision == "":
    return
  elif ".wav" in decision:
    try:
      pygame.mixer.Sound("snd/" + str(decision)).play()
    except Exception as e:
      print("Cannot play sound '" + str(decision) + "':\n" + str(e))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, value, colour, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts[size].render(value, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #to control how long to make text exist for
        self.counter = 0
    def update(self):
        #decrease y cord (move text up)
        self.counter += 1
        #Moves 3 times slower
        if self.counter % 4 == 0:
            self.rect.y -= 1

        self.image.set_alpha(0)
        display.blit(self.image,self.rect)
        #Kill after 2 seconds
        if self.counter > framesrate*2:
            self.kill()


def battle_damagetext(target, message, message_colour, message_size):
    damage_text = DamageText(random.randint(target.rect.x,target.rect.x+target.rect.width), random.randint(target.rect.y,target.rect.y+target.rect.height), message, message_colour,message_size)
    damage_text_group.add(damage_text)

class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_x = target_x
        self.target_y =target_y
        #0.3 second limit
        self.limit = framesrate

        #Flip image if projectile going right to left
        if self.rect.center[0] > self.target_x:
            self.image = pygame.transform.rotate(self.image,180)
    def update(self):
        self.limit -= 1
        self.rect.center = move_to_point(self.rect.center[0],self.rect.center[1],self.target_x,self.target_y,40)
        display.blit(self.image, self.rect)

        if ((self.target_x >= self.rect.x and self.target_x <= self.rect.x + self.rect.width) and (self.target_y >= self.rect.y and self.target_y <= self.rect.y + self.rect.height)) or self.limit <= 0:
            self.kill()

def battle_projectile(actor, target, image):
    projectile = Projectile(image, actor.rect.x+actor.rect.width,random.randint(actor.rect.y,actor.rect.y+actor.rect.height),random.randint(target.rect.x,target.rect.x+target.rect.height),random.randint(target.rect.y,target.rect.y+target.rect.height))
    projectile_group.add(projectile)

class NormalText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts["small"].render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Battle_invisCircle():
    def __init__(self,centre_x,centre_y,radius,angle,angular_velocity,line_width):
        self.centre_x, self.centre_y = centre_x, centre_y
        self.radius = radius
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.line_width = line_width
        self.colour = (255,0,0,0)
        self.top_x, self.top_y = 0,0
        
    def update(self):
        # Update the angle
        self.angle += self.angular_velocity
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
      "Wind Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT", "Num" : 10}]},
      "Wind Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 20}]},
      "Wind Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 25}]},
      "Wind Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT", "Num" : 20}]},
      "Wind Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 40}]},
      "Wind Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 50}]},
      "Wind Type 07" : {"Effects" : [{"Cond" : "Crit", "Stat" : "Buff", "Num" : "Focused"}]},#Landing crit grants Focused buff
      "Wind Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "CRIT DMG", "Num" : 35}, {"Cond" : "Actor HP higher", "Stat" : "CRIT DMG", "Num" : 35}]},#+35 crit dmg if hp higher than target. +35 crit dmg.
      "Wind Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Wind DMG", "Num" : 50},{"Cond" : "Crit", "Stat" : "Wind DMG", "Num" : 50}]},#+50% wind dmg. Landing crit gives +50% wind dmg
      "Prototype: GALE" : {"Effects" : [{"Cond" : "HP 60% higher", "Stat" : "CRIT", "Num" : 20}, {"Cond" : "HP 60% higher", "Stat" : "CRIT DMG", "Num" : 100},{"Cond" : "HP 60% lower", "Stat" : "CRIT", "Num" : 40},{"Cond" : "HP 60% lower", "Stat" : "CRIT DMG", "Num" : 50},{"Cond" : "Critical condition", "Stat" : "CRIT", "Num" : 20},{"Cond" : "Critical condition", "Stat" : "CRIT DMG", "Num" : 100}]},

      "Fire Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "MHP", "Num" : 20}]},
      "Fire Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 30}]},
      "Fire Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Fire DMG", "Num" : 25}]},
      "Fire Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "MHP", "Num" : 40}]},
      "Fire Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 60}]},
      "Fire Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Fire DMG", "Num" : 50}]},
      "Fire Type 07" : {"Effects" : [{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Blaze Shield"}]},#Taking hits grants Blaze Shield buff, extra mhp
      "Fire Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "STR", "Num" : 60},{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Charged"}, {"Cond" : "Take hit", "Stat" : "Debuff", "Num" : "Vulnerable"}]},#+60 str. Grants Charged to self and Vulnerable to opponent when taking hits.
      "Fire Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Buff", "Num" : "Pyroclastic Charge"}]},#Every point of Max HP increases Fire DMG bonus by 0.05%
      "Prototype: BLZE" : {"Effects" : [{"Cond" : "HP 60% lower", "Stat" : "Buff", "Num" : "Pyroclastic Charge"}, {"Cond" : "Critical condition", "Stat" : "Buff", "Num" : "Pyroclastic Surge"}]},#Every point of Max HP increases Fire DMG bonus by 0.05%, double the effect in critical condition
      
      "Water Type 01" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 10}]},
      "Water Type 02" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 30}]},
      "Water Type 03" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 25}]},
      "Water Type 04" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 20}]},
      "Water Type 05" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 60}]},
      "Water Type 06" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 50}]},
      "Water Type 07" : {"Effects" : [{"Cond" : "", "Stat" : "RES", "Num" : 20}, {"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Invulnerable"}, {"Cond" : "Take hit", "Stat" : "Debuff", "Num" : "Drained"}]},#RES +20. Grants invulnerable to self and drained to target when taking hit
      "Water Type 08" : {"Effects" : [{"Cond" : "", "Stat" : "Physical DMG", "Num" : 60}, {"Cond" : "Actor HP higher", "Stat" : "Physical DMG", "Num" : 20}]},#+60 phys dmg. +20 if hp higher than opponent
      "Water Type 09" : {"Effects" : [{"Cond" : "", "Stat" : "Water DMG", "Num" : 50},{"Cond" : "", "Stat" : "Buff", "Num" : "Inspired"}]},#+50% water dmg. Inspired: every point of RES gives 2% Water DMG.
      "Prototype: AQUA" : {"Effects" : [{"Cond" : "Take hit", "Stat" : "Buff", "Num" : "Awakened"},{"Cond" : "Critical condition", "Stat" : "Buff", "Num" : "Awakened One"}]}#Taking hits grants Awakaned: 50% water dmg + 10 RES. Awakened One: all bonuses increased by 50%.
      }
      
  newoutput = ["","",""]
  desc = ""
  if fusion in newfusions:
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
              conditions_outputdesc[effect["Cond"]].append(effect["Stat"] + " increased by " + str(effect["Num"]) + "")
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

def get_enemies():
  #Enemy names:
  #Elemental, Fighter, Guardian, Sentinel
  enemies = [

    {"name" : "Wind Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 25, "RES" : 1, "CRIT" : 30, "CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 01", get_fusion("Wind Type 01")[1]], "moves" : {"Thousand Slaps":0, "Garu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Thousand Slaps"], "Fusion Cards" : ["Wind Type 01"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 50, "RES" : 2, "CRIT" : 30, "CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},"buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 02", get_fusion("Wind Type 02")[1]], "moves" : {"Attack":0, "Garu":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Garu"], "Fusion Cards" : ["Wind Type 02"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 75, "RES" : 3, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 03", get_fusion("Wind Type 03")[1]], "moves" : {"Attack":0, "Garu":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Garu"], "Fusion Cards" : ["Wind Type 03"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 04", get_fusion("Wind Type 04")[1]], "moves" : {"Attack":0, "Garula":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Garula"], "Fusion Cards" : ["Wind Type 04"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 125, "RES" : 5, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 05", get_fusion("Wind Type 05")[1]], "moves" : {"Attack":0, "Cyclone":0, "Garula" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Cyclone","Garula"], "Fusion Cards" : ["Wind Type 05"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 150, "RES" : 6, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},"buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 06", get_fusion("Wind Type 06")[1]], "moves" : {"Attack":0, "Garula":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Garula"], "Fusion Cards" : ["Wind Type 06"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 175, "RES" : 7, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 07", get_fusion("Wind Type 07")[1]], "moves" : {"Attack":0, "Garudyne":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Garudyne"], "Fusion Cards" : ["Wind Type 07"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 200, "RES" : 8, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 08", get_fusion("Wind Type 08")[1]], "moves" : {"Attack":0, "Garudyne":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Garudyne"], "Fusion Cards" : ["Wind Type 08"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Wind Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 225, "RES" : 9, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Wind Type 09", get_fusion("Wind Type 09")[1]], "moves" : {"Cyclone":0, "Garubarion":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Cyclone", "Garubarion"], "Fusion Cards" : ["Wind Type 09"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Kaze", "LVL" : 45, "MHP" : 10000, "HP" : 10000, "STR" : 100, "RES" : 10, "CRIT" : 30,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: GALE", get_fusion("Prototype: GALE")[1]], "moves" : {"Wind Boost":0,"Wrath Tempest":0,"Cyclone":0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Cyclone","Concentrate","Wrath Tempest"], "Fusion Cards" : ["Prototype: GALE"], "Support Items" : ["Flashbang"]}, "weakness" : "Fire"},

    {"name" : "Fire Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 100, "RES" : 1, "CRIT" : 2,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 01", get_fusion("Fire Type 01")[1]], "moves" : {"Attack":0, "Agi":0, "Dia" : 0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 01"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},"buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 02", get_fusion("Fire Type 02")[1]], "moves" : {"Attack":0, "Agi":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 02"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 03", get_fusion("Fire Type 03")[1]], "moves" : {"Attack":0, "Agi":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Agi"], "Fusion Cards" : ["Fire Type 03"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 04", get_fusion("Fire Type 04")[1]], "moves" : {"Agilao":0, "Attack":0, "Diarama" : 0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Agilao"], "Fusion Cards" : ["Fire Type 04"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 05", get_fusion("Fire Type 05")[1]], "moves" : {"Attack":0, "Charge":0, "Megido" : 0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Charge", "Agilao", "Megido"], "Support Items" : ["Molotov"], "Fusion Cards" : ["Fire Type 05"]}, "weakness" : "Water"},

    {"name" : "Fire Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 06", get_fusion("Fire Type 06")[1]], "moves" : {"Attack":0, "Concentrate":0, "Agilao" : 0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Concentrate", "Agilao"], "Fusion Cards" : ["Fire Type 06"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 07", get_fusion("Fire Type 07")[1]], "moves" : {"Diarahan":0, "Agidyne":0, "Attack" : 0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Diarahan", "Agidyne"], "Fusion Cards" : ["Fire Type 07"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 08", get_fusion("Fire Type 08")[1]], "moves" : {"Attack":0, "Agidyne":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Agidyne"], "Fusion Cards" : ["Fire Type 08"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Fire Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Fire Type 09", get_fusion("Fire Type 09")[1]], "moves" : {"Attack":0, "Agibarion":0, "Fire Dance" : 0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Agibarion", "Fire Dance"], "Fusion Cards" : ["Fire Type 09"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Hi", "LVL" : 45, "MHP" : 10000, "HP" : 10000, "STR" : 100, "RES" : 10, "CRIT" : 20,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: BLZE", get_fusion("Prototype: BLZE")[1]], "moves" : {"Fire Boost":0,'Debilitate': 0, "Burning Hell" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Burning Hell", "Fire Dance"], "Fusion Cards" : ["Prototype: BLZE"], "Support Items" : ["Molotov"]}, "weakness" : "Water"},

    {"name" : "Water Elemental", "LVL" : 1, "MHP" : 250, "HP" : 250, "STR" : 100, "RES" : 10, "CRIT" : 2,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 01", get_fusion("Water Type 01")[1]], "moves" : {"Attack":0, "Bufu":0}, "drops" : {"EXP" : 250, "Skill Cards" : ["Bufu"], "Fusion Cards" : ["Water Type 01"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 5, "MHP" : 500, "HP" : 500, "STR" : 100, "RES" : 2, "CRIT" : 4,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 02", get_fusion("Water Type 02")[1]], "moves" : {"Attack" : 0,"Megido":0, "Bufu":0}, "drops" : {"EXP" : 500, "Skill Cards" : ["Bufu", "Megido"], "Fusion Cards" : ["Water Type 02"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Elemental", "LVL" : 10, "MHP" : 750, "HP" : 750, "STR" : 100, "RES" : 3, "CRIT" : 6,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 03", get_fusion("Water Type 03")[1]], "moves" : {"Attack":0, "Rush":0}, "drops" : {"EXP" : 750, "Skill Cards" : ["Rush"], "Fusion Cards" : ["Water Type 03"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 15, "MHP" : 1000, "HP" : 1000, "STR" : 100, "RES" : 4, "CRIT" : 8,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 04", get_fusion("Water Type 04")[1]], "moves" : {"Bufula":0, "Attack":0}, "drops" : {"EXP" : 1000, "Skill Cards" : ["Bufula"], "Fusion Cards" : ["Water Type 04"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 20, "MHP" : 1250, "HP" : 1250, "STR" : 100, "RES" : 5, "CRIT" : 10,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 05", get_fusion("Water Type 05")[1]], "moves" : {"Megido":0, "Charge":0}, "drops" : {"EXP" : 1250, "Skill Cards" : ["Charge"], "Fusion Cards" : ["Water Type 05"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Fighter", "LVL" : 25, "MHP" : 1500, "HP" : 1500, "STR" : 100, "RES" : 6, "CRIT" : 12,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 06", get_fusion("Water Type 06")[1]], "moves" : {"Bufula":0, "Concentrate":0}, "drops" : {"EXP" : 1500, "Skill Cards" : ["Bufula"], "Fusion Cards" : ["Water Type 06"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 30, "MHP" : 1750, "HP" : 1750, "STR" : 100, "RES" : 7, "CRIT" : 14,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},   "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 07", get_fusion("Water Type 07")[1]], "moves" : {"Bufula":0, "Resist":0}, "drops" : {"EXP" : 1750, "Skill Cards" : ["Resist"], "Fusion Cards" : ["Water Type 07"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Guardian", "LVL" : 35, "MHP" : 2000, "HP" : 2000, "STR" : 100, "RES" : 8, "CRIT" : 16,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 08", get_fusion("Water Type 08")[1]], "moves" : {"Bufudyne":0, "Drain Energy":0}, "drops" : {"EXP" : 2000, "Skill Cards" : ["Drain Energy","Bufudyne"], "Fusion Cards" : ["Water Type 08"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Water Sentinel", "LVL" : 40, "MHP" : 2250, "HP" : 2250, "STR" : 100, "RES" : 9, "CRIT" : 18,"CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},  "buff" : {}, "debuff" : {}, "fusion" : ["Water Type 09", get_fusion("Water Type 09")[1]], "moves" : {"Bufubarion":0, "Megidola" : 0,"Charge":0,"Debilitate":0}, "drops" : {"EXP" : 2250, "Skill Cards" : ["Debilitate","Charge","Megidola","Bufubarion"], "Fusion Cards" : ["Water Type 09"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"},

    {"name" : "Mizu", "LVL" : 45, "MHP" : 10000, "HP" : 10000, "STR" : 100, "RES" : 10, "CRIT" : 20, "CRIT DMG" : 50, "EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, "buff" : {}, "debuff" : {}, "fusion" : ["Prototype: AQUA", get_fusion("Prototype: AQUA")[1]], "moves" : {"Water Boost":0, "Thalassic Calamity":0, "Bufubarion" : 0}, "drops" : {"EXP" : 10000, "Skill Cards" : ["Thalassic Calamity","Concentrate"], "Fusion Cards" : ["Prototype: AQUA"], "Support Items" : ["Hydro Bomb"]}, "weakness" : "Wind"}
     ]
  return enemies

def battle_charmslookup(charm):
    #Idea: passives that use stacks can be programmed via Buffs. Measure stacks using buff duration
    all_charms = {
        "CRIT DMG Charm" : {
            "stat" : "CRIT DMG",
            "amount" : 25,},
        "CRIT Charm" : {
            "stat" : "CRIT",
            "amount" : 5},
        "HP Charm" : {
            "stat" : "MHP",
            "amount" : 20},
        "ER Charm" : {
            "stat" : "ER",
            "amount" : 40},
        "Physical DMG Charm" : {
            "stat" : "Physical DMG",
            "amount" : 30},
        "Elemental DMG Charm" : {
            "stat" : "Elemental DMG",
            "amount" : 20},
        "DMG Charm" : {
            "stat" : "DMG",
            "amount" : 10},
        }

    name = charm
    if charm in all_charms: charm = all_charms[charm]
    else:   return {"name" : name, "stat" : "???", "amount" : 0, "desc" : ""}

    charm["name"] = name
    charm["desc"] = "Increases " + str(charm["stat"]) + " by " + str(charm["amount"])
    if charm["stat"] != "CRIT": charm["desc"] += "%"
    charm["desc"] += "."

    return charm

def battle_moveslookup(move):
  #Light, Weak, Medium, Heavy, Severe, Colossal
  #"Name : [BaseDMG, Range of hits, Type Offence/Defence/Heal, Buff/Debuff infliction, Element, Unique attribute]"
  all_moves = {"Nothing" : [0, [0,0], "Other", "None","",""]
                  #Healing
                  ,"Dia" : [50, [0,0], "Defence", "None","Heal",""]
                  ,"Diarama" : [150, [0,0], "Defence", "None","Heal",""]
                  ,"Diarahan" : [250, [0,0], "Defence", "None","Heal",""]
                  #Physical
                  , "Attack" : [90, [1,0], "Offence", "None","Physical",""]
                  ,"Thousand Slaps" : [10, [10,0], "Offence", "None","Physical",""]
                  ,"Lunge" : [100, [1,0], "Offence", "None","Physical","High Critical rate"]
                  ,"Megi" : [150, [1,0], "Offence", "None","Physical",""]
                  ,"Megido" : [175, [1,0], "Offence", "None","Physical",""]
                  ,"Megidola" : [200, [1,0], "Offence", "None","Physical",""]
                  ,"SPECIAL: Shining Arrows" : [50, [8,0], "Offence", "None","Physical",""]
                  #Water
                  ,"Bufu" : [90, [1,0], "Offence", "None","Water",""]
                  ,"Rush" : [50,[2,0], "Offence", "None","Water",""]
                  ,"Bufula" : [115, [1,0], "Offence", "None","Water",""]
                  ,"Bufudyne" : [130, [1,0], "Offence", "None","Water",""]
                  ,"Bufubarion" : [150, [1,0], "Offence", "None","Water",""]
                  ,"Thalassic Calamity" : [83, [3,0], "Offence", "None","Water",""]
                  ,"Striking Tide" : [25,[10,0], "Offence", "None","Water",""]
                  ,"SPECIAL: Hyperflood Abrasion" : [400,[1,0], "Offence", "None","Wind",""]
                  #Fire
                  ,"Agi" : [90, [1,0], "Offence", "None","Fire",""]
                  ,"Agilao" : [115, [1,0], "Offence", "None","Fire",""]
                  ,"Agidyne" : [130, [1,0], "Offence", "None","Fire",""]
                  ,"Agibarion" : [150, [1,0], "Offence", "None","Fire",""]
                  ,"Fire Dance" : [83, [3,0], "Offence", "None","Fire",""]
                  ,"Burning Hell" : [250, [1,0], "Offence", "None","Fire",""]
                  ,"SPECIAL: Cataclysm" : [40,[10,0], "Offence", "None","Fire",""]
                  #Wind
                  ,"Garu" : [90, [1,0], "Offence", "None","Wind",""]
                  ,"Garula" : [115, [1,0], "Offence", "None","Wind",""]
                  ,"Garudyne" : [130, [1,0], "Offence", "None","Wind",""]
                  ,"Garubarion" : [150,[1,0], "Offence", "None","Wind",""]
                  ,"Cyclone" : [31,[8,0], "Offence", "None","Wind",""]
                  ,"Wrath Tempest" : [100,[2,0], "Offence", "None","Wind",""]
                  ,"SPECIAL: Eye of the Storm" : [400,[1,0], "Offence", "None","Wind",""]
                  #Support
                  , "Debilitate" : [0, [0,0], "Offence", "Vulnerable","Debuff","Decreases opponent's RES"]
                  , "Concentrate" : [0, [0,0], "Defence", "Concentrated","Buff","Increases All DMG"]
                  , "Charge" : [0, [0,0], "Defence", "Charged","Buff","Increases Physical DMG"]
                  , "Wind Boost" : [0, [0,0], "Defence", "Wind Boost","Buff","Increases Wind DMG"]
                  , "Fire Boost" : [0, [0,0], "Defence", "Fire Boost","Buff","Increases Fire DMG"]
                  , "Water Boost" : [0, [0,0], "Defence", "Water Boost","Buff","Increases Water DMG"]
                  ,"Drain Energy" : [0, [0,0], "Offence", "Drained","Debuff","Decreases opponent's All DMG"]
                  ,"Resist" : [0, [0,0], "Defence", "Invulnerable","Buff","Increases RES"]
                  ,"Defend" : [0, [0,0], "Defence", "Defending","Buff","Increases RES"]
                  #Items
                  ,"Bead" : [300, [0,0], "Defence", "None","Heal",""]
                  ,"Healing Orb" : [100, [0,0], "Defence", "None","Heal",""]
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
  if move["element"] != "" and move["element"] != "Heal" and move["basedmg"] != 0:
    move["description"] += move["element"] + " DMG "
    if move["hits"] > 1:  move["description"] += "hits. "
    else: move["description"] += "hit. "
  elif move["element"] == "Heal":   move["description"] += move["element"]

  #Buff/Debuff infliction
  if move["affliction"] != "None":
    move["description"] += "Inflicts " + str(move["affliction"]) + " on"
    #Inflicted on opponent/self
    if move["type"] == "Offence": move["description"] += " opponent. "
    elif move["type"] == "Defence" or move["type"] == "Heal": move["description"] += " self. "

  #Unique attribute
  if move["unique"] != "":  move["description"] += str(move["unique"]) + ". "
      
  #Healing numbers
  if move["element"] == "Heal": move["basedmg"] * 2

  output = [move["name"],move["basedmg"], hits, move["type"],move["affliction"],move["element"],move["unique"],move["description"]]
    
  return output

def battle_applybuffs(buff, buffamount, bufftype, target):
    #Do not need to return anything because Object content is changed
    #If buff already in list, add onto it. Otherwise create and add onto it.
    if buff in target.stats[bufftype.lower()]:
        target.stats[bufftype.lower()][buff] += buffamount
        battle_damagetext(target,str(buff) + " +"+str(buffamount)+"!", colour[bufftype],"small")
    else:
        target.stats[bufftype.lower()][buff] = buffamount
        myMixer("hit_" + str(bufftype.lower()) + ".wav")
        battle_damagetext(target,str(buff) + " +"+str(buffamount)+"!", colour[bufftype],"medium")



def battle_changehp(target, amount, element, sound, limit,fontsize):
    myColour = colour[element]
    if element != "Heal":
        amount = -amount
        symbol = ""
    else:
        symbol = "+"
    
    
    #Do not need to return anything because Object content is changed
    battle_damagetext(target,str(symbol) + str(amount), myColour,fontsize)
    myMixer(sound)
    
    target.stats["HP"] += amount
    if target.stats["HP"] >= target.stats["MHP"] and limit == True:
        target.stats["HP"] = target.stats["MHP"]
    elif target.stats["HP"] < 0 and limit == True:
        target.stats["HP"] = 1

    if target.stats["HP"] < 0:
        target.stats["HP"] = 0
        

    #Changing combatent condition based on HP
    if target.stats["HP"] <= 0:
        target.condition = "Defeated"
        target.alive = False
        target.status = "dead"
    elif target.stats["HP"]/target.stats["MHP"] <= 30:
        target.condition = "Critical"
        target.alive = True
    else:
        target.condition = "Normal"
        target.alive = True


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
        moves[i] -= 1
        if moves[i] <= 0:
          moves[i] = 0

  return moves

def battle_bonuscheck(actor,target,data):
    bonus_values = {"MHP" : 0,"CRIT" : 0, "CRIT DMG" : 0, "STR" : 0, "RES" : 0, 'Physical DMG': 0, 'Fire DMG': 0, 'Water DMG': 0, 'Wind DMG': 0, 'All DMG': 0}
    if actor["name"] == player.stats["name"]:
        actor_person = player
        target_person = enemy
        bonus_values["ER"] = 0
    else:
        actor_person = enemy
        target_person = player
        

    #Fusion. 0=Name,1=Desc,2=Conditions and Bonuses
    fusion = get_fusion(actor["fusion"][0])
    for cond in fusion[2]:
        grant_bonus = False
        
        if cond == "Critical condition" and int((actor["HP"]/actor["MHP"])*100) <= 30:  grant_bonus = True
        elif cond == "Not critical condition" and int((actor["HP"]/actor["MHP"])*100) > 30:  grant_bonus = True
        elif cond == "Actor HP higher" and int((actor["HP"]/actor["MHP"])*100) > int((target["HP"]/target["MHP"])*100):  grant_bonus = True
        elif cond == "Target HP higher" and int((target["HP"]/target["MHP"])*100) > int((actor["HP"]/actor["MHP"])*100):  grant_bonus = True
        elif cond == "HP 60% higher" and int((actor["HP"]/actor["MHP"])*100) > 60:  grant_bonus = True
        elif cond == "HP 60% lower" and int((actor["HP"]/actor["MHP"])*100) < 60:  grant_bonus = True
        elif cond == "Crit" and data["crit"] and data["turn"] == actor["name"]:  grant_bonus = True
        elif cond == "Take crit" and data["crit"] and data["turn"] == target["name"]:  grant_bonus = True
        elif cond == "Hit" and data["hit"]>0 and data["turn"] == actor["name"]:  grant_bonus = True
        elif cond == "Take hit" and data["hit"]>0 and data["turn"] == target["name"]:  grant_bonus = True
        elif cond == "":    grant_bonus = True

        if grant_bonus:
            for bonus in fusion[2][cond]:
                if bonus != "Buff" and bonus != "Debuff":   bonus_values[bonus] += fusion[2][cond][bonus]
                elif bonus == "Buff":   battle_applybuffs(fusion[2][cond][bonus][0], 3, "Buff", actor_person)
                elif bonus == "Debuff":   battle_applybuffs(fusion[2][cond][bonus][0], 3, "Debuff", target_person)

    #Buffs and Debuffs
    for buff in actor["buff"]:
        info = get_buff(actor,target,buff)
        if info[1] != None:
            bonus_values[info[1]["Stat"]] += info[1]["Value"]
    for buff in actor["debuff"]:
        info = get_buff(actor,target,buff)
        if info[1] != None:
            bonus_values[info[1]["Stat"]] += info[1]["Value"]

    edmg = {
        "Physical" : bonus_values["Physical DMG"],
        "Fire" : bonus_values["Fire DMG"],
        "Water" : bonus_values["Water DMG"],
        "Wind" : bonus_values["Wind DMG"],
        "All" : bonus_values["All DMG"]}
    bonus_values.pop("Physical DMG")
    bonus_values.pop("Fire DMG")
    bonus_values.pop("Water DMG")
    bonus_values.pop("Wind DMG")
    bonus_values.pop("All DMG")
    bonus_values["EDMG"] = edmg

    return bonus_values
        
def get_buff(actor, target, buff):
    output = [buff, None,"desc"]
    #buff is the Buff to search for and return the corrosponding value of in output variable
    buffs = {
        "Debilitate" : {"Type":"Offence", "Buff" : "Vulnerable", "Stat" : "RES", "Value" : -20},
        "Concentrate" : {"Type":"Defence", "Buff" : "Concentrated", "Stat" : "All DMG", "Value": 20},
        "Charge" : {"Type":"Defence", "Buff" : "Charged", "Stat" : "Physical DMG", "Value": 60},
        "Wind Boost" : {"Type":"Defence", "Buff" : "Wind Boost", "Stat" : "Wind DMG", "Value": 40},
        "Fire Boost" : {"Type":"Defence", "Buff" : "Fire Boost", "Stat" : "Fire DMG", "Value": 40},
        "Water Boost" : {"Type":"Defence", "Buff" : "Water Boost", "Stat" : "Water DMG", "Value": 40},
        "Drain Energy" : {"Type":"Offence", "Buff" : "Drained", "Stat" : "All DMG", "Value": -20},
        "Resist" : {"Type":"Defence", "Buff" : "Invulnerable", "Stat" : "RES", "Value":  20},
        "Focus" : {"Type":"Defence", "Buff" : "Focused", "Stat" : "CRIT", "Value" : 20},
        "Overhype" : {"Type":"Defence", "Buff" : "Hyped", "Stat" : "CRIT DMG", "Value" : 40},
        "Overgrow" : {"Type":"Defence", "Buff" : "Overgrown", "Stat" : "MHP", "Value" : 20},
        "Awaken" : {"Type":"Defence", "Buff" : "Awakened", "Stat" : "All DMG", "Value" : 80},
        "Awaken II" : {"Type":"Defence", "Buff" : "Awakened One", "Stat" : "All DMG", "Value" : 80},
        "Blaze Shield" : {"Type":"Defence", "Buff" : "Blaze Shield", "Stat" : "MHP", "Value" : 60},
        "Pyroclastic Charge" : {"Type":"Defence", "Buff" : "Pyroclastic Charge", "Stat" : "Fire DMG", "Value" : int(actor["MHP"] * 0.015)},
        "Pyroclastic Surge" : {"Type":"Defence", "Buff" : "Pyroclastic Surge", "Stat" : "Fire DMG", "Value" : int(actor["MHP"] * 0.015)},
        "Inspire" : {"Type":"Defence", "Buff" : "Inspired", "Stat" : "Water DMG", "Value" : int(actor["RES"] * 2)}
        }

    for i in buffs:
        if i == buff or buff in buffs[i]["Buff"]:
            output[1] = buffs[i]
            #Make description
            output[2] = buffs[i]["Type"] + ". " + str(buffs[i]["Stat"]) + " "
            if buffs[i]["Value"] > 0:   output[2] += "+" + str(buffs[i]["Value"])
            else:   output[2] += str(buffs[i]["Value"])
            if buffs[i]["Stat"] == "CRIT DMG" or buffs[i]["Stat"] == "MHP" or buffs[i]["Stat"] == "Physical DMG" or buffs[i]["Stat"] == "Fire DMG" or buffs[i]["Stat"] == "Water DMG" or buffs[i]["Stat"] == "Wind DMG" or buffs[i]["Stat"] == "All DMG":
                output[2] += "%"
            break

    return output

def battle_energy(mhp,damage,er,eg,meg):
    #Percent of damage done to health, multiplied by Energy recharge
    amount = int(int(int((damage/mhp)*100))*(er/100))

    #Cannot exceed max limit
    if amount + eg >= meg:
        eg = meg
    else:
        eg += amount

    #Return new energy
    return eg

    

damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

#Main storage for player stats
player_stats = {'name': 'Byleth',
                          'weapon': 'Gold Sword',
                          'LVL': 40, 'MEXP': 100, 'EXP': 0,
                          'MHP': 2000,'HP': 2000,
                          'STR': 225, 'RES': 9, 'CRIT': 30, "CRIT DMG" : 50, "ER" : 100, "EG" : 0, "MEG" : 100,"EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0},
                          'buff': {}, 'debuff': {},
                          "charms" : {
                              "HP Charm" : battle_charmslookup("HP Charm"),
                              "ER Charm" : battle_charmslookup("ER Charm")},
                          'fusion': ["Wind Type 09", get_fusion("Wind Type 09")[1]],
                          'moves': {"Attack" : 0,"Cyclone":0, "Concentrate":0,"Debilitate":0,"Dia" : 0},
                          "weakness" : "Fire"}
enemy_stats = random.choice(get_enemies())

#Temporary stats for this battle
player = Fighter(screen_width/4, int(screen_height/2),player_stats)
enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)


def battle_createability(moves):
    #Creating buttons. Screen, width, height, image, size x, size y
    images = {"Physical" : img_physical,
              "Fire" : img_fire,
              "Water" : img_water,
              "Wind" : img_wind,
              "Heal" : img_heal,
              "Buff" : img_buff,
              "Debuff" : img_debuff}
    abilities = {}
    x_value = 0
    for ability in player.stats["moves"]:
        #Add the Button attribute to ability
        abilities[ability] = {
            "button" : button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), images[battle_moveslookup(ability)[5]], 70,70),
            "image" : images[battle_moveslookup(ability)[5]]}
        #Used for spacing out abilities on screen
        x_value += 80
    abilities["Skip"] = {"button" :button.Button(display, player.rect.x + x_value, screen_height - (screen_height/4), img_skip, 70,70),
                         "image" : img_skip}

    return abilities

abilities = battle_createability(player.stats["moves"])
            

#Create progressbars. Arguements are width and height
player_hp = ProgressBar(100,10)
player_eg = ProgressBar(100,10)
enemy_hp = ProgressBar(100,10)

#Create invisible circle effect
inviscircle = Battle_invisCircle(int(screen_width/2), int(screen_height/2), int(screen_height/2), 0, 1, 1)


player.status = "turn"
cooldown = framesrate
battle_turndata = ""

clicked = False

battle_action = "player"
selected = ""
screen_shake = 0
enemy_shake = 0

#Controls
controls = {
    "M_LCLICK" : False,
    "M_RCLICK" : False,
    "K_SPACE" : False,
    "K_RIGHT" : False}
    
        

battle_music(player.stats["MHP"], enemy.stats["MHP"], "Start")



#Running loop. 1 Loop = 1 Frame
running = True
while running:
    #clock tick
    clock.tick(framesrate)

    #Change rainbow colour
    colour_rainbowcycle()

    #gets mouse position
    mouse_pos = pygame.mouse.get_pos()

    #Update invis circle effect
    if (player.stats["HP"]/player.stats["MHP"])*100 <= 30:
        inviscircle.angular_velocity = 2
    elif battle_action == "Victory!" or battle_action == "Defeat!":
        inviscircle.angular_velocity = 0
    else:
        inviscircle.angular_velocity = 1
    inviscircle.update()
    inviscircle.draw()

    #Display images
    draw_background()

    #Update coords for battle status display and main colours
    if battle_action == "player" or battle_action == "Victory!":
        x = player.rect.x
        y = player.rect.y
        if "SPECIAL" in selected:   myColour = colour["rainbowcycle"]
        else:   myColour = colour["green"]
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

    #Top and bottom borders for effect
        #Black
    size = 140
    box3 = pygame.Rect(0, 0, screen_width, size)
    pygame.draw.rect(display, colour["black"], box3)
    box4 = pygame.Rect(0, screen_height-size, screen_width, size)
    pygame.draw.rect(display, colour["black"], box4)
        #Coloured
    size = 20
    box = pygame.Rect(0, 0, screen_width, size)
    pygame.draw.rect(display, myColour, box)
    box2 = pygame.Rect(0, screen_height-size, screen_width, size)
    pygame.draw.rect(display, myColour, box2)

    #display battle status
    x,y = mouse_hovereffect(x,y)
    draw_text(str(battle_action).upper(), fonts["verylarge"], myColour, x, y-100, True)
    #display selected ability
    x,y = mouse_hovereffect(x,screen_height - (screen_height/4))
    draw_text(str(selected).upper(), fonts["large"], myColour, x, y + 80, True)
    draw_text(str(battle_moveslookup(selected)[-1]).upper(), fonts["dmgsmall"], myColour, x, y + 170, True)


    #Display players
    if player.alive:
        player.update()
        x,y = mouse_hovereffect(screen_width/4, int(screen_height/2))
        player.draw(x,y)

    if enemy.alive:
        enemy.update()
        x,y = mouse_hovereffect(screen_width-(screen_width/4),int(screen_height/2))
        #Add screen shake
        if enemy_shake > 0:
            enemy_shake -= 1
            shake_x, shake_y = image_shake(int(battle_turndata["totaldmg"]/enemy.stats["MHP"]*40))
        else:   shake_x, shake_y = 0,0
        enemy.draw(x+shake_x,y+shake_y)

    #Player and enemy stats
    x,y = mouse_hovereffect(30,30)
    draw_stats(player,x,y)
    x,y = mouse_hovereffect(screen_width-(screen_width/6),30)
    draw_stats(enemy,x,y)

    #Player and enemy health bars
    draw_health(player,player_hp, mouse_pos)
    draw_health(enemy,enemy_hp, mouse_pos)


    
    #damage text
    damage_text_group.update()
    damage_text_group.draw(display)

    #projectiles
    projectile_group.update()
    projectile_group.draw(display)

    #actions
    action = ""
    
    

    if battle_action == "player":
        #For spacing between buttons
        x_value = 0
        for move in player.stats["moves"]:
            if "SPECIAL" in move and player.stats["EG"] != player.stats["MEG"]:
                continue
            elif "SPECIAL" in move and player.stats["EG"] == player.stats["MEG"]:
                myColour = "rainbowcycle"
            else:
                myColour = "green"
            #Display the ability button
            x,y = mouse_hovereffect(player.rect.x + x_value, screen_height - (screen_height/4))
            ability_clicked = abilities[move]["button"].draw(x,y) #(Returns True if button is pressed)
            x_value += 80
            #Display cooldown if > 0, otherwise display READY
            if player.stats["moves"][move] > 0:
                pygame.draw.rect(display, colour["white"], (abilities[move]["button"].rect.x-1, abilities[move]["button"].rect.y-1, abilities[move]["button"].rect.width+1, abilities[move]["button"].rect.height+1), 3)
                draw_text(str(player.stats["moves"][move]), fonts["small"], colour["white"], abilities[move]["button"].rect.topleft[0]+3, abilities[move]["button"].rect.topleft[1]+3, False)
            else:   draw_text("READY", fonts["small"], colour[myColour], abilities[move]["button"].rect.topleft[0]+3, abilities[move]["button"].rect.topleft[1]+3, False)

            #Display ability descriptionif mouse hovering over ability button
            if abilities[move]["button"].hover() == True and selected == "" and battle_action == "player":
                draw_text(str(move.upper())+ " # -" + str(battle_moveslookup(move)[7]), fonts["small"], colour["green"], abilities[move]["button"].rect.x, abilities[move]["button"].rect.y + abilities[move]["button"].rect.width, True)
    
            #If button pressed + Ability cooldown 0 + Player's turn = Can select and perform ability.
            if ability_clicked and selected != move:
                if player.stats["moves"][move] <= 0:
                    myMixer("menu_enter.wav")
                    selected = str(move)
                    break
                else:
                    myMixer("menu_invalid.wav")
            #If ability already selected and they click button again, perform ability
            elif ability_clicked and selected == move:
                if player.stats["moves"][move] <= 0:
                    myMixer("menu_enter.wav")
                    action = selected
                    break
                else:
                    myMixer("menu_invalid.wav")

            #Draw outline over selected ability
            if move == selected and battle_action == "player":
                if "SPECIAL" in selected:   myColour = colour["rainbowcycle"]
                else:   myColour = colour["green"]
                pygame.draw.rect(display, myColour, (abilities[move]["button"].rect.x-1, abilities[move]["button"].rect.y-1, abilities[move]["button"].rect.width+1, abilities[move]["button"].rect.height+1), 3)


        

        #Display skip button at the end
        x,y = mouse_hovereffect(player.rect.x + x_value, screen_height - (screen_height/4))
        skip_clicked = abilities["Skip"]["button"].draw(x,y)
        if skip_clicked:
            myMixer("menu_back.wav")              
            selected = "Skip"
        #Display skip if hovering over Skip button
        if abilities["Skip"]["button"].hover() and selected == "" and battle_action == "player":
                draw_text("Skip turn", fonts["small"], colour["green"], abilities["Skip"]["button"].rect.x, abilities["Skip"]["button"].rect.y + abilities["Skip"]["button"].rect.width, True)

        #Display fusion and buffs/debuffs if hovering over Character
        if player.rect.collidepoint(mouse_pos) and selected == "":
            pygame.mouse.set_visible(False)
            draw_text(str(player.stats["fusion"][0].upper()) + " # " + player.stats["fusion"][1], fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)
        
            #if len(player.stats["buff"]) > 0:   draw_text("Buffs: " + str(player.stats["buff"]), fonts["small"], colour["Buff"], pygame.mouse.get_pos()[0] + lineskip + 20, pygame.mouse.get_pos()[1], False)
            #if len(player.stats["debuff"]) > 0:   draw_text("Debuffs: " + str(player.stats["debuff"]), fonts["small"], colour["Debuff"], pygame.mouse.get_pos()[0] + lineskip + 40, pygame.mouse.get_pos()[1], False)
        elif enemy.rect.collidepoint(mouse_pos) and selected == "":
            pygame.mouse.set_visible(False)
            draw_text(str(enemy.stats["fusion"][0].upper()) + " # " + str(enemy.stats["fusion"][1]), fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)

            #if len(enemy.stats["buff"]) > 0:   draw_text("Buffs: " + str(enemy.stats["buff"]), fonts["small"], colour["Buff"], pygame.mouse.get_pos()[0] + lineskip + 20, pygame.mouse.get_pos()[1], False)
            #if len(enemy.stats["debuff"]) > 0:   draw_text("Debuffs: " + str(enemy.stats["debuff"]), fonts["small"], colour["Debuff"], pygame.mouse.get_pos()[0] + lineskip + 40, pygame.mouse.get_pos()[1], False)
        else:   pygame.mouse.set_visible(True)
            
        #Conditions to perform action (mouse on enemy, its your turn, ability selected, etc. Some conditions to not apply to some moves.)
        if enemy.rect.collidepoint(mouse_pos) and battle_action == "player" and selected != "" and battle_moveslookup(selected)[3] == "Offence":
            draw_text("CONFIRM?", fonts["small"], colour["red"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 20, False)
            if controls["M_LCLICK"]:
                action = selected
        elif player.rect.collidepoint(mouse_pos) and battle_action == "player" and selected != "" and battle_moveslookup(selected)[3] == "Defence":
            draw_text("CONFIRM?", fonts["small"], colour["green"], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 20, False)
            if controls["M_LCLICK"]:
                action = selected
        elif selected == "Skip":
            action = selected
    elif battle_action == "enemy":
        if selected == "":
            #Enemy AI
            selected = "Skip"
            for move in enemy.stats["moves"]:
                if enemy.stats["moves"][move] <= 0:    selected = move

    #cooldown makes turns not instant/1 frame long
    cooldown -= 1
    if cooldown <= 0:
        #Allows combatents to perform actions
        if battle_action == "player" and player.alive and action != "":
            player.status = "move"
            battle_turndata = player.move(action, enemy)
            #Increases cooldown if action completed
            if action != "Skip":   player.stats["moves"][action] = 5
            battle_action = "neutral"

            if battle_turndata["hit"] > 0:
                enemy_shake = framesrate/10
                if int((battle_turndata["totaldmg"]/battle_turndata["target"].stats["MHP"])*100) >= 10:
                    enemy.status = "hurt"
            cooldown = framesrate
            
        elif battle_action == "enemy" and enemy.alive:
            #Increases cooldown if action completed
            if selected != "Skip":   enemy.stats["moves"][selected] = 5
            action = selected
            enemy.status = "move"
            battle_turndata = enemy.move(action, player)
            battle_action = "neutral"
            
            if battle_turndata["hit"] > 0:
                screen_shake = framesrate/10
                if int((battle_turndata["totaldmg"]/battle_turndata["target"].stats["MHP"])*100) >= 10:
                    player.status = "hurt"
                
            cooldown = framesrate
        
            
        elif battle_action == "neutral":
            #Decrease CD
            player.stats["moves"] = battle_movecd(player.stats["moves"])
            enemy.stats["moves"] = battle_movecd(enemy.stats["moves"])
            
            #Detects action completion ("move"). Passes over turn. Crits give combatents extra turns
            #Determines battle outcome
            if battle_turndata["actor"].stats["HP"] <= 0 and battle_turndata["actor"].stats["name"] == player.stats["name"] or battle_turndata["target"].stats["HP"] <= 0 and battle_turndata["target"].stats["name"] == player.stats["name"]:
                battle_action = "Defeat!"
                battle_music(player.stats["MHP"], enemy.stats["MHP"], "End")
            elif battle_turndata["actor"].stats["HP"] <= 0 and battle_turndata["actor"].stats["name"] == enemy.stats["name"] or battle_turndata["target"].stats["HP"] <= 0 and battle_turndata["target"].stats["name"] == enemy.stats["name"]:
                battle_action = "Victory!"
                battle_music(player.stats["MHP"], enemy.stats["MHP"], "End")
            #Regular turn
            elif (battle_turndata["actor"].stats["name"] == enemy.stats["name"] and battle_turndata["critamount"] == 0):
                myMixer("menu_turn.wav")
                player.status = "turn"
                enemy.status = "idle"
                battle_action = "player"
            #1 more turn after crit
            elif (battle_turndata["actor"].stats["name"] == player.stats["name"] and battle_turndata["critamount"] > 0):
                myMixer("menu_1more.wav")
                player.status = "turn"
                enemy.status = "idle"
                battle_action = "player"
            elif (battle_turndata["actor"].stats["name"] == player.stats["name"] and battle_turndata["critamount"] == 0) or (battle_turndata["actor"].stats["name"] == enemy.stats["name"] and battle_turndata["critamount"] > 0):
                player.status = "idle"
                enemy.status = "turn"
                battle_action = "enemy"
            selected = ""
                

            cooldown = framesrate
        

    trigger = False
    if controls["M_LCLICK"]:
        cooldown = 0
    elif controls["M_RCLICK"]:
        if battle_action == "player" and selected != "":
            selected = ""
            myMixer("menu_back.wav")
    elif controls["K_SPACE"]:
        enemy_stats = random.choice(get_enemies())
        trigger = True
    elif controls["K_RIGHT"]:
        name = ""
        while name != "Hi" and name != "Kaze" and name != "Mizu":
            enemy_stats = random.choice(get_enemies())
            name = enemy_stats["name"]
        trigger = True

    if trigger and player.status != "idle":
        enemy = Fighter(screen_width-(screen_width/4), int(screen_height/2),enemy_stats)
        player_stats = {'name': 'Byleth',
                  'weapon': 'Sacrificial Fragments',
                  'LVL': 40, 'MEXP': 100, 'EXP': 0,
                  'MHP': 2000,'HP': 2000,
                  'STR': 225, 'RES': 9, 'CRIT': 30, "CRIT DMG" : 50, "ER" : 100, "EG" : 0, "MEG" : 100,"EDMG" : {"Physical" : 0, "Fire" : 0, "Water" : 0, "Wind" : 0, "All" : 0}, 
                  'buff': {}, 'debuff': {},
                  "charms" : {
                      "HP Charm" : battle_charmslookup("HP Charm"),
                      "ER Charm" : battle_charmslookup("ER Charm")},
                  'fusion': ["Prototype: GALE", get_fusion("Prototype: GALE")[1]],
                  'moves': {"Attack" : 0,"Cyclone":0,"Garubarion":0,"SPECIAL: Eye of the Storm":0, "Concentrate":0,"Debilitate":0,"Dia" : 0},
                  "weakness" : "Fire"}
        player = Fighter((screen_width/4), int(screen_height/2),player_stats)
        
        abilities = battle_createability(player.stats["moves"])
        player.status = "turn"
        enemy.status = "idle"
        battle_music(player.stats["MHP"], enemy.stats["MHP"], "Start")
        battle_action = "player"
        base_stats = {str(player_stats["name"]) : player_stats, str(enemy_stats["name"]) : enemy_stats}

    display_offset = [0,0]
    if screen_shake>0:
        screen_shake -= 1
        display_offset = image_shake(int((battle_turndata["totaldmg"]/battle_turndata["target"].stats["MHP"])*10)*2)
            
    screen.blit(display,display_offset)


    #For events happening in the pygame
    for event in pygame.event.get():
        #If window X clicked
        if event.type == pygame.QUIT:
            running = False

        #Controls
        controls = {
            "M_LCLICK" : False,
            "M_RCLICK" : False,
            "K_SPACE" : False,
            "K_RIGHT" : False}
        #If left mouse button clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                controls["M_LCLICK"] = True
            #Right mouse button
            if event.button == 3:
                controls["M_RCLICK"] = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                controls["K_SPACE"] = True
            elif event.key == pygame.K_RIGHT:
                controls["K_RIGHT"] = True
                
    pygame.display.update()
    
#Terminate
if running == False:
    pygame.quit()
    quit()





    
