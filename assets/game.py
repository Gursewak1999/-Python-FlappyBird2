import pygame
from random import randrange
import math
import os

# Game Variables
win_width, win_height = 720, 1024
win_width, win_height = win_width // 2, win_height // 2
bird_width, bird_height = 50, 50
fps = 120
bird_angle = 0
pipeSpawnerInterval = 300
pipeSpawnerVar = 0
angle_incline, angle_decline = 60, 30
jump_dur = 300
velocity = 1
isRunning = True
paused = False
score = 0
PIPE_ADD_INTERVAL = 3000
isGameOver = False
isJumping = False
BIRD_JUMP_STEPS = 20

# read Previous Highscores
with open("highscore.text", "r") as file:
    highScore = file.read()

# Game Initialisation
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("FLapPy BiRd")
pygame.display.init()
pygame.mixer.init()
score_font = pygame.font.SysFont(None, 32, bold=True)
var = 0

# the bird stays in the same x position, so BIRD_X is a constant
bird_x = 50
bird_y = int(win_height / 2 - bird_height / 2)  # center bird on screen

pipes = []
# temporary Variable to switch frames for animation
_anim_frame = 0
frame = None

background = pygame.transform.scale(pygame.image.load("assets/background/backgroundCastles.png"),
                                    (2048, 512)).convert()
persistant = pygame.transform.scale(pygame.image.load("assets/background/persistantCastles.png"), (1024, 512)).convert()

bird_1 = pygame.transform.scale(pygame.image.load("assets/bird/Frame-1.png"), (bird_width, bird_height)).convert_alpha()
bird_2 = pygame.transform.scale(pygame.image.load("assets/bird/Frame-2.png"), (bird_width, bird_height)).convert_alpha()
bird_3 = pygame.transform.scale(pygame.image.load("assets/bird/Frame-3.png"), (bird_width, bird_height)).convert_alpha()
bird_4 = pygame.transform.scale(pygame.image.load("assets/bird/Frame-4.png"), (bird_width, bird_height)).convert_alpha()
cloud = [pygame.image.load("assets/clouds/cloud1.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud2.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud3.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud4.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud5.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud6.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud7.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud8.png").convert_alpha(),
         pygame.image.load("assets/clouds/cloud9.png").convert_alpha()]


class Game:

    def __init__(self):
        self.cloud1 = cloud[randrange(0, len(cloud))]
        self.cloud2 = cloud[randrange(0, len(cloud))]
        self.cloud3 = cloud[randrange(0, len(cloud))]

        self.cloud1_x = randrange(-200, 200)
        self.cloud2_x = randrange(-200, 200)
        self.cloud3_x = randrange(-200, 200)

        self.cloud1_y = randrange(0, 200)
        self.cloud2_y = randrange(0, 200)
        self.cloud3_y = randrange(0, 200)

        self.cloud1_divisor = randrange(1, 4)
        self.cloud2_divisor = randrange(1, 4)
        self.cloud3_divisor = randrange(1, 4)

    def updateBackground(self):
        global var, persistant, background, velocity, win_width
        var = var + velocity
        win.blit(persistant, (0, 0))
        if var >= 2048 + win_width:
            var = -win_width
        win.blit(background, (- var, 0))

        win.blit(self.cloud1, (600 - self.cloud1_x - var / self.cloud1_divisor, self.cloud1_y))
        win.blit(self.cloud2, (700 - self.cloud2_x - var / self.cloud2_divisor, self.cloud2_y))
        win.blit(self.cloud3, (800 - self.cloud3_x - var / self.cloud3_divisor, self.cloud3_y))

    def handleGameEvents(self):
        global paused, steps_to_jump, isRunning, bird_y
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                isRunning = False
                break
            elif e.type == pygame.KEYUP and e.key in (pygame.K_PAUSE, pygame.K_p):
                paused = not paused
            elif e.type == pygame.MOUSEBUTTONUP or (e.type == pygame.KEYUP and
                                                    e.key in (pygame.K_UP, pygame.K_RETURN, pygame.K_SPACE)):
                player.jump()
                bird_y = bird_y - 60
                steps_to_jump = BIRD_JUMP_STEPS

    def showScore(self):
        global win
        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = win_width / 2 - score_surface.get_width() / 2
        score_y = 100
        win.blit(score_surface, (score_x, score_y))

        score_surface = score_font.render("High Score: " + str(highScore), True, (255, 255, 255))
        score_x = win_width / 2 - score_surface.get_width() / 2
        score_y = 70
        win.blit(score_surface, (score_x, score_y))

    def gameloop(self):
        global pipeSpawnerVar
        while isRunning:
            clock.tick(fps)

            # draws backgrounds
            self.updateBackground()
            # handle key events
            self.handleGameEvents()
            # handle Player Animation
            player.getPlayer()

            if pipeSpawnerVar % pipeSpawnerInterval == 0:
                pipe = newPipe()
                pipes.append(pipe)
            for pipe in pipes:
                pipe.behave()

            self.showScore()
            pipeSpawnerVar += 1
            player.checkBoundaries()

            print(isJumping)
            pygame.display.update()

        with open("highscore.text", "w+") as file:
            file.write(str(score))


