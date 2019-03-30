import pygame, pytmx, time, math, random, pickle
from game import *

# Six Moves - A PyWeek #27 Entry
# Copyright (c) 2019 Orion Williams

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Six Moves")
channel = pygame.mixer.Channel(0)
window.fill([0, 0, 0])
running = True
player = objects.player([250, 150])
screen = "menu"
level = 0
conveyerdata = []
terrain = None
starts = [[0, 0], [4, 0], [2,0], [0, 0], [0, 0], [2, 2], [0, 0], [4, 0], [0, 0], [0, 0], [2, 2], [2, 2], [1, 0], [0, 0], [0, 0], [1, 2], [4, 0], [0, 0], [2, 0], [0, 2], [0, 0], [0, 0], [0, 2], [0, 0], [2, 0], [0, 0], [2, 0], [0, 0], [4, 0], [1, 1]]
pygame.time.set_timer(pygame.USEREVENT, 500) #Update Animations every 0.5 seconds
pygame.time.set_timer(pygame.USEREVENT+1, 75)
fullscreen = False
music = True
sfx = True
load = True
options = open("./data/options.dat", "rb")
try:
    optionvalues = pickle.load(options)
except:
    load = False
if load:
    fullscreen = optionvalues[0]
    music = optionvalues[1]
    sfx = optionvalues[2]
options.close()
if fullscreen:
    window = pygame.display.set_mode([800, 600], pygame.FULLSCREEN)
unlocked = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
unlockedfile = open("./data/unlocked.dat", "rb")
try:
    unlocked = pickle.load(unlockedfile)
except:
    pass
unlockedfile.close()
about = pygame.image.load("./images/about.png")
lock = pygame.image.load("./images/lock.png")
logos = [pygame.image.load("./images/six-moves.png"), pygame.image.load("./images/six-moves2.png")]
logoindex = 0
logo = logos[logoindex]
playerimages = [pygame.image.load("./images/player/goo.png"), pygame.image.load("./images/player/dot.png"), pygame.image.load("./images/player/x5.png"), pygame.image.load("./images/player/x4.png"), pygame.image.load("./images/player/x3.png"),
                pygame.image.load("./images/player/x2.png"), pygame.image.load("./images/player/x.png")]
levelimages = [pygame.image.load("./images/levels/tutorial1.png"), pygame.image.load("./images/levels/tutorial2.png"), pygame.image.load("./images/levels/tutorial3.png"), pygame.image.load("./images/levels/level1.png"),
               pygame.image.load("./images/levels/level2.png"), pygame.image.load("./images/levels/level3.png"), pygame.image.load("./images/levels/level4.png"), pygame.image.load("./images/levels/level5.png"),
               pygame.image.load("./images/levels/conveyer1.png"), pygame.image.load("./images/levels/conveyer2.png"), pygame.image.load("./images/levels/conveyer3.png"), pygame.image.load("./images/levels/conveyer4.png"),
               pygame.image.load("./images/levels/conveyer5.png"), pygame.image.load("./images/levels/portal1.png"), pygame.image.load("./images/levels/portal2.png"), pygame.image.load("./images/levels/portal3.png"),
               pygame.image.load("./images/levels/key1.png"), pygame.image.load("./images/levels/key2.png"), pygame.image.load("./images/levels/key3.png"), pygame.image.load("./images/levels/crumble1.png"),
               pygame.image.load("./images/levels/crumble2.png"), pygame.image.load("./images/levels/crumble3.png"), pygame.image.load("./images/levels/trap1.png"), pygame.image.load("./images/levels/trap2.png"),
               pygame.image.load("./images/levels/trap3.png"), pygame.image.load("./images/levels/level23.png"), pygame.image.load("./images/levels/level24.png"), pygame.image.load("./images/levels/level25.png"),
               pygame.image.load("./images/levels/level26.png"), pygame.image.load("./images/levels/level27.png")]
