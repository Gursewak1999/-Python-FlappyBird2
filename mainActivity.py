from game import *

# actual GameLoop
# game.gameloop()
isUi = True
UI_font = pygame.font.Font("assets/font/kenvector_future_thin.ttf", 24)

rightTap = pygame.image.load("assets/ui/tapLeft.png").convert_alpha()
leftTap = pygame.image.load("assets/ui/tapRight.png").convert_alpha()
gameOver = pygame.image.load("assets/ui/textGameOver.png").convert_alpha()
getReady = pygame.image.load("assets/ui/textGetReady.png").convert_alpha()
tap = [pygame.image.load("assets/ui/tap.png").convert_alpha(),
       pygame.image.load("assets/ui/tapTick.png").convert_alpha()]
settings_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/settings.png"), (60, 60)).convert_alpha()
back_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/back.png"), (60, 60)).convert_alpha()
sound_on_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/sound_on.png"), (60, 60)).convert_alpha()
sound_off_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/sound_off.png"), (60, 60)).convert_alpha()
music_on_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/music_on.png"), (60, 60)).convert_alpha()
music_off_icon = pygame.transform.scale(pygame.image.load("assets/ui/icons/music_off.png"), (60, 60)).convert_alpha()

isSoundOn = True
isMusicOn = True

_click = 0
_tap = tap[0]
_i = 0


