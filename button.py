import pygame 

#button class
class Button():
        def __init__(self, surface, x, y, image, size_x, size_y,key=""):
                self.key = key#key that can also be pressed to trigger this button
                self.size_x = size_x
                self.size_y = size_y
                self.image = pygame.transform.scale(image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.topleft = (x, y)
                self.clicked_m = False
                self.clicked_k = False
                self.surface = surface
                self.hovering = False

        def draw(self,x,y,image,keyboard=[]):
                if image != "":
                        self.image = image
                        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
                        self.rect = self.image.get_rect()
                        self.rect.topleft = (x,y)
                elif x != "" and y != "":
                        self.rect.x = x
                        self.rect.y = y
                        
                action = False
                keyboard = self.key in keyboard#BOOL

                #get mouse position
                pos = pygame.mouse.get_pos()

                if keyboard and self.clicked_k == False:
                        action = True
                        self.clicked_k = True
                #check mouseover and clicked conditions
                if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked_m == False:
                        action = True
                        self.clicked_m = True


                if pygame.mouse.get_pressed()[0] == 0:
                        self.clicked_m = False
                if keyboard == False:
                        self.clicked_k = False

                #draw button
                self.surface.blit(self.image, (self.rect.x, self.rect.y))

                return action
        def hover(self):    
                return self.rect.collidepoint(pygame.mouse.get_pos())
        def scale(self,width,height):
                self.size_x = width
                self.size_y = height
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
                self.rect = self.image.get_rect()
                                
