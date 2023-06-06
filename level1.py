import pygame
from pytmx.util_pygame import load_pygame

pygame.init()

# pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920, 1080)  # rozlisenie

mainscreen = pygame.display.set_mode(res)
level1 = load_pygame("levely\\level1.tmx")

# maximalny cas timeru

TIMERMAXTIME = 1


pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

#funkcia renderMainG(), vykresluje a riesi

def renderMainG():

    #vykreslenie hraca a animacia

    moving_sprites.draw(mainscreen)
    moving_sprites.update()

    if goblin.Health > 0:
        enemy_sprites.draw(mainscreen)
        enemy_sprites.update()

    pygame.display.flip()
    clock.tick(60)

# funkcia renderfight(), vykresluje a stara sa o hlavne vlastnosti suboja

def renderfight():
    global mainG
    mouse = pygame.mouse.get_pos()
    mainscreen.fill((28, 28, 28))
    time = clock.tick(60)
    player.timer += time
    timerS = player.timer/1000
    
    #vykreslenie hraca a animacia
    
    player.updateIdle()
    goblin.updateIdle()
    
    #volanie funkcii tlacidiel

    if attackButton.draw():
        if timerS >= TIMERMAXTIME:
            goblin.Health -= 10
            player.timer = 0
    if defendButton.draw():
        print("DEFENDED")
    if magicButton.draw():
        print("MAGICGED")
    if itemButton.draw():
        print("ITEMED")
    timerText.draw()

    #vykreslenie HealthBaru
    goblin.Healthbar.draw(mainscreen,goblin.Health)
    player.Healthbar.draw(mainscreen,player.Health)
    player.drawtimer()
    mainscreen.blit(cursor, mouse)
    if player.Health <=0:
        mainG = True
        player.Health = 20
    
    if goblin.Health <= 0:
        mainG = True
    pygame.display.flip()

# classa Floor

class Floor(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGHT = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image,(self.imageWIDTH*3,self.imageHEIGHT*3))
        self.rect = self.image.get_rect(topleft=pos)

# classa Walls

class Walls(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGHT = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image,(self.imageWIDTH*3,self.imageHEIGHT*3))
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

#pridanie stien a podlahy do ich vlastných groupov

floorGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()
for layer in level1.visible_layers:
    if layer.name == "ground":
        for x, y, surf in layer.tiles():
            pos = (x * 48, y * 48)
            Floor(pos=pos, surf=surf, groups=floorGroup)

for layer in level1.visible_layers:
    if layer.name == "walls":
        for x, y, surf in layer.tiles():
            pos = (x * 48, y * 48)
            Walls(pos=pos, surf=surf, groups=wallGroup)

#classa Healthbar, vytvara health bar nad hracom a enemy

class Healthbar():
    def __init__(self,x,y,w,h,maxhp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maxhp = maxhp

    # vykreslenie healthbaru

    def draw (self, surface,hp):
        ratio = hp / self.maxhp
        pygame.draw.rect(surface,"red", (self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface,"white", (self.x, self.y, self.w*ratio, self.h))

# classa enemy, velmi podobna hracovi len sa neda hybat

class Enemy (pygame.sprite.Sprite):

    # zakladne nastavenie classy enemy

    def __init__(self,x,y,enemyType):
        super().__init__()

        # enemy premenne
        self.enemyType = enemyType
        self.Health = 100
        self.MaxHealth = 100
        self.Healthbar = Healthbar(1500,250,250,25, self.MaxHealth)
        self.enemyPositionX = x
        self.enemyPositionY = y

        # player sprite nacitanie do listu

        self.sprites = []
        if enemyType == 1:
            for i in range(2):
                self.sprites.append(pygame.image.load(f"sprites\\goblin\\goblin_idle_anim_f{i}.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

         # transformovanie spritu

        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))

        self.rect = self.image.get_rect()
        self.Rect = self.image.get_rect()
        self.Rect.topleft = (1500,300)
        self.rect.center = [self.enemyPositionX, self.enemyPositionY]

    # update funkcia, (zabudovana v Sprite classe), stara sa o animacie

    def update(self):
        self.current_sprite += 0.025
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGTH * 3))
        self.rect.center = [self.enemyPositionX, self.enemyPositionY]

    def updateIdle(self):
        self.current_sprite += 0.025
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
        self.ImageWIDTH = self.image.get_rect().width
        self.ImageHEIGTH = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.ImageWIDTH *12, self.ImageHEIGTH * 12))
        self.filpimage = pygame.transform.flip(self.image,True, False)
        mainscreen.blit(self.filpimage, (self.Rect.x, self.Rect.y))