def showSettings():
    global isSoundOn, isMusicOn

    padding = 100
    box_width = 300
    decr = (box_width + padding + box_width) // 2

    box1_x_from = (win_width // 2) - decr
    box1_x_to = box1_x_from + box_width

    box2_x_from = (win_width // 2) + decr - box_width
    box2_x_to = box2_x_from + box_width

    box1_y_from = box2_y_from = win_height // 2 - box_width // 2
    box1_y_to = box2_y_to = box1_x_from + box_width

    isSettings = True
    while isSettings:
        clock.tick(fps)
        game.updateBackground()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            elif e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                isSettings = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x in range(30, 30 + settings_icon.get_width()) and mouse_y in range(30,
                                                                                             30 + settings_icon.get_height()):
                    # back button
                    isSettings = False

                if mouse_x in range(box1_x_from, box1_x_to) and mouse_y in range(box1_y_from, box1_y_to):
                    # change Backgrounds
                    print("box1")
                    isSettings = False
                    pygame.time.delay(10)
                    chooseBackgrounds()

                if mouse_x in range(box2_x_from, box2_x_to) and mouse_y in range(box2_y_from, box2_y_to):
                    # change Player
                    print("box2")
                    isSettings = False
                    pygame.time.delay(10)
                    choosePlayer()

                if mouse_x in range(30, 30 + sound_on_icon.get_width()) and mouse_y in range(100,
                                                                                             100 + sound_on_icon.get_height()):
                    # sound ON/OFF Button
                    print("Sound btn")
                    if isSoundOn:
                        isSoundOn = False
                    else:
                        isSoundOn = True

                if mouse_x in range(30, 30 + music_on_icon.get_width()) and mouse_y in range(170,
                                                                                             170 + music_on_icon.get_height()):
                    # music ON/OFF Button
                    print("Music btn")
                    if isMusicOn:
                        isMusicOn = False
                    else:
                        isMusicOn = True

        font_surface = UI_font.render("SETTINGS", True, (40, 0, 255))
        _x = win_width // 2 - font_surface.get_width() // 2
        _y = 50
        win.blit(font_surface, (_x, _y))

        _x = 30
        _y = 30
        win.blit(back_icon, (_x, _y))

        _y = 100
        if isSoundOn:
            win.blit(sound_on_icon, (_x, _y))
        else:
            win.blit(sound_off_icon, (_x, _y))

        _y = 170
        if isMusicOn:
            win.blit(music_on_icon, (_x, _y))
        else:
            win.blit(music_off_icon, (_x, _y))

        pygame.draw.rect(win, (255, 255, 255),
                         (box1_x_from, box1_y_from, box1_x_to - box1_x_from, box1_y_to - box1_y_from))
        pygame.draw.rect(win, (255, 255, 255),
                         (box2_x_from, box2_y_from, box2_x_to - box2_x_from, box2_y_to - box2_y_from))

        font_surface = UI_font.render("Choose Background", True, (40, 0, 255))
        _x = (box1_x_from + box1_x_to) // 2 - font_surface.get_width() // 2
        _y = (box1_y_from + box1_y_to) // 2 - font_surface.get_height() // 2
        win.blit(font_surface, (_x, _y))

        font_surface = UI_font.render("Choose Player", True, (40, 0, 255))
        _x = (box2_x_from + box2_x_to) // 2 - font_surface.get_width() // 2
        _y = (box2_y_from + box2_y_to) // 2 - font_surface.get_height() // 2
        win.blit(font_surface, (_x, _y))

        pygame.display.update()


def chooseBackgrounds():
    isBackgrounds = True
    box_size = 200
    padding = 60

    box1_y_from = box2_y_from = box3_y_from = 200
    box4_y_from = box5_y_from = box1_y_from + box_size + padding

    box1_x_from = box4_x_from = win_width // 2 - 1.5 * box_size - padding
    box2_x_from = box5_x_from = box1_x_from + box_size + padding
    box3_x_from = box2_x_from + box_size + padding

    while isBackgrounds:
        clock.tick(fps)
        game.updateBackground()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            elif e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                isBackgrounds = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x in range(30, 30 + settings_icon.get_width()) and mouse_y in range(30,
                                                                                             30 + settings_icon.get_height()):
                    # back button
                    isBackgrounds = False
                if int(mouse_x) in range(int(box1_x_from), int(box1_x_from + box_size)) and int(mouse_y) in range(
                        int(box1_y_from), int(box1_y_from + box_size)):
                    # set background
                    print("background 1")
                    game.setBackgrounds(Backgrounds().getCastle())
                if int(mouse_x) in range(int(box2_x_from), int(box2_x_from + box_size)) and int(mouse_y) in range(
                        int(box2_y_from), int(box2_y_from + box_size)):
                    # set background
                    print("background 2")
                    game.setBackgrounds(Backgrounds().getDesert())

                if int(mouse_x) in range(int(box3_x_from), int(box3_x_from + box_size)) and int(mouse_y) in range(
                        int(box3_y_from), int(box3_y_from + box_size)):
                    # set background
                    print("background 3")
                    game.setBackgrounds(Backgrounds().getFall())

                if int(mouse_x) in range(int(box4_x_from), int(box4_x_from + box_size)) and int(mouse_y) in range(
                        int(box4_y_from), int(box4_y_from + box_size)):
                    # set background
                    print("background 4")
                    game.setBackgrounds(Backgrounds().getForest())

                if int(mouse_x) in range(int(box5_x_from), int(box5_x_from + box_size)) and int(mouse_y) in range(
                        int(box5_y_from), int(box5_y_from + box_size)):
                    # set background
                    print("background 5")
                    game.setBackgrounds(Backgrounds().getGrass())

        font_surface = UI_font.render("Choose Backgrounds", True, (40, 0, 255))
        _x = win_width // 2 - font_surface.get_width() // 2
        _y = 50
        win.blit(font_surface, (_x, _y))

        _x = 30
        _y = 30
        win.blit(back_icon, (_x, _y))

        # draw here boxes for backgrounds total = 5
        # consider 3 boxex in one row

        # box1
        pygame.draw.rect(win, (0, 0, 0),
                         (box1_x_from, box1_y_from, box_size, box_size))
        a, b = Backgrounds().getCastle()
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box1_x_from + 2, box1_y_from + 2, box_size, box_size))

        # box2
        pygame.draw.rect(win, (0, 0, 0),
                         (box2_x_from, box2_y_from, box_size, box_size))
        a, b = Backgrounds().getDesert()
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box2_x_from + 2, box2_y_from + 2, box_size, box_size))

        # box3
        pygame.draw.rect(win, (0, 0, 0),
                         (box3_x_from, box3_y_from, box_size, box_size))
        a, b = Backgrounds().getFall()
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box3_x_from + 2, box3_y_from + 2, box_size, box_size))

        # box4
        pygame.draw.rect(win, (0, 0, 0),
                         (box4_x_from, box4_y_from, box_size, box_size))
        a, b = Backgrounds().getForest()
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box4_x_from + 2, box4_y_from + 2, box_size, box_size))

        # box5
        pygame.draw.rect(win, (0, 0, 0),
                         (box5_x_from, box5_y_from, box_size, box_size))
        a, b = Backgrounds().getGrass()
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box5_x_from + 2, box5_y_from + 2, box_size, box_size))
        pygame.display.update()


