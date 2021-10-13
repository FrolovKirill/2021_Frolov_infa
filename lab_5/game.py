import pygame.draw as dr
import pygame.font
from random import randint

pygame.init()
pygame.font.init()

FPS = 50
START_TIME = 0
screen = pygame.display.set_mode((800, 600))
myfont = pygame.font.SysFont('calibri', 30)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

BALLS = [[0, 0, 0, 0, 0, (0, 0, 0), 0],  # Двумерный массив, отвечающий за параметры шариков.
         [0, 0, 0, 0, 0, (0, 0, 0), 0],  # Первый индекс массива отвечает за номер шарика, параметры которого указаны.
         [0, 0, 0, 0, 0, (0, 0, 0), 0],  # Первый элемент подмассива отвечает за x-координату шарика, второй за y.
         [0, 0, 0, 0, 0, (0, 0, 0), 0],  # Третий элемент массива отвечает за радиус шарика; 4 и 5 за скорость по x и y.
         [0, 0, 0, 0, 0, (0, 0, 0), 0],  # Шестой элемент массива принимает кортеж с цветом шарика в формате RGB.
         [0, 0, 0, 0, 0, (0, 0, 0), 0]]  # Седьмой элемент отвечает за время жизни. Если значение > 0, то шарик есть,
# а само значение показывает оставшееся время жизни шарика; если значение < 0, то это время до появления нового
# шарика вместо исчезшего.


def new_ball(num):
    """
    Функция заполняет массив для шарика, фактически создаёт его.
    :param num: номер шарика. от 0 до 2 - обычный шарик, от 3 до 5 - злой смайлик.
    """
    BALLS[num][0] = randint(100, 700)
    BALLS[num][1] = randint(100, 500)
    BALLS[num][2] = randint(30, 50)
    BALLS[num][3] = randint(-5, 5)
    BALLS[num][4] = randint(-5, 5)
    BALLS[num][5] = COLORS[randint(0, 5)]
    BALLS[num][6] = randint(1000, 5000)


def distance(coord1, coord2):
    """
    Находит расстояние между двумя точками.
    :param coord1: координаты первой точки.
    :param coord2: координаты второй точки.
    :return: расстояние между точками.
    """
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5


def repulse(num):
    """
    Проверяет у стенки ли шарик, и отражает его, если это так.
    :param num: номер шарика. от 0 до 2 - обычный шарик, от 3 до 5 - злой смайлик.
    """
    if BALLS[num][0] <= BALLS[num][2]:
        if num < 3:
            BALLS[num][3] = randint(1, 5)
        else:
            BALLS[num][3] = randint(25, 50)
    if BALLS[num][0] >= 800 - BALLS[num][2]:
        if num < 3:
            BALLS[num][3] = randint(-5, 1)
        else:
            BALLS[num][3] = randint(-50, -25)
    if BALLS[num][1] <= BALLS[num][2] + 30:
        if num < 3:
            BALLS[num][4] = randint(1, 5)
        else:
            BALLS[num][4] = randint(25, 50)
    if BALLS[num][1] >= 600 - BALLS[num][2]:
        if num < 3:
            BALLS[num][4] = randint(-5, 1)
        else:
            BALLS[num][4] = randint(-50, -25)


def time_check(num):
    """
    Проверяет оставшееся время жизни смайлика или время до появления нового. Также создаёт новый шарик или убирает
    старый, если подошло время.
    :param num: номер шарика. от 0 до 2 - обычный шарик, от 3 до 5 - злой смайлик.
    """
    if BALLS[num][6] > 1000 / FPS:
        BALLS[num][6] -= 1000 / FPS
    elif BALLS[num][6] < -1000 / FPS:
        BALLS[num][6] += 1000 / FPS
    elif 0 < BALLS[num][6] <= 1000 / FPS:
        BALLS[num][2] = 0
        BALLS[num][6] = randint(-1500, -800)
    else:
        new_ball(num)


