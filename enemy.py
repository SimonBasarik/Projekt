import pygame,random,healthbar

# classa enemy, velmi podobna hracovi len sa neda hybat

class Enemy(pygame.sprite.Sprite):

    # zakladne nastavenie classy enemy

    def __init__(self, x, y, enemyType, enemyAttack,idlex,idley,enemyFireResistance,enemyIceResistance):
        super().__init__()

        # enemy premenne
        self.enemyFireResistance = enemyFireResistance
        self.enemyIceResistance = enemyIceResistance
        self.enemyType = enemyType
        self.enemyAttack = enemyAttack
        self.idlex = idlex
        self.idley = idley
        self.Health = 100
        self.MaxHealth = 100
        self.Healthbar = healthbar.Healthbar(1500, 250, 250, 25, self.MaxHealth)
        self.enemyPositionX = x
        self.enemyPositionY = y

        self.randomAnimSpeed = random.randint(12, 21) / 100


        # player sprite nacitanie do listu

        self.sprites = []
        if enemyType == 1:
            for i in range(4):
                self.sprites.append(pygame.image.load(f"sprites\\goblin\\goblin_idle_anim_f{i}.png").convert_alpha())
        if enemyType == 2:
            for i in range(4):
                self.sprites.append(pygame.image.load(f"sprites\\demon\\big_demon_idle_anim_f{i}.png").convert_alpha())
        if enemyType == 3:
            for i in range(4):
                self.sprites.append(pygame.image.load(f"sprites\\bigzombie\\big_zombie_idle_anim_f{i}.png").convert_alpha())
        if enemyType == 4:
            for i in range(4):
                self.sprites.append(pygame.image.load(f"sprites\\chort\\chort_idle_anim_f{i}.png").convert_alpha())
        if enemyType == 5:
            for i in range(4):
                self.sprites.append(pygame.image.load(f"sprites\\muddy\\muddy_anim_f{i}.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # transformovanie spritu

        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))

        self.rect = self.image.get_rect()
        self.Rect = self.image.get_rect()
        self.Rect.topleft = (self.idlex,self.idley)
        self.rect.center = [self.enemyPositionX, self.enemyPositionY]

    # update funkcia, (zabudovana v Sprite classe), stara sa o animacie

    def update(self):
        self.current_sprite += self.randomAnimSpeed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))
        self.rect.center = [self.enemyPositionX, self.enemyPositionY]

    def updateIdle(self,mainscreen):
        self.current_sprite += self.randomAnimSpeed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        self.ImageWIDTH = self.image.get_rect().width
        self.ImageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.ImageWIDTH * 12, self.ImageHEIGTH * 12))
        self.filpimage = pygame.transform.flip(self.image, True, False)
        mainscreen.blit(self.filpimage, (self.Rect.x, self.Rect.y))

