import pygame

pygame.init()
pygame.mixer.init()

select = pygame.mixer.Sound("./sfx/Select.wav")

font = pygame.font.Font(None, 24)

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
    font = pygame.font.Font(None, int(size))

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
        clicked = False
        if self.rect.collidepoint(mouse):
            clicked = True
            select.play()
        return clicked
    def draw(self, surface):
        surface.blit(self.image, [self.rect.left, self.rect.top])