class newPipe:

    def __init__(self):
        self.pipeUp = pygame.transform.scale(pygame.image.load("assets/pipes/pipe-green-up.png"),
                                             (bird_width, win_height)).convert_alpha()
        self.pipeDown = pygame.transform.scale(pygame.image.load("assets/pipes/pipe-green-down.png"),
                                               (bird_width, win_height)).convert_alpha()

        # width between pipes HINT: Decrease width to inscrease width
        width = 150
        self.pipeTopHeight = width - win_height
        # self.collision_topHeight = win_height // 2 - width // 2
        # self.collision_botHeight = win_height // 2 + width // 2
        self.pipe_x = win_width

        self.differ = randrange(-150, 200, 30)

        self.pipe_top = self.pipeTopHeight + self.differ
        self.pipe_bottom = -self.pipeTopHeight + self.differ

    def move(self):
        self.pipe_x = self.pipe_x - 1

    def getPair(self):
        win.blit(self.pipeUp, (self.pipe_x, self.pipe_top))
        win.blit(self.pipeDown, (self.pipe_x, self.pipe_bottom))

    def isCollided(self):
        return (bird_y in range(0, self.pipe_top + win_height) or (bird_y + bird_height) in range(self.pipe_bottom,
                                                                                                  win_height)) and (
                       (bird_x + bird_width) in range(self.pipe_x, self.pipe_x + bird_width))

    def selfDestruct(self):
        if self.pipe_x + bird_width < 0:
            pipes.remove(self)

    def getScore(self):
        global score
        if (bird_y in range(self.pipe_top + win_height, self.pipe_bottom)) and (
                (bird_x + bird_width) == (self.pipe_x + self.pipe_x + bird_width) // 2):
            score = score + 1
        pass

    def behave(self):
        global isRunning
        self.getPair()
        self.move()
        self.getScore()
        if self.isCollided():
            isRunning = False
        self.selfDestruct()


class Player:

    def jump(self, jump_var=jump_dur):
        global win, bird_angle, angle_incline, bird_y, isJumping
        if jump_var > 0:
            jump_var = jump_var - 1
            self.jump(jump_var)
            isJumping = True
            if bird_angle < angle_incline:
                bird_angle = bird_angle + angle_incline / jump_dur
        else:
            isJumping = False
        return

    def getPlayer(self):
        global _anim_frame, win, bird_angle, clock, frame, bird_angle, angle_decline, angle_incline, bird_y, isJumping

        if bird_angle > -angle_decline:
            bird_angle = bird_angle - 2

        if not isJumping:
            bird_y = bird_y + 2


        if _anim_frame % 4 == 0:
            frame = bird_1
        elif _anim_frame % 4 == 1:
            frame = bird_2
        elif _anim_frame % 4 == 2:
            frame = bird_3
        elif _anim_frame % 4 == 3:
            frame = bird_4

        win.blit(pygame.transform.rotate(frame, bird_angle), (bird_x, bird_y))
        _anim_frame = _anim_frame + 1
        if _anim_frame >= 4:
            _anim_frame = 0

    def checkBoundaries(self):
        global isRunning
        if not 0 < bird_y < win_height - 50:
            isRunning = False


player = Player()
game = Game()
