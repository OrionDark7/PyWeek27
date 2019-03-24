import pygame, pytmx, time
from game import *

# Copyright (c) 2019 Orion Williams

pygame.init()
window = pygame.display.set_mode([800, 600])
window.fill([0, 0, 0])
running = True
ui.setFontSize(48)
player = objects.player([220, 120])
screen = "game"
map = maploader.loadFile("./levels/level1.tmx")
moves = 6

class ReturnParameters(): #For use when updating sprite groups
    def __init__(self):
        allclear = True
returnparameters = ReturnParameters()

def move():
    global event, moves
    if event.key == pygame.K_LEFT and not player.pos[0] == 0:
        returnparameters.allclear = True
        player.pos = player.pos[0] - 1, player.pos[1]
        map.update(player.pos, "move", returnparameters)
        if returnparameters.allclear:
            player.rect.left -= 60
            moves -= 1
        else:
            player.pos = player.pos[0] + 1, player.pos[1]
    elif event.key == pygame.K_RIGHT and not player.pos[0] == 5:
        returnparameters.allclear = True
        player.pos = player.pos[0] + 1, player.pos[1]
        map.update(player.pos, "move", returnparameters)
        if returnparameters.allclear:
            player.rect.left += 60
            moves -= 1
        else:
            player.pos = player.pos[0] - 1, player.pos[1]
    elif event.key == pygame.K_DOWN and not player.pos[1] == 5:
        returnparameters.allclear = True
        player.pos = player.pos[0], player.pos[1] + 1
        map.update(player.pos, "move", returnparameters)
        if returnparameters.allclear:
            player.rect.top += 60
            moves -= 1
        else:
            player.pos = player.pos[0], player.pos[1] - 1
    elif event.key == pygame.K_UP and not player.pos[1] == 0:
        returnparameters.allclear = True
        player.pos = player.pos[0], player.pos[1] - 1
        map.update(player.pos, "move", returnparameters)
        if returnparameters.allclear:
            player.rect.top -= 60
            moves -= 1
        else:
            player.pos = player.pos[0], player.pos[1] + 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN and not moves == 0:
                move()

    if screen == "menu":
        window.fill([0, 0, 0])
        ui.centeredText("game", [400, 5], [255, 255, 255], window)
    elif screen == "game":
        window.fill([0, 0, 0])
        map.draw(window)
        player.draw(window)
        ui.centeredText("Moves: " + str(moves), [400, 5], [255, 255, 255], window)
        if moves == 0:
            ui.centeredText("Out of Moves!", [400, 55], [255, 255, 255], window)
            pygame.display.flip()
            print "out of moves!"
            time.sleep(2)
            player.reset()
            moves = 6
    pygame.display.flip()
pygame.quit()