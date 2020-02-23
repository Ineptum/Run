import pygame
import time
import random
from functions import load_image, terminate, load_level, generate_level
from classes.camera import Camera
from classes.finish import Finish

clock = pygame.time.Clock()
fps = 60
SCORE = [0, 0, 0]

buttons = {pygame.K_w: "player1.move_up()",
           pygame.K_a: "player1.move_left()",
           pygame.K_s: "player1.move_down()",
           pygame.K_d: "player1.move_right()",
           pygame.K_UP: "player2.move_up()",
           pygame.K_LEFT: "player2.move_left()",
           pygame.K_DOWN: "player2.move_down()",
           pygame.K_RIGHT: "player2.move_right()"}


def start_screen(intro_text, screen, height):
    global displace
    background = pygame.transform.scale(
        load_image('empty.png'), screen.get_size())
    screen.blit(background, (0, 0))
    text_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    size = int(7 / 90 * height)
    font = pygame.font.Font("slkscr.ttf", size)

    buttons = []

    y = height / 6
    for line in intro_text:
        string_rendered = font.render(
            line, 1, [(0, 245, 255), (255, 0, 245)][random.randint(0, 1)])
        intro_rect = string_rendered.get_rect()

        y += height // 10
        x = (width - font.size(line)[0]) // 2 + displace
        text_width, text_height = font.size(line)

        intro_rect.top = y
        intro_rect.x = x
        y += intro_rect.height

        text_rect = (x - 3 / 8 * size, y - 3 / 2 * size,
                     text_width + 3 / 4 * size, text_height + 3 / 4 * size)
        buttons.append(text_rect)
        text_alpha.blit(string_rendered, intro_rect)

    current_button = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_w or pygame.key == pygame.K_UP:
                    current_button = (current_button + 1) % len(buttons)
                elif event.key == pygame.K_s or pygame.key == pygame.K_DOWN:
                    current_button = (current_button - 1) % len(buttons)

                else:
                    if current_button == 1:
                        return

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), buttons[current_button], 3)
        screen.blit(text_alpha, (0, 0))
        pygame.display.update()
        clock.tick(fps)


