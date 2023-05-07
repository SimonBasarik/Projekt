import pygame

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

clock = pygame.time.Clock()

running = True

playerPositionX = 100
playerPositionY = 100
playerIcon = pygame.Rect(playerPositionX, playerPositionY, 50 , 50)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Pohyb hraca
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        playerPositionY += 1


    if pressed[pygame.K_a]:
        playerPositionX -= 1


    if pressed[pygame.K_d]:
        playerPositionX += 1

    if pressed[pygame.K_s]:
        playerPositionY -= 1

    player = pygame.draw.rect(screen, (255, 255, 255), playerIcon)
    pygame.display.flip()
    clock.tick(60)
