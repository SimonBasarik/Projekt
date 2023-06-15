import pygame, json,math
from pytmx.util_pygame import load_pygame
import hrac, button, nepriatel, healthbar, obchodnik

pygame.init()

# pociatocne nastavenie (premenne,konstanty,funkcie)

res = (1920, 1080)  # rozlisenie

mainscreen = pygame.display.set_mode(res)

gej2 = None
enemy = None

# nacitanie levelov z .tmx do premennych

level1 = load_pygame("levely\\level1.tmx")
level2 = load_pygame("levely\\level2.tmx")


#transformovanie obrazkov

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()
fight_img = pygame.image.load("png\\fight.png").convert_alpha()
fight_height = fight_img.get_rect().height
fight_width = fight_img.get_rect().width
fight_img = pygame.transform.scale(fight_img,(fight_width*3,fight_height*3))
shop_img = pygame.image.load("png\\SHOP.png").convert_alpha()
shop_height = shop_img.get_rect().height
shop_width = shop_img.get_rect().width
shop_img = pygame.transform.scale(shop_img,(shop_width*3,shop_height*3))

clock = pygame.time.Clock()

sidebar = False

def renderShop():
    global gamelevel
    global shop
    global sidebar
    global trader1
    global trader2
    global Bussinessman_sprites


    mouse = pygame.mouse.get_pos()
    mainscreen.fill((0, 0, 0))
    mainscreen.blit(shop_img,(0,0))
    shopSHOP.draw(mainscreen)


    if shopHEAL.draw(mainscreen):
        sidebar = True
    if shopMANA.draw(mainscreen):
        sidebar = True
    if shopexit.draw(mainscreen):
        gamelevel = player.gamelevel
        player.pos.y += 50
        shop = False
        sidebar = False

    if sidebar:
        buybutton.draw(mainscreen)
        sellbutton.draw(mainscreen)

    mainscreen.blit(cursor, mouse)

    pygame.display.flip()

# funkcia renderMenu(), vykresluje menu

def renderMenu():
    global gamelevel
    global menu
    global running

    mouse = pygame.mouse.get_pos()

    mainscreen.fill((0, 0, 0))


    #vykreslenie tlacidiel

    if startButton.draw(mainscreen):
        gamelevel = player.gamelevel
        menu = False

    if quitButton.draw(mainscreen):
        writedata()
        running = False

    mainscreen.blit(cursor, mouse)

    pygame.display.flip()

# funkcia renderLevel1(), vykresluje hraca a enemy

def renderLevel1():

    # vykreslenie hraca a animacia

    global gej2
    global enemy
    global gamelevel

    moving_sprites.draw(mainscreen)
    moving_sprites.update()

    enemy_sprites.draw(mainscreen)
    enemy_sprites.update()

    pygame.display.flip()
    clock.tick(60)

    #kontrola kedy sa prepne level na 2

    if player.pos.y > res[1]:
        for wall in wallGroup:
            wallGroup.remove(wall)
        for floor in floorGroup:
            floorGroup.remove(floor)
        enemy_sprites.add(muddy)
        player.gamelevel = 2
        gamelevel = player.gamelevel
        loadlevel2()
        player.pos.y = 50

# funkcia renderLevel2(), vykresluje hraca a enemy

