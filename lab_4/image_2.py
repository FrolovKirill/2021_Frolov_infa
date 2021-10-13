import numpy as np
import pygame
from pygame.draw import polygon, aalines, ellipse, circle, arc, rect, aaline

WHITE = (255, 255, 255)
GREY_BLUE = (102, 99, 113)
BLACK = (0, 0, 0)


def head_neck_body(surface, k):
    """
        Функция рисует голову, шею и туловище чайки.
        :param surface: - объект pygame.Surface
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
    """
    ellipse(surface, WHITE, (112 * k, 120 * k, 117 * k, 55 * k))
    ellipse(surface, WHITE, (207 * k, 128 * k, 58 * k, 25 * k))
    ellipse(surface, (255, 222, 84), (278 * k, 121 * k, 46 * k, 13 * k))
    aaline(surface, BLACK, (278 * k, 127 * k), (322 * k, 127 * k))
    ellipse(surface, WHITE, (248 * k, 115 * k, 44 * k, 27 * k))
    ellipse(surface, BLACK, (271 * k, 120 * k, 10 * k, 5 * k))


def tale(surface, k):
    """
        Функция рисует хвост чайки.
        :param surface: - объект pygame.Surface
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
    """
    t = [(k * (113 - i), k * (155 - i ** 2 * 13 / 51 ** 2)) for i in range(52)]
    t += [(79 * k, 93 * k), (118 * k, 136 * k)]
    polygon(surface, WHITE, t)
    aalines(surface, BLACK, False, t)


def wings(surface, k):
    """
        Функция рисует крылья чайки.
        :param surface: - объект pygame.Surface
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
    """
    wing = pygame.Surface((400 * k, 200 * k), pygame.SRCALPHA, 32)
    track = [(k * (301 + i), k * (102 + i ** 2 * 68 / 49 ** 2)) for i in range(49, -1, -1)]
    track += [(k * (213 + i), k * (102 - (i - 69) ** 2 * 39 / 69 ** 2)) for i in range(69, -1, -1)]
    track += [(k * 213, k * 63), (k * 211, k * 61), (k * 209, k * 63), (k * 209, k * 65),
              (k * 210, k * 67), (k * 260, k * 120), (k * 290, k * 130), (k * 310, k * 170)]
    polygon(wing, WHITE, track)
    aalines(wing, BLACK, False, track)
    surface.blit(wing, (-170 * k, -50 * k))
    surface.blit(pygame.transform.rotate(wing, 15), (-220 * k, -55 * k))


def leg(a, b, k, surface):
    """
        Функция рисует одну ногу чайки.
        :param surface: - объект pygame.Surface
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
        :param a: - аргументы для смещения ног относительно друг друга в самой птице
        :param b: - аргументы для смещения ног относительно друг друга в самой птице
    """
    add_surf = pygame.Surface((50 * k, 25 * k), pygame.SRCALPHA, 32)
    ellipse(add_surf, WHITE, (0, 0, 50 * k, 25 * k))
    add_surf = pygame.transform.rotate(add_surf, -60)
    surface.blit(add_surf, (a * k, b * k))

    add_surf = pygame.Surface((54 * k, 15 * k), pygame.SRCALPHA, 32)
    ellipse(add_surf, WHITE, (0, 0, 54 * k, 14 * k))
    add_surf = pygame.transform.rotate(add_surf, -20)
    surface.blit(add_surf, ((a+23) * k, (b+40) * k))

    holst = pygame.Surface((43 * k, 49 * k), pygame.SRCALPHA, 32)
    track = [(10 * k, 12 * k), (37 * k, 2 * k), (19 * k, 16 * k),
             (41 * k, 24 * k), (22 * k, 26 * k), (31 * k, 44 * k),
             (11 * k, 28 * k), (5 * k, 47 * k), (2 * k, 20 * k)]
    polygon(holst, (255, 231, 129), track)
    aalines(holst, BLACK, False, track)
    surface.blit(holst, ((a+63) * k, (b+46) * k))


def seagull(x, y, k, orientation=1):
    """
        Функция рисует всю птицу, собирая  ее части в одном месте.
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
        :param x: - координаты левого верхнего угла большого холста, на котором рисуется вся птица
        :param y: - координаты левого верхнего угла большого холста, на котором рисуется вся птица
        :param orientation: - если 1, птица смотрит вправо, если -1 - влево
    """
    surface = pygame.Surface((335 * k, 250 * k), pygame.SRCALPHA, 32)
    head_neck_body(surface, k)
    tale(surface, k)
    wings(surface, k)
    leg(150, 146, k, surface)
    leg(130, 161, k, surface)
    screen.blit(surface if orientation == 1 else pygame.transform.flip(surface, True, False), (x, y))


