import pygame, pytmx
from pytmx.util_pygame import load_pygame
import objects

def loadFile(file):
    mapdata = load_pygame(str(file))
    map = pygame.sprite.Group()
    data = pygame.sprite.Group()
    for x in range(6):
        for y in range(6):
            print data
            tile = mapdata.get_tile_image(x, y, 0)
            props = mapdata.get_tile_properties(x, y, 0)
            print props
            newtile = objects.tile(tile, [(x * 60) + 220, (y * 60) + 120], props["type"], [x, y])
            map.add(newtile)

    return map
