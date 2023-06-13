import pygame, json, random
from pytmx.util_pygame import load_pygame
import hrac, button, enemy, healthbar

pygame.init()

# pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920, 1080)  # rozlisenie

mainscreen = pygame.display.set_mode(res)
level1 = load_pygame("levely\\level1.tmx")
gej2 = None
eenemy = None



pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

# funkcia renderMenu(, vykresluje menu

def renderMenu():
    global mainG
    global menu
    global running

    mouse = pygame.mouse.get_pos()

    mainscreen.fill((0, 0, 0))


    if startButton.draw(mainscreen):
        mainG = True
        menu = False

    if quitButton.draw(mainscreen):
        writedata()
        running = False

    mainscreen.blit(cursor, mouse)
    pygame.display.flip()

# funkcia renderMainG(), vykresluje hraca a enemy

def renderMainG():

    # vykreslenie hraca a animacia

    global gej2
    global eenemy

    moving_sprites.draw(mainscreen)
    moving_sprites.update()

    #if enemy:
    enemy_sprites.draw(mainscreen)
    enemy_sprites.update()

    pygame.display.flip()
    clock.tick(60)


# funkcia renderfight(), vykresluje a stara sa o hlavne vlastnosti suboja
draw_mainButtons = True
draw_magicButtons = False
draw_itemButtons = False

def renderfight():
    global draw_mainButtons
    global draw_magicButtons
    global draw_itemButtons
    global mainG
    global gej1
    global gej2
    global eenemy

    mouse = pygame.mouse.get_pos()
    mainscreen.fill((28, 28, 28))
    time = clock.tick(60)
    player.timer += time
    timerS = player.timer / 1000

    # vykreslenie hraca a animacia
    def enemyTurn():
        eenemy.enemyAttack -= player.Ressistance
        player.Health -= eenemy.enemyAttack
        eenemy.enemyAttack += player.Ressistance
        player.Ressistance = 0



    player.updateIdle(mainscreen)
    if gej2 == goblin.image:
        eenemy = goblin
    if gej2 == demon.image:
        eenemy = demon
    if gej2 == muddy.image:
        eenemy = muddy
    if gej2 == chort.image:
        eenemy = chort
    if gej2 == bigzombie.image:
        eenemy = bigzombie

    if not eenemy:
        mainG = True
        return

    eenemy.updateIdle(mainscreen)

    # volanie funkcii tlacidiel

    if draw_mainButtons:
        if attackButton.draw(mainscreen):
            if timerS >= hrac.TIMERMAXTIME:
                eenemy.Health -= 10
                player.timer = 0
                enemyTurn()
        if defendButton.draw(mainscreen):
            if timerS >= hrac.TIMERMAXTIME:
                player.Ressistance = 4
                enemyTurn()

                player.timer = 0
        if magicButton.draw(mainscreen):
            draw_mainButtons = False
            draw_magicButtons = True
        if itemButton.draw(mainscreen):
            draw_mainButtons = False
            draw_itemButtons = True
    timerText.draw(mainscreen)
    if draw_magicButtons == True:
        if fireballButton.draw(mainscreen):
            if timerS >= hrac.TIMERMAXTIME:
                damage = 20 - eenemy.enemyFireResistance
                eenemy.Health -= damage
                player.timer = 0
                enemyTurn()
                draw_magicButtons = False
                draw_mainButtons = True
        if frostfangButton.draw(mainscreen):
            if timerS >= hrac.TIMERMAXTIME:
                damage = 20 - eenemy.enemyIceResistance
                eenemy.Health -= damage
                player.timer = 0
                enemyTurn()
                draw_magicButtons = False
                draw_mainButtons = True
    if draw_itemButtons == True:
        pass

    # vykreslenie HealthBaru
    eenemy.Healthbar.draw(mainscreen, eenemy.Health)
    player.Healthbar.draw(mainscreen, player.Health)
    player.drawtimer(mainscreen)
    mainscreen.blit(cursor, mouse)

    # smrt hraca

    if player.Health <= 0:
        mainG = True
        player.Health = 20
        eenemy.Health = 100
        player.pos.x = 960
        player.pos.y = 540

    #smrt nepriatela

    if eenemy.Health <= 0:
        player.score += 1
        mainG = True
        eenemy = None
        player.playerPositionY += 100
        enemy_sprites.remove(gej1)

    pygame.display.flip()


# classa Floor

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGHT = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGHT * 3))
        self.rect = self.image.get_rect(topleft=pos)


# classa Walls

class Walls(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.imageWIDTH = self.image.get_rect().width
        self.imageHEIGHT = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (self.imageWIDTH * 3, self.imageHEIGHT * 3))
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()


# pridanie stien a podlahy do ich vlastných groupov

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


# Vytvorenie objektov z classy Button(), nastavenie parametrov (x, y, text tlacitka, velkost fontu)

startButton = button.Button(775,400,"START", 125)
quitButton = button.Button(815,600,"QUIT",125)
attackButton = button.Button(100, 725, "ATTACK", 125)
fireballButton = button.Button(100, 725, "FIREBALL", 125)
frostfangButton = button.Button(100, 900, "FROSTFANG", 125)
defendButton = button.Button(100, 900, "DEFEND", 125)
magicButton = button.Button(700, 725, "MAGIC", 125)
itemButton = button.Button(740, 900, "ITEM", 125)
timerText = button.Button(1200, 725, "TIMER :", 125)

# pridanie spritu do sprite groupu

moving_sprites = pygame.sprite.GroupSingle()
player = hrac.Player(wallGroup)
moving_sprites.add(player)

enemy_sprites = pygame.sprite.Group()
goblin = enemy.Enemy(960, 950, 1, 5, 1500, 300,0,0)
demon = enemy.Enemy(760, 750, 2, 15, 1400, 200,15,-5)
bigzombie = enemy.Enemy(660, 650, 3, 15, 1400, 200,5,5)
muddy = enemy.Enemy(560, 550, 5, 10, 1500, 300,5,0)
chort = enemy.Enemy(960, 750, 4, 5, 1500, 300,5,-5)
enemy_sprites.add(goblin, demon, bigzombie,muddy,chort)


# Vytvorenie objektov z classy Healthbar(), nastavenie parametrov (x, y, sirka, vyska,maxhp)

playerHealthBar = healthbar.Healthbar(325, 175, 250, 25, player.MaxHealth)

pipik = dict()

with open("data.json", "r", encoding="UTF-8") as f:
    pipik = json.load(f)

saves = pipik["saves"]


def writedata():
    global saves

    data = {"health": player.Health, "score": player.score}

    saves.append(data)

    new_data = {"saves": saves}

    new_json = json.dumps(new_data, indent=3)

    with open("data.json", "w", encoding="UTF-8") as f:
        f.write(new_json)

# main loop

running = True
menu = True
mainG = False
while running:
    mainscreen.fill((0, 0, 0))
    floorGroup.draw(mainscreen)
    wallGroup.draw(mainscreen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            writedata()
            running = False

    # enemy trigger

    for i in enemy_sprites:
        penis = pygame.sprite.collide_mask(player, i)
        if penis:
            gej1 = i
            gej2 = i.image
            mainG = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        menu = True

    if menu:
        renderMenu()

    elif mainG:
        renderMainG()

    else:
        renderfight()
