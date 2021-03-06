import pygame
import random
import math
import os
import insectart2
#länkningsbara färger
#alternerandep



# GLOBAL
global gameDisplay
gameDisplay = pygame.display.set_mode((32*32, 32*18))
factor = 3
size=32

# LOAD IMAGES
heads=[]
bodies=[]
wings=[]
legs=[]
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 1_"+str(i)+".png"))
    heads.append(image)
for i in range(7):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 2_"+str(i)+".png"))
    bodies.append(image)
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 3_"+str(i)+".png"))
    wings.append(image)
for i in range(5):
    image = pygame.image.load(os.path.join("blueprints", "blueprint_Animation 4_"+str(i)+".png"))
    legs.append(image)



# FUNCTIONS
def randomColors():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
def determineColors():
    darkColor=[random.randint(0,50),random.randint(0,50),random.randint(0,50)]
    lightColor=[100+random.randint(0,155),100+random.randint(0,155),100+random.randint(0,155)]
    return [darkColor,randomColors(),randomColors(),random.choice([[255,0,0],[255,255,0],[0,255,255]]),lightColor]
def getColor(x,y,image,colors):
    a=colors[0]
    b=colors[1]
    c=colors[2]
    d=colors[3]
    f=colors[4]
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
        possbileColors=[a,b,c,e,e,e]
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

def createSprite():
    h=size
    w=size
    colors=determineColors()
    sprite=pygame.Surface((h,w))
    sprite.fill([100]*3)
    for layer in range(4):
        image=None
        if(layer==0):
            image=random.choice(legs)
            if(random.random()<0.1):
                image=None
        elif(layer==1):
            image=random.choice(wings)
            if(random.random()<0.7):
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
    return sprite

#DRAW LOOP
if __name__=="__main__":
    jump_out = False
    changed=0
    while jump_out == False:
        bg_color=100
        if changed==0:
            gameDisplay.fill([bg_color]*3)
            for x in range(int(32*32/(factor*size))):
                for y in range(int(32*18/(factor*size))):
                    sprite=createSprite()
                    gameDisplay.blit(sprite,(int((x-0.5)*factor*size)+size*factor/2,int((y-0.5)*factor*size)+size*factor/2))
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

