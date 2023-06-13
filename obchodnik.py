import pygame
import random

class Bussinessman(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        super().__init__()

        self.bussinessmanposX = posX
        self.bussinessmanposY = posY
        self.randomAnimSpeed = random.randint(12, 21) / 100

        self.sprites = []

        for i in range(4):
            self.sprites.append(pygame.image.load(f"sprites\\dwarf\\dwarf_m_idle_anim_f{i}.png").convert_alpha())

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.Rect = self.image.get_rect()
        self.rect.center = [self.bussinessmanposX, self.bussinessmanposY]

    def update(self):
        self.current_sprite += self.randomAnimSpeed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))
        self.rect.center = [self.bussinessmanposX, self.bussinessmanposY]