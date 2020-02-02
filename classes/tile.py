import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, all_sprites, tile_group, image, tile_size):
        super().__init__(tile_group, all_sprites)
        self.name = name
        self.exists = True
        self.image = image
        self.rect = self.image.get_rect().move(pos_x * tile_size,
                                               pos_y * tile_size)

    def __str__(self):
        return self.name
