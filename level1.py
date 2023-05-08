import pygame

pygame.init()

#pociatocne nastavenie (premenne,konstanty,funkcie)
PLAYER_SPEED = 5

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

playerPositionX = 100
playerPositionY = 100
def playerIcon(x,y):
    return pygame.Rect(int(x),int(y), 50, 50)

#zaciatok hlavneho skriptu
running = True
while running:
    screen.fill((0, 0, 0))
    mouse = pygame.mouse.get_pos()
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #pohyb hraca
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        playerPositionY -= PLAYER_SPEED

    if pressed[pygame.K_s]:
        playerPositionY += PLAYER_SPEED

    if pressed[pygame.K_a]:
        playerPositionX -= PLAYER_SPEED

    if pressed[pygame.K_d]:
        playerPositionX += PLAYER_SPEED
    #vykreslovanie
    player = pygame.draw.rect(screen, (255, 255, 255), playerIcon(playerPositionX, playerPositionY))
    screen.blit(cursor, mouse)
    pygame.display.flip()
    clock.tick(60)