menuimage = pygame.transform.scale(random.choice(levelimages), [1000, 1000])
menux = 0
menuy = 0
levelnames = ["Tutorial 1", "Tutorial 2", "Tutorial 3", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9", "Level 10", "Level 11", "Level 12", "Level 13", "Level 14", "Level 15", "Level 16", "Level 17", "Level 18", "Level 19", "Level 20", "Level 21", "Level 22", "Level 23", "Level 24", "Level 25", "Level 26", "Level 27"]
sequence = ["tutorial1", "tutorial2", "tutorial3", "level1", "level2", "level3", "level4", "level5", "conveyer1", "conveyer2", "conveyer3", "conveyer4", "conveyer5", "portal1", "portal2", "portal3", "key1", "key2", "key3", "crumble1", "crumble2", "crumble3", "trap1", "trap2", "trap3", "level23", "level24", "level25", "level26", "level27"]
howtoplayimages = [pygame.image.load("./images/howtoplay/goal.png"), pygame.image.load("./images/howtoplay/controls.png"), pygame.image.load("./images/howtoplay/objects.png"), pygame.image.load("./images/howtoplay/move.png")]
levels = {"level1":"level1", "level2":"level2", "tutorial1":"noprefs", "tutorial2":"noprefs", "tutorial3":"tutorial3", "level3":"level3", "level4":"level4", "level5":"level5",
          "conveyer1":"conveyer1", "conveyer2":"conveyer2", "conveyer3":"conveyer3", "conveyer4":"conveyer4", "conveyer5":"conveyer5",
          "portal1":"portal1", "portal2":"portal2", "portal3":"portal3", "key1":"key1", "key2":"key2", "key3":"key3",
          "crumble1":"crumble1", "crumble2":"crumble2", "crumble3":"crumble3", "trap1":"trap1", "trap2":"trap2", "trap3":"trap3",
          "level23":"level23", "level24":"level24", "level25":"level25", "level26":"level26", "level27":"level27"}
map, floor, traps, conveyerdata = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx", "./levels/" + str(levels[sequence[level]]) + ".txt")
moves = 6
Move = pygame.mixer.Sound("./sfx/Move.wav")
loops = ["./music/stroll.wav", "./music/fate.wav", "./music/thinking.wav"]
Move.set_volume(0.5)
mouse = [0, 0]
sounds = {"key": pygame.mixer.Sound("./sfx/Key.wav"), "portal": pygame.mixer.Sound("./sfx/Portal.wav"), "trap": pygame.mixer.Sound("./sfx/Trap.wav"), "win": pygame.mixer.Sound("./sfx/You Win.wav"), "wall":pygame.mixer.Sound("./sfx/Wall.wav"), "gem":pygame.mixer.Sound("./sfx/Gem.wav"), "splat":pygame.mixer.Sound("./sfx/Splat.wav")}
prev = "menu"
selectpage = 0
page = 0
trap = None
menusequence = 0

ui.setFontSize(36)
playb = ui.button("Play Game", [400, 95], [255, 255, 255], centered=True)
resumeb = ui.button("Resume Game", [400, 95], [255, 255, 255], centered=True)
howtoplayb = ui.button("How to Play", [400, 130], [255, 255, 255], centered=True)
settingsb = ui.button("Settings", [400, 165], [255, 255, 255], centered=True)
quitb = ui.button("Quit Game", [400, 200], [255, 255, 255], centered=True)
back = ui.button("Back", [5, 5], [255, 0, 0])
fullscreenb = ui.button("Toggle Fullscreen", [5, 105], [255, 255, 255])
musicb = ui.button("Toggle Music", [5, 195], [255, 255, 255])
sfxb = ui.button("Toggle SFX", [5, 285], [255, 255, 255])
aboutbutton = ui.button("More About this Game", [5, 375], [0, 128, 255])

goalbutton = ui.button("Goal of the Game", [5, 125], [255, 255, 255])
controlsbutton = ui.button("Controls", [5, 160], [255, 255, 255])
objectsbutton = ui.button("Objects and Obstacles", [5, 195], [255, 255, 255])
gamemechbutton = ui.button("Movement", [5, 230], [255, 255, 255])

if sfx:
    audio = ui.imagebutton("./images/buttons/audio.png", [730, 5], [60, 60])
else:
    audio = ui.imagebutton("./images/buttons/audio-off.png", [730, 5], [60, 60])

if music:
    musict = ui.imagebutton("./images/buttons/music.png", [665, 5], [60, 60])
else:
    musict = ui.imagebutton("./images/buttons/music-off.png", [665, 5], [60, 60])

ui.setFontSize(24)
restart = ui.button("Restart", [5, 30], [0, 200, 255])

ui.setFontSize(36)
startlevel = ui.button("Start Level", [400, 535], [0, 255, 0], centered=True)
next = ui.button("Next >", [675, 280], [255, 255, 255], centered=True)
previous = ui.button("< Prev.", [125, 280], [255, 255, 255], centered=True)

def update(action, grp=None): #Updates Specifed Group, if None Specifed, then all are Updated.
    global player, returnparameters, map, floor, traps
    returnparameters.sound = None
    if grp == None:
        traps.update(player.pos, action, returnparameters)
        floor.update(player.pos, action, returnparameters)
        map.update(player.pos, action, returnparameters)
    elif grp == map:
        map.update(player.pos, action, returnparameters)
    elif grp == floor:
        floor.update(player.pos, action, returnparameters)
    elif grp == traps:
        traps.update(player.pos, action, returnparameters)
    if not returnparameters.sound == None and not action == "move":
        sounds[returnparameters.sound].play()

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
        self.sound = None
        self.wallappearsat = -1, -1
        self.destroywall = None
        self.destroywallat = -1, -1
        self.conveyerdata = []
        self.floor = -1, -1
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
        self.sound = None
        self.wallappearsat = -1, -1
        self.destroywall = None
        self.destroywallat = -1, -1
        self.conveyerdata = []
        self.floor = -1, -1

returnparameters = ReturnParameters()

def resetGroups(): #Clears Group Values, see loadLevel() for re-loading groups
    global map, floor, traps
    map = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    traps = pygame.sprite.Group()

def loadLevel(): #Restarts the Level, reloads Groups, and Resets Return Parameters.
    global map, floor, traps, starts, level, levels, sequence, returnparameters, moves, conveyerdata
    resetGroups()
    player.reset(start=starts[level])
    map, floor, traps, conveyerdata = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                           "./levels/" + str(levels[sequence[level]]) + ".txt")
    returnparameters.reset()
    moves = 6

