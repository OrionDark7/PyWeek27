import pygame

pygame.init()

images = {"key":[pygame.image.load("./images/tiles/key.png"), pygame.image.load("./images/tiles/keys/key2.png"), pygame.image.load("./images/tiles/keys/key3.png"), pygame.image.load("./images/tiles/keys/key4.png"),
                           pygame.image.load("./images/tiles/keys/key5.png"), pygame.image.load("./images/tiles/keys/key6.png"), pygame.image.load("./images/tiles/keys/key7.png"), pygame.image.load("./images/tiles/keys/key8.png"),
                           pygame.image.load("./images/tiles/keys/key9.png"), pygame.image.load("./images/tiles/keys/key10.png"), pygame.image.load("./images/tiles/key.png"), pygame.image.load("./images/tiles/key.png"),
                            pygame.image.load("./images/tiles/key.png"), pygame.image.load("./images/tiles/key.png"), pygame.image.load("./images/tiles/key.png")],
        "portal":[pygame.image.load("./images/tiles/portal.png"), pygame.image.load("./images/tiles/portal2.png")],
        "trap":[pygame.image.load("./images/tiles/trap.png"), pygame.image.load("./images/tiles/traps/trap2.png"), pygame.image.load("./images/tiles/traps/trap3.png"), pygame.image.load("./images/tiles/traps/trap4.png"),
                pygame.image.load("./images/tiles/traps/trap5.png"), pygame.image.load("./images/tiles/traps/trap4.png"), pygame.image.load("./images/tiles/traps/trap3.png"), pygame.image.load("./images/tiles/traps/trap2.png")]}

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
        global images
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = [None, None]
        self.image = pygame.image.load("./images/tiles/" + type + ".png")
        if type in images.keys():
            self.images = images[type]
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
        global images
        if action == "reverse" and not allclear.conveyerdata == [] and self.type.startswith("conveyer"):
            if tuple(self.pos) in allclear.conveyerdata[0]:
                if self.type.endswith("left"):
                    self.type = "conveyer-right"
                elif self.type.endswith("right"):
                    self.type = "conveyer-left"
                elif self.type.endswith("up"):
                    self.type = "conveyer-down"
                elif self.type.endswith("down"):
                    self.type = "conveyer-up"
                self.image = pygame.image.load("./images/tiles/" + self.type + ".png")
        if action == "update":
            if self.data[1] == "wall" and self.pos == list(pos):
                allclear.wallappear = self.data[0]
                allclear.sound = "wall"
        if action == "animate" and self.type in images.keys():
            if self.index < len(self.images)-1:
                self.index += 1
            else:
                self.index = 0
            self.image = self.images[self.index]
        if action == "get" and self.rect.collidepoint(allclear.mouse):
            allclear.type = self.type
        if action == "wallappear" and self.pos == allclear.wallappearsat:
            self.kill()
        if action == "destroywall" and tuple(self.pos) == allclear.destroywallat and self.type == "wall":
            self.kill()
        if action == "move":
            self.count += 1
            if self.type == "crumble" and self.crumble and self.crumbletime + 1 == self.count:
                self.type = "trap"
                self.index = 0
                self.images = images[self.type]
                self.image = self.images[self.index]
            if self.pos == list(pos):
                if self.data[1] == "dswall":
                    allclear.destroywall = self.data[0]
                    allclear.update = "destroywall"
                if self.data[1] == "wall":
                    allclear.wallappear = self.data[0]
                    allclear.sound = "wall"
                    print allclear.sound
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
                    print allclear.sound
                elif self.type == "gem":
                    allclear.allclear = True
                    allclear.sound = "gem"
                    print allclear.sound
                    self.kill()
                elif self.type == "key":
                    allclear.allclear = True
                    allclear.update = "unlockdoor"
                    allclear.door = self.data[0]
                    allclear.moveagain = False
                    allclear.sound = "key"
                    print allclear.sound
                    self.kill()
                elif self.type == "exit":
                    allclear.moveagain = False
                    allclear.won = True
                    allclear.sound = "win"
                    print allclear.sound
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
                    allclear.sound = "trap"
                    print allclear.sound
                elif self.type == "crumble":
                    allclear.allclear = True
                    self.crumble = True
                    self.crumbletime = self.count
            print allclear.sound
        elif action == "unlockdoor" and self.type == "door":
            if self.pos[0] == allclear.door[0] and self.pos[1] == allclear.door[1]:
                self.kill()
        elif action == "whereis" and self.rect.collidepoint(allclear.mouse):
            allclear.where = self.pos

