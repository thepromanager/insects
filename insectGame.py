import pygame
import pygame_gui
import random
import math
import insect as insectart
import types
import time
import json
import inspect

pygame.init()
screenSize=(1200,700)
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(screenSize)

background = pygame.Surface(screenSize)
background.fill(pygame.Color('#FFFFFF'))

managers={
    "":pygame_gui.UIManager(screenSize), #Main menu
    "f":pygame_gui.UIManager(screenSize), #Fight
    "i":pygame_gui.UIManager(screenSize), #Inspection
    "a":pygame_gui.UIManager(screenSize), #Altar
    "m":pygame_gui.UIManager(screenSize), #Movelist
    "w":pygame_gui.UIManager(screenSize), #Win
    }
#overlay=pygame_gui.UIManager(screenSize)

factor = 3
size=32
scientificHash={}
with open('insectscientificName4.json', 'r') as f:
    scientificHash = json.load(f)
vernacularHash={}
with open('insectvernacularName4.json', 'r') as f:
    vernacularHash = json.load(f)

class World():
    def __init__(self):
        self.day = 0
        self.mode = ""
        self.buttonMode="action" # action // target // inspect
        self.active=None
        self.enemies=[]
        self.allies=[]
        self.lootInsect=None
        self.scientificHash={} 
world=World()

class Action():
    def __init__(self,owner,activateFunction):
        self.owner=owner
        self.name=activateFunction.__name__.capitalize()
        self.targetRequired=True
        self.isBad=True
        self.target=None
        self.activate=types.MethodType(activateFunction, self)
    def generateAction(self):
        pass

#Fling  Bash Prick Pound DashSlashthwack amputate splice skewer scar
def pummel(self):
    if(self.owner in world.allies):
        for enemy in world.enemies:
            enemy.hurt(max(1,self.owner.strength-2))
    else:
        for ally in world.allies:
            ally.hurt(max(1,self.owner.strength-2))
def lick(self):
    self.target.hurt(0)
    self.target.poison+=2
def tackle(self):
    self.target.hurt(self.owner.strength) # stun
def slam(self):
    self.target.hurt(self.owner.strength*2) # +2?
    self.owner.hurt(4)
