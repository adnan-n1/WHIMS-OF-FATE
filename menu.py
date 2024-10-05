import pygame
import random
import time
import button

#pygame.mixer.pre_init(44100, -16, 2, 2048)
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
fonts={"small":pygame.font.SysFont("Calbri", 26),
       "dmgsmall":pygame.font.SysFont("Franklin Gothic Medium Cond", 39),
       "medium":pygame.font.SysFont("Franklin Gothic Medium Cond", 58),
       "large":pygame.font.SysFont("Franklin Gothic Medium Cond", 84),
       "verylarge":pygame.font.SysFont("Franklin Gothic Medium Cond", 110)}

colour = {"red" : (255, 0, 0), "green" : (0, 255, 0), "white" : (255,255,255), "black" : (0,0,0),"grey" : (100,100,100), "rainbowcycle" : (255,0,0),
          "Fire" : (247, 65, 15), "Water" : (10, 86, 240), "Wind" : (48, 242, 129), "Physical" : (200, 200, 200),
          "Buff" : (66, 135, 245), "Debuff" : (162, 78, 222), "Heal" : (0, 255, 0)}

background = pygame.image.load("img/Background/background.jpg").convert_alpha()

#background display
def draw_background():
    display.blit(background, (0,0))

def menu_main(x,y):
    options = {"Play" : "", "Options" : "", "Quit" : ""}
    x_value = 0
    
    for option in options:
        box = pygame.Rect(x, y, 200, 200)
        box_surface = display.subsurface(box)
        box_surface.fill(colour["grey"])
        options[option] = {
            "button" : button.Button(display, x + x_value, y, box_surface, 200,200),
            }
        #Used for spacing out abilities on screen
        x_value += 80
        
    return options
    

running = True
buttons = menu_main(screen_width/2,screen_height/2)

while running:
    #clock tick
    clock.tick(framesrate)

    #Display images
    draw_background()

    x_value = 0
    x, y = screen_width/2,screen_height/2
    for option in buttons:
        if buttons[option]["button"].draw(x+x_value,y):
            print("Clicked!")
        elif buttons[option]["button"].hover():
            print("Hover!")
        x_value += buttons[option]["button"].rect.width + 10

    screen.blit(display,(0,0))
    pygame.display.update()

#Terminate
if running == False:
    pygame.quit()
    quit()
    