def renderLevel2():


    # vykreslenie hraca a animacia

    global gej2
    global enemy

    moving_sprites.draw(mainscreen)
    moving_sprites.update()

    enemy_sprites.draw(mainscreen)
    enemy_sprites.update()

    Bussinessman_sprites.draw(mainscreen)
    Bussinessman_sprites.update()

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
    global gamelevel
    global gej1
    global gej2
    global enemy
    global fight

    # nastavenie mysi a fill obrazovky

    mouse = pygame.mouse.get_pos()
    mainscreen.fill((28, 28, 28))

    # casovac hraca

    time = clock.tick(60)
    player.timer += time
    timerS = player.timer / 1000

    # blit pozadie fightu (to pozadie za tlacidlami)

    mainscreen.blit(fight_img, (0, 0))

    #nastavenie nepriatelskych objektov do premennej enemy

    player.updateIdle(mainscreen)
    if gej2 == goblin.image:
        enemy = goblin
    if gej2 == demon.image:
        enemy = demon
    if gej2 == muddy.image:
        enemy = muddy
    if gej2 == chort.image:
        enemy = chort
    if gej2 == bigzombie.image:
        enemy = bigzombie

    if not enemy:
        gamelevel = player.gamelevel
        return

    #vykreslenie nepriatela

    enemy.updateIdle(mainscreen)

    # casovac utokov nepriatela

    if enemy.enemyTimer():
        enemy.enemyAttack -= player.Ressistance
        player.Health -= enemy.enemyAttack
        enemy.enemyAttack += player.Ressistance
        player.Ressistance = 0

    # vykreslovanie hlavnych tlacidiel, a ich funkcie

    if draw_mainButtons:
        if attackButton.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME:
                enemy.Health -= 10
                player.timer = 0

        if defendButton.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME:
                player.Ressistance = 4
                player.timer = 0

        if magicButton.draw(mainscreen):
            draw_mainButtons = False
            draw_magicButtons = True
        if itemButton.draw(mainscreen):
            draw_mainButtons = False
            draw_itemButtons = True
    timerText.draw(mainscreen)
    manaText.draw(mainscreen)

    # vykreslovanie magic tlacidiel, a ich funkcie

    if draw_magicButtons == True:
        if fireballButton.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME and player.Mana >= 5:
                damage = 20 - enemy.enemyFireResistance
                player.Mana -= 5
                enemy.Health -= damage
                player.timer = 0

        if frostfangButton.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME and player.Mana >= 5:
                damage = 20 - enemy.enemyIceResistance
                player.Mana -= 5
                enemy.Health -= damage
                player.timer = 0

        if backbutton.draw(mainscreen):
            draw_magicButtons = False
            draw_mainButtons = True

    # vykreslovanie item tlacidiel, a ich funkcie

    if draw_itemButtons == True:

        if manapotion.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME:
                player.Mana += 10
                player.timer = 0
        if healpotion.draw(mainscreen):
            if timerS >= player.TIMERMAXTIME:
                player.Health += 20
                player.timer = 0
                if player.Health > player.MaxHealth:
                    player.Health = player.MaxHealth
        if backbutton.draw(mainscreen):
            draw_itemButtons = False
            draw_mainButtons = True
            player.timer = 0

    # vykreslenie HealthBaru

    enemy.Healthbar.draw(mainscreen, enemy.Health)
    player.Healthbar.draw(mainscreen, player.Health)
    player.drawMP(mainscreen)
    player.drawtimer(mainscreen)
    mainscreen.blit(cursor, mouse)

    # smrt hraca

    if player.Health <= 0:
        player.pos.x =player
        player.pos.y = 540
        gamelevel = player.gamelevel
        fight = False
        player.Health = 20
        enemy.Health = 100

    #smrt nepriatela

    if enemy.Health <= 0:
        player.score += 1
        gamelevel = player.gamelevel
        fight = False
        enemy = None
        pygame.sprite.Sprite.kill(gej1)



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

# Vytvorenie objektov z classy Button(), nastavenie parametrov (x, y, text tlacitka, velkost fontu)

startButton = button.Button(775,400,"START", 60)
quitButton = button.Button(815,600,"QUIT",60)
attackButton = button.Button(150, 720, "ATTACK", 60)
fireballButton = button.Button(150, 720, "FIREBALL", 60)
frostfangButton = button.Button(150, 870, "FROSTFANG", 60)
defendButton = button.Button(150, 870, "DEFEND", 60)
magicButton = button.Button(700, 720, "MAGIC", 60)
itemButton = button.Button(700, 870, "ITEM", 60)
timerText = button.Button(1250, 720, "TIMER:", 45)
manaText = button.Button(1280,790,"MANA:",45)
healpotion = button.Button(150, 720, "HEALPOTION", 60)
manapotion = button.Button(150, 870, "MANAPOTION", 60)
backbutton = button.Button(1300,900,"<- BACK",45)
buybutton = button.Button(1300,850,"BUY",60)
sellbutton = button.Button(1600,850,"SELL",60)
shopexit = button.Button(100,850,"LEAVE", 50)
shopSHOP = button.Button(770,150,"SHOP", 120)
shopHEAL = button.Button(100,150,"HEALPOTION", 50)
shopMANA = button.Button(100,250,"MANAPOTION", 50)
shopSWORD = button.Button(300,850,"EXIT", 60)

