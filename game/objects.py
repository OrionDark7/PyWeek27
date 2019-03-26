import pygame

pygame.init()

class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("./images/player/goo.png"), pygame.image.load("./images/player/goo2.png")]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.pos = [0, 0]
    def draw(self, surface):
        surface.blit(self.image, [self.rect.left, self.rect.top])
    def moveto(self, pos):
        self.pos = pos
        self.rect.left, self.rect.top = (pos[0] * 60) + 250, (pos[1] * 60) + 150
    def reset(self, start=[0, 0]):
        self.rect.left, self.rect.top = [250 + start[0]*60, 150 + start[1]*60]
        self.pos = start
    def animate(self):
        if self.index == 0:
            self.index = 1
        else:
            self.index = 0
        self.image = self.images[self.index]

class tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, type, objectpos, data):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = [None, None]
        self.image = pygame.image.load("./images/tiles/" + type + ".png")
        if type == "portal":
            self.images = [pygame.image.load("./images/tiles/portal.png"), pygame.image.load("./images/tiles/portal2.png")]
            self.image = self.images[self.index]
        else:
            self.image = pygame.image.load("./images/tiles/" + type + ".png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.type = type
        self.pos = objectpos
        self.data = data
        self.crumble = False
        self.count = 0
    def update(self, pos, action, allclear):
        if action == "animate" and self.type == "portal":
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0
            self.image = self.images[self.index]
        if action == "get" and self.rect.collidepoint(allclear.mouse):
            allclear.type = self.type
        if action == "move":
            self.count += 1
            if self.type == "crumble" and self.crumble and self.crumbletime + 1 == self.count:
                self.type = "trap"
                self.image = pygame.image.load("./images/tiles/" + self.type + ".png")
            if self.pos == list(pos):
                if self.data[1] == "wall":
                    allclear.wallappear = self.data[0]
                    allclear.sound = "wall"
                if self.type == "tile":
                    allclear.moveagain = False
                elif self.type == "wall" or self.type == "door":
                    allclear.allclear = False
                    allclear.moveagain = False
                elif self.type == "portal" and self.data[1] == "p2p":
                    allclear.allclear = True
                    allclear.moveto = self.data[0]
                    allclear.moveagain = False
                    allclear.sound = "portal"
                elif self.type == "key":
                    allclear.allclear = True
                    allclear.update = "unlockdoor"
                    allclear.door = self.data[0]
                    allclear.moveagain = False
                    allclear.sound = "key"
                    self.kill()
                elif self.type == "exit":
                    allclear.moveagain = False
                    allclear.won = True
                    allclear.sound = "win"
                elif self.type.startswith("conveyer"):
                    allclear.allclear = True
                    conveyertype = self.type.split("conveyer-")[1]
                    if conveyertype == "left":
                        allclear.moveagain = True
                        allclear.where = self.pos[0] - 1, self.pos[1]
                    if conveyertype == "right":
                        allclear.moveagain = True
                        allclear.where = self.pos[0] + 1, self.pos[1]
                    if conveyertype == "down":
                        allclear.moveagain = True
                        allclear.where = self.pos[0], self.pos[1] + 1
                    if conveyertype == "up":
                        allclear.moveagain = True
                        allclear.where = self.pos[0], self.pos[1] - 1
                elif self.type == "trap":
                    allclear.allclear = True
                    allclear.trap = True
                    allclear.moveagain = False
                    self.kill()
                    allclear.sound = "trap"
                elif self.type == "crumble":
                    allclear.allclear = True
                    self.crumble = True
                    self.crumbletime = self.count
        elif action == "unlockdoor" and self.type == "door":
            if self.pos[0] == allclear.door[0] and self.pos[1] == allclear.door[1]:
                self.kill()
        elif action == "whereis" and self.rect.collidepoint(allclear.mouse):
            allclear.where = self.pos