def choosePlayer():
    isPlayer = True

    box_size = 150
    padding = 60

    box1_y_from = box2_y_from = box3_y_from = 100
    box4_y_from = box5_y_from = box6_y_from = box1_y_from + box_size + padding
    box7_y_from = box4_y_from + box_size + padding

    box1_x_from = box4_x_from = box7_x_from = win_width // 2 - 1.5 * box_size - padding
    box2_x_from = box5_x_from = box1_x_from + box_size + padding
    box3_x_from = box6_x_from = box2_x_from + box_size + padding

    while isPlayer:
        clock.tick(fps)
        game.updateBackground()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            elif e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                isPlayer = False
                pygame.time.delay(10)
                showSettings()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x in range(30, 30 + settings_icon.get_width()) and mouse_y in range(30,
                                                                                             30 + settings_icon.get_height()):
                    # back button
                    isPlayer = False
                if int(mouse_x) in range(int(box1_x_from), int(box1_x_from + box_size)) and int(mouse_y) in range(
                        int(box1_y_from), int(box1_y_from + box_size)):
                    # set Player
                    print("player 1")
                    player.setPlayer(Bird().getGreenPlane())
                if int(mouse_x) in range(int(box2_x_from), int(box2_x_from + box_size)) and int(mouse_y) in range(
                        int(box2_y_from), int(box2_y_from + box_size)):
                    # set Player
                    print("player 2")
                    player.setPlayer(Bird().getRedBird())

                if int(mouse_x) in range(int(box3_x_from), int(box3_x_from + box_size)) and int(mouse_y) in range(
                        int(box3_y_from), int(box3_y_from + box_size)):
                    # set Player
                    print("player 3")
                    player.setPlayer(Bird().getBlueBird())
                if int(mouse_x) in range(int(box4_x_from), int(box4_x_from + box_size)) and int(mouse_y) in range(
                        int(box4_y_from), int(box4_y_from + box_size)):
                    # set Player
                    print("player 4")
                    player.setPlayer(Bird().getGreenPlane())

                if int(mouse_x) in range(int(box5_x_from), int(box5_x_from + box_size)) and int(mouse_y) in range(
                        int(box5_y_from), int(box5_y_from + box_size)):
                    # set Player
                    print("player 5")
                    player.setPlayer(Bird().getRedBird())
                if int(mouse_x) in range(int(box6_x_from), int(box6_x_from + box_size)) and int(mouse_y) in range(
                        int(box6_y_from), int(box6_y_from + box_size)):
                    # set Player
                    print("player 6")
                    player.setPlayer(Bird().getYellowPlane())
                if int(mouse_x) in range(int(box7_x_from), int(box7_x_from + box_size)) and int(mouse_y) in range(
                        int(box7_y_from), int(box7_y_from + box_size)):
                    # set Player
                    print("player 7")
                    player.setPlayer(Bird().getYellowBird())

        font_surface = UI_font.render("Choose Player", True, (40, 0, 255))
        _x = win_width // 2 - font_surface.get_width() // 2
        _y = 50
        win.blit(font_surface, (_x, _y))

        _x = 30
        _y = 30
        win.blit(back_icon, (_x, _y))

        # draw here boxes for player total = 7
        # consider 3 boxex in one row

        # box1
        pygame.draw.rect(win, (0, 0, 0),
                         (box1_x_from, box1_y_from, box_size, box_size))
        a = Bird().getGreenPlane()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box1_x_from + 2, box1_y_from + 2, box_size, box_size))

        # box2
        pygame.draw.rect(win, (0, 0, 0),
                         (box2_x_from, box2_y_from, box_size, box_size))
        a = Bird().getRedBird()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box2_x_from + 2, box2_y_from + 2, box_size, box_size))

        # box3
        pygame.draw.rect(win, (0, 0, 0),
                         (box3_x_from, box3_y_from, box_size, box_size))
        a = Bird().getBlueBird()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box3_x_from + 2, box3_y_from + 2, box_size, box_size))

        # box4
        pygame.draw.rect(win, (0, 0, 0),
                         (box4_x_from, box4_y_from, box_size, box_size))
        a = Bird().getGreenPlane()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box4_x_from + 2, box4_y_from + 2, box_size, box_size))

        # box5
        pygame.draw.rect(win, (0, 0, 0),
                         (box5_x_from, box5_y_from, box_size, box_size))
        a = Bird().getRedPlane()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box5_x_from + 2, box5_y_from + 2, box_size, box_size))

        # box6
        pygame.draw.rect(win, (0, 0, 0),
                         (box6_x_from, box6_y_from, box_size, box_size))
        a = Bird().getYellowBird()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box6_x_from + 2, box6_y_from + 2, box_size, box_size))

        # box7
        pygame.draw.rect(win, (0, 0, 0),
                         (box7_x_from, box7_y_from, box_size, box_size))
        a = Bird().getYellowPlane()[0]
        a = pygame.transform.scale(a, (box_size - 4, box_size - 4))
        win.blit(a, (box7_x_from + 2, box7_y_from + 2, box_size, box_size))

        pygame.display.update()


