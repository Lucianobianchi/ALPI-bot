import pygame
from colors import RED

class DraggablePoint(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.select_offset = (0, 0)
        self.drag = False

        self.image = pygame.Surface([size, size])

        # pygame.draw.line(self.imag
        # self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        #pygame.draw.rect(self.image, RED, (x, y, x+size, y+size))

        self.rect = self.image.get_rect()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1 and self.rect.collidepoint(pos):
                self.drag = True
                self.select_offset = (self.rect.x - pos[0], self.rect.y - pos[1])
               
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False
               
        elif event.type == pygame.MOUSEMOTION:
            if self.drag: # selected can be `0` so `is not None` is required
                # move object
                self.rect.x = event.pos[0] + self.select_offset[0]
                self.rect.y = event.pos[1] + self.select_offset[1]