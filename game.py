import pygame
from random import randrange, choice
import math
import os

# Game Variables
win_width, win_height = 1024, 720
# win_width, win_height = win_width // 2, win_height // 2
bird_width, bird_height = 50, 50
pipe_width = win_height // 10
spikes_width = win_width // 5
fps = 120
isSpike = False
bird_angle = 0
pipeSpawnerInterval = 320
pipeSpawnerVar = 0
angle_incline, angle_decline = 20, 70
jump_dur = 300
velocity = 1
isRunning = True
paused = False
score = 0
isGameOver = False
isJumping = False

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
bird_x = win_width // 5
bird_y = int(win_height / 2 - bird_height / 2)  # center bird on screen

pipes = []
# temporary Variable to switch frames for animation
_anim_frame = 0
frame = None


class Backgrounds:

    def __init__(self):
        self.width = 2 * win_width
        self.height = win_height

    def getDefault(self):
        return self.getCastle()

    def getCastle(self):
        return pygame.transform.scale(pygame.image.load("assets/background/backgroundCastles.png"),
                                      (self.width, self.height)).convert(), pygame.transform.scale(
            pygame.image.load("assets/background/persistantCastles.png"), (self.width, self.height)).convert()

    def getDesert(self):
        return pygame.transform.scale(pygame.image.load("assets/background/backgroundColorDesert.png"),
                                      (self.width, self.height)).convert(), pygame.transform.scale(
            pygame.image.load("assets/background/persistantDesert.png"), (self.width, self.height)).convert()

    def getFall(self):
        return pygame.transform.scale(pygame.image.load("assets/background/backgroundColorFall.png"),
                                      (self.width, self.height)).convert(), pygame.transform.scale(
            pygame.image.load("assets/background/persistantFall.png"), (self.width, self.height)).convert()

    def getForest(self):
        return pygame.transform.scale(pygame.image.load("assets/background/backgroundColorForest.png"),
                                      (self.width, self.height)).convert(), pygame.transform.scale(
            pygame.image.load("assets/background/persistantForest.png"), (self.width, self.height)).convert()

    def getGrass(self):
        return pygame.transform.scale(pygame.image.load("assets/background/backgroundColorGrass.png"),
                                      (self.width, self.height)).convert(), pygame.transform.scale(
            pygame.image.load("assets/background/persistantGrass.png"), (self.width, self.height)).convert()


