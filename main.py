import pygame, pytmx, time, math
from game import *

# Copyright (c) 2019 Orion Williams

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Six Moves")
window.fill([0, 0, 0])
running = True
player = objects.player([250, 150])
screen = "menu"
level = 0
starts = [[0, 0], [4, 0], [2,0], [0, 0], [0, 0], [2, 2], [0, 0], [4, 0], [0, 0], [0, 0]]
sequence = ["tutorial1", "tutorial2", "tutorial3", "level1", "level2", "level3", "level4", "level5", "level6", "level7"]
levels = {"level1":"level1", "level2":"level2", "tutorial1":"noprefs", "tutorial2":"noprefs", "tutorial3":"tutorial3", "level3":"level3", "level4":"level4", "level5":"level5", "level6":"level6", "level7":"level7"}
map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx", "./levels/" + str(levels[sequence[level]]) + ".txt")
moves = 6
Move = pygame.mixer.Sound("./sfx/Move.wav")
Move.set_volume(0.5)
mouse = [0, 0]
fullscreen = False
prev = "menu"

ui.setFontSize(36)
playb = ui.button("Play Game", [400, 55], [255, 255, 255], centered=True)
resumeb = ui.button("Resume Game", [400, 55], [255, 255, 255], centered=True)
howtoplayb = ui.button("How to Play", [400, 85], [255, 255, 255], centered=True)
settingsb = ui.button("Settings", [400, 115], [255, 255, 255], centered=True)
quitb = ui.button("Quit Game", [400, 145], [255, 255, 255], centered=True)
back = ui.button("Back", [5, 5], [255, 255, 255])

class ReturnParameters(pygame.sprite.Sprite): #For use when updating sprite groups
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.allclear = True
        self.moveto = None
        self.door = None
        self.update = None
        self.mouse = -1, -1
        self.where = -1, -1
        self.moveagain = False
        self.trap = False
        self.won = False
        self.wallappear = None
        self.type = None
    def reset(self):
        self.allclear = True
        self.moveto = None
        self.door = None
        self.update = None
        self.mouse = -1, -1
        self.where = -1, -1
        self.moveagain = False
        self.trap = False
        self.won = False
        self.wallappear = None
        self.type = None

returnparameters = ReturnParameters()

def resetGroups():
    global map, floor, traps
    map = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    traps = pygame.sprite.Group()

def tutorial():
    global level
    ui.setFontSize(36)
    if level == 0:
        ui.centeredText("Click on any open adjacent tile to move to it.", [400, 470], [255, 255, 255], window)
        ui.centeredText("To check if a tile is open, just hover over it.", [400, 500], [255, 255, 255], window)
        ui.centeredText("If its bordered in green, then you can move there.", [400, 530], [255, 255, 255], window)
    elif level == 1:
        ui.centeredText("Well Done!", [400, 470], [255, 255, 255], window)
        ui.centeredText("Now lets get to the main concept of the game, six moves.", [400, 500], [255, 255, 255], window)
        ui.centeredText("Try to complete this level in six moves or less.", [400, 530], [255, 255, 255], window)
    elif level == 2:
        ui.centeredText("Pretty easy, right?", [400, 470], [255, 255, 255], window)
        ui.centeredText("This one will be a little harder, as theres something", [400, 500], [255, 255, 255], window)
        ui.centeredText("there you probably don't expect...", [400, 530], [255, 255, 255], window)

def drawScreen():
    global floor, moves, window, traps, player, returnparameters, map, level
    ui.setFontSize(48)
    window.fill([0, 0, 0])
    traps.draw(window)
    floor.draw(window)
    map.draw(window)
    player.draw(window)
    ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
    if level < 3:
        tutorial()
    drawCursor()
    if returnparameters.won:
        ui.centeredText("You Win!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        level += 1
        if level >= len(sequence):
            level = 0
        resetGroups()
        map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                               "./levels/" + str(levels[sequence[level]]) + ".txt")
        player.reset(start=starts[level])
        returnparameters.reset()
        moves = 6
        screen = "you win"
    if moves == 0:
        ui.centeredText("Out of Moves!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        resetGroups()
        map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                               "./levels/" + str(levels[sequence[level]]) + ".txt")
        player.reset(start=starts[level])
        returnparameters.reset()
        moves = 6
    if returnparameters.trap:
        ui.centeredText("You fell into a hidden Trap!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        resetGroups()
        map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                               "./levels/" + str(levels[sequence[level]]) + ".txt")
        player.reset(start=starts[level])
        returnparameters.reset()
        moves = 6
    pygame.display.flip()

def update(action):
    global player, returnparameters, map, floor, traps
    map.update(player.pos, action, returnparameters)
    floor.update(player.pos, action, returnparameters)
    traps.update(player.pos, action, returnparameters)

def drawCursor():
    global mouse, returnparameters
    if mouse[0] > 250 and mouse[0] < 550 and mouse[1] < 540 and mouse[1] > 150:
        coordinates = [mouse[0] - 250, mouse[1] - 150]
        coordinates = [math.floor(coordinates[0] / 60), math.floor(coordinates[1] / 60)]
        coordinates = [(coordinates[0] * 60)+250, (coordinates[1] * 60)+150]
        returnparameters.mouse = mouse
        update("get")
        if not returnparameters.type == "wall" and not returnparameters.type == "door":
            pygame.draw.rect(window, [0, 255, 0], [coordinates[0], coordinates[1], 60, 60], 3)
        else:
            pygame.draw.rect(window, [255, 0, 0], [coordinates[0], coordinates[1], 60, 60], 3)
        pygame.display.flip()

