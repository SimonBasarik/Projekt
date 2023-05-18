import pygame

pygame.init()

#pociatocne nastavenie (premenne,konstanty,funkcie)
PLAYER_SPEED = 5

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

bg_image = pygame.image.load('levely\\level1.png')
bg_imageWIDTH = bg_image.get_rect().width
bg_imageHEIGHT = bg_image.get_rect().height
backGround = pygame.transform.scale(bg_image, (bg_imageWIDTH*3,bg_imageHEIGHT*3))

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

playerPositionX = 910
playerPositionY = 540


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        # return pygame.Rect(int(x),int(y), 50, 50)
        self.sprites = []
        self.is_animating = False
        for i in range(4):
            self.sprites.append(pygame.image.load(f"sprites\\run\\knight_m_run_anim_f{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH*3,self.imageHEIGTH*3))
        self.rect = self.image.get_rect()
        self.rect = [x,y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.3
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]
            self.imageWIDTH = self.image.get_rect().width
            self.imageHEIGTH = self.image.get_rect().height
            self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))



moving_sprites = pygame.sprite.Group()
player = Player(playerPositionX,playerPositionY)
moving_sprites.add(player)

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
    key_pressed = pygame.key.get_pressed()
    pressed = False
    if key_pressed[pygame.K_w] and pressed == False:
        player.animate()
        pressed = True
        playerPositionY -= PLAYER_SPEED

    if key_pressed[pygame.K_s] and pressed == False:
        player.animate()
        pressed = True
        playerPositionY += PLAYER_SPEED

    if key_pressed[pygame.K_a] and pressed == False:
        player.animate()
        pressed = True
        playerPositionX -= PLAYER_SPEED

    if key_pressed[pygame.K_d] and pressed == False:
        player.animate()
        pressed = True
        playerPositionX += PLAYER_SPEED
    #vykreslovanie
    # playerIcon(playerPositionX, playerPositionY)
    moving_sprites.draw(screen)
    moving_sprites.update()
    screen.blit(cursor, mouse)
    pygame.display.flip()
    clock.tick(60)