def dash(self):
    self.target.hurt(1+self.owner.speed//4,2) # stun
def duel(self):
    if(self.owner.speed>self.target.speed and self.owner.strength>self.target.strength):
        self.target.hurt(6,3)
    else:
        self.target.hurt(2)         
def charge(self):
    self.target.hurt(self.owner.strength//2+self.owner.speed//5)
def sting(self):
    self.target.hurt(2,3)
    if(self.target.poison<1):
        self.target.poison+=1
def prick(self):
    self.target.hurt(2,2)
    self.target.hurt(2,2)
def bite(self):
    self.target.hurt(2)
    self.owner.hp=min(self.owner.hp+max(0,2-target.defense), self.owner.maxhp)
def heal(self):
    self.owner.hp=min(self.owner.hp+4, self.owner.maxhp)
actionPool = [
    [lick],
    [tackle],
    [slam],
    [dash],
    [duel],
    [charge],
    [sting],
    [prick],
    [bite],
    [pummel, ("targetRequired", False)],
    [heal, ("targetRequired", False)],
]

class Insect():
    def __init__(self):
        self.alive=True
        self.image=insectart.createSprite()        
        self.setActions()
        self.determinedAction=None
        self.speed=random.randint(1,20)
        self.maxhp=random.randint(10,30)       
        self.defense=random.randint(0,random.randint(0,2))
        self.strength=random.randint(2,6)
        self.poison=0
        self.stun=0
        self.hp=self.maxhp        
        self.setAttributes()
        self.createName()
        #self.level=lvl
    def setActions(self):
        self.actions=[]
        actionTemplates=random.sample(actionPool, 2)
        for actionTemplate in actionTemplates:
            action = Action(self,actionTemplate[0])
            for keyWord in actionTemplate[1:]:
                setattr(action,keyWord[0],keyWord[1])
            self.actions.append(action)
    def hurt(self,damage,pierce=0):
        self.hp-=max(damage-max(self.defense-pierce,0),0)+self.poison
    def setAttributes(self):
        self.attributeHash={}
        attributeList=["speed","maxhp","defense","strength","poison","stun"]
        for attr in attributeList:
            self.attributeHash[attr]=getattr(self,attr)
    def resetAttributes(self):
        for attr in self.attributeHash:
            setattr(self,attr,self.attributeHash[attr]) 
        self.poison=0
        self.hp=self.maxhp
    def createName(self):
        self.name=""
        self.species=""
        length=4
        name=""
        letter=random.choice(vernacularHash[""])
        while letter != "end":
            name+=letter
            letter=random.choice(vernacularHash[name[-length:]])
        self.name=name
        species=""
        letter=random.choice(scientificHash[""])
        while letter != "end":
            species+=letter
            letter=random.choice(scientificHash[species[-length:]])
        self.species=species
        #a = ["Skr", "Gn", "Ghr","Kr","Br"]
        #b = ["ee","ooh","ie","ig","ix"]
        #return random.choice(a)+random.choice(b)
    def description(self):
        desc = ""
        desc+= "Name: "+str(self.name)+"<br>"
        desc+= "Species: "+str(self.species)+"<br>"
        desc+= "HP: "+str(self.hp)+" / "+str(self.maxhp)+"<br>"
        desc+= "Speed: "+str(self.speed)+"<br>"
        desc+= "Strength: "+str(self.strength)+"<br>"
        desc+= "Defense: "+str(self.defense)+"<br>"
        desc+= " <br>Attacks: <br>"
        for a in self.actions:
            desc+=a.name+"<br>"
        if(self.poison):
            desc+= " <br>Poisoned: "+str(self.poison)+"<br>"
        return desc

world.allies.append(Insect())
# Main
day_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 25), (200, 75)),html_text="Days ahead so long",manager=managers[""])
fight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (200, 50)),text='Fight ye Foes',manager=managers[""])
inspect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 350), (200, 50)),text='Inspect ye Insects',manager=managers[""])
altar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 425), (200, 50)),text='Sacrifice ye Mates',manager=managers[""])
moveset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 500), (200, 50)),text="Understand Brawlin'",manager=managers[""])

#health_window = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((450, 275), (size*factor, size*factor)),manager=managers[""],image_surface=Insect().image)

# Fight
enemy_buttons = [
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 175+size*factor), (100, 50)),text='Select',manager=managers["f"]),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450+size*factor, 175+size*factor), (100, 50)),text='Select',manager=managers["f"]),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450+2*size*factor, 175+size*factor), (100, 50)),text='Select',manager=managers["f"]),
]

ally_buttons = [
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 275+2*size*factor), (100, 50)),text='Select',manager=managers["f"]),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450+size*factor, 275+2*size*factor), (100, 50)),text='Select',manager=managers["f"]),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450+2*size*factor, 275+2*size*factor), (100, 50)),text='Select',manager=managers["f"]),
]

action_selectionlist = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 175), (200, 2*size*factor+150)),item_list=[],manager=managers["f"],allow_multi_select=False)
ok_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 375+size*factor+50+40), (3*size*factor, 100)),text='Confirm Turn',manager=managers["f"])
fight_inspect_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((450+3*size*factor+50, 175), (200, 2*size*factor+150)),html_text="Inspect with haste, lest thou be struck!",manager=managers["f"])

# Inspection
inspection_selectionlist = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 175), (200, 2*size*factor+150)),item_list=[],manager=managers["i"],allow_multi_select=False)
inspect_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((800, 175), (300, 350)),html_text="Insect information up ahead <br> so far",manager=managers["i"])

back_buttons = [
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),text='Back',manager=managers["i"]),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),text='Back',manager=managers["m"]),
]

# Win
win_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 25), (200, 75)),html_text="YOU WIN <br>This insect will join your team",manager=managers["w"])
loot_insect_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((800, 175), (300, 350)),html_text="This insect is cool.",manager=managers["w"])
loot_insect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((360, 200+4*size*factor), (4*size*factor, 100)),text='This insect will join my team',manager=managers["w"])

