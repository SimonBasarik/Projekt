import pygame

pygame.init()

# pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920, 1080)  # rozlisenie

mainscreen = pygame.display.set_mode(res)

bg_image = pygame.image.load('levely\\level1.png').convert_alpha()
bg_imageWIDTH = bg_image.get_rect().width
bg_imageHEIGHT = bg_image.get_rect().height
backGround = pygame.transform.scale(bg_image, (bg_imageWIDTH * 3, bg_imageHEIGHT * 3))
enemy_image = pygame.image.load('sprites\\goblin\\goblin_idle_anim_f0.png').convert_alpha()
enemy_WIDTH = enemy_image.get_rect().width
enemy_HEIGHT = enemy_image.get_rect().height
enemy = pygame.transform.scale(enemy_image, (enemy_WIDTH * 3, enemy_HEIGHT * 3))


pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

#funkcia renderMainG(), vykresluje a
def renderMainG():

    # pohyb hraca

    player.movement()

    # vykreslenie enemy (zatial iba takto, neskôr bude riesene cez classu)

    mainscreen.blit(enemy, (910, 950))

    #vykreslenie hraca a animacia
    moving_sprites.draw(mainscreen)
    moving_sprites.update()

    pygame.display.flip()
    clock.tick(60)

# funkcia renderfight(), vykresluje a stara sa o hlavne vlastnosti suboja

def renderfight():
    mouse = pygame.mouse.get_pos()
    mainscreen.fill((28, 28, 28))

    #volanie funkcii tlacidiel

    if attackButton.draw():
        print("ATTACKED")
    if defendButton.draw():
        print("DEFENDED")
    if magicButton.draw():
        print("MAGICGED")
    if itemButton.draw():
        print("ITEMED")

    mainscreen.blit(cursor, mouse)

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
            self.sprites.append(pygame.image.load(f"sprites\\run\\knight_m_run_anim_f{i}.png").convert_alpha())
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

    # pohyb hraca
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

class Button():
    # metoda __init__ (nacitava parametre, umiestnuje text na spravnu poziciu)
    def __init__(self,x,y,text,fontsize):
        super().__init__()
        self.fontsize = fontsize
        self.font = pygame.font.Font('Font\\rainyhearts.ttf', self.fontsize)
        self.text = text
        self.button = self.font.render(self.text,True,(255,255,255))
        self.rect = self.button.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    # metoda draw (vykresluje, kontroluje stlacenie, a returnuje akciu)
    def draw(self):
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
# Vytvorenie objektov z classy Button(), nastavenie parametrov (x,y,text tlacitka, velkost fontu)

attackButton = Button(100,725,"ATTACK",125)
defendButton = Button(100,900,"DEFEND",125)
magicButton = Button(700,725,"MAGIC",125)
itemButton = Button(740,900,"ITEM",125)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # enemy trigger (zatial iba stlacenim klavesy, kedze kolizie nejdu)
    stlacene = pygame.key.get_pressed()

    if stlacene[pygame.K_l]:
        mainG = False

    # vykreslovanie
    if mainG:
        renderMainG()
    else:
        renderfight()
