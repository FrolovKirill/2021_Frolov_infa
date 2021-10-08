import numpy as np
import pygame
import pygame.draw as dr


def seagull(x, y, k=1.0, orientation=1):
    surface = pygame.Surface((335 * k, 250 * k), pygame.SRCALPHA, 32)

    dr.ellipse(surface, (255, 255, 255), (int(112 * k), int(120 * k), int(117 * k), int(55 * k)))
    dr.ellipse(surface, (255, 255, 255), (int(207 * k), int(128 * k), int(58 * k), int(25 * k)))
    dr.ellipse(surface, (255, 222, 84), (int(278 * k), int(121 * k), int(46 * k), int(13 * k)))
    dr.aaline(surface, (0, 0, 0), (int(278 * k), int(127 * k)), (int(322 * k), int(127 * k)))
    dr.ellipse(surface, (255, 255, 255), (int(248 * k), int(115 * k), int(44 * k), int(27 * k)))
    dr.ellipse(surface, (0, 0, 0), (int(271 * k), int(120 * k), int(10 * k), int(5 * k)))

    add_surf = pygame.Surface((50 * k, 25 * k), pygame.SRCALPHA, 32)
    dr.ellipse(add_surf, (255, 255, 255), (0, 0, int(50 * k), int(25 * k)))
    add_surf = pygame.transform.rotate(add_surf, -60)
    surface.blit(add_surf, (140 * k, 151 * k))

    add_surf = pygame.Surface((40 * k, 20 * k), pygame.SRCALPHA, 32)
    dr.ellipse(add_surf, (255, 255, 255), (0, 0, int(40 * k), int(20 * k)))
    add_surf = pygame.transform.rotate(add_surf, -60)
    surface.blit(add_surf, (165 * k, 154 * k))

    add_surf = pygame.Surface((54 * k, 15 * k), pygame.SRCALPHA, 32)
    dr.ellipse(add_surf, (255, 255, 255), (0, 0, int(54 * k), int(12 * k)))
    add_surf = pygame.transform.rotate(add_surf, -20)
    surface.blit(add_surf, (163 * k, 191 * k))

    add_surf = pygame.Surface((54 * k, 15 * k), pygame.SRCALPHA, 32)
    dr.ellipse(add_surf, (255, 255, 255), (0, 0, int(54 * k), int(12 * k)))
    add_surf = pygame.transform.rotate(add_surf, -20)
    surface.blit(add_surf, (177 * k, 180 * k))

    tale = [(int(k * (113 - i)), int(k * (155 - i ** 2 * 13 / 51 ** 2))) for i in range(52)]
    tale += [(int(79 * k), int(93 * k)), (int(118 * k), int(136 * k))]
    dr.polygon(surface, (255, 255, 255), tale)
    dr.aalines(surface, (0, 0, 0), False, tale)

    wings = pygame.Surface((400 * k, 200 * k), pygame.SRCALPHA, 32)
    track = [(int(k * (301 + i)), int(k * (102 + i ** 2 * 68 / 49 ** 2))) for i in range(49, -1, -1)]
    track += [(int(k * (213 + i)), int(k * (102 - (i - 69) ** 2 * 39 / 69 ** 2))) for i in range(69, -1, -1)]
    track += [(int(k * 213), int(k * 63)), (int(k * 211), int(k * 61)), (int(k * 209), int(k * 63)),
              (int(k * 209), int(k * 65)), (int(k * 210), int(k * 67))]
    track += [(int(k * 260), int(k * 120)), (int(k * 290), int(k * 130)), (int(k * 310), int(k * 170))]
    dr.polygon(wings, (255, 255, 255), track)
    dr.aalines(wings, (0, 0, 0), False, track)
    surface.blit(wings, (-170 * k, -50 * k))
    surface.blit(pygame.transform.rotate(wings, 15), (-220 * k, -55 * k))

    leg = pygame.Surface((43 * k, 49 * k), pygame.SRCALPHA, 32)
    track = [(int(10 * k), int(12 * k)), (int(37 * k), int(2 * k)), (int(19 * k), int(16 * k))]
    track += [(int(41 * k), int(24 * k)), (int(22 * k), int(26 * k)), (int(31 * k), int(44 * k))]
    track += [(int(11 * k), int(28 * k)), (int(5 * k), int(47 * k)), (int(2 * k), int(20 * k))]
    dr.polygon(leg, (255, 231, 129), track)
    dr.aalines(leg, (0, 0, 0), False, track)
    surface.blit(leg, (218 * k, 187 * k))
    surface.blit(leg, (205 * k, 198 * k))

    screen.blit(surface if orientation == 1 else pygame.transform.flip(surface, True, False), (x, y))


def bird(x, y, k, angle=0):
    surf = pygame.Surface((447, 632), pygame.SRCALPHA, 32)
    surface = pygame.Surface((86 * k, 62 * k), pygame.SRCALPHA, 32)

    dr.arc(surface, (255, 255, 255), (0, 0, int(86 * k), int(62 * k)), 0, 2 * np.pi / 3, int(np.ceil(2.4 * k)))
    surf.blit(pygame.transform.rotate(surface, 30), (x - 88 * k, y - 27 * k))

    surface = pygame.Surface((86 * k, 62 * k), pygame.SRCALPHA, 32)

    dr.arc(surface, (255, 255, 255), (0, 0, int(86 * k), int(62 * k)), np.pi / 3, np.pi, int(np.ceil(2.4 * k)))
    surf.blit(pygame.transform.rotate(surface, -30), (x - 18 * k, y - 26 * k))

    surf2 = pygame.Surface((894, 1264), pygame.SRCALPHA)
    surf2.blit(surf, (447 - x, 632 - y))
    surf2 = pygame.transform.rotate(surf2, angle)
    x2, y2 = surf2.get_size()
    screen.blit(surf2, (x - x2 / 2, y - y2 / 2))


