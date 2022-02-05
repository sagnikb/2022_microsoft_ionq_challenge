import pygame
import sys
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
import time
from Quantum_Measure import QuantumBackend
from random import choice
import copy

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1000
SMALL_SQ_DIM = 50
PACMAN_IMAGE = "Player.png"

# What kinds of gates and ghosts (measurements) are allowed in the game.
GATES = ['X', 'Y', 'Z']
SCORE_GATES = ['CN', 'H']
GHOSTS = ['X', 'Y', 'Z']

# Number of such ghosts and gates to generate
NUMBER_OF_GATES = 5
NUMBER_OF_SCORE_GATES = 2
NUMBER_OF_GHOSTS = 5

# Setting up game parameters
FPS = 10

pygame.init()
GAME_FONT = pygame.font.SysFont('Arial', 20)
GAME_FONT_LARGE = pygame.font.SysFont('Arial', 30)
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")
FramePerSec = pygame.time.Clock()

# Maze layout
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


class Sprite(pygame.sprite.Sprite):
    all_sprites = pygame.sprite.Group()

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.all_sprites.add(self)

    @property
    def current_tile(self) -> tuple[int, int]:
        """Computes the tile id of the current location

        Returns:
            tuple[int, int]: (row, column) of the current tile
        """
        return (self.rect.center[1]//SMALL_SQ_DIM,
                self.rect.center[0]//SMALL_SQ_DIM)

    def random_empty_cell(self) -> tuple[int, int]:
        """Selects a random empty legal cell with no Sprites on it

        Returns:
            tuple[int, int]: (row, col) of the cell
        """
        tiles_copy = copy.deepcopy(TILES)
        for sprite in self.all_sprites:
            tiles_copy[sprite.current_tile[1]][sprite.current_tile[0]] = 'X'
        gen_row = choice(list(range(2, 19)))
        indices = [i for i, col in enumerate(tiles_copy[gen_row]) if col == 1]
        gen_col = choice(indices)
        return (gen_row, gen_col)

    @staticmethod
    def tiles2center(location: tuple[int, int]) -> tuple[int, int]:
        """computes the center of the tile from the tile id

        Args:
            location (tuple[int, int]): tile id

        Returns:
            tuple[int, int]: location of center of tile
        """
        return(location[1]*SMALL_SQ_DIM + 25, location[0]*SMALL_SQ_DIM + 25)


class Enemy(Sprite):
    all_enemies = pygame.sprite.Group()

    def __init__(self, kind: str) -> None:
        """Initializes a moving measurement gate and sets the corresponding
        picture. For example, the picture for the X gate is EnemyX.png.

        Args:
            kind (str): the kind of measurement, one of ['X', 'Y', 'Z']
        """
        super().__init__()
        self.all_enemies.add(self)
        self.image = pygame.image.load(
                                "Enemy" + str(kind) + ".png").convert_alpha()
        self.kind = kind
        self.image = pygame.transform.smoothscale(
                                            self.image,
                                            (SMALL_SQ_DIM, SMALL_SQ_DIM)
                                        )
        self.rect = self.image.get_rect()
        self.rect.center = self.tiles2center(self.random_empty_cell())
        self.currentdir = (0, 0, 0, 1)

    def move(self, frame: int) -> None:
        """If the gate can move legally in its current direction, then move in
        that direction. If not, move randomly among the available legal
        directions. Move only when frame == 0.

        Args:
            frame (int): frame id, to control the movement speed of the sprite
        """
        if not frame:
            legal = []  # top = 0, down = 1, left = 2, right = 3
            (cur_row, cur_col) = (self.rect.center[1]//SMALL_SQ_DIM,
                                  self.rect.center[0]//SMALL_SQ_DIM)
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
                self.rect.move_ip(0, SMALL_SQ_DIM)
                self.currentdir = (0, 1, 0, 0)
            elif move == 2:
                self.rect.move_ip(-SMALL_SQ_DIM, 0)
                self.currentdir = (0, 0, 1, 0)
            else:
                self.rect.move_ip(SMALL_SQ_DIM, 0)
                self.currentdir = (0, 0, 0, 1)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the sprite at the current location

        Args:
            surface (pygame.Surface): the surface to be drawn on
        """
        surface.blit(self.image, self.rect)


class Pacman(Sprite):
    def __init__(self) -> None:
        """Initialized the pacman sprite. The image is set in the PACMAN_IMAGE
        variable.
        """
        super().__init__()
        self.kind = 'P'
        self.image = pygame.image.load(PACMAN_IMAGE).convert_alpha()
        self.image = pygame.transform.smoothscale(
                                                self.image,
                                                (SMALL_SQ_DIM, SMALL_SQ_DIM)
                                            )
        self.rect = self.image.get_rect()
        self.rect.center = self.tiles2center(self.random_empty_cell())
        self.qGates = []

    def update(self) -> None:
        """Takes the keypress and moves the sprite in that direction.
        """
        pressed_keys = pygame.key.get_pressed()
        (cur_row, cur_col) = (self.rect.center[1]//SMALL_SQ_DIM,
                              self.rect.center[0]//SMALL_SQ_DIM)
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

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the sprite at the current location

        Args:
            surface (pygame.Surface): the surface to be drawn on
        """
        surface.blit(self.image, self.rect)


class Gate(Sprite):
    all_gates = pygame.sprite.Group()

    def __init__(self, kind: str) -> None:
        """Initializes a non-moving gate

        Args:
            kind (str): the kind of gate, one of ['CN', 'H', 'X', 'Y', 'Z']
        """
        super().__init__()
        self.all_gates.add(self)
        self.kind = kind
        self.image = pygame.Surface([SMALL_SQ_DIM, SMALL_SQ_DIM])
        self.rect = self.image.get_rect()
        self.rect.center = self.tiles2center(self.random_empty_cell())

    def draw(self, surface: pygame.Surface) -> None:
        """Draws what kind of gate it is at the current location

        Args:
            surface (pygame.Surface): the surface to be drawn on
        """
        txt = pygame.font.Font.render(GAME_FONT, self.kind, True, WHITE)
        surface.blit(txt, (self.rect.centerx - SMALL_SQ_DIM/5,
                           self.rect.centery - SMALL_SQ_DIM/5))


class Game():
    P1 = Pacman()
    for i in range(NUMBER_OF_GHOSTS):
        Enemy(choice(GHOSTS))
    for i in range(NUMBER_OF_GATES):
        Gate(choice(GATES))
    for i in range(NUMBER_OF_SCORE_GATES):
        Gate('H')
        Gate('CN')

    def __init__(self) -> None:
        """initializes the quantum backend and variables
        """
        self.qb = QuantumBackend(0)
        self.scorelist = []
        self.frame = 0
        self.score = 0

    def draw(self) -> None:
        """draws the maze, score and sprites
        """
        for row_id, row in enumerate(TILES):
            for col_id, col in enumerate(row):
                if col == 0:
                    pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(
                        SMALL_SQ_DIM*col_id,
                        SMALL_SQ_DIM*row_id,
                        SMALL_SQ_DIM,
                        SMALL_SQ_DIM
                        )
                    )
        txt = pygame.font.Font.render(
                                    GAME_FONT_LARGE,
                                    "SCORE:" + str(self.score),
                                    True,
                                    RED
                                )
        DISPLAYSURF.blit(txt, (860, 960))
        for entity in Sprite.all_sprites:
            entity.draw(DISPLAYSURF)

    def finish_game(self) -> None:
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def die(self) -> None:
        DISPLAYSURF.fill(BLACK)
        txt = pygame.font.Font.render(
                                    GAME_FONT_LARGE,
                                    "You just died :D",
                                    True,
                                    WHITE
                                )
        DISPLAYSURF.blit(txt, (300, 400))
        pygame.display.update()
        self.finish_game()

    def victory(self) -> None:
        DISPLAYSURF.fill(BLACK)
        txt = pygame.font.Font.render(
                                    GAME_FONT_LARGE,
                                    "YOU WON! :D",
                                    True,
                                    WHITE
                                )
        DISPLAYSURF.blit(txt, (300, 400))
        pygame.display.update()
        self.finish_game()

    def measurement(self, player: Pacman, enemy: Enemy) -> int:
        """Pauses the game for the measurement, returns measurement result,
        called when pacman encounters a ghost.

        Args:
            player (Pacman): the player with associated quantum state
            enemy (Enemy): the gate performing the measurement

        Returns:
            int: the measurement result
        """
        DISPLAYSURF.fill(BLACK)
        txt = pygame.font.Font.render(
                                    GAME_FONT_LARGE,
                                    "You're being measured now!",
                                    True,
                                    WHITE
                                )
        DISPLAYSURF.blit(txt, (300, 300))
        pygame.display.update()
        verAlive = self.qb.execute_measurement(
                                                player.qGates,
                                                enemy.kind
                                            )
        time.sleep(2)
        txt2 = pygame.font.Font.render(
                                    GAME_FONT_LARGE,
                                    "Measurement result is... "+str(verAlive),
                                    True,
                                    WHITE
                                )
        DISPLAYSURF.blit(txt2, (300, 400))
        pygame.display.update()
        time.sleep(2)
        return verAlive

    def Score_fn(self):
        if 'H' in self.scorelist:
            idx = self.scorelist.index('H')
            if idx + 1 == len(self.scorelist):
                pass
            elif 'CN' in self.scorelist[idx+1:]:
                self.scorelist.pop(idx)
                self.scorelist.pop(self.scorelist.index('CN'))
                self.score += 1

    def main_loop(self) -> None:
        """main game loop

        Raises:
            NotImplementedError: if some gate is not implemented
        """
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            for enemy in Enemy.all_enemies:
                enemy.move(game.frame)
            self.P1.update()
            pygame.display.update()
            DISPLAYSURF.fill(BLACK)
            enemy_collision = pygame.sprite.spritecollide(
                                            self.P1,
                                            Enemy.all_enemies, False
                                        )
            if enemy_collision:
                for enemy in enemy_collision:
                    verAlive = self.measurement(self.P1, enemy)
                    if verAlive == 0:
                        self.die()
                    else:
                        if enemy.kind == 'Z':
                            self.P1.qGates = ['X']
                        elif enemy.kind == 'X':
                            self.P1.qGates = ['X', 'H']
                        elif enemy.kind == 'Y':
                            self.P1.qGates = ['X', 'H', 'S']
                        else:
                            raise NotImplementedError
                        enemy.kill()
                        continue
            gate_collision = pygame.sprite.spritecollide(
                                                self.P1,
                                                Gate.all_gates,
                                                False)
            if gate_collision:
                for gate in gate_collision:
                    if gate.kind in SCORE_GATES:
                        self.scorelist.append(gate.kind)
                    elif gate.kind in GATES:
                        self.P1.qGates.append(gate.kind)
                    gate.kill()
                self.Score_fn()
            '''Commenting since quantum scorecircuit has a bug
            if gate_collision:
                for gate in gate_collision:
                    if gate.kind == 'H':
                        self.scorelist.append('H')
                        self.score, self.scoreCircuit = self.quantumbackend.\
                            Score_circuit('H', self.score, self.scorelist)
                    elif gate.kind == 'CN':
                        self.scorelist.append('CN')
                        self.score, self.scoreCircuit = self.quantumbackend.\
                            Score_circuit('CN', self.score, self.scorelist)
                    self.P1.qGates.append(gate.kind)
                    gate.kill()
                    if self.score == 2:
                        self.victory()'''
            self.frame += 1
            self.frame = self.frame % 4
            FramePerSec.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.main_loop()