# Movelist
move_selectionlist = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 175), (200, 2*size*factor+150)),item_list=[],manager=managers["m"],allow_multi_select=False)
move_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((800, 175), (300, 350)),html_text="Moveset information up ahead <br> so far",manager=managers["m"])




clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    manager=managers[world.mode]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                
                #buttons
                if event.ui_element in back_buttons:
                    world.mode=""
                if event.ui_element == moveset_button:
                    world.mode="m"
                    move_selectionlist.set_item_list(new_item_list=[action[0].__name__.capitalize() for action in actionPool])
                if event.ui_element == fight_button:
                    world.mode="f"
                    world.enemies=[]
                    for i in range(random.randint(1,2)): #...
                        world.enemies.append(Insect())
                    for button in enemy_buttons+ally_buttons:
                        button.hide()
                    for i in range(len(world.enemies)):
                        button=enemy_buttons[i]
                        button.show()
                        button.set_text("select")
                    for i in range(len(world.allies)):
                        world.allies[i].resetAttributes()
                        button=ally_buttons[i]
                        button.show()
                        button.set_text("select")
                if event.ui_element == loot_insect_button:
                    world.mode=""
                    if(len(world.allies)<3):
                        world.allies.append(world.lootInsect)
                        world.lootInsect.alive = True
                    else:
                        print("Not enough space in your party!")
                    for ally in world.allies:
                        ally.resetAttributes()
                if event.ui_element == inspect_button:
                    world.mode="i"
                    inspection_selectionlist.set_item_list(new_item_list=[ally.name for ally in world.allies])
                if event.ui_element == altar_button:
                    world.mode="a"
                if(world.buttonMode=="action"):
                    if event.ui_element == ok_button:
                        for enemy in world.enemies:
                            enemy.determinedAction=random.choice(enemy.actions)
                            if(enemy.determinedAction.targetRequired):
                                if(enemy.determinedAction.isBad):
                                    enemy.determinedAction.target=random.choice(world.allies)
                                else:
                                    enemy.determinedAction.target=random.choice(world.enemies)
                        insects=world.enemies+world.allies #copy of all initial insects
                        insects.sort(key=lambda x:-x.speed)
                        for insect in insects: #loop through all initial insects
                            if(insect.determinedAction and insect.alive):
                                insect.determinedAction.activate()
                                print(insect.name, "used", insect.determinedAction.name)
                                insect.determinedAction.target=None
                                insect.determinedAction=None
                                for insect2 in world.allies:
                                    if insect2.hp<=0:
                                        insect2.alive=False
                                        world.allies.remove(insect2)
                                        ally_buttons[len(world.allies)].hide()
                                for insect2 in world.enemies:
                                    if insect2.hp<=0:
                                        insect2.alive=False
                                        world.enemies.remove(insect2)
                                        enemy_buttons[len(world.enemies)].hide()
                                if not world.enemies:
                                    world.mode="w"
                                    world.lootInsect=insect2 #from the for loop 
                                    world.lootInsect.resetAttributes()
                                elif not world.allies:
                                    print("you lose")
                    for i, button in enumerate(ally_buttons):
                        if(event.ui_element == button):
                            actionNames=[action.name for action in world.allies[i].actions]
                            action_selectionlist.set_item_list(new_item_list=actionNames)
                            world.active=world.allies[i]
                            #fight_inspect_textbox.html_text=world.allies[i].description() #happens every frame instead lol
                            #fight_inspect_textbox.rebuild()
                            break
                    for i, button in enumerate(enemy_buttons):
                        if(event.ui_element == button):
                            action_selectionlist.set_item_list(new_item_list=[])
                            world.active=world.enemies[i]
                            break

                if(world.buttonMode=="target" and action_selectionlist.get_single_selection()):
                    for action in world.active.actions:
                        if action.name==action_selectionlist.get_single_selection():
                            break
                    
                    for i, button in enumerate(ally_buttons):
                        if event.ui_element == button:
                            action.target=world.allies[i]
                            world.active.determinedAction=action
                            action_selectionlist.set_item_list(new_item_list=[])

                            world.buttonMode="action"
                            for button in enemy_buttons:
                                button.set_text("select")
                            for i in range(len(world.allies)):
                                button=ally_buttons[i]
                                button.set_text("select")
                            break
                    for i, button in enumerate(enemy_buttons):
                        if event.ui_element == button:
                            action.target=world.enemies[i]
                            world.active.determinedAction=action
                            action_selectionlist.set_item_list(new_item_list=[])
                            world.buttonMode="action"
                            for button in enemy_buttons:
                                button.set_text("select")
                            for i in range(len(world.allies)):
                                button=ally_buttons[i]
                                button.set_text("select")
                            break
        manager.process_events(event)


    if(action_selectionlist.get_single_selection()):

        for action in world.active.actions:
            if action.name==action_selectionlist.get_single_selection():
                break
        if(action.targetRequired==False):
            world.buttonMode="action"
            for i in range(len(world.allies)):
                button=ally_buttons[i]
                button.set_text("select")
            for i in range(len(world.enemies)):
                button=enemy_buttons[i]
                button.set_text("select")
            world.active.determinedAction=action
            action_selectionlist.set_item_list(new_item_list=[])
        else:
            world.buttonMode="target"
            for i in range(len(world.allies)):
                button=ally_buttons[i]
                button.set_text("target")
            for i in range(len(world.enemies)):
                button=enemy_buttons[i]
                button.show()
                button.set_text("target")
                
        
    manager.update(time_delta)
    #draw
    window_surface.blit(background, (0, 0)) 
    manager.draw_ui(window_surface)
    if(world.mode=="f"):
        for i in range(len(world.allies)):
            person = world.allies[i]
            window_surface.blit(person.image,(450+i*size*factor, 275+size*factor))
            pygame.draw.rect(window_surface, (100,0,0),(450+i*size*factor, 275+2*size*factor, size*factor, factor*2), 0)
            pygame.draw.rect(window_surface, (0,200,0),(450+i*size*factor, 275+2*size*factor, (size*factor*person.hp)//person.maxhp, factor*2), 0)
        for i in range(len(world.enemies)):
            person = world.enemies[i]
            window_surface.blit(pygame.transform.flip(person.image,0,1),(450+i*size*factor, 175))
            pygame.draw.rect(window_surface, (100,0,0),(450+i*size*factor, 175+1*size*factor, size*factor, factor*2), 0)
            pygame.draw.rect(window_surface, (0,200,0),(450+i*size*factor, 175+1*size*factor, (size*factor*person.hp)//person.maxhp, factor*2), 0)
        if world.active:
            fight_inspect_textbox.html_text=world.active.description()
            fight_inspect_textbox.rebuild()
        else:
            fight_inspect_textbox.html_text="Inspect with haste, lest thou be struck!"
            fight_inspect_textbox.rebuild()
    elif(world.mode=="i"): #every frame!?
        if(inspection_selectionlist.get_single_selection()):

            for insect in world.allies:
                if insect.name==inspection_selectionlist.get_single_selection():
                    break
            inspect_textbox.html_text=insect.description()
            inspect_textbox.rebuild()
            bigImage=pygame.transform.scale(insect.image,(4*size*factor,4*size*factor))
            window_surface.blit(bigImage,(360, 160))
        else:
            inspect_textbox.html_text="Insect information up ahead <br> so far"
            inspect_textbox.rebuild()
    elif(world.mode=="m"):
        if(move_selectionlist.get_single_selection()):

            for action in actionPool:
                if action[0].__name__.capitalize()==move_selectionlist.get_single_selection():
                    break
            move_textbox.html_text=inspect.getsource(action[0])
            move_textbox.rebuild()
        else:
            move_textbox.html_text="Moveset information up ahead <br> so far"
            move_textbox.rebuild()
    elif(world.mode=="w"):
        loot_insect_textbox.html_text=world.lootInsect.description()
        loot_insect_textbox.rebuild()
        bigImage=pygame.transform.scale(world.lootInsect.image,(4*size*factor,4*size*factor))
        window_surface.blit(bigImage,(360, 160))

    pygame.display.update()

