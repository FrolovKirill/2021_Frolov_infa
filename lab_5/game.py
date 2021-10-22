import pygame.draw as dr
import pygame.font
from random import randint

pygame.init()
pygame.font.init()

FPS = 50
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


def start():
    """
    Функция рисует кнопку START и ожидает её нажатия.
    :return: возвращает время начала самой игры.
    """
    finish = False

    while not finish:
        clock.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                finish = True
            else:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    if 350 < events.pos[0] < 450 and 285 < events.pos[1] < 315:
                        finish = True

        dr.rect(screen, BLUE, (350, 285, 100, 30), 2)
        surface = myfont.render("START", True, RED)
        screen.blit(surface, (363, 288))
        pygame.display.update()
        screen.fill(BLACK)

    return pygame.time.get_ticks()


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
    BALLS[num][6] = randint(2000, 5000)


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
            BALLS[num][3] = randint(5, 10)
    if BALLS[num][0] >= 800 - BALLS[num][2]:
        if num < 3:
            BALLS[num][3] = randint(-5, 1)
        else:
            BALLS[num][3] = randint(-10, -5)
    if BALLS[num][1] <= BALLS[num][2] + 30:
        if num < 3:
            BALLS[num][4] = randint(1, 5)
        else:
            BALLS[num][4] = randint(5, 10)
    if BALLS[num][1] >= 600 - BALLS[num][2]:
        if num < 3:
            BALLS[num][4] = randint(-5, 1)
        else:
            BALLS[num][4] = randint(-10, -5)


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
    time = pygame.time.get_ticks() - START_TIME

    surf = myfont.render("Your score:" + str(points), True, WHITE)
    screen.blit(surf, (0, 0))
    surf = myfont.render("Time left: " + str(round((120 - time / 1000) // 60)) + "m "
                         + str(round((120 - time / 1000) % 60, 1)) + "s", True, WHITE)
    screen.blit(surf, (550, 0))
    return 1 if time / 1000 >= 119.9 else 0


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


def balls_draw(num):
    """
    Функция отрисовывает все шары, двигает их координы, проверяет отражение от стенок, устанавливает скорости
    смайликам. :param num: номер итерации цикла в основной программе. Нужен, чтобы менять направление движения
    смайликов раз в 15 итераций.
    """
    for i in range(6):
        repulse(i)
        BALLS[i][0] += BALLS[i][3]
        BALLS[i][1] += BALLS[i][4]
        time_check(i)

    for i in range(3):
        dr.circle(screen, BALLS[i][5], (BALLS[i][0], BALLS[i][1]), BALLS[i][2])

    for i in range(3, 6):
        smile(i)
        if (num + 3 * i) % 15 == 0:  # (num + 3 * i), а не num, чтобы смайлики в разное время меняли свои траектории.
            direction = randint(-1000, 1000)
            if direction != 0:
                BALLS[i][3] = randint(5, 10) * int(direction / abs(direction))
            else:
                BALLS[i][3] = 0

            direction = randint(-1000, 1000)
            if direction != 0:
                BALLS[i][4] = randint(5, 10) * int(direction / abs(direction))
            else:
                BALLS[i][4] = 0


def snitch(x, y, vx, vy):
    """
    Рисует снитч, меняет его координаты и отражает от стенок. Если его поймать, то получешь 50 очков.
    :param x: координата левого верхнего угла снитча по оси x.
    :param y: координата левого верхнего угла снитча по оси y.
    :param vx: скорость снитча по оси x.
    :param vy: скорость снитча по оси y.
    :return: возвращает новые значения координат и скоростей.
    """
    if x <= 0:
        vx = randint(20, 35)
    if x >= 720:
        vx = randint(-35, -20)
    if y <= 0:
        vy = randint(20, 35)
    if y >= 560:
        vy = randint(-35, -20)

    x = x + vx
    y = y + vy
    snitch_surf = pygame.image.load("snitch.png")
    snitch_surf = pygame.transform.scale(snitch_surf, (100, 50))
    screen.blit(snitch_surf, (x, y))

    return x, y, vx, vy


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
        surface = myfont.render("Enter your name", True, WHITE)
        screen.blit(surface, (300, 250))
        surface = myfont.render(user_name, True, WHITE)
        screen.blit(surface, (400 - 6.4 * len(user_name), 285))
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

START_TIME = start()

score = 0

finished = False

for k in range(6):
    new_ball(k)
    BALLS[k][6] += randint(-1000, 1500)

x_snitch = randint(0, 700)
y_snitch = randint(0, 500)
Vx_snitch = randint(20, 35)
Vy_snitch = randint(20, 35)

snitch_is_alive = 1
count = 1  # Переменная считает, какой раз запускается цикл.
# Нужна для того, чтобы злые смайлики меняли траекторию раз в 15 итераций цикла.

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(6):
                    score = counter(k, score)

                if x_snitch < event.pos[0] < x_snitch + 100 and y_snitch < event.pos[1] < y_snitch + 50 \
                        and snitch_is_alive:
                    score += 50
                    snitch_is_alive = 0

    balls_draw(count)

    if snitch_is_alive:
        x_snitch, y_snitch, Vx_snitch, Vy_snitch = snitch(x_snitch, y_snitch, Vx_snitch, Vy_snitch)

    if display(score) == 1:
        finished = True

    pygame.display.update()
    screen.fill(BLACK)

    count += 1

username = user()

player_scores, player_names = file_reading()

file_writing(player_scores, player_names)

results_drawing()

pygame.quit()
