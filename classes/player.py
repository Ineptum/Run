import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, all_sprites, player_group, image, tile_size):
        super().__init__(player_group, all_sprites)
        self.isPlayable = False
        self.tile_size = tile_size
        self.inverted = 0
        self.other_inverted = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = (self.tile_size * pos_x +
                       (self.tile_size - self.rect.w) // 2)
        self.rect.y = (self.tile_size * pos_y +
                       (self.tile_size - self.rect.h) // 2)
        self.isFlipped = False
        self.rotation = 0

        self.constant_speed = 12  # blocks per second
        self.speed = self.constant_speed * self.tile_size
        self.isMoving = False
        self.acceleration = 0.3 * self.tile_size
        self.xDisplacement, self.yDisplacement = 0, 0

        self.isMovingUp = False
        self.isMovingDown = False
        self.isMovingLeft = False
        self.isMovingRight = False

    def __str__(self):
        return "Player"

    def reset_velocities(self):
        self.speed = self.constant_speed * self.tile_size
        self.isMoving = False
        (self.isMovingRight,
         self.isMovingLeft,
         self.isMovingDown,
         self.isMovingUp) = (False,
                             False,
                             False,
                             False)

    def turn(self, angle):
        self.image = pygame.transform.rotate(self.image, 360 - self.rotation)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rotation = angle

    def check_horizontal_collisions(self, tile_group, all_sprites):
        for sprite in tile_group:
            if self.rect.colliderect(sprite.rect):
                if str(sprite) != "invert":

                    if self.isMovingRight and self.rect.right <= sprite.rect.right:
                        self.rect.right = sprite.rect.left
                        self.turn(90)
                    elif self.isMovingLeft and self.rect.left >= sprite.rect.left:
                        self.rect.left = sprite.rect.right
                        self.turn(270)
                    return True

                else:
                    tile_group.remove(sprite)
                    self.other_inverted = 1

        return False

    def check_vertical_collisions(self, tile_group, all_sprites, finish):
        for sprite in tile_group:
            if self.rect.colliderect(sprite.rect):
                if str(sprite) != "invert":
                    if self.rect.colliderect(sprite.rect):
                        if self.isMovingDown and self.rect.bottom <= sprite.rect.bottom:
                            self.rect.bottom = sprite.rect.top
                            self.turn(0)

                        elif self.isMovingUp and self.rect.top >= sprite.rect.top:
                            self.rect.top = sprite.rect.bottom
                            self.turn(180)
                        return True
                else:
                    tile_group.remove(sprite)
                    self.other_inverted = 1

        if self.rect.colliderect(finish):
            return "Finished"

        return False

    def move_left(self, ignore_inverting=False):
        if self.isPlayable:
            if not self.isMoving:
                if not self.inverted or ignore_inverting:
                    self.reset_velocities()
                    self.isMoving = True
                    self.isMovingLeft = True
                    self.turn(0)
                    if not self.isFlipped:
                        self.isFlipped = True
                        self.image = pygame.transform.flip(
                            self.image, 1, 0)
                    self.turn(90)
                else:
                    self.move_right(True)
                    self.inverted -= 1

    def move_right(self, ignore_inverting=False):
        if self.isPlayable:
            if not self.isMoving:
                if not self.inverted or ignore_inverting:
                    self.reset_velocities()
                    self.isMoving = True
                    self.isMovingRight = True
                    self.turn(0)
                    if self.isFlipped:
                        self.isFlipped = False
                        self.image = pygame.transform.flip(
                            self.image, 1, 0)
                    self.turn(270)
                else:
                    self.move_left(True)
                    self.inverted -= 1

    def move_up(self, ignore_inverting=False):
        if self.isPlayable:
            if not self.isMoving:
                if not self.inverted or ignore_inverting:
                    self.reset_velocities()
                    self.isMoving = True
                    self.isMovingUp = True
                    self.turn(0)
                else:
                    self.move_down(True)
                    self.inverted -= 1

    def move_down(self, ignore_inverting=False):
        if self.isPlayable:
            if not self.isMoving:
                if not self.inverted or ignore_inverting:
                    self.reset_velocities()
                    self.isMoving = True
                    self.isMovingDown = True
                    self.turn(180)
                else:
                    self.move_up(True)
                    self.inverted -= 1

    def switch_off(self):
        self.isPlayable = False

    def move(self, time_delta, player_group, tile_group, all_sprites, alpha_surf, finish):
        self.xDisplacement = time_delta * self.speed * \
            (-1) ** self.isMovingLeft * (self.isMovingRight or self.isMovingLeft)
        self.yDisplacement = time_delta * self.speed * \
            (-1) ** self.isMovingUp * (self.isMovingDown or self.isMovingUp)

        if abs(self.xDisplacement) >= 1:
            xSign = self.xDisplacement // abs(self.xDisplacement)
            while abs(self.xDisplacement) >= 1:
                self.xDisplacement -= xSign
                self.speed += self.acceleration * self.tile_size
                self.rect.x += xSign
                player_group.draw(alpha_surf)
                if self.check_horizontal_collisions(tile_group, all_sprites):
                    self.isMoving = False
                    break
        if abs(self.yDisplacement) >= 1:
            ySign = self.yDisplacement // abs(self.yDisplacement)
            while abs(self.yDisplacement) >= 1:
                self.yDisplacement -= ySign
                self.speed += self.acceleration * self.tile_size
                self.rect.y += ySign
                player_group.draw(alpha_surf)
                colliding = self.check_vertical_collisions(
                    tile_group, all_sprites, finish)
                if colliding:
                    if colliding == "Finished":
                        return False
                    self.isMoving = False
                    break
        return True
