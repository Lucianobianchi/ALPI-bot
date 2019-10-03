import pygame, sys
from pygame.locals import *
from Bot import Bot
from DraggablePoint import DraggablePoint
from colors import BG, RED

def offsetted(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])

fps = pygame.time.Clock()

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE)
pygame.display.set_caption('ALPIBot Simulator')

# Create The Backgound
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BG)

ALPIBOT = Bot(200, 200)
DRAG_POINT = DraggablePoint(50, 50, 10)

event_delegates = [DRAG_POINT]
all_sprites = pygame.sprite.RenderPlain((ALPIBOT, DRAG_POINT))

# Display The Background
screen.blit(background, (0, 0))
pygame.display.flip()

# Game loop
is_running = True
while is_running:
    fps.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
            if event.key == pygame.K_k:
                ALPIBOT.accelerate(0, 0.1)
            if event.key == pygame.K_l:
                ALPIBOT.accelerate(1, 0.1)
            if event.key == pygame.K_COMMA:
                ALPIBOT.accelerate(0, -0.1)
            if event.key == pygame.K_PERIOD:
                ALPIBOT.accelerate(1, -0.1)
        else:
            for delegate in event_delegates:
                delegate.handle_event(event)

    all_sprites.update()

    # Draw Everything
    screen.blit(background, (0, 0))

    la, ra = ALPIBOT.get_anchors()
    pygame.draw.line(screen, RED, offsetted(la.center, ALPIBOT.rect.topleft), DRAG_POINT.rect.center)
    pygame.draw.line(screen, RED, offsetted(ra.center, ALPIBOT.rect.topleft), DRAG_POINT.rect.center)

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
    
        
