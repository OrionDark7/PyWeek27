import pygame, pytmx
from pytmx.util_pygame import load_pygame
import objects

def stringToTuple(oldstring):
    if oldstring.endswith("\n"):
        oldstring = oldstring[1:len(oldstring) - 2]
    else:
        oldstring = oldstring[1:len(oldstring) - 1]
    pos = oldstring.split(",")
    pos[0] = int(pos[0])
    pos[1] = int(pos[1][0])
    return tuple(pos)

def loadFile(file,meta):
    data = {}
    conveyerdata = []
    metadata = open(str(meta), "rb")
    for i in range(10):
        try:
            line = metadata.readline()
        except:
            break
        if line == "":
            break
        else:
            if "=" in line:
                line = line.split("=")
                pos = stringToTuple(line[1])
                data[line[0]] = [pos, "p2p"]  # Portal to Portal
            elif ">" in line:
                line = line.split(">")
                if " " in line[1]:
                    line[1] = line[1].split(" ")
                    positions = []
                    for i in line[1]:
                        pos = stringToTuple(i)
                        positions.append(pos)
                    data[line[0]] = [positions, "k2d"]
                else:
                    pos = stringToTuple(line[1])
                    data[line[0]] = [[pos], "k2d"]  # Key opens Door
            elif "dw" in line:
                line = line.split("dw")
                if " " in line[1]:
                    line[1] = line[1].split(" ")
                    positions = []
                    for i in line[1]:
                        pos = stringToTuple(i)
                        positions.append(pos)
                    data[line[0]] = [positions, "dswall"]  # Imaginary Field destroys multiple Walls
                else:
                    pos = stringToTuple(line[1])
                    data[line[0]] = [[pos], "dswall"]  # Imaginary Field destroys Wall
            elif "w" in line:
                line = line.split("w")
                if " " in line[1]:
                    line[1] = line[1].split(" ")
                    positions = []
                    for i in line[1]:
                        pos = stringToTuple(i)
                        positions.append(pos)
                    data[line[0]] = [positions, "wall"]  # Imaginary Field triggers Multiple Walls
                else:
                    pos = stringToTuple(line[1])
                    data[line[0]] = [[pos], "wall"]  # Imaginary Field triggers Wall
            elif "r" in line:
                line = line.split("r")
                if " " in line[1]:
                    line[1] = line[1].split(" ")
                    positions = []
                    for i in line[1]:
                        pos = stringToTuple(i)
                        positions.append(pos)
                    conveyerdata = [positions, "rev"]  # Conveyor Belts Reverse Direction Every Turn.
                else:
                    pos = stringToTuple(line[1])
                    conveyerdata = [[pos], "rev"]  # Conveyer Belt Reverses Direction Every Turn.
    metadata.close()
    mapdata = load_pygame(str(file))
    map = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    trap = pygame.sprite.Group()
    for x in range(5):
        for y in range(5):
            tile = mapdata.get_tile_image(x, y, 2)
            props = mapdata.get_tile_properties(x, y, 2)
            if not tile == None:
                datastr = str((x,y))
                try:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], data[datastr])
                except:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], [None, None])
                map.add(newtile)

            tile = mapdata.get_tile_image(x, y, 1)
            props = mapdata.get_tile_properties(x, y, 1)

            if not tile == None:
                datastr = str((x,y))
                try:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], data[datastr])
                except:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], [None, None])
                floor.add(newtile)

            tile = mapdata.get_tile_image(x, y, 0)
            props = mapdata.get_tile_properties(x, y, 0)

            if not tile == None:
                datastr = str((x, y))
                try:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], data[datastr])
                except:
                    newtile = objects.tile(tile, [(x * 60) + 250, (y * 60) + 150], props["type"], [x, y], [None, None])
                trap.add(newtile)

    return map, floor, trap, conveyerdata