def play(screen, height):
    global current_level
    smooth_end = 0
    finished = []

    alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    alpha_surf.fill((255, 255, 255, 220),
                    special_flags=pygame.BLEND_RGBA_MULT)

    camera = Camera(screen.get_size()[1])

    running = True
    player1.isMoving = True
    player1.isMovingDown = True
    player2.isMoving = True
    player2.isMovingDown = True
    draw_sprites = pygame.sprite.Group()

    while running:
        playable = player1.isPlayable and player2.isPlayable
        draw_sprites.empty()

        time_delta = clock.tick(fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    eval(str(buttons.get(event.key)))

        alpha_surf.fill((255, 255, 255, 250),
                        special_flags=pygame.BLEND_RGBA_MULT)
        new_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        screen.fill((0, 0, 0))

        if not player1.move(time_delta, player_group, tile_group,
                            all_sprites, alpha_surf, finish):
            finished.append(1)

        if not player2.move(time_delta, player_group, tile_group,
                            all_sprites, alpha_surf, finish):
            finished.append(2)

        if playable and not finished:
            if player1.rect.y > screen.get_size()[1]:
                finish.rect.y = player2.rect.y - finish.rect.h
                finished.append(2)
            if player2.rect.y > screen.get_size()[1]:
                finish.rect.y = player1.rect.y - finish.rect.h
                finished.append(1)

        elif ((not player1.isPlayable and not player2.isPlayable) and
              (not finished and (player1.rect.y <= screen.get_size()[1] * 0.6 or
                                 player2.rect.y <= screen.get_size()[1] * 0.6))):
            player1.isPlayable = True
            player2.isPlayable = True
            alpha_surf.blit(pygame.transform.scale(
                load_image("start.png"), screen.get_size()), (0, 0))

        player1.inverted += player2.other_inverted * 3
        player2.inverted += player1.other_inverted * 3
        player1.other_inverted, player2.other_inverted = 0, 0

        y = camera.scroll_for(player1 if player1.rect.y <
                              player2.rect.y else player2)

        new_alpha.blit(alpha_surf, (0, -y))
        alpha_surf = new_alpha

        for sprite in all_sprites:
            camera.apply(sprite)
        camera.apply(finish)

        screen.blit(alpha_surf, (0, 0))

        for sprite in tile_group:
            if 0 - 2 / 3 * tile_size < sprite.rect.y < height:  # + tile_size:
                sprite.add(draw_sprites)

        draw_sprites.draw(screen)

        pygame.display.flip()

        if finished:
            if playable:
                result = "Player " + str(finished[0]) + " has won!" if len(
                    finished) == 1 else "draw!"
                if result == "draw!":
                    player1.isPlayable = False
                    player2.isPlayable = False
                else:
                    k = ("player" +
                         str(int(result.split("Player ")[1][0]) % 2 + 1) + ".switch_off()")
                    eval(k)

            smooth_end += time_delta

            if smooth_end > 1.22:
                time.sleep(0.3)
                running = False
                SCORE[1] += 1 in finished
                SCORE[2] += 2 in finished
                current_level += 1
                return result
        # print(1 / time_delta)


def finish_screen(outro_text, screen, height):
    global displace
    new_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    new_alpha.blit(screen.copy(), (0, 0))

    background = pygame.transform.scale(
        load_image('empty.png'), screen.get_size())
    screen.blit(background, (0, 0))
    text_alpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    size = int(5 / 90 * height)
    font = pygame.font.Font("slkscr.ttf", size)

    y = height / 9
    for line in outro_text:
        string_rendered = font.render(
            line, 1, [(0, 245, 255), (255, 0, 245)][random.randint(0, 1)])
        intro_rect = string_rendered.get_rect()

        y += height // 10
        x = (width - font.size(line)[0]) // 2 + displace
        text_width, text_height = font.size(line)

        intro_rect.top = y
        intro_rect.x = x
        y += intro_rect.height

        text_alpha.blit(string_rendered, intro_rect)
    y = 5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_SPACE:
                    return next_level()

        screen.fill((0, 0, 0))
        screen.blit(new_alpha, (0, y))
        screen.blit(text_alpha, (0, 0))
        y += 3
        new_alpha.fill((255, 255, 255, 255),
                       special_flags=pygame.BLEND_RGBA_MULT)
        pygame.display.flip()
        clock.tick(fps)


def next_level(gamestart=False):
    global finish, level, level_width, level_height, player1, player2
    global all_sprites, player_group, tile_group
    global tile_size, displace, width
    level, level_width, level_height = load_level(
        levels[current_level % len(levels)])

    width, height = 350, 350
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE |
                                     pygame.DOUBLEBUF | pygame.FULLSCREEN)
    pygame.display.set_caption("Run")
    pygame.display.set_icon(load_image("invert.png"))

    width_fraction = 0.9
    displace = (width - int(width_fraction * width)) // 2
    width = int(width_fraction * width)
    tile_size = width // level_width
    displace += (width - tile_size * level_width) / 2

    if gamestart:
        start_screen(["QR", "WASD <^>"], screen, height)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()

    player1, player2 = generate_level(
        level, all_sprites, tile_group, player_group, tile_size)

    for sprite in all_sprites:
        sprite.rect.x += displace
    finish = Finish()
    finish_screen(["Stage Over!", play(screen, height), str(SCORE[1]) + " : " + str(SCORE[2]),
                   "SPACE to continue"], screen, height)


if __name__ == "__main__":
    current_level = 0
    levels = ["level" + str(i) + ".txt" for i in range(1, 3)]

    pygame.init()
    pygame.mixer.music.load("data/bptsm.wav")
    pygame.mixer.music.play(-1)
    next_level(gamestart=True)