# Vytvorenie floor, a wall group, neskôr v kóde sa do nich pridajú jednotlivé tily

floorGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()

# pridanie spritu do sprite groupu

moving_sprites = pygame.sprite.GroupSingle()
player = hrac.Player(wallGroup)
moving_sprites.add(player)

# Vytvorenie enemies z classy Enemy(posx,posy,enemytype,sila utoku, x pozicia pri suboju, y pozicia pri suboju, fire resistance, ice resistance)

enemy_sprites = pygame.sprite.Group()
goblin = nepriatel.Enemy(960, 950, 1, 5, 1500, 300,0,0,1.5)
demon = nepriatel.Enemy(760, 750, 2, 15, 1400, 200,15,-5,2.2)
bigzombie = nepriatel.Enemy(660, 650, 3, 15, 1400, 200,5,5,2.2)
muddy = nepriatel.Enemy(560, 560, 5, 10, 1500, 300,5,0,2)
chort = nepriatel.Enemy(960, 750, 4, 5, 1500, 300,5,-5,0.5)
enemy_sprites.add(goblin)

Bussinessman_sprites = pygame.sprite.Group()
Bussinessman = obchodnik.Bussinessman(270,150)
Bussinessman_sprites.add(Bussinessman)

# Vytvorenie objektov z classy Healthbar(), nastavenie parametrov (x, y, sirka, vyska,maxhp)

playerHealthBar = healthbar.Healthbar(325, 175, 250, 25, player.MaxHealth)

# zapisanie zakladnych statistik do data.json

dickt = dict()

with open("data.json", "r", encoding="UTF-8") as f:
    dickt = json.load(f)

saves = dickt["saves"]

def writedata():
    global saves

    data = {"health": player.Health,"mana": player.Mana, "score": player.score, "game level": player.gamelevel}

    saves.append(data)

    new_data = {"saves": saves}

    new_json = json.dumps(new_data, indent=3)

    with open("data.json", "w", encoding="UTF-8") as f:
        f.write(new_json)

# pridanie stien a podlahy do ich vlastných groupov, a loadovanie

def loadlevel2():
    for layer in level2.visible_layers:
        if layer.name == "ground":
            for x, y, surf in layer.tiles():
                pos = (x * 48, y * 48)
                Floor(pos=pos, surf=surf, groups=floorGroup)

    for layer in level2.visible_layers:
        if layer.name == "walls":
            for x, y, surf in layer.tiles():
                pos = (x * 48, y * 48)
                Walls(pos=pos, surf=surf, groups=wallGroup)

# funkcia na kontrolu levelov (ktory sa ma loadnut atd.)

def checklevels():
    if player.gamelevel == 1:
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
    elif player.gamelevel == 2:
        loadlevel2()


#premenne pre hlavny loop

shop = False
running = True
menu = True
gamelevel = 1
fight = False
checklevels()
last_trader_pos = [-1, -1]
trader1 = None

# main loop

while running:
    mainscreen.fill((0, 0, 0))
    floorGroup.draw(mainscreen)
    wallGroup.draw(mainscreen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            writedata()
            running = False

    # kontrola kolizii s nepriatelmi

    for i in enemy_sprites:
        penis = pygame.sprite.collide_mask(player, i)
        if penis:
            gej1 = i
            gej2 = i.image
            fight = True

    # kontrola kolizii s obchodnikom

    for i in Bussinessman_sprites:
        last_trader_pos = [i.rect.x, i.rect.y]
        trader = pygame.sprite.collide_mask(player, i)
        if trader:
            trader1 = i
            trader2 = i.image
            shop = True
            Bussinessman_sprites.remove(i)

    # kopec ifov ktore kontroluju co sa ma nacitat

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        menu = True

    if menu:
        renderMenu()
    else:

        if not fight and not shop:
            if last_trader_pos[0] != -1 and last_trader_pos[1] != -1:
                distance_trader = math.dist(player.pos, last_trader_pos)
                if distance_trader > 50 and trader1 and trader1 not in Bussinessman_sprites:
                    Bussinessman_sprites.add(trader1)

            if gamelevel == 1:
                renderLevel1()

            elif gamelevel == 2:
                renderLevel2()

        if fight:
            renderfight()

        if shop:
            renderShop()
