import math
import sys

import pygame

clock = pygame.time.Clock()


# Картинка тайла 128х128
# клетка d1=128px, d2=64px
# сторона ромба = 64px
# сторона ромба = 71px (71.55) (a = ((D**2 + d**2) ** 0.5) / 2)
# центр клетки находится на 34px ниже верхнего угла


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    result = math.floor(n * multiplier + 0.5) / multiplier
    if decimals == 0:
        result = int(result)
    return result


def cart_to_iso(cartesian):
    # https://www.youtube.com/watch?v=KvSjJ-kdGio
    x, y = tuple(cartesian)
    converted = pygame.math.Vector2()
    converted.x = x - y
    converted.y = (x + y) / 2
    return converted


def iso_to_cart(iso):
    # https://www.youtube.com/watch?v=KvSjJ-kdGio
    x, y = tuple(iso)
    converted = pygame.math.Vector2()
    converted.x = (x + y * 2) / 2
    converted.y = -x + converted.x
    return converted


marked = (0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('farmer.png').convert_alpha()

        pos = pygame.math.Vector2(*marked) * 64
        pos = cart_to_iso(pos)
        # TODO add camera offset
        # 450 + 0 - 64, 64 - 64 + 42
        # pos.x += 450 + 0 - 64
        # pos.y += 64 - 64 - 34
        # pos.x += 34
        pos.y += 42

        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self):
        self.get_inputs()

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        # скорость должна быть чётной
        if keys[pygame.K_UP]:
            vector = cart_to_iso((0, -2))
            self.rect.x += vector.x
            self.rect.y += vector.y
        if keys[pygame.K_DOWN]:
            vector = cart_to_iso((0, 2))
            self.rect.x += vector.x
            self.rect.y += vector.y
        if keys[pygame.K_LEFT]:
            vector = cart_to_iso((-2, 0))
            self.rect.x += vector.x
            self.rect.y += vector.y
        if keys[pygame.K_RIGHT]:
            vector = cart_to_iso((2, 0))
            self.rect.x += vector.x
            self.rect.y += vector.y


def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode((900, 900), 0, 32)
    # display = pygame.Surface((900, 900))
    display = screen

    grass_img = pygame.image.load('my_grass_scaled.png').convert()
    grass_img.set_colorkey((0, 0, 0))
    grass_img_marked = pygame.image.load('my_grass_scaled_marked.png').convert()
    grass_img_marked.set_colorkey((0, 0, 0))

    # 450 is the half of the display width
    camera = pygame.math.Vector2(0, 0)

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
        camera_spped = 10
        if keys[pygame.K_w]:
            camera.y += camera_spped
            player.sprite.rect.y += camera_spped
        if keys[pygame.K_s]:
            camera.y += -camera_spped
            player.sprite.rect.y += -camera_spped
        if keys[pygame.K_a]:
            camera.x += camera_spped
            player.sprite.rect.x += camera_spped
        if keys[pygame.K_d]:
            camera.x += -camera_spped
            player.sprite.rect.x += -camera_spped

        for x in range(40):
            for y in range(40):
                # https://www.youtube.com/watch?v=04oQ2jOUjkU
                # x * 0.5w + y * -0.5w
                # x * 0.5h + y * 0.5h (0.5h == 0.25w)
                x1 = x * 64 + y * -64
                y1 = x * 32 + y * 32
                # y1 = x * 20 + y * 20
                # 64 offset is half of the tile width
                # это позиция левого верхнего угла картинки (не угла тайла!)
                if (x, y) == marked:
                    display.blit(grass_img_marked, (camera.x + x1, camera.y + y1))
                else:
                    display.blit(grass_img, (camera.x + x1, camera.y + y1))
                # OR!!!
                # pos = pygame.math.Vector2(x, y) * 64
                # pos = cart_to_iso(pos)
                # display.blit(grass_img, (camera.x + pos.x, camera.y + pos.y))


                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x * 16, y * 16, 16, 16), 1)

                # if (x, y) == (1, 1):
                #     # print((camera.x + x1 - 64, camera.y + y1 - 64))
                #     # 42 для центрирования по середине тайла земли
                #     # персонажи рисуются относительно низа (bottomleft) на середине тайла (34px + офсет тайла персонажа)
                #     player_sprite = Player((camera.x + x1 - 64, camera.y + y1 - 64 + 42))
                #     player.add(player_sprite)
                #     player.draw(display)

        player.update()
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
                print('mouse', pos)
                print('camera', camera)
                pos = iso_to_cart(pos - camera)
                print(round_half_up(pos[0] / 64) - 1, round_half_up(pos[1] / 64))

        # screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        # screen.blit(pygame.transform.rotozoom(display, 0, 1), (0, 0))
        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
