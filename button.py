import pygame 

#button class
class Button():
        def __init__(self, surface, x, y, image, size_x, size_y):
                self.size_x = size_x
                self.size_y = size_y
                self.image = pygame.transform.scale(image, (size_x, size_y))
                self.rect = self.image.get_rect()
                self.rect.topleft = (x, y)
                self.clicked = False
                self.surface = surface
                self.hovering = False

        def draw(self,x,y,image):
                if image != "":
                        self.image = image
                        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
                        self.rect = self.image.get_rect()
                        self.rect.topleft = (x,y)
                elif x != "" and y != "":
                        self.rect.x = x
                        self.rect.y = y
                        
                action = False

                #get mouse position
                pos = pygame.mouse.get_pos()

                #check mouseover and clicked conditions
                if self.rect.collidepoint(pos):
                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                                action = True
                                self.clicked = True

                if pygame.mouse.get_pressed()[0] == 0:
                        self.clicked = False

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
                                
