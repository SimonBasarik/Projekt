import pygame

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
