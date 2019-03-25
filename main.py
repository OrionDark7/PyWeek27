import pygame, pytmx, time, math
from game import *

# Six Moves - A PyWeek #27 Entry
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
music = True
sfx = True
prev = "menu"

ui.setFontSize(36)
playb = ui.button("Play Game", [400, 75], [255, 255, 255], centered=True)
resumeb = ui.button("Resume Game", [400, 75], [255, 255, 255], centered=True)
howtoplayb = ui.button("How to Play", [400, 110], [255, 255, 255], centered=True)
settingsb = ui.button("Settings", [400, 145], [255, 255, 255], centered=True)
quitb = ui.button("Quit Game", [400, 180], [255, 255, 255], centered=True)
back = ui.button("Back", [5, 5], [255, 255, 255])
fullscreenb = ui.button("Toggle Fullscreen", [5, 105], [255, 255, 255])
musicb = ui.button("Toggle Music", [5, 195], [255, 255, 255])
sfxb = ui.button("Toggle SFX", [5, 285], [255, 255, 255])

t1 = ui.imagebutton("./images/levels/tutorial1.png", [28, 100], [100, 100])

def update(action, grp=None): #Updates Specifed Group, if None Specifed, then all are Updated.
    global player, returnparameters, map, floor, traps
    if grp == None:
        map.update(player.pos, action, returnparameters)
        floor.update(player.pos, action, returnparameters)
        traps.update(player.pos, action, returnparameters)
    elif grp == map:
        map.update(player.pos, action, returnparameters)
    elif grp == floor:
        floor.update(player.pos, action, returnparameters)
    elif grp == traps:
        traps.update(player.pos, action, returnparameters)

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

def resetGroups(): #Clears Group Values, see loadLevel() for re-loading groups
    global map, floor, traps
    map = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    traps = pygame.sprite.Group()

def loadLevel(): #Restarts the Level, reloads Groups, and Resets Return Parameters.
    global map, floor, traps, starts, level, levels, sequence, returnparameters, moves
    resetGroups()
    player.reset(start=starts[level])
    map, floor, traps = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                           "./levels/" + str(levels[sequence[level]]) + ".txt")
    returnparameters.reset()
    moves = 6

def tutorial(): #Displays Tutorial Text
    global level
    ui.setFontSize(24)
    if level == 0:
        ui.centeredText("Click on any open adjacent tile to move to it.", [400, 470], [255, 255, 255], window)
        ui.centeredText("To check if a tile is open, just hover over it.", [400, 500], [255, 255, 255], window)
        ui.centeredText("If its bordered in green, then you can move there.", [400, 530], [255, 255, 255], window)
    elif level == 1:
        ui.centeredText("Well Done!", [400, 470], [255, 255, 255], window)
        ui.centeredText("Now on to the main concept of the game, six moves.", [400, 500], [255, 255, 255], window)
        ui.centeredText("Try to complete this level in six moves or less.", [400, 530], [255, 255, 255], window)
    elif level == 2:
        ui.centeredText("Pretty easy, right?", [400, 470], [255, 255, 255], window)
        ui.centeredText("This one will be a little harder, as theres something", [400, 500], [255, 255, 255], window)
        ui.centeredText("there you probably don't expect...", [400, 530], [255, 255, 255], window)
    elif level == 3:
        ui.centeredText("Good job!", [400, 470], [255, 255, 255], window)
        ui.centeredText("That it for now. But remember, it only gets", [400, 500], [255, 255, 255], window)
        ui.centeredText("more difficult from here...", [400, 530], [255, 255, 255], window)

def drawCursor():
    global mouse, returnparameters
    if mouse[0] > 250 and mouse[0] < 550 and mouse[1] < 450 and mouse[1] > 150:
        coordinates = [mouse[0] - 250, mouse[1] - 150]
        coordinates = [math.floor(coordinates[0] / 60), math.floor(coordinates[1] / 60)]
        coordinates = [(coordinates[0] * 60)+250, (coordinates[1] * 60)+150]
        returnparameters.mouse = mouse
        update("get")
        if not returnparameters.type == "wall" and not returnparameters.type == "door" and not returnparameters.type == None:
            pygame.draw.rect(window, [0, 255, 0], [coordinates[0], coordinates[1], 60, 60], 3)
        else:
            pygame.draw.rect(window, [255, 0, 0], [coordinates[0], coordinates[1], 60, 60], 3)

