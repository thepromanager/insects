import pygame
import pygame_gui
import random
import math
import insect as insectart
import types
import time

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
    }
#overlay=pygame_gui.UIManager(screenSize)

factor = 3
size=32

class Insect():
    def __init__(self):
        self.alive=True
        self.image=insectart.createSprite()
        def bite(self):
            self.target.hp-=2
        def heal(self):
            self.owner.hp=min(self.owner.hp+2, self.owner.maxhp)
        
        self.actions=[Action(self,"Bite",bite),Action(self,"Heal",heal,targetRequired=False)]
        self.determinedAction=None
        self.speed=10
        self.hp=10
        self.maxhp=10
        self.name=self.createName()
        #self.level=lvl
    def createName(self):

        return str(random.random())
    def description(self):
        return str(self.__dict__)
class Action():
    def __init__(self,owner,name,activateFunction,targetRequired=True,isBad=True):
        self.owner=owner
        self.name=name
        self.targetRequired=targetRequired
        self.isBad=isBad
        self.target=None
        self.activate=types.MethodType(activateFunction,self)

    def activate(self):
        pass

class World():
    def __init__(self):
        self.day = 0
        self.mode = ""
        self.buttonMode="action" # action // target // inspect
        self.active=None
        self.enemies=[]
        self.allies=[Insect(),Insect(),Insect()]
 
world=World()

# Main
day_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 25), (200, 75)),html_text="Days ahead so long",manager=managers[""])
fight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (200, 50)),text='Fight ye Foes',manager=managers[""])
inspect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 350), (200, 50)),text='Inspect ye Insects',manager=managers[""])
altar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 425), (200, 50)),text='Sacrifice ye Mates',manager=managers[""])

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
ok_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450+3*size*factor+50, 175), (200, 2*size*factor+150)),text='Confirm Turn',manager=managers["f"])

# Inspection
inspection_selectionlist = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100, 175), (200, 2*size*factor+150)),item_list=[],manager=managers["i"],allow_multi_select=False)
inspect_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((800, 175), (300, 350)),html_text="Insect information up ahead <br> so far",manager=managers["i"])
back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),text='Back',manager=managers["i"])




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
                if event.ui_element == back_button:
                    world.mode=""
                if event.ui_element == fight_button:
                    world.mode="f"
                    world.enemies=[Insect(),Insect(),Insect()]
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
                        insects.sort(key=lambda x:x.speed)
                        for insect in insects: #loop through all initial insects
                            if(insect.determinedAction and insect.alive):
                                insect.determinedAction.activate()
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
                    for i, button in enumerate(ally_buttons):
                        if(event.ui_element == button):
                            actionNames=[action.name for action in world.allies[i].actions]
                            action_selectionlist.set_item_list(new_item_list=actionNames)
                            world.active=world.allies[i]

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
                    for i, button in enumerate(enemy_buttons):
                        if event.ui_element == button:
                            action.target=world.enemies[i]
                            world.active.determinedAction=action
                            action_selectionlist.set_item_list(new_item_list=[])
                            world.buttonMode="action"
        manager.process_events(event)


    if(action_selectionlist.get_single_selection()):

        for action in world.active.actions:
            if action.name==action_selectionlist.get_single_selection():
                break
        if(action.targetRequired==False):
            world.active.determinedAction=action
            action_selectionlist.set_item_list(new_item_list=[])
        else:
            world.buttonMode="target"
        
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
            window_surface.blit(person.image,(450+i*size*factor, 175))
            pygame.draw.rect(window_surface, (100,0,0),(450+i*size*factor, 175+1*size*factor, size*factor, factor*2), 0)
            pygame.draw.rect(window_surface, (0,200,0),(450+i*size*factor, 175+1*size*factor, (size*factor*person.hp)//person.maxhp, factor*2), 0)
    elif(world.mode=="i"):
        if(inspection_selectionlist.get_single_selection()):

            for insect in world.allies:
                if insect.name==inspection_selectionlist.get_single_selection():
                    break
            inspect_textbox.html_text=insect.description()
            inspect_textbox.rebuild()
            bigImage=pygame.transform.scale(insect.image,(4*size*factor,4*size*factor))
            window_surface.blit(bigImage,(360, 160))
    pygame.display.update()