def fish(x, y):
    par5 = [(x + i, y + 7 - np.floor((i - 35) ** 2 / 175)) for i in range(35, -1, -1)]
    par4 = [(x + i, y - 12 + np.ceil((i - 91) ** 2 * 19 / 56 ** 2)) for i in range(91, 34, -1)]
    par3 = [(x + i, y - 12 + np.ceil((i - 91) ** 2 * 22 / 46 ** 2)) for i in range(137, 90, -1)]
    par2 = [(x + i, y + 21 - np.ceil((i - 86) ** 2 * 11 / 51 ** 2)) for i in range(86, 138)]
    par1 = [(x + i, y + 21 - np.ceil((i - 86) ** 2 * 14 / 51 ** 2)) for i in range(35, 87)]
    track = [(x, y), (x + 6, y + 26)] + par1 + par2 + par3 + par4 + par5
    dr.polygon(screen, (69, 137, 148), track)

    par5 = [(x + i, y + 7 - np.ceil((i - 35) ** 2 / 175)) for i in range(35, 0, -2)]
    par4 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 19 / 56 ** 2)) for i in range(91, 34, -2)]
    par3 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 22 / 46 ** 2)) for i in range(137, 90, -2)]
    par2 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 11 / 51 ** 2)) for i in range(86, 137, 2)]
    par1 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 14 / 51 ** 2)) for i in range(35, 86, 2)]
    track = [(x, y), (x + 6, y + 26)] + par1 + par2 + par3 + par4 + par5
    dr.aalines(screen, (25, 25, 25), True, track)

    par5 = [(x + i, y + 7 - np.ceil((i - 35) ** 2 / 175)) for i in range(34, -1, -2)]
    par4 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 19 / 56 ** 2)) for i in range(90, 35, -2)]
    par3 = [(x + i, y - 12 + np.floor((i - 91) ** 2 * 22 / 46 ** 2)) for i in range(136, 91, -2)]
    par2 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 11 / 51 ** 2)) for i in range(87, 138, 2)]
    par1 = [(x + i, y + 21 - np.floor((i - 86) ** 2 * 14 / 51 ** 2)) for i in range(36, 87, 2)]
    track = [(x, y), (x + 6, y + 26)] + par1 + par2 + par3 + par4 + par5
    dr.aalines(screen, (25, 25, 25), True, track)

    dr.circle(screen, (0, 50, 190), (x + 113, y + 7), 6)
    dr.circle(screen, (1, 62, 84), (x + 113, y + 8), 3)
    dr.ellipse(screen, (90, 145, 175), (x + 112, y + 7, -3, 2))

    dr.polygon(screen, (102, 99, 113), [(x + 54, y + 17), (x + 43, y + 27), (x + 64, y + 30), (x + 62, y + 19)])
    dr.aalines(screen, (0, 25, 25), True, [(x + 54, y + 17), (x + 43, y + 27), (x + 64, y + 30), (x + 62, y + 19)])

    track = [(x + 76, y - 12), (x + 58, y - 25), (x + 93, y - 21), (x + 94, y - 20),
             (x + 95, y - 19), (x + 96, y - 19), (x + 97, y - 18), (x + 98, y - 17),
             (x + 98, y - 16), (x + 97, y - 15), (x + 96, y - 14), (x + 95, y - 13), (x + 94, y - 12)]
    dr.polygon(screen, (102, 99, 113), track)
    dr.aalines(screen, (0, 25, 25), True, track)

    dr.polygon(screen, (102, 99, 113), [(x + 107, y + 20), (x + 110, y + 38), (x + 125, y + 28), (x + 113, y + 18)])
    dr.aalines(screen, (0, 25, 25), True, [(x + 107, y + 20), (x + 110, y + 38), (x + 125, y + 28), (x + 113, y + 18)])


pygame.init()

FPS = 30
screen = pygame.display.set_mode((447, 632))
screen.fill((0, 102, 129))
pygame.display.update()

dr.rect(screen, (255, 154, 84), (0, 0, 447, 316))
dr.rect(screen, (223, 136, 172), (0, 0, 447, 246))
dr.rect(screen, (206, 136, 223), (0, 0, 447, 158))
dr.rect(screen, (142, 95, 212), (0, 0, 447, 102))
dr.rect(screen, (27, 27, 121), (0, 0, 447, 65))

birds = [(260, 120, 0.9, 2), (100, 30, 0.9, 15), (140, 250, 0.9, -15), (100, 120, 0.3, -15), (320, 230, 0.3, -15),
         (120, 200, 0.3, -15), (249, 132, 0.3, 15), (289, 193, 0.3, 15), (145, 150, 0.3, 15), (228, 188, 0.3, 15),
         (122, 72, 0.3, 15), (230, 90, 0.3, 0), (250, 40, 0.3, 0), (290, 80, 0.3, 0), (400, 140, 0.5, 0),
         (390, 190, 0.5, 0), (430, 210, 0.5, 0), (350, 170, 0.5, 0)]

for j in birds:
    bird(j[0], j[1], j[2], j[3])

fish(270, 570)
fish(40, 585)
fish(290, 480)

seagull(-5, 330)
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