def tutorial(): #Displays Tutorial Text
    global level
    ui.setFontSize(24)
    if level == 0:
        ui.centeredText("Click on any open tile adjacent to your player to", [400, 470], [255, 255, 255], window)
        ui.centeredText("move to it. To check if a tile is open, just hover", [400, 500], [255, 255, 255], window)
        ui.centeredText("over it. If its bordered in green, then it is open.", [400, 530], [255, 255, 255], window)
        ui.centeredText("Complete the level by getting to the staircase.", [400, 560], [255, 255, 255], window)
    elif level == 1:
        ui.centeredText("Well Done!", [400, 470], [255, 255, 255], window)
        ui.centeredText("Now on to the main concept of the game, six moves.", [400, 500], [255, 255, 255], window)
        ui.centeredText("Try to complete this level in six moves or less.", [400, 530], [255, 255, 255], window)
    elif level == 2:
        ui.centeredText("Pretty easy, right?", [400, 470], [255, 255, 255], window)
        ui.centeredText("This one will be a little trickier, as theres something", [400, 500], [255, 255, 255], window)
        ui.centeredText("there you probably don't expect...", [400, 530], [255, 255, 255], window)
    elif level == 3:
        ui.centeredText("Good job!", [400, 470], [255, 255, 255], window)
        ui.centeredText("That it for now. But remember, it only gets", [400, 500], [255, 255, 255], window)
        ui.centeredText("more difficult from here...", [400, 530], [255, 255, 255], window)

def adjacent(oldpos, newpos):
    isAdjacent = False
    if oldpos[0] + 1 == newpos[0] or oldpos[0] - 1 == newpos[0] or (oldpos[0] == newpos[0] and not oldpos[1] == newpos[1]):
        if oldpos[1] + 1 == newpos[1] or oldpos[1] - 1 == newpos[1] or (oldpos[1] == newpos[1] and not oldpos[0] == newpos[0]):
            isAdjacent = True
    if oldpos == newpos:
        isAdjacent = True
    return isAdjacent

