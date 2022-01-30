import pygame, sys
from pygame.locals import *
import random
import time
# import tkinter as tk
# from tkinter import *
from Quantum_Measure import *
from random import choice

SCREEN_WIDTH = 1000
POPUP = 'PYGAME'

pygame.init()
FPS = 10
FramePerSec = pygame.time.Clock()

game_font = pygame.font.SysFont('Arial', 20)
game_font_large = pygame.font.SysFont('Arial', 30)
 
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

frame = 0
scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator = initialize(0)
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def tiles2coord(row_id: int, col_id: int):
    return(row_id*50, col_id*50)

def tiles2center(row_id: int, col_id: int):
    return(row_id*50 + 25, col_id*50 + 25)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_WIDTH))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__() 
        self.image = pygame.image.load("Enemy" + str(kind) + ".png").convert_alpha()
        self.kind = kind
        self.image = pygame.transform.smoothscale(self.image, (50,50)) 
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        self.currentdir = (0,0,0,1)
 
    def move(self):
        if not frame:
            legal  = [] # top = 0, down = 1, left = 2, right = 3
            (cur_row, cur_col) = (self.rect.center[1]//50, self.rect.center[0]//50)
            cur_dir = self.currentdir.index(1)
            if tiles[cur_row - 1][cur_col]:
                legal.append(0)
            if tiles[cur_row + 1][cur_col]:
                legal.append(1)
            if tiles[cur_row][cur_col - 1]:
                legal.append(2)
            if tiles[cur_row][cur_col + 1]:
                legal.append(3)
            if cur_dir in legal:
                if cur_dir == 0:
                    self.rect.move_ip(0, -50)
                    return
                elif cur_dir == 1:
                    self.rect.move_ip(0,50)
                    return
                elif cur_dir == 2:
                    self.rect.move_ip(-50, 0)
                    return
                elif cur_dir == 3:
                    self.rect.move_ip(50, 0)
                    return
            move = choice(legal)
            if move == 0:
                self.rect.move_ip(0, -50)
                self.currentdir = (1,0,0,0)
            elif move == 1:
                self.rect.move_ip(0,50)
                self.currentdir = (0,1,0,0)
            elif move == 2:
                self.rect.move_ip(-50, 0)
                self.currentdir = (0,0,1,0)
            else:
                self.rect.move_ip(50, 0)
                self.currentdir = (0,0,0,1)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50)) 
        self.rect = self.image.get_rect()
        self.rect.center = tiles2center(2, 1)
        self.qGates = []
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        (cur_row, cur_col) = (self.rect.center[1]//50, self.rect.center[0]//50)
        if pressed_keys[K_UP]:
            if tiles[cur_row - 1][cur_col]:
                self.rect.move_ip(0,-50)  
        if pressed_keys[K_DOWN]:
            if tiles[cur_row + 1][cur_col]:
                self.rect.move_ip(0,50)     
        if pressed_keys[K_LEFT]:
            if tiles[cur_row][cur_col - 1]:
                self.rect.move_ip(-50, 0)
        if pressed_keys[K_RIGHT]:
            if tiles[cur_row][cur_col + 1]:
                self.rect.move_ip(50, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

class HGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "Hadamard"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'H'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['H'], True, WHITE)
        surface.blit(txt, self.rect.center)

class PZGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliZ"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'Z'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
    
    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['Z'], True, WHITE)
        surface.blit(txt, self.rect.center)


class PXGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliX"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'X'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['X'], True, WHITE)
        surface.blit(txt, self.rect.center)

class PYGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'Y'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['Y'], True, WHITE)
        surface.blit(txt, self.rect.center)

class RYGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RY'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['RY'], True, WHITE)
        surface.blit(txt, self.rect.center)

class RZGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RZ'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['RZ'], True, WHITE)
        surface.blit(txt, self.rect.center)

class RXGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RX'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
        txt = pygame.font.Font.render(game_font, what_to_draw['RX'], True, WHITE)
        surface.blit(txt, self.rect.center)

class CNOT(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "CNOT"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RX'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ', 'CN': 'CN'}
        txt = pygame.font.Font.render(game_font, what_to_draw['CN'], True, WHITE)
        surface.blit(txt, self.rect.center)
    
         
P1 = Pacman()
E1 = Enemy('X')
E2 = Enemy('Y')
E3 = Enemy('Z')
E4 = Enemy('X')
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
all_sprites.add(E3)
all_sprites.add(E4)

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
enemies.add(E3)
enemies.add(E4)

# prevents two gates from generating on the same spot
temp_tiles = tiles

H = HGate()
PauliZ = PZGate()
PauliY = PYGate()
PauliX = PXGate()
# Rx = RXGate()
# Ry = RYGate()
# Rz = RZGate()
cnot = CNOT()

tiles = temp_tiles

gates = pygame.sprite.Group()
gates.add(H)
gates.add(PauliZ)
gates.add(PauliY)
gates.add(PauliX)
gates.add(cnot)
# gates.add(Rx)
# gates.add(Rz)
# gates.add(Ry)

scoreGates = pygame.sprite.Group()
gates.add(cnot)

def drawMaze(surface):
    # what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
    for row_id, row in enumerate(tiles):
        for col_id, col in enumerate(row):
            if col == 0:
                pygame.draw.rect(surface, WHITE, pygame.Rect(50*col_id, 50*row_id, 50, 50))
            elif col == 1:
                continue
            # else:
            #     txt = pygame.font.Font.render(game_font, what_to_draw[col], True, WHITE)
            #     surface.blit(txt, (50*col_id + 15, 50*row_id + 10))


