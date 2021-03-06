import pygame
import random
import time
import math

WIDTH=32
HEIGHT=32
SQUARESIZE=32
factor=3
def createSprite():
    spriteSurface = pygame.Surface((32, 32), pygame.SRCALPHA)
    samplePig = Insect()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if samplePig.art[y][x]:
                spriteSurface.set_at((x, y), samplePig.art[y][x])
    sprite=pygame.transform.scale(spriteSurface,(WIDTH*factor,HEIGHT*factor))
    return sprite


def distort(color, strength=30):
    move = lambda x: max(0,min(255,x+random.random()*strength-random.random()*strength))
    a,b,c = color
    return (move(a),move(b),move(c))

class Insect():

    def __init__(self, ):
        self.art = []
        for i in range(HEIGHT):
            self.art.append([False]*WIDTH)
        self.baseColor = (random.random()*255, random.random()*255, random.random()*155)
        self.legColor = (random.random()*55, random.random()*55, random.random()*55)
        self.eyeColor = (200+random.random()*55, 200+random.random()*55, random.random()*55)
        self.hasWings = random.randint(1,1)
        if self.hasWings:
            self.wingColor = (100+random.random()*155, 100+random.random()*155, 100+random.random()*155)

        self.generateArt()

    def generateExtremity(self, legColor, y, length=6, thick=0):
        legX = WIDTH//2-2
        legY = HEIGHT//2+y
        for i in range(length):

            tempColor = distort(legColor, strength=40) #main distortion
            self.art[legY][legX] = distort(tempColor, strength=15) #some additional left/right distortion
            self.art[legY][WIDTH-legX-1] = distort(tempColor, strength=15)
            if thick and legY<HEIGHT-1:
                tempColor = distort(legColor, strength=40) #main distortion
                self.art[legY+1][legX] = distort(tempColor, strength=15) #some additional left/right distortion
                self.art[legY+1][WIDTH-legX-1] = distort(tempColor, strength=15)


            legX= max(0, min(WIDTH//2 -1, legX+random.choice([-1,0,1])))
            legY= max(0, min(HEIGHT -1, legY+random.choice([-1,0,1])))

    def generateArt(self):
        self.generateExtremity(self.legColor, -2)
        self.generateExtremity(self.legColor, 1)
        self.generateExtremity(self.legColor, 4)

        for y in range(HEIGHT):
            for x in range(WIDTH//2): #rounded up
                dx = abs(x-WIDTH//2)
                dy = abs(y-HEIGHT//2)
                densityFunction = lambda DX,DY: 1 - (4*DX**2 + DY**2)*0.02
                if random.random()<densityFunction(dx,dy):
                    tempColor = distort(self.baseColor, strength=40) #main distortion
                    self.art[y][x] = distort(tempColor, strength=15) #some additional left/right distortion
                    self.art[y][WIDTH-x-1] = distort(tempColor, strength=15)

        self.generateExtremity(self.wingColor, 1, length = 20, thick=1)
        self.generateExtremity(self.eyeColor, -4, length = 3)

   
    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.art[y][x]:
                    pygame.draw.rect(gameDisplay, self.art[y][x], (x*SQUARESIZE, y*SQUARESIZE, SQUARESIZE, SQUARESIZE), 0)

if __name__ == "__main__":

    insect = Insect()
    gameDisplay = pygame.display.set_mode((SQUARESIZE*WIDTH, SQUARESIZE*HEIGHT))#(1540, 800))
    jump_out = False
    while jump_out == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jump_out = True
               
        pressed = pygame.key.get_pressed()

        if(pressed[pygame.K_a]):
            insect = Insect()
             
        gameDisplay.fill((0, 0, random.random()*50+100))
        insect.draw()
       
        pygame.display.update()
       
    pygame.quit()
    quit()