class Player(pygame.sprite.Sprite):

    # init metoda

    def __init__(self,obstacles):
        super().__init__()

        # player premenne
        self.obstacles = obstacles
        self.PLAYER_SPEED = 6
        self.Health = 100
        self.MaxHealth = 100
        self.Healthbar = Healthbar(300,215,250,25, self.MaxHealth)
        self.timer = 0
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
        self.idleRect.topleft = (300,100)

    # metoda na spustenie animacie

    def animate(self):
        self.is_animating = True

    # input metoda, cita vstup z klaves

    def input(self):
        keys = pygame.key.get_pressed()
        self.pressed = False

        # input

        if keys[pygame.K_w] and self.pressed == False:
            player.animate()
            self.direction.y = -1
            self.pressed = True

        elif keys[pygame.K_s] and self.pressed == False:
            player.animate()
            self.direction.y = 1
            self.pressed = True

        else:
            self.direction.y = 0

        if keys[pygame.K_d] and self.pressed == False:
            player.animate()
            self.direction.x = 1
            self.pressed = True

        elif keys[pygame.K_a] and self.pressed == False:
            player.animate()
            self.direction.x = -1
            self.pressed = True

        else:
            self.direction.x = 0

    # metoda collision, kontroluje

    def collision(self,direction):
        collision_sprites = pygame.sprite.spritecollide(self,self.obstacles,False)
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
            #self.rect.center = [self.pos.x, self.pos.y]
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y

    # idle update, animuje idle animaciu pri fighte

    def updateIdle(self):
        self.current_idleSprite += 0.025
        if self.current_idleSprite >= len(self.idlesprites):
            self.current_idleSprite = 0
        self.idleImage = self.idlesprites[int(self.current_idleSprite)]
        
        self.idleImageWIDTH = self.image.get_rect().width
        self.idleImageHEIGTH = self.image.get_rect().height
        self.idleImage = pygame.transform.scale(self.idleImage, (self.idleImageWIDTH * 6, self.idleImageHEIGTH * 6))
        mainscreen.blit(self.idleImage, (self.idleRect.x, self.idleRect.y))

    # metoda drawtimer, vykresluje casovac vo fighte

    def drawtimer(self):
        timerS = self.timer/1000
    
        ratio = min(timerS / TIMERMAXTIME, 1)
        

        pygame.draw.rect(mainscreen,"black", (1600,745,300,75))
        pygame.draw.rect(mainscreen,"white", (1600,745,300*ratio,75))


#classa Button, vyrvtvara tlacitka

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

# Vytvorenie objektov z classy Button(), n# astavenie parametrov (x, y, text tlacitka, velkost fontu)

attackButton = Button(100,725,"ATTACK",125)
defendButton = Button(100,900,"DEFEND",125)
magicButton = Button(700,725,"MAGIC",125)
itemButton = Button(740,900,"ITEM",125)
timerText = Button(1200,725,"TIMER :",125)
# pridanie spritu do sprite groupu

moving_sprites = pygame.sprite.GroupSingle()
player = Player(wallGroup)
moving_sprites.add(player)

enemy_sprites = pygame.sprite.Group()
goblin = Enemy(960,950,1)
enemy_sprites.add(goblin)

# Vytvorenie objektov z classy Healthbar(), nastavenie parametrov (x, y, sirka, vyska,maxhp)

playerHealthBar = Healthbar(325,175,250,25, player.MaxHealth)

# main loop

running = True
mainG = True
while running:
    mainscreen.fill((0, 0, 0))
    floorGroup.draw(mainscreen)
    wallGroup.draw(mainscreen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # enemy trigger

    if pygame.sprite.spritecollide(player,enemy_sprites,True):
        mainG = False

    # vykreslovanie

    if mainG:
        renderMainG()
    else:
        renderfight()