def die():
    DISPLAYSURF.fill(RED)
    txt2 = pygame.font.Font.render(game_font_large, "You just died :D", True, WHITE)
    DISPLAYSURF.blit(txt2, (300,400))
    pygame.display.update()
    time.sleep(2)
    for entity in all_sprites:
        entity.kill() 
    pygame.quit()
    sys.exit()

def victory():
    DISPLAYSURF.fill(BLUE)
    txt2 = pygame.font.Font.render(game_font_large, "YOU WON! :D", True, WHITE)
    DISPLAYSURF.blit(txt2, (300,400))
    pygame.display.update()
    time.sleep(2)
    for entity in all_sprites:
        entity.kill() 
    pygame.quit()
    sys.exit()

# def popup(gates, simulator, playerCircuit, quantumRotDict, quantumGateDict, state):
#     window = Tk()
#     window.title("IQuHACK")
#     window.resizable(width=FALSE, height=FALSE)
#     window.geometry('{}x{}'.format(200, 150))
#     window.grid_rowconfigure(0, weight=1)
#     window.grid_rowconfigure(1, weight=0)
#     window.grid_columnconfigure(0, weight=0)
#     frame = Frame(window)
#     frame.grid(row = 0, column = 0)
#     frame.grid_columnconfigure(0, weight=0)
#     frame.grid_columnconfigure(1, weight=0)
#     frame.grid_columnconfigure(2, weight=0)
#     label = Label(frame, text = "Please wait while you are measured!").grid(row = 0, column = 1)
#     img = PhotoImage(file="Enemy.png")
#     label2 = Label(window, image = img)
#     label2.grid(row = 1, column = 0)
#     verAlive = execute_measurement(gates, simulator, playerCircuit, quantumRotDict, quantumGateDict, state)
#     time.sleep(5)
#     window.destroy()
#     window.mainloop()
#     return verAlive

def pgpopup(surface, gates, simulator, playerCircuit, quantumRotDict, quantumGateDict, state):
    surface.fill(BLACK)
    txt = pygame.font.Font.render(game_font_large, "You're being measured now!", True, WHITE)
    surface.blit(txt, (300,300))
    pygame.display.update()
    verAlive = execute_measurement(gates, simulator, playerCircuit, quantumRotDict, quantumGateDict, state)
    time.sleep(2)
    txt2 = pygame.font.Font.render(game_font_large, "Measurement result is... "+str(verAlive), True, WHITE)
    surface.blit(txt2, (300,400))
    pygame.display.update()
    time.sleep(2)
    return verAlive

def scoreupdate(surface, score):
    txt2 = pygame.font.Font.render(game_font_large, "SCORE:" + str(score), True, RED)
    surface.blit(txt2, (860, 960))
    pygame.display.update()


score = 0
scorelist = [] 
while True:
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()

    for enemy in enemies:
        enemy.move()
    scoreupdate(DISPLAYSURF, score)
    DISPLAYSURF.fill(BLACK)
    drawMaze(DISPLAYSURF)
    for entity in all_sprites:
        entity.draw(DISPLAYSURF)
    for gate in gates:
        gate.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(P1, enemies):
        if P1.is_collided_with(E1):
            if POPUP == 'TKINTER':
                continue
                verAlive = popup(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E1.kind)
            elif POPUP == 'PYGAME':
                verAlive = pgpopup(DISPLAYSURF, P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E1.kind)
            if verAlive == 0:   
                die()
            else: 
                P1.qGates = ["PauliX"] 
                E1.kill()
                continue

        elif P1.is_collided_with(E2):
            if POPUP == 'TKINTER':
                continue
                verAlive = popup(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E2.kind)
            elif POPUP == 'PYGAME':
                verAlive = pgpopup(DISPLAYSURF, P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E2.kind)
            if verAlive == 0:   
                die()
            else: 
                P1.qGates = ["PauliX"]
                E2.kill()
                continue

        elif P1.is_collided_with(E3):
            if POPUP == 'TKINTER':
                continue
                verAlive = popup(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E3.kind)
            elif POPUP == 'PYGAME':
                verAlive = pgpopup(DISPLAYSURF, P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E3.kind)
            if verAlive == 0:   
                die()
            else: 
                P1.qGates = ["PauliX"]
                E3.kill()
                continue

        elif P1.is_collided_with(E4):
            if POPUP == 'TKINTER':
                continue
                verAlive = popup(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E4.kind)
            elif POPUP == 'PYGAME':
                verAlive = pgpopup(DISPLAYSURF, P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, E4.kind)
            if verAlive == 0:   
                die()
            else: 
                P1.qGates = ["PauliX"]
                E4.kill()
                continue
    
    if pygame.sprite.spritecollideany(P1, gates):
        if P1.is_collided_with(H):
            P1.qGates.append("Hadamard")
            scorelist.append("H")
            score, scoreCircuit = Score_circuit("H", scoreCircuit, score, scorelist)
            H.kill()
        elif P1.is_collided_with(PauliZ):
            P1.qGates.append("PauliZ")
            PauliZ.kill()
        elif P1.is_collided_with(PauliX):
            P1.qGates.append("PauliX")
            PauliX.kill()
        elif P1.is_collided_with(PauliY):
            P1.qGates.append("PauliY")
            PauliY.kill()
        elif P1.is_collided_with(cnot):
            P1.qGates.append("CNOT")
            scorelist.append("CNOT")
            score, scoreCircuit = Score_circuit("CNOT", scoreCircuit, score, scorelist)
            cnot.kill()
        if score == 2:
            victory()


    # pygame.display.update()
    frame += 1
    frame = frame % 4
    FramePerSec.tick(FPS)
