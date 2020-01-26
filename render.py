import pygame
import sys
import socket

clock = pygame.time.Clock()
fps = 60
SCORE = [0, 0, 0]
inverted = [0, 0]
# pygame.mixer.pre_init(44100, 16, 2, 4096)


def load_level(filename):
    filename = "data/" + filename
    with open(filename) as mapFile:
        level_map = [line.rstrip() for line in mapFile]

    max_width = max(map(len, level_map))
    max_height = len(level_map)

    return list(map(lambda x: x.ljust(max_width, '.'), level_map)), max_width, max_height


def generate_level(level):
    global tile_width
    player1, player2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == " ":
                pass
            elif level[y][x] == '|':
                Tile("vert1.png", x, y)

            elif level[y][x] == '-':
                Tile("hori1.png", x, y)

            elif level[y][x] == '/':
                Tile("lu.png", x, y)

            elif level[y][x] == '\\':
                Tile("ru.png", x, y)

            elif level[y][x] == '<':
                Tile("ld.png", x, y)

            elif level[y][x] == '>':
                Tile("rd.png", x, y)

            elif level[y][x] == 'L':
                Tile("dlu.png", x, y)

            elif level[y][x] == 'R':
                Tile("urd.png", x, y)

            elif level[y][x] == 'T':
                Tile("lur.png", x, y)

            elif level[y][x] == 'B':
                Tile("ldr.png", x, y)

            elif level[y][x] == 'i':
                Tile("invert.png", x, y)

            elif level[y][x] == 'p':
                player1 = Player("Player1.png", x, y)

            elif level[y][x] == "q":
                player2 = Player("Player2.png", x, y)

    return player1, player2


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load("data/" + name)
    except Exception as exception:
        print("Cannot load image: {}".format(name))
        raise SystemExit(exception)

    image = image.convert_alpha()
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Finish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(finish_group, all_sprites)
        self.image = pygame.Surface((1024, tile_width * 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def __str__(self):
        return "Finish"


class Camera:
    def __init__(self, width, height):
        self.y_Difference = 0
        self.time_delta = 0
        self.windowWidth, self.windowHeight = width, height

    def apply(self, obj):
        obj.rect.y -= int(self.y_Difference)

    def scroll_for(self, target, slow=True):
        self.y_Difference = int((target.rect.y + target.rect.h / 2 - self.windowHeight * (1 / 2)) /
                                (24 if slow else 1))
        return self.y_Difference


class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_image, pos_x, pos_y):
        global tile_width
        super().__init__(tile_group, all_sprites)
        self.name = sprite_image.rstrip('.png')
        self.image = pygame.transform.scale(
            load_image(sprite_image), (tile_width, tile_width))
        self.rect = self.image.get_rect().move(pos_x * tile_width,
                                               pos_y * tile_width)

    def __str__(self):
        return self.name


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_image, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        global tile_width
        self.image = pygame.transform.scale(
            load_image(sprite_image), tuple(map(int, (tile_width * 0.8, tile_width * 0.8))))
        self.rect = self.image.get_rect()
        self.rect.x = (tile_width * pos_x + (tile_width - self.rect.w) // 2)
        self.rect.y = (tile_width * pos_y + (tile_width - self.rect.h) // 2)
        self.isFlipped = False
        self.rotation = 0

        self.constant_speed = 12  # blocks per second
        self.speed = self.constant_speed * tile_width
        self.isMoving = False
        self.acceleration = 0.3 * tile_width
        self.xDisplacement, self.yDisplacement = 0, 0

        self.isMovingUp = False
        self.isMovingDown = False
        self.isMovingLeft = False
        self.isMovingRight = False

        self.name = sprite_image.rstrip('.png')

    def __str__(self):
        return self.name

    def reset_velocities(self):
        self.speed = self.constant_speed * tile_width
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

    def check_horizontal_collisions(self):
        global inverted, tile_group
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
                    inverted[int(str(self)[-1]) % 2] = 3

        return False

    def invert(self):
        pass

    def check_vertical_collisions(self):
        global running, finished, tile_group
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
                    inverted[int(str(self)[-1]) % 2] = 3

        if self.rect.colliderect(finish):
            running = False
            finished.append(int(str(self)[-1]))
            return True

        return False

    def move(self, time_delta):
        global alpha_surf
        self.xDisplacement = time_delta * self.speed * \
            (-1) ** self.isMovingLeft * (self.isMovingRight or self.isMovingLeft)
        self.yDisplacement = time_delta * self.speed * \
            (-1) ** self.isMovingUp * (self.isMovingDown or self.isMovingUp)

        if abs(self.xDisplacement) >= 1:
            xSign = self.xDisplacement // abs(self.xDisplacement)
            while abs(self.xDisplacement) >= 1:
                self.xDisplacement -= xSign
                self.speed += self.acceleration * tile_width
                self.rect.x += xSign
                player_group.draw(alpha_surf)
                if self.check_horizontal_collisions():
                    self.isMoving = False
                    break
        if abs(self.yDisplacement) >= 1:
            ySign = self.yDisplacement // abs(self.yDisplacement)
            while abs(self.yDisplacement) >= 1:
                self.yDisplacement -= ySign
                self.speed += self.acceleration * tile_width
                self.rect.y += ySign
                player_group.draw(alpha_surf)
                if self.check_vertical_collisions():
                    self.isMoving = False
                    break


# -------------------------------
def start_screen(intro_text, screen):
    global displace
    background = pygame.transform.scale(
        load_image('empty.png'), screen.get_size())
    screen.blit(background, (0, 0))
    text_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    font = pygame.font.Font("slkscr.ttf", 42)

    buttons = []

    y = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, (100, 0, 200))
        intro_rect = string_rendered.get_rect()

        y += 50
        x = (width - font.size(line)[0]) // 2 + displace
        text_width, text_height = font.size(line)

        intro_rect.top = y
        intro_rect.x = x
        y += intro_rect.height

        text_rect = (x - 15, y - 60, text_width + 30, text_height + 30)
        buttons.append(text_rect)
        # pygame.draw.rect(screen, (255, 255, 255), text_rect, 3)
        text_alpha.blit(string_rendered, intro_rect)

    current_button = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_w:
                    current_button = (current_button + 1) % len(buttons)
                elif event.key == pygame.K_s:
                    current_button = (current_button - 1) % len(buttons)

                else:
                    if current_button == 1:
                        return

        screen.fill((0, 0, 40))
        pygame.draw.rect(screen, (255, 255, 255), buttons[current_button], 3)
        screen.blit(text_alpha, (0, 0))
        pygame.display.flip()
        clock.tick(fps)


# --------------------------------


def play(screen):
    global running, alpha_surf, finished, current_level, inverted
    finished = []
    playable = False
    alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    alpha_surf.fill((255, 255, 255, 220),
                    special_flags=pygame.BLEND_RGBA_MULT)

    camera = Camera(*screen.get_size())

    running = True

    player1.isMoving = True
    player1.isMovingDown = True
    player2.isMoving = True
    player2.isMovingDown = True

    while running:
        time_delta = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if playable:

                    if event.key == pygame.K_DOWN and not player2.isMoving:
                        if not inverted[1]:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingDown = True
                            player2.turn(180)
                        else:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingUp = True
                            player2.turn(0)
                            inverted[1] = inverted[1] - 1

                    elif event.key == pygame.K_UP and not player2.isMoving:
                        if not inverted[1]:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingUp = True
                            player2.turn(0)
                        else:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingDown = True
                            player2.turn(180)
                            inverted[1] = inverted[1] - 1

                    elif event.key == pygame.K_LEFT and not player2.isMoving:
                        if not inverted[1]:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingLeft = True
                            player2.turn(0)
                            if not player2.isFlipped:
                                player2.isFlipped = True
                                player2.image = pygame.transform.flip(
                                    player2.image, 1, 0)
                            player2.turn(90)
                        else:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingRight = True
                            player2.turn(0)
                            if player2.isFlipped:
                                player2.isFlipped = False
                                player2.image = pygame.transform.flip(
                                    player2.image, 1, 0)
                            player2.turn(270)
                            inverted[1] = inverted[1] - 1

                    elif event.key == pygame.K_RIGHT and not player2.isMoving:
                        if inverted[1]:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingLeft = True
                            player2.turn(0)
                            if not player2.isFlipped:
                                player2.isFlipped = True
                                player2.image = pygame.transform.flip(
                                    player2.image, 1, 0)
                            player2.turn(90)
                            inverted[1] = inverted[1] - 1
                        else:
                            player2.reset_velocities()
                            player2.isMoving = True
                            player2.isMovingRight = True
                            player2.turn(0)
                            if player2.isFlipped:
                                player2.isFlipped = False
                                player2.image = pygame.transform.flip(
                                    player2.image, 1, 0)
                            player2.turn(270)

                    elif event.key == pygame.K_s and not player1.isMoving:
                        if not inverted[0]:
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingDown = True
                            player1.turn(180)
                        else:
                            inverted[0] = inverted[0] - 1
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingUp = True
                            player1.turn(0)

                    elif event.key == pygame.K_w and not player1.isMoving:
                        if inverted[0]:
                            inverted[0] = inverted[0] - 1
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingDown = True
                            player1.turn(180)
                        else:
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingUp = True
                            player1.turn(0)

                    elif event.key == pygame.K_a and not player1.isMoving:
                        if not inverted[0]:
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingLeft = True
                            player1.turn(0)
                            if not player1.isFlipped:
                                player1.isFlipped = True
                                player1.image = pygame.transform.flip(
                                    player1.image, 1, 0)
                            player1.turn(90)
                        else:
                            inverted[0] = inverted[0] - 1
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingRight = True
                            player1.turn(0)
                            if player1.isFlipped:
                                player1.isFlipped = False
                                player1.image = pygame.transform.flip(
                                    player1.image, 1, 0)
                            player1.turn(270)

                    elif event.key == pygame.K_d and not player1.isMoving:
                        if inverted[0]:
                            inverted[0] = inverted[0] - 1
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingLeft = True
                            player1.turn(0)
                            if not player1.isFlipped:
                                player1.isFlipped = True
                                player1.image = pygame.transform.flip(
                                    player1.image, 1, 0)
                            player1.turn(90)
                        else:
                            player1.reset_velocities()
                            player1.isMoving = True
                            player1.isMovingRight = True
                            player1.turn(0)
                            if player1.isFlipped:
                                player1.isFlipped = False
                                player1.image = pygame.transform.flip(
                                    player1.image, 1, 0)
                            player1.turn(270)
        alpha_surf.fill((255, 255, 255, 250),
                        special_flags=pygame.BLEND_RGBA_MULT)
        new_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        screen.fill((0, 0, 40))

        player1.move(time_delta)
        player2.move(time_delta)

        if finished and playable:
            result = "Player " + str(finished[0]) + "has won!" if len(
                finished) == 1 else "draw!"
            playable = False
            SCORE[1] += 1 in finished
            SCORE[2] += 2 in finished
            current_level += 1
            return result

        y = camera.scroll_for(player1 if player1.rect.y <
                              player2.rect.y else player2)

        new_alpha.blit(alpha_surf, (0, -y))
        alpha_surf = new_alpha

        for sprite in all_sprites:
            camera.apply(sprite)

        player_group.draw(alpha_surf)

        screen.blit(alpha_surf, (0, 0))
        tile_group.draw(screen)
        if running:
            player_group.draw(screen)
        finish_group.draw(screen)

        pygame.display.flip()
        if playable and not finished:
            if player1.rect.y > screen.get_size()[1]:
                finished.append(2)
            if player2.rect.y > screen.get_size()[1]:
                finished.append(1)
        elif not playable and not finished and (player1.rect.y <= screen.get_size()[1] * 0.6 or
                                                player2.rect.y <= screen.get_size()[1] * 0.6):
            playable = True
            alpha_surf.blit(pygame.transform.scale(
                load_image("start.png"), screen.get_size()), (0, 0))
        # print(1 / time_delta)


def finish_screen(outro_text, screen):
    global displace
    background = pygame.transform.scale(
        load_image('empty.png'), screen.get_size())
    screen.blit(background, (0, 0))
    text_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    font = pygame.font.Font("slkscr.ttf", 42)

    y = 100
    for line in outro_text:
        string_rendered = font.render(line, 1, (100, 0, 200))
        intro_rect = string_rendered.get_rect()

        y += 50
        x = (width - font.size(line)[0]) // 2 + displace
        text_width, text_height = font.size(line)

        intro_rect.top = y
        intro_rect.x = x
        y += intro_rect.height

        text_alpha.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_SPACE:
                    return next_level()

        screen.fill((0, 0, 40))
        screen.blit(text_alpha, (0, 0))
        pygame.display.flip()
        clock.tick(fps)


def next_level(gamestart=False):
    global finish, level, level_width, level_height, player1, player2, all_sprites, player_group, tile_group, finish_group, tile_width, displace, width
    comp = pygame.mixer.Sound("data/bptsm.wav")
    comp.play()
    level, level_width, level_height = load_level(levels[current_level])

    # display_info = pygame.display.Info()
    # width, height = ((display_info.current_h, display_info.current_h))
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE |
                                     pygame.DOUBLEBUF | pygame.RESIZABLE)

    width_fraction = 0.9
    displace = (width - int(width_fraction * width)) // 2
    width = int(width_fraction * width)
    tile_width = width // level_width
    displace += (width - tile_width * level_width) / 2

    if gamestart:
        start_screen(["Play with phones", "Regular play"], screen)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()

    player1, player2 = generate_level(level)
    finish = Finish()

    for sprite in all_sprites:
        sprite.rect.x += displace
    finish_screen(["Game Over!", play(screen), str(SCORE[1]) + " : " + str(SCORE[2]),
                   "SPACE to continue"], screen)


if __name__ == "__main__":
    current_level = 0
    levels = ["level" + str(i) + ".txt" for i in range(1, 3)]

    pygame.init()
    next_level(gamestart=True)
