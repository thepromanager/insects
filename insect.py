import pygame
import random
import math
import noise
import os

#insekt: sprite
#för varje lager loopa igenom och välj färger
#sedan symmetri

# GLOBAL
global gameDisplay
gameDisplay = pygame.display.set_mode((32*32, 32*18))
factor = 4

# LOAD IMAGES
heads=[]
bodies=[]
wings=[]
legs=[]
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 1_"+str(i)+".png"))
    heads.append(image)
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 2_"+str(i)+".png"))
    bodies.append(image)
for i in range(4):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 3_"+str(i)+".png"))
    wings.append(image)
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 4_"+str(i)+".png"))
    legs.append(image)



# FUNCTIONS
def randomColors():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
def determineColors():
    return [[0,0,0],randomColors(),randomColors(),random.choice([[255,0,0],[255,255,0],[0,255,255]])]
def getColor(x,y,image,colors):
    a=colors[0]
    b=colors[1]
    c=colors[2]
    d=colors[3]
    e=[]
    possbileColors=[]
    imageColor=image.get_at((x,y))
    if(imageColor==(0,0,0,255)): # border
        possbileColors=[a]
    elif(imageColor==(0,0,255,255)): # primary color
        possbileColors=[b]
    elif(imageColor==(0,255,255,255)): # light blend
        possbileColors=[b,c]
    elif(imageColor==(0,255,0,255)): # secondary color
        possbileColors=[c]
    elif(imageColor==(200,200,200,255)): # abc + empty
        possbileColors=[a,b,c,e]
    elif(imageColor==(100,100,100,255)): # abc
        possbileColors=[a,b,c]
    elif(imageColor==(255,0,0,255)): # eyes
        possbileColors=[d]
    elif(imageColor==(255,255,0,255)): # primary or secondary
        possbileColors=[b,c]
    elif(imageColor==(255,0,255,255)): # border / empty
        possbileColors=[a,e]
    elif(imageColor==(0,0,0,0)): # dont color
        return []
    else:
        print(imageColor)
    return random.choice(possbileColors)

def createSprite(posx,posy):
    h=16
    w=16
    colors=determineColors()
    sprite=pygame.Surface((h,w))
    sprite.fill([100]*3)
    for layer in range(4):
        image=None
        if(layer==0):
            image=random.choice(legs)
            if(random.random()>0.9):
                image=None
        elif(layer==1):
            image=random.choice(wings)
            if(random.random()>0.3):
                image=None
        elif(layer==2):
            image=random.choice(bodies)
        elif(layer==3):
            image=random.choice(heads)
        if(image):
            for y in range(h):
                for x in range(w//2):
                    c=getColor(x,y,image,colors)
                    if(c):
                        sprite.set_at((x,y),c)
                        sprite.set_at((w-x-1,y),c)
    sprite=pygame.transform.scale(sprite,(w*factor,h*factor))
    gameDisplay.blit(sprite,(posx+w*factor/2,posy+h*factor/2))
    #return sprite

#DRAW LOOP
jump_out = False
changed=0
while jump_out == False:
    bg_color=100
    if changed==0:
        gameDisplay.fill([bg_color]*3)
        for x in range(int(int(32*4/16)*4/factor)):
            for y in range(int(int(32*4/16)*0.6*4/factor)):
                createSprite(32*32*x/int(int(32*4/16)*4/factor),32*18*y/int(int(32*4/16)*0.6*4/factor))
    changed = 1
    jump_out = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True
    if jump_out:
        pygame.display.quit()
        quit()
    pygame.display.update()
    

pt.end_program() 

