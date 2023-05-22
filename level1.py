import pygame

pygame.init()

# pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920, 1080)  # rozlisenie

mainscreen = pygame.display.set_mode(res)


bg_image = pygame.image.load('levely\\level1.png')
bg_imageWIDTH = bg_image.get_rect().width
bg_imageHEIGHT = bg_image.get_rect().height
backGround = pygame.transform.scale(bg_image, (bg_imageWIDTH * 3, bg_imageHEIGHT * 3))
enemy_image = pygame.image.load('sprites\\goblin\\goblin_idle_anim_f0.png')
enemy_WIDTH = enemy_image.get_rect().width
enemy_HEIGHT = enemy_image.get_rect().height
enemy = pygame.transform.scale(enemy_image, (enemy_WIDTH * 3, enemy_HEIGHT * 3))

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

def renderMainG():
    mainscreen.blit(enemy, (910, 950))
    moving_sprites.draw(mainscreen)
    moving_sprites.update()
    pygame.display.flip()
    clock.tick(60)

def renderfight():
    mouse = pygame.mouse.get_pos()
    mainscreen.fill((0, 0, 0))
    mainscreen.blit(cursor, mouse)
    pygame.draw.rect(mainscreen, (255, 255, 255), pygame.Rect(100, 100, 50, 50))
    clock.tick(60)
    pygame.display.flip()


class Player(pygame.sprite.Sprite):
    # init funkcia
    def __init__(self):
        super().__init__()
        # player premenne
        self.PLAYER_SPEED = 6
        self.playerPositionX = 910
        self.playerPositionY = 540
        # player sprite nacitanie do listu
        self.sprites = []
        self.is_animating = False
        for i in range(4):
            self.sprites.append(pygame.image.load(f"sprites\\run\\knight_m_run_anim_f{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        # transformovanie spritu
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))

        self.rect = self.image.get_rect()
        self.rect = [self.playerPositionX, self.playerPositionY]

    # funkcia na spustenie animacie
    def animate(self):
        self.is_animating = True

    # prechadzanie png z listu
    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.5
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]
            self.imageWIDTH = self.image.get_rect().width
            self.imageHEIGTH = self.image.get_rect().height
            self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))
            self.rect = [self.playerPositionX, self.playerPositionY]

    # pogyb hraca
    def movement(self):
        self.key_pressed = pygame.key.get_pressed()
        self.pressed = False
        if self.key_pressed[pygame.K_w] and self.pressed == False:
            player.animate()
            self.pressed = True
            self.playerPositionY -= self.PLAYER_SPEED

        if self.key_pressed[pygame.K_s] and self.pressed == False:
            player.animate()
            self.pressed = True
            self.playerPositionY += self.PLAYER_SPEED

        if self.key_pressed[pygame.K_a] and self.pressed == False:
            player.animate()
            self.pressed = True
            self.playerPositionX -= self.PLAYER_SPEED

        if self.key_pressed[pygame.K_d] and self.pressed == False:
            player.animate()
            self.pressed = True
            self.playerPositionX += self.PLAYER_SPEED


# pridanie spritu do sprite groupu
moving_sprites = pygame.sprite.Group()
player = Player()
moving_sprites.add(player)

# main loop
running = True
mainG = True
while running:
    mainscreen.fill((0, 0, 0))
    mainscreen.blit(backGround, (0, 0))
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # enemy trigger (zatial iba stlacenim klavesy, kedze kolizie nejdu)
    stlacene = pygame.key.get_pressed()

    if stlacene[pygame.K_l]:
        mainG = False

    # pohyb hraca

    player.movement()

    # vykreslovanie
    if mainG == True:
        renderMainG()
    # mainscreen.blit(enemy, (910, 950))
    # moving_sprites.draw(mainscreen)
    # moving_sprites.update()
    # mainscreen.blit(cursor, mouse)
    # pygame.display.flip()
    # clock.tick(60)
