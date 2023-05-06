import pygame

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

clock = pygame.time.Clock()

running = True



while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)
