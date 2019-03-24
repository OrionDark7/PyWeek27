import pygame

class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([60, 60])
        self.image.fill([0, 255, 0])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.pos = [0, 0]
    def draw(self, surface):
        surface.blit(self.image, [self.rect.left, self.rect.top])
    def reset(self):
        self.rect.left, self.rect.top = [220, 120]
        self.pos = [0, 0]

class tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, type, objectpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/tiles/" + type + ".png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.type = type
        self.pos = objectpos
    def update(self, pos, action, allclear):
        if action == "move":
            if self.pos == list(pos):
                if self.type == "wall" or self.type == "door":
                    allclear.allclear = False