def mouseClicked():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x in range(30, 30 + settings_icon.get_width()) and mouse_y in range(30, 30 + settings_icon.get_height()):
        showSettings()


def handleKeys():
    global isUi
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
            quit()
            break
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked()
        elif e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
            print("Space")
            isUi = False
            break


def drawUI():
    global _tap, _click, _i

    font_surface = UI_font.render("--Flappy Bird Remake--", True, (255, 255, 255))
    _x = win_width // 2 - font_surface.get_width() // 2
    _y = 100
    win.blit(font_surface, (_x, _y))

    font_surface = UI_font.render("--By: Gursewak Singh--", True, (255, 255, 225))
    _x = win_width // 2 - font_surface.get_width() // 2
    _y = 130
    win.blit(font_surface, (_x, _y))

    font_surface = UI_font.render("HighScore : " + highScore, True, (255, 45, 90))
    _x = win_width // 2 - font_surface.get_width() // 2
    _y = 300
    win.blit(font_surface, (_x, _y))

    _x = win_width // 2 - tap[0].get_width() // 2
    _y = 400

    _click = _click + 1

    if _click % 50 == 0:
        if _i == 0:
            _i = 1
        else:
            _i = 0

        _tap = tap[_i]

    win.blit(player.bird_1, (win_width // 2 - bird_width // 2, win_height // 2 - bird_height // 2))
    win.blit(_tap, (_x, _y))
    _x = win_width // 2 - leftTap.get_width() // 2 - 110
    win.blit(leftTap, (_x, _y))
    _x = win_width // 2 - rightTap.get_width() // 2 + 110
    win.blit(rightTap, (_x, _y))
    _x = 30
    _y = 30
    win.blit(settings_icon, (_x, _y))


def Ui():
    while isUi:
        clock.tick(fps)

        # draws backgrounds
        handleKeys()
        game.updateBackground()
        drawUI()
        pygame.display.update()


Ui()
pygame.time.delay(10)
game.gameloop()
