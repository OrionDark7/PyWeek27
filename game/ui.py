import pygame

pygame.init()
pygame.mixer.init()

select = pygame.mixer.Sound("./sfx/Select.wav")
sfx = True

font = pygame.font.Font("./font/slkscr.ttf", 24)

def text(text, pos, color, surface):
    global font
    render = font.render(str(text), 1, list(color))
    surface.blit(render, list(pos))

def centeredText(text, pos, color, surface):
    global font
    render = font.render(str(text), 1, list(color))
    rect = pos[0] - (render.get_rect().width / 2)
    surface.blit(render, [rect, pos[1]])

def setFontSize(size):
    global font
    font = pygame.font.Font("./font/slkscr.ttf", int(size))

class button(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, centered=False):
        global font
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(text), 1, list(color))
        self.rect = self.image.get_rect()
        if centered:
            self.rect.left, self.rect.top = pos[0] - (self.rect.width/2), pos[1]
        else:
            self.rect.left, self.rect.top = list(pos)
    def click(self, mouse):
        global sfx
        clicked = False
        if self.rect.collidepoint(mouse):
            clicked = True
            if sfx:
                select.play()
        return clicked
    def draw(self, surface):
        surface.blit(self.image, [self.rect.left, self.rect.top])

class imagebutton(pygame.sprite.Sprite):
    def __init__(self, image, pos, size, centered=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(str(image))
        self.image = pygame.transform.scale(self.image, list(size))
        self.rect = self.image.get_rect()
        self.centered = centered
        if centered:
            self.rect.left, self.rect.top = pos[0] - (self.rect.width/2), pos[1]
        else:
            self.rect.left, self.rect.top = list(pos)
    def click(self, mouse):
        global sfx
        clicked = False
        if self.rect.collidepoint(mouse):
            clicked = True
            if sfx:
                select.play()
        return clicked
    def draw(self, surface):
        surface.blit(self.image, [self.rect.left, self.rect.top])
    def changeImage(self, image, size):
        oldposition = self.rect.left, self.rect.top
        self.image = pygame.image.load(str(image))
        self.image = pygame.transform.scale(self.image, list(size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = oldposition