def howtoplay():
    global window, page, howtoplayimages
    if page == 0:
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("How to Play", [400, 5], [255, 255, 255], window)
        back.draw(window)
        ui.setFontSize(27)
        ui.text("Click on a Topic Below to learn more about it.", [5, 75], [255, 255, 255], window)
        goalbutton.draw(window)
        controlsbutton.draw(window)
        objectsbutton.draw(window)
        gamemechbutton.draw(window)
    elif page > 0:
        window.blit(howtoplayimages[page - 1], [0, 0])
        back.draw(window)

def drawCursor():
    global mouse, returnparameters
    if mouse[0] > 250 and mouse[0] < 550 and mouse[1] < 450 and mouse[1] > 150:
        coordinates = [mouse[0] - 250, mouse[1] - 150]
        coordinates = [math.floor(coordinates[0] / 60), math.floor(coordinates[1] / 60)]
        oldcoordinates = coordinates
        coordinates = [(coordinates[0] * 60)+250, (coordinates[1] * 60)+150]
        returnparameters.mouse = mouse
        returnparameters.type = None
        update("get", grp=map)
        acceptable = [None, "portal", "key", "exit", "gem"]
        if (returnparameters.type in acceptable or str(returnparameters.type).startswith("conveyer")) and adjacent(player.pos, oldcoordinates):
            pygame.draw.rect(window, [0, 255, 0], [coordinates[0], coordinates[1], 60, 60], 3)
        elif not adjacent(player.pos, oldcoordinates) and (returnparameters.type in acceptable or str(returnparameters.type).startswith("conveyer")):
            pygame.draw.rect(window, [0, 122, 255], [coordinates[0], coordinates[1], 60, 60], 3)
        else:
            pygame.draw.rect(window, [255, 0, 0], [coordinates[0], coordinates[1], 60, 60], 3)

def insideMap(position):
    inside = False
    if position[0] >= 0 and position[0] <= 4 and position[1] >= 0 and position[1] <= 4:
        inside = True
    return inside

