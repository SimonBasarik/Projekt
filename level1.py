import pygame

pygame.init()

#pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

bg_image = pygame.image.load('levely\\level1.png')
bg_imageWIDTH = bg_image.get_rect().width
bg_imageHEIGHT = bg_image.get_rect().height
backGround = pygame.transform.scale(bg_image, (bg_imageWIDTH*3,bg_imageHEIGHT*3))

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    #init funkcia
    def __init__(self,):
        super().__init__()
        #player premenne
        self.PLAYER_SPEED = 6
        self.playerPositionX = 910
        self.playerPositionY = 540
        #player sprite nacitanie do listu
        self.sprites = []
        self.is_animating = False
        for i in range(4):
            self.sprites.append(pygame.image.load(f"sprites\\run\\knight_m_run_anim_f{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        #transformovanie spritu
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH*3,self.imageHEIGTH*3))

        self.rect = self.image.get_rect()
        self.rect = [self.playerPositionX,self.playerPositionY]

    #funkcia na spustenie animacie
    def animate(self):
        self.is_animating = True
    #prechadzanie png z listu
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
            self.rect = [self.playerPositionX,self.playerPositionY]
    #pogyb hraca
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

#pridanie spritu do sprite groupu
moving_sprites = pygame.sprite.Group()
player = Player()
moving_sprites.add(player)

#main loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backGround, (0,0))
    mouse = pygame.mouse.get_pos()
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #pohyb hraca

    player.movement()

    #vykreslovanie
    moving_sprites.draw(screen)
    moving_sprites.update()
    screen.blit(cursor, mouse)
    pygame.display.flip()
    clock.tick(60)