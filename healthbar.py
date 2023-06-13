import pygame

# classa Healthbar, vytvara health bar nad hracom a enemy

class Healthbar():
    def __init__(self, x, y, w, h, maxhp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maxhp = maxhp

    # vykreslenie healthbaru

    def draw(self, surface, hp):
        ratio = hp / self.maxhp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "white", (self.x, self.y, self.w * ratio, self.h))