def drawScreen():
    global floor, moves, window, traps, player, returnparameters, map, level, trap, surface
    ui.setFontSize(48)
    window.fill([0, 0, 0])
    traps.draw(window)
    floor.draw(window)
    map.draw(window)
    player.draw(window)
    ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
    drawCursor()
    audio.draw(window)
    musict.draw(window)
    returnparameters.mouse = player.rect.centerx, player.rect.centery
    returnparameters.type = None
    ui.setFontSize(24)
    ui.text(levelnames[level], [5, 5], [255, 255, 255], window)
    restart.draw(window)
    update("get", grp=map)
    if level < 4:
        tutorial()
    if returnparameters.won:
        ui.setFontSize(48)
        ui.centeredText("You Win!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        level += 1
        if level >= len(sequence):
            level = 30
        try:
            unlocked[level] = True
        except:
            pass
        if level < 30:
            loadLevel()
        returnparameters.won = False
    elif moves == 0:
        ui.centeredText("Out of Moves!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        loadLevel()
    elif trap:
        ui.setFontSize(36)
        ui.centeredText("You fell into a Trap!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        loadLevel()
        returnparameters.reset()
        trap = False
    elif not insideMap(player.pos) or returnparameters.type == "wall" or returnparameters.type == "door":
        sounds["splat"].play()
        animateDeath()
        ui.setFontSize(36)
        ui.centeredText("You crashed into a Wall!", [400, 55], [255, 255, 255], window)
        pygame.display.flip()
        time.sleep(2)
        loadLevel()
        returnparameters.reset()
    pygame.display.flip()
    returnparameters.mouse = mouse

def setMusic(file):
    global music, channel
    if music:
        channel.stop()
        sound = pygame.mixer.Sound(str(file))
        channel.play(sound, loops=50)

def updateAudioButtons():
    global sfx, audio
    if sfx:
        audio.changeImage("./images/buttons/audio.png", [60, 60])
    elif not sfx:
        audio.changeImage("./images/buttons/audio-off.png", [60, 60])

def updateMusicButtons():
    global music, musict
    if music:
        musict.changeImage("./images/buttons/music.png", [60, 60])
    elif not music:
        musict.changeImage("./images/buttons/music-off.png", [60, 60])

def toggleFullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode([800, 600], pygame.FULLSCREEN)
    elif not fullscreen:
        window = pygame.display.set_mode([800, 600])

def animateDeath():
    global map, floor, traps, player, playerimages, level, levelnames, surface
    for i in range(len(playerimages)):
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        audio.draw(window)
        musict.draw(window)
        ui.setFontSize(48)
        ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
        ui.setFontSize(24)
        ui.text(levelnames[level], [5, 5], [255, 255, 255], window)
        restart.draw(window)
        player.image = playerimages[i]
        window.blit(player.image, [player.rect.left, player.rect.top])
        pygame.display.flip()
        time.sleep(0.03)
    player.image = pygame.image.load("./images/player/goo.png")

def animatePlayer(oldpos, newpos):
    global window, map, floor, traps, player, level, levelnames, surface
    for i in range(20):
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        audio.draw(window)
        musict.draw(window)
        ui.setFontSize(48)
        ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
        ui.setFontSize(24)
        ui.text(levelnames[level], [5, 5], [255, 255, 255], window)
        restart.draw(window)
        if level < 4:
            tutorial()
        coordinates = [(oldpos[0] * 60) + ((newpos[0]-oldpos[0])*(3*i)) + 250, (oldpos[1] * 60) + ((newpos[1]-oldpos[1])*(3*i)) + 150]
        window.blit(player.image, coordinates)
        pygame.display.flip()

def teleportPlayer(oldpos, newpos):
    global window, map, floor, traps, player
    for i in range(30):
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        ui.setFontSize(48)
        ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
        ui.setFontSize(24)
        ui.text(levelnames[level], [5, 5], [255, 255, 255], window)
        restart.draw(window)
        audio.draw(window)
        musict.draw(window)
        if level < 4:
            tutorial()
        coordinates = [(oldpos[0]*60)+i+250, (oldpos[1]*60)+i+150]
        image = pygame.transform.scale(player.image, [60-(2*i), 60-(2*i)])
        window.blit(image, coordinates)
        pygame.display.flip()
    for i in range(30):
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        ui.setFontSize(48)
        ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
        audio.draw(window)
        musict.draw(window)
        ui.setFontSize(24)
        ui.text(levelnames[level], [5, 5], [255, 255, 255], window)
        restart.draw(window)
        if level < 4:
            tutorial()
        coordinates = [newpos[0]*60+(30-i)+250, newpos[1]*60+(30-i)+150]
        image = pygame.transform.scale(player.image, [(2*i), (2*i)])
        window.blit(image, coordinates)
        pygame.display.flip()

def animateSelect(direction):
    if direction == 1:
        for i in range(20):
            window.fill([0, 0, 0])
            ui.setFontSize(64)
            ui.centeredText("Level Select", [400, 5], [255, 255, 255], window)
            back.draw(window)
            if selectpage == 29:
                index = -1
            else:
                index = selectpage
            window.blit(levelimages[index], [250 - (28 * i), 150])
            ui.centeredText(str(levelnames[index]), [400 - (28 * i), 460], [255, 255, 255], window)
            window.blit(levelimages[index+1], [800 - (28 * i), 150])
            ui.centeredText(str(levelnames[index+1]), [950 - (28 * i), 460], [255, 255, 255], window)
            pygame.display.flip()
    elif direction == -1:
        for i in range(20):
            window.fill([0, 0, 0])
            ui.setFontSize(64)
            ui.centeredText("Level Select", [400, 5], [255, 255, 255], window)
            back.draw(window)
            if selectpage == 0:
                index = 0
                index2 = 29
            else:
                index = selectpage
                index2 = index - 1
            window.blit(levelimages[index], [250 + (28 * i), 150])
            ui.centeredText(str(levelnames[index]), [400 + (28 * i), 460], [255, 255, 255], window)
            window.blit(levelimages[index2], [-300 + (28 * i), 150])
            ui.centeredText(str(levelnames[index2]), [-150 + (28 * i), 460], [255, 255, 255], window)
            pygame.display.flip()

def move():
    global event, moves, sfx, returnparameters, player, map, Move, conveyerdata
    oldpos = player.pos
    sound = None
    if not oldpos == returnparameters.where: #IF NOT SAME TILE
        if not returnparameters.where[0] < 0 and not returnparameters.where[0] > 5 and not returnparameters.where[1] < 0 and not returnparameters.where[1] > 5:
            if oldpos[0]+1 == returnparameters.where[0] or oldpos[0]-1 == returnparameters.where[0] or (oldpos[0] == returnparameters.where[0] and not oldpos[1] == returnparameters.where[1]):
                if oldpos[1]+1 == returnparameters.where[1] or oldpos[1]-1 == returnparameters.where[1] or (oldpos[1] == returnparameters.where[1] and not oldpos[0] == returnparameters.where[0]):
                    player.pos = returnparameters.where
                    newpos = returnparameters.where
                    returnparameters.sound = None
                    returnparameters.conveyerdata = conveyerdata
                    update("move")
                    sound = returnparameters.sound
                    update("update")
                    if returnparameters.allclear:
                        player.moveto(returnparameters.where)
                        if returnparameters.moveagain:
                            animatePlayer(oldpos, newpos)
                            animatePlayer(newpos, player.pos)
                        else:
                            animatePlayer(oldpos, player.pos)
                        if not returnparameters.wallappear == None:
                            for i in returnparameters.wallappear:
                                map.add(objects.tile(None, [(i[0]*60)+250, (i[1]*60)+150], "wall", list(i), [None, None]))
                                returnparameters.wallappearsat = i
                                update("wallappear", grp=map)
                        if not returnparameters.destroywall == None:
                            for i in returnparameters.destroywall:
                                returnparameters.destroywallat = i
                                update("destroywall", grp=map)
                        if returnparameters.moveagain:
                            while returnparameters.moveagain and insideMap(player.pos):
                                oldpos = player.pos
                                update("move")
                                sound = returnparameters.sound
                                if not returnparameters.wallappear == None:
                                    for i in returnparameters.wallappear:
                                        map.add(
                                            objects.tile(None, [(i[0] * 60) + 250, (i[1] * 60) + 150], "wall", list(i),
                                                         [None, None]))
                                        returnparameters.wallappearsat = i
                                        update("wallappear", grp=map)
                                if not returnparameters.destroywall == None:
                                    for i in returnparameters.destroywall:
                                        returnparameters.destroywallat = i
                                        update("destroywall", grp=map)
                                if returnparameters.allclear:
                                    animatePlayer(player.pos, returnparameters.where)
                                    player.moveto(returnparameters.where)
                                update("update")
                            if sfx:
                                Move.play()
                            moves -= 1
                        elif not returnparameters.moveagain:
                            moves -= 1
                            if sfx:
                                Move.play()
                        update("reverse", grp=map)
                        if not insideMap(player.pos):
                            drawScreen()
                    else:
                        player.pos = oldpos
                        returnparameters.reset()
    if not sound == None and sfx:
        sounds[str(sound)].play()

setMusic("./music/sunshine.wav")

while running:
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
                    channel.pause()
                if event.key == pygame.K_r:
                    player.reset(start=starts[level])
                    resetGroups()
                    map, floor, traps, conveyerdata = maploader.loadFile("./levels/" + str(sequence[level]) + ".tmx",
                                                           "./levels/" + str(levels[sequence[level]]) + ".txt")
                    returnparameters.reset()
                    moves = 6
            elif screen == "pause":
                if event.key == pygame.K_ESCAPE:
                    screen = "game"
                    channel.unpause()
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
                        channel.stop()
                        running = False
                elif screen == "select":
                    if back.click(mouse):
                        screen = "menu"
                    if next.click(mouse):
                        animateSelect(1)
                        if selectpage < 30:
                            selectpage += 1
                        if selectpage == 30:
                            selectpage = 0
                    if previous.click(mouse):
                        animateSelect(-1)
                        if selectpage > 0:
                            selectpage -=1
                        elif selectpage <= 0:
                            selectpage = 29
                    if startlevel.click(mouse) and unlocked[selectpage]:
                        screen = "game"
                        level = selectpage
                        loadLevel()
                        setMusic(random.choice(loops))
                elif screen == "how to play":
                    if page == 0:
                        if back.click(mouse):
                            screen = prev
                        elif goalbutton.click(mouse):
                            page = 1
                        elif controlsbutton.click(mouse):
                            page = 2
                        elif objectsbutton.click(mouse):
                            page = 3
                        elif gamemechbutton.click(mouse):
                            page = 4
                    elif page > 0:
                        if back.click(mouse):
                            page = 0
                elif screen == "settings":
                    if back.click(mouse):
                        screen = prev
                    if fullscreenb.click(mouse):
                        fullscreen = not fullscreen
                        toggleFullscreen()
                    if sfxb.click(mouse):
                        sfx = not sfx
                        ui.sfx = sfx
                        updateAudioButtons()
                    if musicb.click(mouse):
                        music = not music
                        updateMusicButtons()
                        if not music:
                            channel.stop()
                    if aboutbutton.click(mouse):
                        screen = "about"
                elif screen == "about":
                    if back.click(mouse):
                        screen = "settings"
                elif screen == "pause":
                    if resumeb.click(mouse):
                        screen = "game"
                        channel.unpause()
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
                    if mouse[0] > 250 and mouse[0] < 550 and mouse[1] > 150 and mouse[1] < 450:
                        returnparameters.mouse = mouse
                        update("whereis")
                        move()
                        trap = returnparameters.trap
                        if not returnparameters.moveto == None:
                            oldpos = player.pos
                            player.moveto(returnparameters.moveto)
                            teleportPlayer(oldpos, player.pos)
                            returnparameters.reset()
                        if not returnparameters.update == None:
                            if returnparameters.update == "unlockdoor":
                                positions = returnparameters.door
                                for i in positions:
                                    returnparameters.door = i
                                    update(returnparameters.update)
                                returnparameters.reset()
                            elif returnparameters.update == "destroywall":
                                positions = returnparameters.destroywall
                            else:
                                update(returnparameters.update)
                                returnparameters.reset()

                    else:
                        if audio.click(mouse):
                            sfx = not sfx
                            updateAudioButtons()
                        if musict.click(mouse):
                            music = not music
                            updateMusicButtons()
                            if not music:
                                channel.stop()
                        if restart.click(mouse):
                            loadLevel()
        elif event.type == pygame.USEREVENT:
            if screen == "game":
                player.animate()
            if screen == "menu":
                if logoindex == 0:
                    logoindex = 1
                elif logoindex == 1:
                    logoindex = 0
                logo = logos[logoindex]
        elif event.type == pygame.USEREVENT+1:
            if screen == "game":
                update("animate")

    if screen == "menu":
        window.fill([0, 0, 0])

        if menux == -200 and menuy == -400 and menusequence == 0:
            menusequence = 1
        elif menux == 0 and menuy == -400 and menusequence == 1:
            menusequence = 2
        elif menux == -200 and menuy == 0 and menusequence == 2:
            menusequence = 3
        elif menux == 0 and menuy == 0 and menusequence == 3:
            menusequence = 0

        if menusequence == 0:
            menux -= 2
            menuy -= 4
        elif menusequence == 1:
            menux += 2
        elif menusequence == 2:
            menux -= 2
            menuy += 4
        elif menusequence == 3:
            menux += 2

        window.blit(menuimage, [menux, menuy])
        surf = pygame.surface.Surface([800, 250])
        surf.set_alpha(200)
        window.blit(surf, [0, 0])
        ui.setFontSize(64)
        window.blit(logo, [250, 0])
        playb.draw(window)
        howtoplayb.draw(window)
        settingsb.draw(window)
        quitb.draw(window)
        ui.setFontSize(16)
        ui.text("Copyright (c) 2019 Orion Williams", [1, 235], [255, 255, 255], window)
        if not channel.get_busy() and music:
            setMusic("./music/sunshine.wav")
    elif screen == "you win":
        channel.stop()
        if music:
            hero = pygame.mixer.Sound("./music/Heroic-Intro.wav")
            hero.play(2)
        window.fill([0, 0, 0])
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [i * 20, 30], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(4)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [800 - (20 * i), 100], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(3)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [400, 100], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("You've proven youself to be an outstanding...", [20 * i, 170], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(3)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [400, 100], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("You've proven youself to be an outstanding...", [400, 170], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("Thinker", [800 - (20 * i), 220], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(2)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [400, 100], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("You've proven youself to be an outstanding...", [400, 170], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("Thinker", [400, 220], [255, 255, 255], window)
            ui.centeredText("Problem Solver", [20 * i, 270], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(2)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [400, 100], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("You've proven youself to be an outstanding...", [400, 170], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("Thinker", [400, 220], [255, 255, 255], window)
            ui.centeredText("Problem Solver", [400, 270], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("And Last but not least...", [800 - (20 * i), 320], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(2)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Congratulations!", [400, 30], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("You finished the entire game!", [400, 100], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("You've proven youself to be an outstanding...", [400, 170], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("Thinker", [400, 220], [255, 255, 255], window)
            ui.centeredText("Problem Solver", [400, 270], [255, 255, 255], window)
            ui.setFontSize(24)
            ui.centeredText("And Last but not least...", [400, 320], [255, 255, 255], window)
            ui.setFontSize(36)
            ui.centeredText("A true Genius!", [800 - (20 * i), 400], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(4)
        for i in range(21):
            window.fill([0, 0, 0])
            ui.setFontSize(48)
            ui.centeredText("Thanks for Playing!", [20 * i, 276], [255, 255, 255], window)
            pygame.display.flip()
        time.sleep(4)
        screen = "menu"
        if music:
            setMusic("./music/sunshine.wav")
    elif screen == "select":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Level Select", [400, 5], [255, 255, 255], window)
        back.draw(window)
        window.blit(levelimages[selectpage], [250, 150])
        ui.centeredText(str(levelnames[selectpage]), [400, 460], [255, 255, 255], window)
        if not unlocked[selectpage]:
            window.blit(lock, [250, 525])
            ui.setFontSize(13)
            ui.text("This Level is not Unlocked Yet", [300, 555], [255, 255, 255], window)
        else:
            startlevel.draw(window)
        next.draw(window)
        previous.draw(window)
        if not channel.get_busy() and music:
            setMusic("./music/sunshine.wav")
    elif screen == "pause":
        window.fill([0, 0, 0])
        traps.draw(window)
        floor.draw(window)
        map.draw(window)
        player.draw(window)
        if level < 4:
            tutorial()
        surf = pygame.surface.Surface([800, 250])
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
        howtoplay()
    elif screen == "settings":
        window.fill([0, 0, 0])
        ui.setFontSize(64)
        ui.centeredText("Settings", [400, 5], [255, 255, 255], window)
        back.draw(window)
        fullscreenb.draw(window)
        musicb.draw(window)
        sfxb.draw(window)
        aboutbutton.draw(window)
        ui.setFontSize(36)
        ui.text("Fullscreen is:", [5, 75], [255, 255, 255], window)
        if not channel.get_busy() and music:
            setMusic("./music/sunshine.wav")
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
    elif screen == "about":
        window.fill([0, 0, 0])
        window.blit(about, [0, 0])
        back.draw(window)
    elif screen == "game":
        if level == 30:
            screen = "you win"
        else:
            drawScreen()
            if not channel.get_busy():
                setMusic(random.choice(loops))
            if returnparameters.moveagain and music:
                move()
                if not returnparameters.moveto == None:
                    player.moveto(returnparameters.moveto)
                    returnparameters.reset()
                if not returnparameters.update == None:
                    update(returnparameters.update)
                    returnparameters.reset()
    pygame.display.flip()
unlockedfile = open("./data/unlocked.dat", "wb")
pickle.dump(unlocked, unlockedfile)
unlockedfile.close()
options = open("./data/options.dat", "wb")
pickle.dump([fullscreen, music, sfx], options)
options.close()
pygame.quit()