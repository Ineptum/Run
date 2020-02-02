import pygame


class Finish(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((1024, 1))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, -70
        self.rect.h = 90

    def __str__(self):
        return "Finish"
