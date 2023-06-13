import pygame

# classa Button, vyrvtvara tlacitka

class Button():

    # metoda __init__ (nacitava parametre, umiestnuje text na spravnu poziciu)

    def __init__(self, x, y, text, fontsize):
        super().__init__()
        self.fontsize = fontsize
        self.font = pygame.font.Font('Font\\rainyhearts.ttf', self.fontsize)
        self.text = text
        self.button = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.button.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # metoda draw (vykresluje, kontroluje stlacenie, a returnuje akciu)

    def draw(self,mainscreen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        mainscreen.blit(self.button, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
