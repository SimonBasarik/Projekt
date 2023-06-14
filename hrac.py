import pygame, healthbar

# maximalny cas timeru

TIMERMAXTIME = 1

class Player(pygame.sprite.Sprite):

    # init metoda

    def __init__(self, obstacles):
        super().__init__()

        # player premenne
        self.obstacles = obstacles
        self.PLAYER_SPEED = 6
        self.Health = 100
        self.MaxHealth = 100
        self.Healthbar = healthbar.Healthbar(300, 215, 250, 25, self.MaxHealth)
        self.Ressistance = 0
        self.timer = 0
        self.score = 0
        self.gamelevel = 1
        self.playerlevel = 1
        self.playerPositionX = 960
        self.playerPositionY = 540

        # player sprite nacitanie do listu

        self.sprites = []
        self.idlesprites = []
        self.is_animating = False
        for i in range(4):
            self.sprites.append(pygame.image.load(f"sprites\\run\\knight_m_run_anim_f{i}.png").convert_alpha())
        for i in range(2):
            self.idlesprites.append(pygame.image.load(f"sprites\\idle\\knight_f_idle_anim_f{i}.png").convert_alpha())
        self.current_sprite = 0
        self.current_idleSprite = 0
        self.image = self.sprites[self.current_sprite]
        self.idleImage = self.sprites[self.current_idleSprite]

        # transformovanie spritu

        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))

        self.idleImageWIDTH = self.image.get_rect().width
        self.idleImageHEIGTH = self.image.get_rect().height
        self.idleImage = pygame.transform.scale(self.idleImage, (self.idleImageWIDTH * 6, self.idleImageHEIGTH * 6))

        self.rect = self.image.get_rect()
        self.rect.center = [self.playerPositionX, self.playerPositionY]
        self.old_rect = self.rect.copy()

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()

        self.idleRect = self.idleImage.get_rect()
        self.idleRect.topleft = (300, 100)

    # metoda na spustenie animacie

    def animate(self):
        self.is_animating = True

    # input metoda, cita vstup z klaves

    def input(self):
        keys = pygame.key.get_pressed()
        self.pressed = False

        # input

        if keys[pygame.K_w] and self.pressed == False:
            self.animate()
            self.direction.y = -1
            self.pressed = True

        elif keys[pygame.K_s] and self.pressed == False:
            self.animate()
            self.direction.y = 1
            self.pressed = True

        else:
            self.direction.y = 0

        if keys[pygame.K_d] and self.pressed == False:
            self.animate()
            self.direction.x = 1
            self.pressed = True

        elif keys[pygame.K_a] and self.pressed == False:
            self.animate()
            self.direction.x = -1
            self.pressed = True

        else:
            self.direction.x = 0

    # metoda collision, kontroluje

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:

            # kontrola horizontalnych kolizii

            if direction == "horizontal":
                for sprite in collision_sprites:

                    # colizia na pravo
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x

                    # colizia na lavo
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x

            # kontrola verticalnych kolizii

            if direction == "vertical":
                for sprite in collision_sprites:

                    # colizia na bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y

                    # colizia na top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y

    # update funkcia, (zabudovana v Sprite classe), riesi pohyb a animacie

    def update(self):
        self.old_rect = self.rect.copy()

        self.input()

        self.pos.x += self.direction.x * self.PLAYER_SPEED
        self.rect.x = self.pos.x
        self.collision("horizontal")
        self.pos.y += self.direction.y * self.PLAYER_SPEED
        self.rect.y = self.pos.y
        self.collision("vertical")

        if self.is_animating:
            self.current_sprite += 0.3
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]
            self.imageWIDTH = self.image.get_rect().width
            self.imageHEIGTH = self.image.get_rect().height
            self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))
            # self.rect.center = [self.pos.x, self.pos.y]
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y

    # idle update, animuje idle animaciu pri fighte

    def updateIdle(self,mainscreen):
        self.current_idleSprite += 0.025
        if self.current_idleSprite >= len(self.idlesprites):
            self.current_idleSprite = 0
        self.idleImage = self.idlesprites[int(self.current_idleSprite)]

        self.idleImageWIDTH = self.image.get_rect().width
        self.idleImageHEIGTH = self.image.get_rect().height
        self.idleImage = pygame.transform.scale(self.idleImage, (self.idleImageWIDTH * 6, self.idleImageHEIGTH * 6))
        mainscreen.blit(self.idleImage, (self.idleRect.x, self.idleRect.y))

    # metoda drawtimer, vykresluje casovac vo fighte

    def drawtimer(self,mainscreen):
        timerS = self.timer / 1000

        ratio = min(timerS / TIMERMAXTIME, 1)

        pygame.draw.rect(mainscreen, "black", (1550, 720, 250, 55))
        pygame.draw.rect(mainscreen, "white", (1550, 720, 250 * ratio, 55))

