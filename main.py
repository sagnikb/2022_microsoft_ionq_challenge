import pygame
import sys
from pygame.locals import *
import time
from Quantum_Measure import *
from random import choice

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1000
SMALL_SQ_DIM = 50
PACMAN_IMAGE = "Player.png"

FPS = 10

pygame.init()
scoreCircuit, playerCircuit, quantumGateDict, simulator = initialize(0)

GAME_FONT = pygame.font.SysFont('Arial', 20)
GAME_FONT_LARGE = pygame.font.SysFont('Arial', 30)
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")
FramePerSec = pygame.time.Clock()

TILES = [
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
    return(row_id*SMALL_SQ_DIM, col_id*SMALL_SQ_DIM)


def tiles2center(location):
    return(location[1]*SMALL_SQ_DIM + 25, location[0]*SMALL_SQ_DIM + 25)


def random_empty_cell():
    gen_row = choice(list(range(2,19)))
    indices = [i for i, col in enumerate(TILES[gen_row]) if col == 1]
    gen_col = choice(indices)
    return (gen_col, gen_row)


def drawMaze(surface):
    for row_id, row in enumerate(TILES):
        for col_id, col in enumerate(row):
            if col == 0:
                pygame.draw.rect(surface, WHITE, pygame.Rect(
                    SMALL_SQ_DIM*col_id, 
                    SMALL_SQ_DIM*row_id, 
                    SMALL_SQ_DIM, 
                    SMALL_SQ_DIM
                    )
                )


class Enemy(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__(all_moving_sprites, enemies) 
        self.image = pygame.image.load("Enemy" + str(kind) + ".png").convert_alpha()
        self.kind = kind
        self.image = pygame.transform.smoothscale(self.image, (SMALL_SQ_DIM,SMALL_SQ_DIM)) 
        self.rect = self.image.get_rect()
        generated_location = random_empty_cell()
        self.rect.center = tiles2center(generated_location)
        TILES[generated_location[1]][generated_location[0]] = kind
        self.currentdir = (0, 0, 0, 1)

    def move(self):
        if not frame:
            legal = []  # top = 0, down = 1, left = 2, right = 3
            (cur_row, cur_col) = (self.rect.center[1]//SMALL_SQ_DIM, self.rect.center[0]//SMALL_SQ_DIM)
            cur_dir = self.currentdir.index(1)
            if TILES[cur_row - 1][cur_col]:
                legal.append(0)
            if TILES[cur_row + 1][cur_col]:
                legal.append(1)
            if TILES[cur_row][cur_col - 1]:
                legal.append(2)
            if TILES[cur_row][cur_col + 1]:
                legal.append(3)
            if cur_dir in legal:
                if cur_dir == 0:
                    self.rect.move_ip(0, -SMALL_SQ_DIM)
                    return
                elif cur_dir == 1:
                    self.rect.move_ip(0, SMALL_SQ_DIM)
                    return
                elif cur_dir == 2:
                    self.rect.move_ip(-SMALL_SQ_DIM, 0)
                    return
                elif cur_dir == 3:
                    self.rect.move_ip(SMALL_SQ_DIM, 0)
                    return
            move = choice(legal)
            if move == 0:
                self.rect.move_ip(0, -SMALL_SQ_DIM)
                self.currentdir = (1, 0, 0, 0)
            elif move == 1:
                self.rect.move_ip(0,SMALL_SQ_DIM)
                self.currentdir = (0, 1, 0, 0)
            elif move == 2:
                self.rect.move_ip(-SMALL_SQ_DIM, 0)
                self.currentdir = (0, 0, 1, 0)
            else:
                self.rect.move_ip(SMALL_SQ_DIM, 0)
                self.currentdir = (0, 0, 0, 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_moving_sprites) 
        self.image = pygame.image.load(PACMAN_IMAGE).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SMALL_SQ_DIM,SMALL_SQ_DIM)) 
        self.rect = self.image.get_rect()
        generated_location = random_empty_cell()
        self.rect.center = tiles2center(generated_location)
        TILES[generated_location[1]][generated_location[0]] = 'P'
        self.qGates = []

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        (cur_row, cur_col) = (self.rect.center[1]//SMALL_SQ_DIM, self.rect.center[0]//SMALL_SQ_DIM)
        if pressed_keys[K_UP]:
            if TILES[cur_row - 1][cur_col]:
                self.rect.move_ip(0, -SMALL_SQ_DIM)
        if pressed_keys[K_DOWN]:
            if TILES[cur_row + 1][cur_col]:
                self.rect.move_ip(0, SMALL_SQ_DIM)
        if pressed_keys[K_LEFT]:
            if TILES[cur_row][cur_col - 1]:
                self.rect.move_ip(-SMALL_SQ_DIM, 0)
        if pressed_keys[K_RIGHT]:
            if TILES[cur_row][cur_col + 1]:
                self.rect.move_ip(SMALL_SQ_DIM, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)     


class Gate(pygame.sprite.Sprite):
    def __init__(self, kind, **kwargs) -> None:
        super().__init__(gates)
        self.kind = kind
        self.image = pygame.Surface([SMALL_SQ_DIM, SMALL_SQ_DIM])
        self.rect = self.image.get_rect()
        generated_location = random_empty_cell()
        self.rect.center = tiles2center(generated_location)
        TILES[generated_location[1]][generated_location[0]] = kind

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, surface):
        txt = pygame.font.Font.render(GAME_FONT, self.kind, True, WHITE)
        surface.blit(txt, (self.rect.centerx - SMALL_SQ_DIM/5, self.rect.centery - SMALL_SQ_DIM/5))


class HGate(Gate):
    def __init__(self, **kwargs):
        super().__init__('H', **kwargs)


class PXGate(Gate):
    def __init__(self, **kwargs):
        super().__init__('X', **kwargs)


class PYGate(Gate):
    def __init__(self, **kwargs):
        super().__init__('Y', **kwargs)


class PZGate(Gate):
    def __init__(self, **kwargs):
        super().__init__('Z', **kwargs)


class CNOT(Gate):
    def __init__(self, **kwargs):
        super().__init__('CN', **kwargs)


gates = pygame.sprite.Group()
all_moving_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
scoreGates = pygame.sprite.Group()

# prevents two gates from generating on the same spot
temp_tiles = TILES

P1 = Pacman()
E1 = Enemy('X')
E2 = Enemy('Y')
E3 = Enemy('Z')
E4 = Enemy('X')
H = HGate()
PauliZ = PZGate()
PauliY = PYGate()
PauliX = PXGate()
cnot = CNOT()

TILES = temp_tiles


def finish_game():
    time.sleep(2)
    for entity in all_moving_sprites:
        entity.kill() 
    pygame.quit()
    sys.exit()


def die():
    DISPLAYSURF.fill(RED)
    txt = pygame.font.Font.render(GAME_FONT_LARGE, "You just died :D", True, WHITE)
    DISPLAYSURF.blit(txt, (300, 400))
    pygame.display.update()
    finish_game()


def victory():
    DISPLAYSURF.fill(BLACK)
    txt = pygame.font.Font.render(GAME_FONT_LARGE, "YOU WON! :D", True, WHITE)
    DISPLAYSURF.blit(txt, (300, 400))
    pygame.display.update()
    finish_game()


def measurement(surface, gates, simulator, playerCircuit, quantumGateDict, state):
    surface.fill(BLACK)
    txt = pygame.font.Font.render(GAME_FONT_LARGE, "You're being measured now!", True, WHITE)
    surface.blit(txt, (300, 300))
    pygame.display.update()
    verAlive = execute_measurement(gates, simulator, playerCircuit, quantumGateDict, state)
    time.sleep(2)
    txt2 = pygame.font.Font.render(GAME_FONT_LARGE, "Measurement result is... "+str(verAlive), True, WHITE)
    surface.blit(txt2, (300, 400))
    pygame.display.update()
    time.sleep(2)
    return verAlive


frame = 0
score = 0
scorelist = []
while True:  # TODO: There's a weird bug where pacman may not appear in the maze until a move is made, idk why that's happening
    drawMaze(DISPLAYSURF)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for enemy in enemies:
        enemy.move()
    txt = pygame.font.Font.render(GAME_FONT_LARGE, "SCORE:" + str(score), True, RED)
    DISPLAYSURF.blit(txt, (860, 960))
    P1.update()
    pygame.display.update()
    DISPLAYSURF.fill(BLACK)
    
    for entity in all_moving_sprites:
        entity.draw(DISPLAYSURF)
    for gate in gates:
        gate.draw(DISPLAYSURF)

    enemy_collision = pygame.sprite.spritecollide(P1, enemies, False)
    if enemy_collision:
        for enemy in enemy_collision:
            verAlive = measurement(DISPLAYSURF, P1.qGates, simulator, playerCircuit, quantumGateDict, enemy.kind)
            if verAlive == 0:
                die()
            else:
                P1.qGates = ["PauliX"]  # TODO: Change this to whatever gate gives the post measurement state we want
                enemy.kill()
                continue

    gate_collision = pygame.sprite.spritecollide(P1, gates, False)
    if gate_collision:
        for gate in gate_collision:
            if gate.kind == 'H':
                scorelist.append('H')
                score, scoreCircuit = Score_circuit('H', scoreCircuit, score, scorelist)
            elif gate.kind == 'CN':
                scorelist.append('CN')
                score, scoreCircuit = Score_circuit('CN', scoreCircuit, score, scorelist)
            P1.qGates.append(gate.kind)
            gate.kill()
            if score == 2:
                victory()

    # pygame.display.update()
    frame += 1
    frame = frame % 4
    FramePerSec.tick(FPS)
