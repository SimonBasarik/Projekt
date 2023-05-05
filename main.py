import pygame

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

mainButtonColor = (255,0,0)
fontButtonColor = (255,255,255)
WIDTH = 910
HEIGHT = 540
font = pygame.font.Font('Font\\rainyhearts.ttf', 50)






buttonQuit = pygame.draw.rect(screen,mainButtonColor,(WIDTH,HEIGHT, 105,50))
text = font.render('QUIT', True, fontButtonColor)

screen.blit(text, (WIDTH,HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    buttonQuit

    pygame.display.update()