import pygame

PLAYER_SPEED = 5

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

clock = pygame.time.Clock()

running = True

playerPositionX = 100
playerPositionY = 100
def playerIcon(x,y):
    return pygame.Rect(int(x),int(y), 50, 50)

while running:
    screen.fill((0, 0, 0))
    mouse = pygame.mouse.get_pos()
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Pohyb hraca
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        playerPositionY -= PLAYER_SPEED

    if pressed[pygame.K_s]:
        playerPositionY += PLAYER_SPEED

    if pressed[pygame.K_a]:
        playerPositionX -= PLAYER_SPEED

    if pressed[pygame.K_d]:
        playerPositionX += PLAYER_SPEED

    player = pygame.draw.rect(screen, (255, 255, 255), playerIcon(playerPositionX, playerPositionY))
    screen.blit(cursor, mouse)
    pygame.display.flip()
    clock.tick(60)