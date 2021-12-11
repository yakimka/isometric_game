import sys

import pygame

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('farmer.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft=pos)


def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode((900, 900), 0, 32)
    # display = pygame.Surface((900, 900))
    display = screen

    grass_img = pygame.image.load('my_grass_scaled2.png').convert()
    grass_img.set_colorkey((0, 0, 0))

    # 450 is the half of the display width
    camera = pygame.math.Vector2(450, 0)

    player = pygame.sprite.GroupSingle()
    player_sprite = Player((450 + 0 - 64, 64 - 64 + 42))
    player.add(player_sprite)

    # Начало координат - середина ширины, 0 (450,0) (можно оставить на 0,0 а сдвиг делать камерой)
    # Нужно разобраться с масштабированием и координатами (учитывать скейл?)
    # Рисуем карту с середины экрана (самый первый тайл, даже если там пустота, ведь карта прямоугольная)
    # Наводим камеру на игрока
    # У нас есть сдвиг камеры, начало
    while True:
        display.fill((128, 0, 0))

        # for x in range(int(600 / TILE_WIDTH)):
        #     for y in range(int(600 / TILE_HEIGHT)):
        #         x1 = x * TILE_WIDTH
        #         y1 = y * TILE_HEIGHT
        #         display.blit(grass_img, (x1, y1))

        # camera move function
        # двигаем все спрайты уровня
        # поверхности, которые не спрайты будут рисоваться сразу со сдвигом камеры
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.y += 3
            player.sprite.rect.y += 3
        if keys[pygame.K_s]:
            camera.y += -3
            player.sprite.rect.y += -3
        if keys[pygame.K_a]:
            camera.x += 3
            player.sprite.rect.x += 3
        if keys[pygame.K_d]:
            camera.x += -3
            player.sprite.rect.x += -3

        def cart_to_iso(cartesian):
            # https://www.youtube.com/watch?v=KvSjJ-kdGio
            x, y = tuple(cartesian)
            converted = pygame.math.Vector2()
            converted.x = x - y
            converted.y = (x + y) / 2
            return converted


        if keys[pygame.K_UP]:
            # player.sprite.rect.y += -3
            vector = cart_to_iso((0, -2))
            player.sprite.rect.x += vector.x
            player.sprite.rect.y += vector.y
        if keys[pygame.K_DOWN]:
            # player.sprite.rect.y += 3
            # скорость должна быть чётной
            vector = cart_to_iso((0, 2))
            player.sprite.rect.x += vector.x
            player.sprite.rect.y += vector.y
        if keys[pygame.K_LEFT]:
            vector = cart_to_iso((-2, 0))
            player.sprite.rect.x += vector.x
            player.sprite.rect.y += vector.y
        if keys[pygame.K_RIGHT]:
            vector = cart_to_iso((2, 0))
            player.sprite.rect.x += vector.x
            player.sprite.rect.y += vector.y

        for x in range(1, 41):
            for y in range(1, 41):
                # https://www.youtube.com/watch?v=04oQ2jOUjkU
                # x * 0.5w + y * -0.5w
                # x * 0.5h + y * 0.5h (0.5h == 0.25w)
                x1 = x * 64 + y * -64
                y1 = x * 32 + y * 32
                # y1 = x * 20 + y * 20
                # 64 offset is half of the tile width
                # это позиция левого верхнего угла картинки (не угла тайла!)
                display.blit(grass_img, (camera.x + x1 - 64, camera.y + y1 - 64))
                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x * 16, y * 16, 16, 16), 1)

                # if (x, y) == (1, 1):
                #     # print((camera.x + x1 - 64, camera.y + y1 - 64))
                #     # 42 для центрирования по середине тайла земли
                #     # персонажи рисуются относительно низа (bottomleft) на середине тайла (34px + офсет тайла персонажа)
                #     player_sprite = Player((camera.x + x1 - 64, camera.y + y1 - 64 + 42))
                #     player.add(player_sprite)
                #     player.draw(display)

        player.draw(display)

        # for y in range(20):
        #     for x in range(20):
        #         display.blit(grass_img, (x * 10 - y * 10, x * 5 + y * 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

        # screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        # screen.blit(pygame.transform.rotozoom(display, 0, 1), (0, 0))
        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