def bird(x, y, k, angle=0):
    """
        Функция рисует всю птицу-галочку.
        :param k: - размер изображения, меняется от 0 до бесконечности, может быть дробным
        :param x: - координаты левого верхнего угла большого холста, на котором рисуется вся птица
        :param y: - координаты левого верхнего угла большого холста, на котором рисуется вся птица
        :param angle: - угол в градусах, на которую поворачивается птица
    """
    surf = pygame.Surface((447, 632), pygame.SRCALPHA)
    surface = pygame.Surface((86 * k, 62 * k), pygame.SRCALPHA)

    arc(surface, WHITE, (0, 0, 86 * k, 62 * k), 0, 2 * np.pi / 3, int(np.ceil(2.4 * k)))
    surf.blit(pygame.transform.rotate(surface, 30), (x - 88 * k, y - 27 * k))

    surface = pygame.Surface((86 * k, 62 * k), pygame.SRCALPHA)

    arc(surface, WHITE, (0, 0, 86 * k, 62 * k), np.pi / 3, np.pi, int(np.ceil(2.4 * k)))
    surf.blit(pygame.transform.rotate(surface, -30), (x - 18 * k, y - 26 * k))

    surf2 = pygame.Surface((894, 1264), pygame.SRCALPHA)
    surf2.blit(surf, (447 - x, 632 - y))
    surf2 = pygame.transform.rotate(surf2, angle)
    x2, y2 = surf2.get_size()
    screen.blit(surf2, (x - x2 / 2, y - y2 / 2))


def fish(x, y):
    """
        Функция рисует рыбу.
        :param x:  - координаты левого верхнего угла хвоста
        :param y: - координаты левого верхнего угла хвоста
    """
    par5 = [(x + i, y + 7 - np.ceil((i - 35) ** 2 / 175)) for i in range(35, 0, -2)]
    par4 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 19 / 56 ** 2)) for i in range(91, 34, -2)]
    par3 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 22 / 46 ** 2)) for i in range(137, 90, -2)]
    par2 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 11 / 51 ** 2)) for i in range(86, 137, 2)]
    par1 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 14 / 51 ** 2)) for i in range(35, 86, 2)]
    track = [(x, y), (x + 6, y + 26)] + par1 + par2 + par3 + par4 + par5
    polygon(screen, (69, 137, 148), track)
    aalines(screen, (25, 25, 25), True, track)

    circle(screen, (0, 50, 190), (x + 113, y + 7), 6)
    circle(screen, (1, 62, 84), (x + 113, y + 8), 3)
    ellipse(screen, (90, 145, 175), (x + 112, y + 7, -3, 2))

    polygon(screen, GREY_BLUE, [(x + 54, y + 17), (x + 43, y + 27), (x + 64, y + 30), (x + 62, y + 19)])
    aalines(screen, (0, 25, 25), True, [(x + 54, y + 17), (x + 43, y + 27), (x + 64, y + 30), (x + 62, y + 19)])

    track = [(x + 76, y - 12), (x + 58, y - 25), (x + 93, y - 21), (x + 94, y - 20),
             (x + 95, y - 19), (x + 96, y - 19), (x + 97, y - 18), (x + 98, y - 17),
             (x + 98, y - 16), (x + 97, y - 15), (x + 96, y - 14), (x + 95, y - 13), (x + 94, y - 12)]
    polygon(screen, GREY_BLUE, track)
    aalines(screen, (0, 25, 25), True, track)

    polygon(screen, GREY_BLUE, [(x + 107, y + 20), (x + 110, y + 38), (x + 125, y + 28), (x + 113, y + 18)])
    aalines(screen, (0, 25, 25), True, [(x + 107, y + 20), (x + 110, y + 38), (x + 125, y + 28), (x + 113, y + 18)])


pygame.init()

FPS = 30
screen = pygame.display.set_mode((447, 632))
screen.fill((0, 102, 129))
pygame.display.update()

rect(screen, (255, 154, 84), (0, 0, 447, 316))
rect(screen, (223, 136, 172), (0, 0, 447, 246))
rect(screen, (206, 136, 223), (0, 0, 447, 158))
rect(screen, (142, 95, 212), (0, 0, 447, 102))
rect(screen, (27, 27, 121), (0, 0, 447, 65))

birds = [(260, 120, 0.9, 2), (100, 30, 0.9, 15), (140, 250, 0.9, -15), (100, 120, 0.3, -15), (320, 230, 0.3, -15),
         (120, 200, 0.3, -15), (249, 132, 0.3, 15), (289, 193, 0.3, 15), (145, 150, 0.3, 15), (228, 188, 0.3, 15),
         (122, 72, 0.3, 15), (230, 90, 0.3, 0), (250, 40, 0.3, 0), (290, 80, 0.3, 0), (400, 140, 0.5, 0),
         (390, 190, 0.5, 0), (430, 210, 0.5, 0), (350, 170, 0.5, 0)]

for j in birds:
    bird(j[0], j[1], j[2], j[3])

fish(270, 570)
fish(40, 585)
fish(290, 480)

seagull(-5, 330, 1)
seagull(170, 350, 0.25)
seagull(300, 330, 0.4, -1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
