import pygame
from colors import BLUE, GREEN, RED
import math

FRONT_AXIS_WIDTH = 15
FRONT_AXIS_LENGTH = 150

WHEEL_DIAMETER = 80
WHEEL_WIDTH = 20

ANCHOR_DISTANCE_FROM_WHEEL = 30
ANCHOR_SIZE = 10

R = 10
L = FRONT_AXIS_LENGTH + WHEEL_WIDTH

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect

class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.angle = 0
        self.x = x
        self.y = y
        self.v = 0
        self.a = 0
        self.left_wheel_v = 0
        self.right_wheel_v = 0

        self.base_image = pygame.Surface([WHEEL_DIAMETER, FRONT_AXIS_LENGTH + 2*WHEEL_WIDTH])
        self.base_image.set_colorkey((250, 250, 250))
        self.base_image.fill((250, 250, 250))

        left_wheel = pygame.Rect(0, 0, WHEEL_DIAMETER, WHEEL_WIDTH)
        right_wheel = pygame.Rect(0, WHEEL_WIDTH + FRONT_AXIS_LENGTH, WHEEL_DIAMETER, WHEEL_WIDTH)
        pygame.draw.rect(self.base_image, GREEN, left_wheel)
        pygame.draw.rect(self.base_image, GREEN, right_wheel)
        
        axis = (WHEEL_DIAMETER/2 - FRONT_AXIS_WIDTH/2, WHEEL_WIDTH, FRONT_AXIS_WIDTH, FRONT_AXIS_LENGTH)
        pygame.draw.rect(self.base_image, BLUE, axis)

        # Se rompen con la rotación
        self.left_anchor = pygame.Rect(left_wheel.right + ANCHOR_DISTANCE_FROM_WHEEL, 0, ANCHOR_SIZE, ANCHOR_SIZE)
        self.right_anchor = pygame.Rect(right_wheel.left - ANCHOR_DISTANCE_FROM_WHEEL, 0, ANCHOR_SIZE, ANCHOR_SIZE)
        pygame.draw.rect(self.base_image, RED, self.left_anchor)
        pygame.draw.rect(self.base_image, RED, self.right_anchor)

        self.image = self.base_image
        self.rect = self.base_image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def accelerate(self, wheel, a):
        if wheel == 0:
            self.left_wheel_v += a
            print('Left W V: ', self.left_wheel_v)
            return self.left_wheel_v
        else:
            self.right_wheel_v += a
            print('Right W V: ', self.right_wheel_v)
            return self.right_wheel_v

    def get_anchors(self):
        return (self.left_anchor, self.right_anchor)

    def update(self):
        cx = self.rect.center[0] + ((R/2) * (self.left_wheel_v + self.right_wheel_v) * math.cos(self.angle))
        cy = self.rect.center[1] + ((R/2) * (self.left_wheel_v + self.right_wheel_v) * math.sin(self.angle))
        self.rect.center = (cx, cy)

        self.angle += (R/L) * (self.right_wheel_v - self.left_wheel_v)
        print(self.rect.center)
        self.image, self.rect = rot_center(self.base_image, self.rect, math.degrees(self.angle))
        print('new center', self.rect.center)
        