def drawScreen():
    global floor, moves, window, traps, player, returnparameters, map, level
    ui.setFontSize(48)
    window.fill([0, 0, 0])
    traps.draw(window)
    floor.draw(window)
    map.draw(window)
    player.draw(window)
    ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
    drawCursor()
    if level < 4:
        tutorial()
    if returnparameters.won:
        ui.centeredText("You Win!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        level += 1
        if level >= len(sequence):
            level = 0
        loadLevel()
        screen = "you win"
    if moves == 0:
        ui.centeredText("Out of Moves!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        loadLevel()
    if returnparameters.trap:
        ui.centeredText("You fell into a hidden Trap!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        loadLevel()
    pygame.display.flip()

def setMusic(file):
    global music
    if music:
        pygame.mixer_music.stop()
        pygame.mixer_music.load(str(file))
        pygame.mixer_music.play(50)

def toggleFullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode([800, 600], pygame.FULLSCREEN)
    elif not fullscreen:
        window = pygame.display.set_mode([800, 600])

def move():
    global event, moves, sfx, returnparameters, player, map, Move
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
                            map.add(objects.tile(None, [(returnparameters.wallappear[0]*60)+250, (returnparameters.wallappear[1]*60)+150], "wall", list(returnparameters.wallappear), [None, None]))
                        if returnparameters.moveagain:
                            drawScreen()
                            time.sleep(0.1)
                            while returnparameters.moveagain:
                                update("move")
                                if returnparameters.allclear:
                                    player.moveto(returnparameters.where)
                                    drawScreen()
                                    time.sleep(0.1)
                            if sfx:
                                Move.play()
                        elif not returnparameters.moveagain:
                            moves -= 1
                            if sfx:
                                Move.play()
                    else:
                        player.pos = oldpos
                        returnparameters.reset()

setMusic("./music/sunshine.wav")

while running:
    print music
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10:
                fullscreen = not fullscreen
                toggleFullscreen()
            if screen == "game":
                if event.key == pygame.K_ESCAPE:
                    screen = "pause"
                    pygame.mixer_music.pause()
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
                    pygame.mixer_music.unpause()
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos[0], event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos[0], event.pos[1]
            pressed = pygame.mouse.get_pressed()
            if pressed[0]:
                if screen == "menu":
                    if playb.click(mouse):
                        screen = "select"
                    elif howtoplayb.click(mouse):
                        screen = "how to play"
                        prev = "menu"
                    elif settingsb.click(mouse):
                        screen = "settings"
                        prev = "menu"
                    elif quitb.click(mouse):
                        pygame.mixer_music.stop()
                        running = False
                elif screen == "select":
                    if back.click(mouse):
                        screen = "menu"
                    if t1.click(mouse):
                        screen = "game"
                        level = 0
                        loadLevel()
                        setMusic("./music/stroll.wav")
                elif screen == "how to play":
                    if back.click(mouse):
                        screen = prev
                elif screen == "settings":
                    if back.click(mouse):
                        screen = prev
                    if fullscreenb.click(mouse):
                        fullscreen = not fullscreen
                        toggleFullscreen()
                    if sfxb.click(mouse):
                        sfx = not sfx
                        objects.sfx = sfx
                        ui.sfx = sfx
                    if musicb.click(mouse):
                        music = not music
                        if not music:
                            pygame.mixer_music.stop()
                elif screen == "pause":
                    if resumeb.click(mouse):
                        screen = "game"
                        pygame.mixer_music.unpause()
                    elif howtoplayb.click(mouse):
                        screen = "how to play"
                        prev = "pause"
                    elif settingsb.click(mouse):
                        screen = "settings"
                        prev = "pause"
                    elif quitb.click(mouse):
                        screen = "menu"
                        setMusic("./music/sunshine.wav")
                elif screen == "game":
                    returnparameters.mouse = mouse
                    update("whereis")
                    move()
                    if not returnparameters.moveto == None:
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
        ui.setFontSize(16)
        ui.text("Copyright (c) 2019 Orion Williams", [5, 580], [255, 255, 255],window)
    elif screen == "select":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Level Select", [400, 5], [255, 255, 255], window)
        back.draw(window)
        ui.setFontSize(16)
        t1.draw(window)
        ui.centeredText("Tutorial 1", [78, 205], [255, 255, 255], window)
    elif screen == "pause":
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        player.draw(window)
        if level < 4:
            tutorial()
        surf = pygame.surface.Surface([800, 220])
        surf.set_alpha(200)
        window.blit(surf, [0, 0])
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
        fullscreenb.draw(window)
        musicb.draw(window)
        sfxb.draw(window)
        ui.setFontSize(36)
        ui.text("Fullscreen is:", [5, 75], [255, 255, 255], window)
        if fullscreen:
            ui.text("On", [315, 75], [0, 255, 0], window)
        else:
            ui.text("Off", [315, 75], [255, 0, 0], window)

        ui.text("Music is:", [5, 165], [255, 255, 255], window)
        if music:
            ui.text("On", [195, 165], [0, 255, 0], window)
        else:
            ui.text("Off", [195, 165], [255, 0, 0], window)

        ui.text("Sound Effects are:", [5, 255], [255, 255, 255], window)
        if sfx:
            ui.text("On", [415, 255], [0, 255, 0], window)
        else:
            ui.text("Off", [415, 255], [255, 0, 0], window)
    elif screen == "you win":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("You Win!", [400, 5], [255, 255, 255], window)
    elif screen == "game":
        drawScreen()
        if returnparameters.moveagain:
            move()
            if not returnparameters.moveto == None:
                player.moveto(returnparameters.moveto)
                returnparameters.reset()
            if not returnparameters.update == None:
                update(returnparameters.update)
                returnparameters.reset()
    pygame.display.flip()
pygame.quit()