class Bird:

    @staticmethod
    def getDefault():
        return Bird.getRedBird()

    @staticmethod
    def getBlueBird():
        return pygame.transform.scale(pygame.image.load("assets/bird/bluebird1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/bluebird2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/bluebird3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getRedBird():
        return pygame.transform.scale(pygame.image.load("assets/bird/redbird1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/redbird2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/redbird3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getYellowBird():
        return pygame.transform.scale(pygame.image.load("assets/bird/yellowbird1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/yellowbird2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/yellowbird3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getBluePlane():
        return pygame.transform.scale(pygame.image.load("assets/bird/planeBlue1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeBlue2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeBlue3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getGreenPlane():
        return pygame.transform.scale(pygame.image.load("assets/bird/planeGreen1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeGreen2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeGreen3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getRedPlane():
        return pygame.transform.scale(pygame.image.load("assets/bird/planeRed1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeRed2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeRed3.png"),
            (bird_width, bird_height)).convert_alpha()

    @staticmethod
    def getYellowPlane():
        return pygame.transform.scale(pygame.image.load("assets/bird/planeYellow1.png"),
                                      (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeYellow2.png"),
            (bird_width, bird_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/bird/planeYellow3.png"),
            (bird_width, bird_height)).convert_alpha()


class Pipes:
    def getGreen(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/pipe-green-up.png"),
                                      (pipe_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/pipe-green-down.png"),
            (pipe_width, win_height)).convert_alpha()

    def getRed(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/pipe-red-up.png"),
                                      (pipe_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/pipe-red-down.png"),
            (pipe_width, win_height)).convert_alpha()


class Spikes:

    def getRock(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/rockDown.png"),
                                      (spikes_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/rock.png"),
            (spikes_width, win_height)).convert_alpha()

    def getGrass(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/rockGrassDown.png"),
                                      (spikes_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/rockGrass.png"),
            (spikes_width, win_height)).convert_alpha()

    def getIce(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/rockIceDown.png"),
                                      (spikes_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/rockIce.png"),
            (spikes_width, win_height)).convert_alpha()

    def getSnow(self):
        return pygame.transform.scale(pygame.image.load("assets/pipes/rockSnowDown.png"),
                                      (spikes_width, win_height)).convert_alpha(), pygame.transform.scale(
            pygame.image.load("assets/pipes/rockSnow.png"),
            (spikes_width, win_height)).convert_alpha()


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

        self.background, self.persistant = Backgrounds().getDesert()
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
        global var, velocity, win_width
        var = var + velocity
        win.blit(self.persistant, (0, 0))
        if var >= 2048 + win_width:
            var = -win_width
        win.blit(self.background, (- var, 0))

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

    def showScore(self):
        global win

        score_surface = score_font.render("Score: " + str(score), True, (255, 255, 255))
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
                # pipe = newPipe()
                pipe = newPipe()
                pipes.append(pipe)
            for pipe in pipes:
                pipe.behave()

            self.showScore()
            pipeSpawnerVar += 1
            player.checkBoundaries()

            pygame.display.update()

        if int(highScore) < score:
            with open("highscore.text", "w+") as file:
                file.write(str(score))

    def setBackgrounds(self, param):

        self.background, self.persistant = param


class newPipe:

    def __init__(self):
        self.pipeUp, self.pipeDown = Pipes().getGreen()

        # width between upper and lower pipe, HINT: Decrease width to inscrease width

        self.width = 200

        self.pipeTopHeight = win_height // 2 - win_height
        self.pipe_x = win_width

        # changes pipes height randomly
        self.differ = randrange(0, win_height // 2 - 100, 20)
        self.differ = choice((-1, 1)) * self.differ

        self.pipe_top = self.pipeTopHeight - self.width // 2 - self.differ
        self.pipe_bottom = win_height // 2 + self.width // 2 - self.differ  # - differ
        # print("pipe ", self.pipe_top, "  ", self.pipe_bottom, " ", win_height // 2, "  ", width // 2)

    def move(self):
        self.pipe_x = self.pipe_x - 1

    def getPair(self):
        win.blit(self.pipeUp, (self.pipe_x, self.pipe_top))
        win.blit(self.pipeDown, (self.pipe_x, self.pipe_bottom))

    def isCollided(self):
        # pygame.draw.rect(win, (255, 0, 255), (self.pipe_x, 0, pipe_width,win_height // 2 - self.differ - self.width // 2))
        # pygame.draw.rect(win, (0, 0, 255), (self.pipe_x, self.pipe_bottom, pipe_width, win_height))

        if bird_x + bird_width in range(self.pipe_x, self.pipe_x + pipe_width) and (
                int(bird_y) in range(0, win_height // 2 - self.differ - self.width // 2) or int(
            bird_y + bird_height) in range(self.pipe_bottom, win_height)):
            print(" You Died")
            return True
        # print(self.pipe_bottom,"-",win_height, "  P",bird_y+bird_height)
        return False

    def selfDestruct(self):
        if self.pipe_x + pipe_width + 100 < 0:
            pipes.remove(self)

    def getScore(self):
        global score
        if (int(bird_y) in range(self.pipe_top + win_height, self.pipe_bottom)) and (
                int(bird_x + bird_width) == (self.pipe_x + self.pipe_x + bird_width) // 2):
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


class newSpikes:

    def __init__(self):
        self.spikeUp, self.spikeDown = Spikes().getSnow()

        # width between upper and lower pipe, HINT: Decrease width to inscrease width
        self.width = 200

        self.pipeTopHeight = win_height // 2 - win_height
        self.pipe_x = win_width

        # changes pipes height randomly
        self.differ = randrange(0, win_height // 2 - 100, 20)
        self.differ = choice((-1, 1)) * self.differ

        self.pipe_top = self.pipeTopHeight - self.width // 2 - self.differ
        self.pipe_bottom = win_height // 2 + self.width // 2 - self.differ  # - differ
        # print("pipe ", self.pipe_top, "  ", self.pipe_bottom, " ", win_height // 2, "  ", width // 2)

    def move(self):
        self.pipe_x = self.pipe_x - 1

    def getPair(self):
        win.blit(self.spikeUp, (self.pipe_x, self.pipe_top))
        win.blit(self.spikeDown, (self.pipe_x, self.pipe_bottom))

    def getSpikesX(self):
        # consider width with bird for variance
        w = (spikes_width / win_height) * (win_height - bird_y)
        w = int(w)
        return w

    def getSpikesX_up(self):
        w = (spikes_width / win_height) * (bird_y)
        w = int(w)
        return w

    def getSpikeCenter(self):
        return self.pipe_x + (spikes_width // 2)

    def isCollided(self):
        # print(self.getSpikeCenter() - self.getSpikesX(), self.getSpikeCenter() + self.getSpikesX())

        if ((int(bird_y) in range(0, win_height // 2 - self.differ - self.width // 2) and
             int(bird_x + bird_width) in range(self.getSpikeCenter() - self.getSpikesX_up(),
                                               self.getSpikeCenter() + self.getSpikesX_up()))):
            print("You Died UP")
            return True

        if (int(bird_y + bird_height) in range(self.pipe_bottom, win_height) and (int(
                bird_x + bird_width) in range(self.getSpikeCenter(), self.getSpikeCenter() + 2))):
            print("You Died Down")
            return True

        # print(self.pipe_bottom,"-",win_height, "  P",bird_y+bird_height)
        return False

    def selfDestruct(self):
        if self.pipe_x + pipe_width + 100 < 0:
            pipes.remove(self)

    def getScore(self):
        global score
        if (int(bird_y) in range(self.pipe_top + win_height, self.pipe_bottom)) and (
                int(bird_x + bird_width) == (self.pipe_x + self.pipe_x + bird_width) // 2):
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

    def __init(self):
        self.bird_1, self.bird_2, self.bird_3 = Bird().getDefault()

    @staticmethod
    def jump():
        global win, bird_angle, angle_incline, bird_y, isJumping

        bird_y -= 70
        isJumping = True
        if bird_angle <= angle_incline:
            bird_angle = angle_incline
        return

    def getPlayer(self):
        global _anim_frame, win, bird_angle, clock, frame, bird_angle, angle_decline, angle_incline, bird_y, isJumping

        if bird_angle >= -angle_decline:
            bird_angle -= velocity

        if (not isJumping) and bird_angle <= angle_decline:
            bird_y += 1.4 * velocity

        isJumping = False

        if _anim_frame % 3 == 0:
            frame = self.bird_1
        elif _anim_frame % 3 == 1:
            frame = self.bird_2
        elif _anim_frame % 3 == 2:
            frame = self.bird_3

        win.blit(pygame.transform.rotate(frame, bird_angle), (bird_x, bird_y))
        _anim_frame = _anim_frame + 1
        if _anim_frame >= 6:
            _anim_frame = 0

    @staticmethod
    def checkBoundaries():
        global isRunning
        if not 0 < bird_y < win_height - 50:
            isRunning = False

    def setPlayer(self, param):
        self.bird_1, self.bird_2, self.bird_3 = param
        pass


player = Player()
player.setPlayer(Bird().getDefault())
game = Game()
game.setBackgrounds(Backgrounds().getDesert())