def move():
    global event, moves
    oldpos = player.pos
    if not oldpos == returnparameters.where: #IF NOT SAME TILE
        if not returnparameters.where[0] < 0 and not returnparameters.where[0] > 5 and not returnparameters.where[1] < 0 and not returnparameters.where[1] > 5:
            if oldpos[0]+1 == returnparameters.where[0] or oldpos[0]-1 == returnparameters.where[0] or (oldpos[0] == returnparameters.where[0] and not oldpos[1] == returnparameters.where[1]):
                if oldpos[1]+1 == returnparameters.where[1] or oldpos[1]-1 == returnparameters.where[1] or (oldpos[1] == returnparameters.where[1] and not oldpos[0] == returnparameters.where[0]):
                    player.pos = returnparameters.where
                    update("move")
                    if returnparameters.allclear:
                        player.moveto(returnparameters.where)
                        if not returnparameters.wallappear == None:
                            print map
                            map.add(objects.tile(None, [(returnparameters.wallappear[0]*60)+250, (returnparameters.wallappear[1]*60)+150], "wall", list(returnparameters.wallappear), [None, None]))
                            print map
                        if returnparameters.moveagain:
                            drawScreen()
                            time.sleep(0.1)
                            while returnparameters.moveagain:
                                update("move")
                                if returnparameters.allclear:
                                    player.moveto(returnparameters.where)
                                    drawScreen()
                                    time.sleep(0.1)
                            Move.play()
                        elif not returnparameters.moveagain:
                            moves -= 1
                            Move.play()
                    else:
                        player.pos = oldpos
                        returnparameters.reset()

pygame.mixer_music.load("./music/sunshine.wav")
pygame.mixer_music.play(50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10:
                fullscreen = not fullscreen
                if fullscreen:
                    window = pygame.display.set_mode([800, 600], pygame.FULLSCREEN)
                elif not fullscreen:
                    window = pygame.display.set_mode([800, 600])
            if screen == "game":
                if event.key == pygame.K_ESCAPE:
                    screen = "pause"
                if event.key == pygame.K_r:
                    player.reset(start=starts[level])
                    resetGroups()
                    map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                                           "./levels/" + str(levels[sequence[level]]) + ".txt")
                    returnparameters.reset()
                    moves = 6
            elif screen == "pause":
                if event.key == pygame.K_ESCAPE:
                    screen = "game"
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos[0], event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos[0], event.pos[1]
            pressed = pygame.mouse.get_pressed()
            if pressed[0]:
                if screen == "menu":
                    if playb.click(mouse):
                        screen = "game"
                        pygame.mixer_music.stop()
                        pygame.mixer_music.load("./music/stroll.wav")
                        pygame.mixer_music.play(50)
                    elif howtoplayb.click(mouse):
                        screen = "how to play"
                        prev = "menu"
                    elif settingsb.click(mouse):
                        screen = "settings"
                        prev = "menu"
                    elif quitb.click(mouse):
                        pygame.mixer_music.stop()
                        running = False
                elif screen == "how to play":
                    if back.click(mouse):
                        screen = prev
                elif screen == "settings":
                    if back.click(mouse):
                        screen = prev
                elif screen == "pause":
                    if resumeb.click(mouse):
                        screen = "game"
                    elif howtoplayb.click(mouse):
                        screen = "how to play"
                        prev = "pause"
                    elif settingsb.click(mouse):
                        screen = "settings"
                        prev = "pause"
                    elif quitb.click(mouse):
                        screen = "menu"
                elif screen == "game":
                    returnparameters.mouse = mouse
                    update("whereis")
                    print returnparameters.where
                    move()
                    if not returnparameters.moveto == None:
                        print returnparameters.moveto
                        player.moveto(returnparameters.moveto)
                        returnparameters.reset()
                    if not returnparameters.update == None:
                        update(returnparameters.update)
                        returnparameters.reset()

    if screen == "menu":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Six Moves", [400, 5], [255, 255, 255], window)
        playb.draw(window)
        howtoplayb.draw(window)
        settingsb.draw(window)
        quitb.draw(window)
    elif screen == "select":
        pass
    elif screen == "pause":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Game Paused", [400, 5], [255, 255, 255], window)
        resumeb.draw(window)
        howtoplayb.draw(window)
        settingsb.draw(window)
        quitb.draw(window)
    elif screen == "how to play":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("How to Play", [400, 5], [255, 255, 255], window)
        back.draw(window)
    elif screen == "settings":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Settings", [400, 5], [255, 255, 255], window)
        back.draw(window)
    elif screen == "you win":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("You Win!", [400, 5], [255, 255, 255], window)
    elif screen == "game":
        drawScreen()
        if returnparameters.moveagain:
            move()
            if not returnparameters.moveto == None:
                print returnparameters.moveto
                player.moveto(returnparameters.moveto)
                returnparameters.reset()
            if not returnparameters.update == None:
                update(returnparameters.update)
                returnparameters.reset()
    pygame.display.flip()
pygame.quit()