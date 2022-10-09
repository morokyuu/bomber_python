# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Usable Font search
$ fc-list

::References::
Enum class
https://www.fenet.jp/dotnet/column/language/6708/

super class constructor(init) call
https://uxmilk.jp/15665

"""

import pygame
from pygame.locals import *
import random
from enum import Enum

# field value
CH_FREE = 0
CH_FIRE = 1
CH_HARD = 2
CH_SOFT = 3
CH_BOM = 4
CH_ITEM = 5

class Type(Enum):
    FREE = 0
    FIRE = 1
    HARD = 2
    SOFT = 3
    BOM = 4
    ITEM = 5
    PLAYER = 6

# item type
ITEM_NONE = 0
ITEM_BOM = 1
ITEM_FIRE = 2 


field = []

bom_list = []
fire_list = []
block_list = []
item_list = []

# color value
CL_FREE = (0,130,0)
CL_HARD = (80,80,80)
CL_SOFT = (95,95,95)

# frame rate
FPS = 50
fpsClock = pygame.time.Clock()

# game state transition wait
STATE_TRANSITION_FRAME = 50
state_transition_count = 0

# window size
WINDOW_W = 640
WINDOW_H = 480
CHIPSIZE = 32
CHIPNUM_W = int(WINDOW_W/CHIPSIZE)-1
CHIPNUM_H = int(WINDOW_H/CHIPSIZE)

# game state
ST_TITLE = 0
ST_GAME = 1
ST_GAMEOVER = 2

# game constants
BOM_TIMEOUT_FRAME = 100
FIRE_FRAME = 30


def print_field():
    for f in field:
        print(f)

class Chara:
    def __init__(self,XY,chType,field_map):
        self.XY = XY
        self.chType = chType
        self.field_map = field_map
        self.dead = False
    def disp(self):
        pass
    def act(self):
        pass
        

class Item(Chara):
    def __init__(self, X, Y, item_type):
        super.__init__(X,Y)
        field[self.ch_y][self.ch_x] = CH_ITEM
        self.item_type = item_type

    def draw(self):
        if self.item_type == ITEM_BOM:
            item_surface_bom = mono_item_font.render("B", True, 'Red')
        elif self.item_type == ITEM_FIRE:
            item_surface_bom = mono_item_font.render("F", True, 'Red')
        pygame.draw.rect(screen, (220,220,0), (self.ch_x * CHIPSIZE,self.ch_y * CHIPSIZE,32,32))
        screen.blit(item_surface_bom, (self.ch_x * CHIPSIZE + 8,self.ch_y * CHIPSIZE))

    def execute(self):
        current = field[self.ch_y][self.ch_x]
        if current == CH_FIRE:
            self.dead = True
            field[self.ch_y][self.ch_x] = CH_FREE

    def get(self,px,py):
        for i in item_list:
            if i.ch_x == px and i.ch_y == py:
                self.dead = True
                field[py][px] = CH_FREE
                return i.item_type



class Block(Chara):
    def __init__(self, XY, field_map,item_type=ITEM_NONE):
        super().__init__(XY,Type.SOFT,field_map)
        self.item_type = item_type

    def execute(self):
        return 
    
    def draw(self):
        pygame.draw.rect(screen, CL_SOFT, (self.XY[0]*CHIPSIZE, self.XY[1]*CHIPSIZE, 32,32))

class HardBlock(Chara):
    def __init__(self, XY, field_map):
        super().__init__(XY,Type.HARD,field_map)

    def execute(self):
        return 
    
    def draw(self):
        pygame.draw.rect(screen, CL_HARD, (self.XY[0]*CHIPSIZE, self.XY[1]*CHIPSIZE, 32,32))

class oldBom():
    def __init__(self, ch_x, ch_y, power):
        self.ch_x = ch_x
        self.ch_y = ch_y
        field[self.ch_y][self.ch_x] = CH_BOM
        self.timer = BOM_TIMEOUT_FRAME
        self.dead = False
        self.power = power
        self.size_ratio = [1.0,0.9,0.8,0.9]
    
    def explode(self):
        
        dx = 0
        dy = 0
        
        px = self.ch_x + dx
        py = self.ch_y + dy
        fire_list.append(Fire(px, py))
        
        for dx in range(1,self.power+1):
            dy = 0
            
            px = self.ch_x + dx
            py = self.ch_y + dy
            
            if not field[py][px] == CH_HARD:
                if field[py][px] == CH_FREE:
                    fire_list.append(Fire(px, py))
                else:
                    field[py][px] = CH_FIRE
                    break
            else:
                break
            
        for dx in range(1,self.power+1):
            dy = 0
            
            px = self.ch_x - dx
            py = self.ch_y + dy
            
            if not field[py][px] == CH_HARD:
                if field[py][px] == CH_FREE:
                    fire_list.append(Fire(px, py))
                else:
                    field[py][px] = CH_FIRE
                    break
            else:
                break

        for dy in range(1,self.power+1):
            dx = 0
            
            px = self.ch_x + dx
            py = self.ch_y + dy
            
            if not field[py][px] == CH_HARD:
                if field[py][px] == CH_FREE:
                    fire_list.append(Fire(px, py))
                else:
                    field[py][px] = CH_FIRE
                    break
            else:
                break
            
        for dy in range(1,self.power+1):
            dx = 0
            
            px = self.ch_x + dx
            py = self.ch_y - dy
            
            if not field[py][px] == CH_HARD:
                if field[py][px] == CH_FREE:
                    fire_list.append(Fire(px, py))
                else:
                    field[py][px] = CH_FIRE
                    break
            else:
                break

    def execute(self):
        # timer overflow
        self.timer -= 1
        if self.timer < 0:
            self.dead = True
            self.explode()
        # in an explosion
        if field[self.ch_y][self.ch_x] == CH_FIRE:
            self.dead = True
            self.explode()
        
    def draw(self):
        pygame.draw.rect(screen, CL_FREE, (self.ch_x * CHIPSIZE,self.ch_y * CHIPSIZE,32,32))
        
        pygame.draw.circle(
            screen,
            (0,0,0),
            (self.ch_x * CHIPSIZE+CHIPSIZE/2,self.ch_y * CHIPSIZE+CHIPSIZE/2),
            CHIPSIZE/2 * self.size_ratio[int(self.timer / 7 % 4)])

class Fire():
    def __init__(self, ch_x, ch_y):
        self.ch_x = ch_x
        self.ch_y = ch_y
        field[self.ch_y][self.ch_x] = CH_FIRE
        self.timer = 0
        self.dead = False
    
    def execute(self):
        self.timer += 1
        if self.timer > FIRE_FRAME:
            field[self.ch_y][self.ch_x] = CH_FREE
            self.dead = True
            
    def draw(self):
        bom_sound.play()
        
        pygame.draw.rect(screen, CL_FREE, (self.ch_x * CHIPSIZE,self.ch_y * CHIPSIZE,32,32))
        pygame.draw.circle(
            screen,
            (255,0,0),
            (self.ch_x * CHIPSIZE+CHIPSIZE/2,self.ch_y * CHIPSIZE+CHIPSIZE/2),
            CHIPSIZE/2)
        
        
class Player(Chara):
    def __init__(self,XY,field_map):
        super().__init__(XY,Type.PLAYER,field_map)
        # game variable
        self.bom_power = 2
        self.bom_stock = 2
        self.dead = False


    def execute(self, dx, dy, btn_space):
        # death
        if self.field_map[self.XY[1]][self.XY[0]] == CH_FIRE:
            self.dead = True
#        # put a bom
#        if len(bom_list) < self.bom_stock:
#            if field[self.ch_y][self.ch_x] == CH_FREE:
#                if btn_space == True:
#                    bom_list.append(Bom(self.ch_x, self.ch_y,self.bom_power))
        # walking
        px = self.ch_x+dx
        py = self.ch_y+dy
        targ = field[py][px]
        if not (targ == CH_HARD or targ == CH_SOFT or targ == CH_BOM):
            self.ch_x += dx
            self.ch_y += dy

            # item get
            if targ == CH_ITEM:
                item_type = item_list[0].get(self.ch_x, self.ch_y)

                if item_type == ITEM_FIRE:
                    self.bom_power += 1
                elif item_type == ITEM_BOM:
                    self.bom_stock += 1
        
    def draw(self):
        pygame.draw.circle(
            screen,
            (255,255,255),
            (self.ch_x * CHIPSIZE + CHIPSIZE/2,self.ch_y * CHIPSIZE + CHIPSIZE/2),
            0.8*CHIPSIZE/2
            )




def drawWorld(field_map):
    for Y,line in enumerate(field_map.field):
        for X,f in enumerate(line):
            if f == Type.FREE:
                pygame.draw.rect(screen, CL_FREE, (X*CHIPSIZE, Y*CHIPSIZE, 32,32))
            elif f == Type.HARD:
                pygame.draw.rect(screen, CL_HARD, (X*CHIPSIZE, Y*CHIPSIZE, 32,32))


def drawChip(type,x,y):
    if type == CH_FREE:
        pygame.draw.rect(screen, CL_FREE, (x,y,32,32))
    elif type == CH_HARD:
        pygame.draw.rect(screen, CL_HARD, (x,y,32,32))
    elif type == CH_SOFT:
        for b in block_list:
            b.draw()
    elif type == CH_BOM:
        for b in bom_list:
            b.draw()
    elif type == CH_FIRE:
        for f in fire_list:
            f.draw()
    elif type == CH_ITEM:
        for i in item_list:
            i.draw()



def execute_list(obj_list):
    for o in obj_list:
        if o.dead == False:
            o.execute()

def delete_dead_from_list(obj_list):
    while len(obj_list):
        obj_list.sort(key= lambda x: x.dead == False)
        if obj_list[0].dead == True:
            obj_list.pop(0)
        else:
            break

def isStateTransitionTimming(state_transition_count):
    state_transition_count += 1
    if state_transition_count > STATE_TRANSITION_FRAME:
        state_transition_count = 0
        return True
    return False

class GameClass:
    def __init__(self):
        # Object init
        self.makeMap()
        self.player = Player(1,1)
        
    def isContinue(self):
        if self.player.dead == True:
            return False
        else:
            return True

    def makeMap(self):
        field.clear()
        item_list.clear()
        fire_list.clear()
        block_list.clear()
        bom_list.clear()

        for i in range(CHIPNUM_H):
            if i == 0 or i == CHIPNUM_H-1:
                field.append([CH_HARD] * CHIPNUM_W)
            elif i % 2 == 1:
                line = [CH_FREE] * CHIPNUM_W
                line[0] = CH_HARD
                line[CHIPNUM_W-1] = CH_HARD
                field.append(line)
            elif i % 2 == 0:
                line = [CH_HARD] * CHIPNUM_W
                for i in range(1,CHIPNUM_W,2):
                    line[i] = CH_FREE
                field.append(line)
        
        #TODO New Block
#        for i in range(10):
#            x = random.randint(2, CHIPNUM_W-1)
#            y = random.randint(2, CHIPNUM_H-1)
#            if field[y][x] == CH_FREE:
#                block_list.append(Block(x,y))

        # Soft block randomly contains an item
        contain_index = random.randint(0,len(block_list))
        block_list[contain_index].containItem(ITEM_BOM)
        block_list[contain_index+1].containItem(ITEM_FIRE)


    def mainloop(self,running):
        dx = 0
        dy = 0
        btn_space = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dy -= 1
                elif event.key == pygame.K_DOWN:
                    dy += 1
                elif event.key == pygame.K_LEFT:
                    dx -= 1
                elif event.key == pygame.K_RIGHT:
                    dx += 1
                elif event.key == pygame.K_SPACE:
                    btn_space = True
                elif event.key == pygame.K_d:
                    print_field()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0,0,0))
        
        # field drawing
        for y,line in enumerate(field):
            for x,l in enumerate(line):
                drawChip(l,x*CHIPSIZE,y*CHIPSIZE)
        
        # draw player
        if self.player.dead == False:
            self.player.execute(dx, dy, btn_space)
            self.player.draw()

        execute_list(fire_list)
        execute_list(block_list)
        execute_list(bom_list)
        execute_list(item_list)
        
        # delete
        delete_dead_from_list(fire_list)
        delete_dead_from_list(block_list)
        delete_dead_from_list(bom_list)    
        delete_dead_from_list(item_list)
        
        pygame.display.flip()
        fpsClock.tick(FPS)
        
        return running


def st_game_loop(running,gamestate):

    game = GameClass()
    
    while game.isContinue() and running:
        running = game.mainloop(running)
    
    gamestate = ST_GAMEOVER

    return running,gamestate


def st_gameover_loop(running, gamestate):
    btn_space = False
    
    screen.fill((200,100,100))

    
    title_surface = mono_font.render("GAMEOVER", True, 'Black')
    sub_surface = mono_font.render("Hit space button", True, 'Black')
    screen.blit(title_surface, (WINDOW_W/2-200,WINDOW_H/2))
    screen.blit(sub_surface, (WINDOW_W/2-300,WINDOW_H/2+180))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                btn_space = True
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    if btn_space == True:
        pygame.time.wait(800)
        gamestate = ST_TITLE
    else:
        gamestate = ST_GAMEOVER
    
    return running,gamestate

def st_title_loop(running, gamestate):
    btn_space = False
    
    screen.fill((100,100,100))

    
    title_surface = mono_font.render("BOMBERMAN", True, 'Black')
    sub_surface = mono_font.render("Hit space button", True, 'Black')
    screen.blit(title_surface, (WINDOW_W/2-300,WINDOW_H/2))
    screen.blit(sub_surface, (WINDOW_W/2-300,WINDOW_H/2+180))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                btn_space = True
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    if btn_space == True:
        pygame.time.wait(800)
        gamestate = ST_GAME
    else:
        gamestate = ST_TITLE
    
    return running,gamestate

class FieldMap:
    def __init__(self):
        self.field = list() #2-dimention
        self._initMap()
        pass

    def put(self,XY,chType):
        self.field[XY[1]][XY[0]] = chType

    def get(self,XY):
        return self.field[XY[1]][XY[0]]

    def getXY(self,xy):
        return (xy[0] // CHIPSIZE, xy[1] // CHIPSIZE)

    def getxy(self,XY):
        offset = CHIPSIZE//2
        return (XY[0] * CHIPSIZE + offset,
                XY[1] * CHIPSIZE + offset)

    def _initMap(self):
        for i in range(CHIPNUM_H):
            if i == 0 or i == CHIPNUM_H-1:
                field.append([Type.HARD] * CHIPNUM_W)
            elif i % 2 == 1:
                line = [Type.FREE] * CHIPNUM_W
                line[0] = Type.HARD
                line[CHIPNUM_W-1] = Type.HARD
                field.append(line)
            elif i % 2 == 0:
                line = [Type.HARD] * CHIPNUM_W
                for i in range(1,CHIPNUM_W,2):
                    line[i] = Type.FREE
                field.append(line)
        self.field = field
        #print(self.field)
        
#        for i in range(10):
#            x = random.randint(2, CHIPNUM_W-1)
#            y = random.randint(2, CHIPNUM_H-1)
#            if field[y][x] == Type.FREE:
#                block_list.append(Block(x,y))

#        # Soft block randomly contains an item
#        contain_index = random.randint(0,len(block_list))
#        block_list[contain_index].containItem(ITEM_BOM)
#        block_list[contain_index+1].containItem(ITEM_FIRE)
#        pass



def keyInput():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    keystate = pygame.key.get_pressed()
    return running,keystate


####################################################################

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_W, WINDOW_H])
    pygame.display.set_caption("bomber man")
    clock = pygame.time.Clock()

    fmap = FieldMap()
    


    running = True
    while running:
        running,keystate = keyInput()
        screen.fill((0,0,0))
        #print(keystate)
        #fmap.disp()
        drawWorld(fmap)
        pygame.display.flip()
        fpsClock.tick(FPS)

    pygame.quit()

