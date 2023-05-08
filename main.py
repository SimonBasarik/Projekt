import pygame

pygame.init()

res = (1920,1080) #rozlisenie

screen = pygame.display.set_mode(res)

clock = pygame.time.Clock()

mainButtonColor = (255,0,0)
fontButtonColor = (255,255,255)
#tlacitko vypnut
buttonQuitWIDTH = 900
buttonQuitHEIGHT = 540
#tlacitko zapnut
buttonStartWIDTH = 900
buttonStartHEIGHT = 480
font = pygame.font.Font('Font\\rainyhearts.ttf', 50)




pygame.mouse.set_visible(False)
cursor = pygame.image.load('slick_arrow-delta.png').convert_alpha()

running = True
while running:
    mouse = pygame.mouse.get_pos()
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    screen.fill((0, 0, 0))

    buttonStart = pygame.draw.rect(screen, mainButtonColor, (buttonStartWIDTH, buttonStartHEIGHT, 140, 50))
    buttonStartText = font.render('START', True, fontButtonColor)

    screen.blit(buttonStartText, (buttonStartWIDTH, buttonStartHEIGHT))

    buttonQuit = pygame.draw.rect(screen, mainButtonColor, (buttonQuitWIDTH, buttonQuitHEIGHT, 140, 50))
    buttonQuitText = font.render('QUIT', True, fontButtonColor)

    screen.blit(buttonQuitText, (buttonQuitWIDTH + 18, buttonQuitHEIGHT))

    if buttonQuit.collidepoint(mouse) and mouse_click:
        running = False

    if buttonStart.collidepoint(mouse) and mouse_click:
        with open("level1.py") as f:
            exec(f.read())




    screen.blit(cursor,mouse)
    pygame.display.update()
    clock.tick(60)