def display(points):
    """
    Выводит на экран оставшееся время игры и счёт игрока.
    :param points: колличество очков, заработанных игроком.
    :return: возвращает 1, если закончилось время игры, иначе 0.
    """
    surf = myfont.render("Your score:" + str(points), True, WHITE)
    screen.blit(surf, (0, 0))
    surf = myfont.render("Time left: " + str(round((120 - pygame.time.get_ticks() / 1000) // 60)) + "m "
                         + str(round((120 - pygame.time.get_ticks() / 1000) % 60, 1)) + "s", True, WHITE)
    screen.blit(surf, (550, 0))
    return 1 if pygame.time.get_ticks() / 1000 >= 119.9 else 0


def eye(num, x, y, coef):
    """
    Функция рисует глаз злого смайлика.
    :param num: номер шарика, которому соответствует смайлик.
    :param x: х-координата центра глаза.
    :param y: y-координата центра глаза.
    :param coef: отношение радиуса глаза к радиусу смайлика.
    """
    dr.circle(screen, RED, (x, y), coef * BALLS[num][2])
    dr.circle(screen, BLACK, (x, y), coef * BALLS[num][2], 1)
    dr.circle(screen, BLACK, (x, y), 0.08 * BALLS[num][2])


def smile(num):
    """
    Функция рисует злой смайлик.
    :param num: номер шарика, от 3 до 5.
    """
    x, y = BALLS[num][0], BALLS[num][1]
    r = BALLS[num][2]
    dr.circle(screen, YELLOW, (x, y), r)
    dr.circle(screen, BLACK, (x, y), r, 1)

    eye(num, x - 0.5 * r, y - 0.25 * r, 0.2)
    eye(num, x + 0.5 * r, y - 0.25 * r, 0.16)

    dr.rect(screen, BLACK, (x - int(0.55 * r), y + int(0.4 * r), int(1.1 * r), int(0.2 * r)))

    dr.polygon(screen, BLACK, [(x - 1.04 * r, y - 0.88 * r), (x - 0.2 * r, y - 0.42 * r),
                               (x - 0.24 * r, y - 0.34 * r), (x - 1.08 * r, y - 0.8 * r)])
    dr.polygon(screen, BLACK, [(x + 0.94 * r, y - 0.71 * r), (x + 0.2 * r, y - 0.4 * r),
                               (x + 0.24 * r, y - 0.32 * r), (x + 0.98 * r, y - 0.64 * r)])


def counter(num, points):
    """
    Пересчитывает баллы при нажатии мышкой и уничтожает шарик, если попал.
    :param num: номер шарика, нажатие на который смотрят.
    :param points: кол-во уже набранных игроком очков без учёта новых.
    :return: кол-во набранных игроков очков с учётом нового нажатия мыши.
    """
    if distance(event.pos, BALLS[num][0:2]) <= BALLS[num][2]:
        if num < 3:
            points += 1
        else:
            points += 3
        BALLS[num][2] = 0
        BALLS[num][6] = randint(-1500, -800)

    return points


def user():
    """
    Позволяет игроку ввести своё имя и выводит это на экран.
    :return: имя игрока.
    """
    user_name = []
    finish = False

    while not finish:
        clock.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                finish = True
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RETURN:
                    finish = True
                elif events.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += events.unicode
        user_name = ''.join(user_name)
        surface = myfont.render("Enter your name: " + user_name, True, WHITE)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        screen.fill(BLACK)
    return user_name


def file_reading():
    """
    :return: возвращает из файла массивы с именами игроков из рейтинга и их баллами.
    """
    points = [""] * 5
    names = [""] * 5

    f = open("rating.txt", "r")
    file = f.readlines()
    for i in range(1, 6):
        string = file[i]
        pos = -1
        while string[pos] != " ":
            points[i - 1] = string[pos] + points[i - 1]
            pos -= 1
        pos = 3
        while string[pos] != ",":
            names[i - 1] = names[i - 1] + string[pos]
            pos += 1
    for i in range(5):
        points[i] = points[i].replace("\n", "")

    f.close()

    return points, names


def file_writing(points, names):
    """
    Записывает в файл новые результаты.
    :param points: массив с результатами пяти лучших игроков.
    :param names: массив с именами пяти лучших игроков.
    """
    f = open("rating.txt", "w")
    f.write("Top players: \n")

    i = 1
    boolean = True
    while i < 6 and boolean:
        if score > int(points[i - 1]):
            f.write(str(i) + ". " + username + ", score: " + str(score) + "\n")
            boolean = False
        else:
            f.write(str(i) + ". " + names[i - 1] + ", score: " + points[i - 1] + "\n")
        i += 1

    if not boolean:
        for j in range(i, 6):
            f.write(str(j) + ". " + names[j - 2] + ", score: " + points[j - 2] + "\n")

    f.close()


def results_drawing():
    """
    Выводит новый рейтинг из файла на экран.
    """
    f = open("rating.txt", "r")
    file = f.readlines()

    finish = False

    while not finish:
        clock.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                finish = True
        for i in range(6):
            surface = myfont.render(file[i].replace("\n", ""), True, WHITE)
            screen.blit(surface, (0, 30 * i))
        pygame.display.update()
        screen.fill(BLACK)

    f.close()


pygame.display.update()
clock = pygame.time.Clock()
score = 0

finished = False

for k in range(6):
    new_ball(k)
    BALLS[k][6] += randint(0, 1500)

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(6):
                    score = counter(k, score)

    for k in range(6):
        BALLS[k][0] += BALLS[k][3]
        BALLS[k][1] += BALLS[k][4]
        time_check(k)
        repulse(k)

    for k in range(3):
        dr.circle(screen, BALLS[k][5], (BALLS[k][0], BALLS[k][1]), BALLS[k][2])

    for k in range(3, 6):
        smile(k)
        BALLS[k][3] = randint(-25, 25)
        BALLS[k][4] = randint(-25, 25)

    if display(score) == 1:
        finished = True
    pygame.display.update()
    screen.fill(BLACK)

username = user()

player_scores, player_names = file_reading()

file_writing(player_scores, player_names)

results_drawing()

pygame.quit()
