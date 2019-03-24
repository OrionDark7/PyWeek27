import pygame

pygame.init()

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
    def __init__(self, pos, text, color):
        global font
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(text), 1, list(color))