import math
import pygame.draw as dr
import pygame.key as key
import pygame.font
from time import sleep
from random import choice
from random import randint

FPS = 30

pygame.init()
pygame.font.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

myfont = pygame.font.SysFont('calibri', 30)

"""
Управление в игре.
Движение такнка можно осуществлять как клавишами A и D, так и стрелочками. 
При зажатии левой кнопки мыши происходит "зарядка" пушки, и при отпускании клавишы происходит выстрел шарами.
При единоразовом нажатии правой кнопкой происходит выстрел ракетой.
У такнка 3 жизни, при потере всех трёх игра заканчивается. В одной жизни 100 единиц здоровья,
одно попадание бомбы отнимает 10 единиц здоровья.
"""


def distance(coord1, coord2):
    """
    Находит расстояние между двумя точками.
    :param coord1: координаты первой точки.
    :param coord2: координаты второй точки.
    :return: расстояние между точками.
    """
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5


def explosion(obj):
    """
    Начинает взрыв объекта(ракеты или бомбы).
    :param obj: объект, начинающий взрываться.
    """
    obj.vx = obj.vy = 0
    obj.explosion_time -= 1


class Bullet:
    """
    Класс снарядов, вылетающих из пушки.
    """

    def __init__(self, screen, x, y):
        """
        Конструктор класса Bullet.
        :param screen: экран, на котором рисуются снаряды.
        :param x: начальная x-координата снаряда, вылетающего из пушки.
        :param y: начальная y-координата снаряда, вылетающего из пушки.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def move(self):
        """
        Переместить снаряд по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения.
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.x += self.vx
        self.y += self.vy

    def hittest(self, obj, self_width):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        :param obj: объекти класса Target.
        :param self_width: "ширина объекта", для шариков - радиус, для ракеты - ширина.
        :return: True - если произошло поражение цели, False - иначе.
        """
        if distance((self.x, self.y), (obj.x, obj.y)) <= self_width + obj.r:
            return True
        else:
            return False

    def draw(self):
        """
        Метод, рисующий снаряды. Переопределяется в дочерних классах снарядов.
        """
        pass


class Ball(Bullet):
    def __init__(self, screen, x, y):
        """
        Конструктор класса Ball.
        :param screen: экран, на котором рисуются мячи.
        :param x: начальная x-координата мяча, вылетающего из пушки.
        :param y: начальная y-координата мяча, вылетающего из пушки.
        """
        super().__init__(screen, x, y)
        self.r = 15
        self.live = 30
        self.color = choice(GAME_COLORS)

    def repulse(self):
        """
        Отражает мячи от стенок с потерей энергии.
        :param self: объект класса Ball.
        """
        if self.x <= self.r or self.x >= 800 - self.r:
            self.vx = -0.65 * self.vx
        if self.x <= self.r:
            self.x = self.r
        elif self.x >= 800 - self.r:
            self.x = 800 - self.r
        if self.y >= 553 - self.r:
            self.vy = -0.65 * self.vy
            self.vx = 0.65 * self.vx
            self.y = 553 - self.r

        if self.vx ** 2 < 1:
            self.vx = 0

        if self.vy ** 2 < 1:
            self.vy = 0

    def move(self):
        """
        Переместить снаряд по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения.
        self.x и self.y с учетом скоростей self.vx и self.vy. Также учитывает гравитацию.
        """
        self.vy += 1.5
        super().move()
        self.repulse()
        if self.vx == self.vy == 0:
            self.live -= 1

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране.
        """
        dr.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        dr.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )


class Rocket(Bullet):
    def __init__(self, screen, x, y):
        """
        Конструктор класса Rocket.
        :param screen: экран, на котором рисуются ракеты.
        :param x: начальная x-координата ракеты, вылетающей из пушки.
        :param y: начальная y-координата ракеты, вылетающей из пушки.
        """
        super().__init__(screen, x, y)
        self.angle = 0
        self.explosion_time = 30

    def move(self):
        """
        Переместить ракету по прошествии единицы времени.
        Метод описывает перемещение ракеты за один кадр перерисовки. То есть, обновляет значения.
        self.x и self.y с учетом скоростей self.vx и self.vy. При вылете заьгрницы экрана ракета уничтожается.
        """
        super().move()
        if self.x > 820 or self.x < -20 or self.y < -20:
            self.explosion_time = 0

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране. В случае, если ракета уже взрывается,
        на экране появляются круги взрыва.
        """
        if self.explosion_time == 30:
            rotate_matrix = [[math.cos(self.angle), -math.sin(self.angle)],
                             [math.sin(self.angle), math.cos(self.angle)]]
            points = [[-17.0, -7.0], [18.0, -7.0], [18.0, 7.0], [-17.0, 7.0]]
            for i in range(4):
                x = points[i][0]
                y = points[i][1]
                points[i][0] = x * rotate_matrix[0][0] + y * rotate_matrix[0][1]
                points[i][0] += self.x

                points[i][1] = x * rotate_matrix[1][0] + y * rotate_matrix[1][1]
                points[i][1] += self.y

            pygame.draw.polygon(self.screen, BLUE, points)

            points = [[18.0, -10.0], [30.0, 0.0], [18.0, 10.0]]
            for i in range(3):
                x = points[i][0]
                y = points[i][1]
                points[i][0] = x * rotate_matrix[0][0] + y * rotate_matrix[0][1]
                points[i][0] += self.x

                points[i][1] = x * rotate_matrix[1][0] + y * rotate_matrix[1][1]
                points[i][1] += self.y

            pygame.draw.polygon(self.screen, RED, points)
            pygame.draw.aalines(self.screen, RED, True, points)

            points = [[-17.0, -7.0], [-34.0, -14.0], [-24.0, -5.0], [-37.0, 0.0],
                      [-24.0, 5.0], [-34.0, 14.0], [-17.0, 7.0]]
            for i in range(7):
                x = points[i][0]
                y = points[i][1]
                points[i][0] = x * rotate_matrix[0][0] + y * rotate_matrix[0][1]
                points[i][0] += self.x

                points[i][1] = x * rotate_matrix[1][0] + y * rotate_matrix[1][1]
                points[i][1] += self.y

            pygame.draw.polygon(self.screen, (255, 150, 0), points)
            pygame.draw.aalines(self.screen, (255, 150, 0), True, points)

            points = [[-17.0, -7.0], [18.0, -7.0], [18.0, -10.0], [30.0, 0.0], [18.0, 10.0], [18.0, 7.0], [-17.0, 7.0],
                      [-34.0, 14.0], [-24.0, 5.0], [-37.0, 0.0], [-24.0, -5.0], [-34.0, -14.0]]
            for i in range(12):
                x = points[i][0]
                y = points[i][1]
                points[i][0] = x * rotate_matrix[0][0] + y * rotate_matrix[0][1]
                points[i][0] += self.x

                points[i][1] = x * rotate_matrix[1][0] + y * rotate_matrix[1][1]
                points[i][1] += self.y
            pygame.draw.aalines(self.screen, BLACK, True, points)
        else:
            for i in range(3):
                dr.circle(
                    self.screen,
                    (255, 255 - 127 * i, 0),
                    (self.x, self.y),
                    (30 - self.explosion_time) / 3 * (3 - i)
                )
            self.explosion_time -= 1


class Tank:
    """
    Класс танка.
    """

    def __init__(self, screen):
        """
        Конструктор класса Tank.
        :param screen: экран, на котором рисуется пушка.
        """
        self.screen = screen
        self.power = 5
        self.f2_on = 0
        self.angle = 0
        self.color = GREY
        self.location = [50, 520]
        self.health = 100
        self.lives = 3
        self.moving = False

    def move(self):
        """
        Метод, отвечающий за перемещение танка по земле. Перемещение осуществляется клавишами A и D или стрелочками.
        """
        keys = key.get_pressed()
        if self.location[0] < 765 and self.moving and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.location[0] += 8
        if self.location[0] > 35 and self.moving and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.location[0] -= 8

    def loading_start(self):
        """
        Начало "заряжания" пушки.
        """
        self.f2_on = 1

    def loading_end(self, event):
        """
        Выстрел снарядом.
        Происходит при отпускании кнопки мыши. Запускается шарик при нажатиии левой кнопокй мыши,
        ракета - при нажатии правой. Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        :param event: событие отпускания клавиши мыши.
        """
        if event.button == 1:
            new_bullet = Ball(self.screen, 60 * math.cos(self.angle) + self.location[0],
                              60 * math.sin(self.angle) + self.location[1])
            new_bullet.vx = self.power * math.cos(self.angle)
            new_bullet.vy = self.power * math.sin(self.angle)
            new_bullet.x -= new_bullet.vx
            new_bullet.y -= new_bullet.vy
            self.f2_on = 0
            self.power = 5
            return new_bullet
        elif event.button == 3:
            new_bullet = Rocket(self.screen, 80 * math.cos(self.angle) + self.location[0],
                                80 * math.sin(self.angle) + self.location[1])
            new_bullet.vx = 75 * math.cos(self.angle)
            new_bullet.vy = 75 * math.sin(self.angle)
            new_bullet.x -= new_bullet.vx
            new_bullet.y -= new_bullet.vy
            new_bullet.angle = self.angle
            return new_bullet

    def targetting(self, event):
        """
        Прицеливание, происходящее при движении мыши.
        :param event: событие движения мыши.
        """
        if event:
            self.angle = math.atan2((event.pos[1] - self.location[1]), (event.pos[0] - self.location[0]))
            if 0 < self.angle <= math.pi / 2:
                self.angle = 0
            elif math.pi / 2 < self.angle <= math.pi:
                self.angle = math.pi

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране.
        """
        rotate_matrix = [[math.cos(self.angle), -math.sin(self.angle)], [math.sin(self.angle), math.cos(self.angle)]]

        points = [[0.0, -3.0], [60.0, -3.0], [60.0, 3.0], [0.0, 3.0]]
        for i in range(4):
            x = points[i][0]
            y = points[i][1]
            for j in range(2):
                points[i][j] = x * rotate_matrix[j][0] + y * rotate_matrix[j][1]
                points[i][j] += self.location[j]

        dr.polygon(self.screen, self.color, points)
        dr.aalines(self.screen, BLACK, True, points)

        dr.rect(self.screen, (0, 40, 0), (self.location[0] - 15, self.location[1] - 4, 30, 10))
        dr.rect(self.screen, BLACK, (self.location[0] - 15, self.location[1] - 4, 30, 10), 1)

        points = [[-15, 6], [-35, 15], [-35, 25], [35, 25], [35, 15], [15, 6]]
        for i in range(6):
            points[i][0] += self.location[0]
            points[i][1] += self.location[1]
        dr.polygon(self.screen, (0, 40, 0), points)
        dr.aalines(self.screen, BLACK, True, points)

        dr.circle(self.screen, BLACK, (self.location[0] - 15, self.location[1] + 25), 8)
        dr.circle(self.screen, BLACK, (self.location[0] + 15, self.location[1] + 25), 8)

    def power_up(self):
        """
        Процесс "заряжания" пушки.
        """
        if self.f2_on:
            if self.power < 60:
                self.power += 1
            self.color = (255, 255 - 255 / 55 * (self.power - 5), 150 - 150 / 55 * (self.power - 5))
        else:
            self.color = (255, 255, 150)


class Target:
    """
    Класс мишеней.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Конструктор класса Target.
        :param screen: экран, на котором рисуются цели.
        """
        self.screen = screen
        self.points = 0
        self.x = randint(36, 765)
        self.y = randint(35, 425)
        self.vx = randint(-10, 11)
        self.vy = randint(-10, 11)
        self.r = randint(5, 36)
        self.bomb_time_waiting = randint(20, 91)

    def move(self):
        """
        Переместить мишень по прошествии единицы времени.
        """
        self.x += self.vx
        self.y += self.vy
        self.repulse()

    def repulse(self):
        """
        Отражает мишени от границ области, в которой они могут находиться.
        :param self: объект класса Target
        """
        if self.x <= self.r or self.x >= 800 - self.r:
            self.vx = -self.vx
        if self.x <= self.r:
            self.x = self.r
        elif self.x >= 800 - self.r:
            self.x = 800 - self.r

        if self.y <= self.r or self.y >= 460 - self.r:
            self.vy = -self.vy
        if self.y <= self.r:
            self.y = self.r
        elif self.y >= 460 - self.r:
            self.y = 460 - self.r

    def hit(self, points=1):
        """
        Попадание шарика в мишень.
        """
        self.points += points


class Ball_Target(Target):
    def __init__(self, screen):
        """
        Конструктор класса Ball_Target.
        :param screen: экран, на котором рисуются мишени.
        """
        super().__init__(screen)
        self.color = choice([RED, BLUE, YELLOW])

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране.
        """
        dr.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Smile_Target(Target):
    def __init__(self, screen):
        """
        Конструктор класса Smile_Target.
        :param screen: экран, на котором рисуются снаряды.
        """
        super().__init__(screen)
        self.direction_time = 35
        self.vx = choice([-10, -9, -8, -7, -6, 6, 7, 8, 9, 10])
        self.vy = choice([-10, -9, -8, -7, -6, 6, 7, 8, 9, 10])

    def move(self):
        """
        Метод вырисовывает объект этого класса на экране. Раз в 1.17 секунды этот тип мишеней случайно
        меняет направление своего движения.
        """
        super().move()
        if self.direction_time <= 0:
            self.vx = choice([-10, -9, -8, -7, -6, 6, 7, 8, 9, 10])
            self.vy = choice([-10, -9, -8, -7, -6, 6, 7, 8, 9, 10])
            self.direction_time = 35

    def eye(self, x, y, coef):
        """
        Функция рисует глаз злого смайлика.
        :param x: х-координата центра глаза.
        :param y: y-координата центра глаза.
        :param coef: отношение радиуса глаза к радиусу смайлика.
        """
        dr.circle(self.screen, RED, (x, y), coef * self.r)
        dr.circle(self.screen, BLACK, (x, y), coef * self.r, 1)
        dr.circle(self.screen, BLACK, (x, y), 0.08 * self.r)

    def draw(self):
        """
        Метод рисует злой смайлик.
        """
        dr.circle(self.screen, YELLOW, (self.x, self.y), self.r)
        dr.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)

        self.eye(self.x - 0.5 * self.r, self.y - 0.25 * self.r, 0.2)
        self.eye(self.x + 0.5 * self.r, self.y - 0.25 * self.r, 0.16)

        dr.rect(self.screen, BLACK, (self.x - int(0.55 * self.r), self.y + int(0.4 * self.r), int(1.1 * self.r),
                                     int(0.2 * self.r)))

        points = [[-1.04 * self.r, -0.88 * self.r], [-0.2 * self.r, -0.42 * self.r], [-0.24 * self.r, -0.34 * self.r],
                  [-1.08 * self.r, -0.8 * self.r]]
        for i in range(4):
            points[i][0] += self.x
            points[i][1] += self.y
        dr.polygon(self.screen, BLACK, points)

        points = [[0.94 * self.r, -0.71 * self.r], [0.2 * self.r, -0.4 * self.r], [0.24 * self.r, -0.32 * self.r],
                  [0.98 * self.r, -0.64 * self.r]]
        for i in range(4):
            points[i][0] += self.x
            points[i][1] += self.y
        dr.polygon(self.screen, BLACK, points)
        dr.polygon(self.screen, BLACK, points)


class Bomb:
    def __init__(self, screen, x, y):
        """
        Конструктор класса Bomb.
        :param screen: экран, на котором появляются бомбы.
        :param x: начальная x-координата бомбы.
        :param y: начальная y-координата бомбы.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = randint(-8, 9)
        self.vy = randint(-8, 1)
        self.r = 10
        self.explosion_time = 16

    def move(self):
        """
        Переместить бомбу по прошествии единицы времени.
        Метод описывает перемещение бомбы за один кадр перерисовки. То есть, обновляет значения.
        self.x и self.y с учетом скоростей self.vx и self.vy, также учитывает гравитацию.
        """
        self.vy += 1
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране. В случае, если бомба уже взрывается,
        на экране появляются круги взрыва.
        """
        if self.explosion_time == 16:
            dr.circle(self.screen, (50, 50, 50), (self.x, self.y), self.r)
        else:
            for i in range(3):
                dr.circle(
                    self.screen,
                    (255, 255 - 127 * i, 0),
                    (self.x, self.y),
                    (16 - self.explosion_time) / 3 * (3 - i)
                )
            self.explosion_time -= 1


class Game:
    """
    Класс игры.
    """

    def __init__(self):
        """
        Конструктор класса Game.
        """
        self.points = 0
        self.finish = 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bullet_count = 0
        self.balls = []
        self.rockets = []
        self.ball_targets = []
        self.smile_targets = []
        self.targets = []
        self.bombs = []
        self.tank = Tank(self.screen)

    def draw(self):
        """
        Метод вырисовывает все действующие объекты на экране.
        """
        self.screen.fill(WHITE)
        self.tank.draw()
        for b in self.bombs[:]:
            if b.explosion_time > 0:
                b.draw()
            else:
                self.bombs.remove(b)
        for t in self.targets:
            t.draw()
        for b in self.balls[:]:
            if b.live > 0:
                b.draw()
            else:
                self.balls.remove(b)
        for r in self.rockets[:]:
            if r.explosion_time > 0:
                r.draw()
            else:
                self.rockets.remove(r)

        surf = myfont.render("Score:" + str(self.points), True, BLACK)
        self.screen.blit(surf, (30, 0))
        surf = myfont.render("Health:" + str(self.tank.health), True, BLACK)
        self.screen.blit(surf, (230, 0))
        surf = myfont.render("Lives:", True, BLACK)
        self.screen.blit(surf, (450, 0))
        for i in range(self.tank.lives):
            dr.circle(self.screen, RED, (540 + 25 * i, 15), 10)
            dr.circle(self.screen, BLACK, (540 + 25 * i, 15), 10, 1)
        dr.line(self.screen, BLACK, (0, 553), (800, 553), 1)
        dr.rect(self.screen, (25, 15, 0), (0, 554, 800, 46))

    def action(self):
        """
        В основной части игры метод производит перемещение всех объектов и проверку их взаимодействий.
        :return: main_finished - переменная, отвечающая, должен ли закончиться первый цикл main.
        """
        keys = key.get_pressed()
        main_finished = 0
        if keys:
            self.tank.moving = True
        else:
            self.tank.moving = False

        for bt in self.ball_targets:
            bt.move()
        for st in self.smile_targets:
            st.move()
            st.direction_time -= 1

        self.targets = self.smile_targets + self.ball_targets

        for t in self.targets:
            if t.bomb_time_waiting <= 0:
                self.bombs.append(Bomb(self.screen, t.x, t.y + 0.75 * t.r))
                t.bomb_time_waiting = 60
            t.bomb_time_waiting -= 1

        for b in self.bombs:
            if b.explosion_time == 16:
                b.move()
                if abs(b.x - self.tank.location[0]) < 40 and (-9 < b.y - self.tank.location[1] < 30):
                    self.tank.health -= 10
                    explosion(b)
                elif b.x < 10:
                    explosion(b)
                    b.x = 10
                elif b.x > 790:
                    explosion(b)
                    b.x = 790
                elif b.y > 553:
                    explosion(b)
                    b.y = 553

        if self.tank.health == 0:
            self.tank.lives -= 1
            if self.tank.lives == 0:
                self.finish = -1
            else:
                main_finished = -2

        for b in self.balls:
            b.move()
            for t in self.targets[:]:
                if b.hittest(t, b.r):
                    t.points = self.points
                    t.hit(1 * isinstance(t, Ball_Target) + 2 * isinstance(t, Smile_Target))
                    self.points = t.points
                    if isinstance(t, Ball_Target):
                        self.ball_targets.remove(t)
                    elif isinstance(t, Smile_Target):
                        self.smile_targets.remove(t)
                    self.targets.remove(t)

                    main_finished += 1
        for r in self.rockets:
            if r.explosion_time == 30:
                r.move()
                for t in self.targets[:]:
                    if r.hittest(t, 20):
                        t.points = self.points
                        t.hit(1 * isinstance(t, Ball_Target) + 2 * isinstance(t, Smile_Target))
                        self.points = t.points

                        explosion(r)
                        r.x = (r.x + t.x) / 2
                        r.y = (r.y + t.y) / 2

                        if isinstance(t, Ball_Target):
                            self.ball_targets.remove(t)
                        elif isinstance(t, Smile_Target):
                            self.smile_targets.remove(t)
                        self.targets.remove(t)
                        main_finished += 1

        self.tank.move()
        self.tank.power_up()
        return main_finished

    def main(self):
        """
        Метод, отвечающий за саму игру. Разбит на два цикла: в первом происходсят основные действия, во втором после
        попадания снаряда в мишень/бомбы в танк на экране на 2.1 секунды выводится надпись,
        новые снаряды и бомбы при этом не выпускаются, старые снаряды не взаимодействуют с мишенями, а бомбы с танком.
        """

        for _ in range(2 - len(self.ball_targets)):
            self.ball_targets.append(Ball_Target(self.screen))
        for _ in range(2 - len(self.smile_targets)):
            self.smile_targets.append(Smile_Target(self.screen))

        main_finished = False

        while main_finished == 0 and self.finish == 0:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.tank.loading_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.balls.append(self.tank.loading_end(event))
                    elif event.button == 3:
                        self.rockets.append(self.tank.loading_end(event))
                    self.bullet_count += 1
                elif event.type == pygame.MOUSEMOTION:
                    self.tank.targetting(event)

            main_finished = self.action()

            self.draw()
            pygame.display.update()

        if main_finished < 0:
            self.tank.health = 100

        i = 0
        while not self.finish and i < 70:

            clock.tick(FPS)
            keys = key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.tank.loading_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.tank.f2_on = 0
                    self.tank.power = 5
                elif event.type == pygame.MOUSEMOTION:
                    self.tank.targetting(event)

            if keys:
                self.tank.moving = True
            else:
                self.tank.moving = False

            for bt in self.ball_targets:
                bt.move()
            for st in self.smile_targets:
                st.move()
                st.direction_time -= 1
            self.targets = self.smile_targets + self.ball_targets

            for b in self.bombs:
                if b.explosion_time == 16:
                    b.move()
                    if b.x < 10:
                        explosion(b)
                        b.x = 10
                    elif b.x > 790:
                        explosion(b)
                        b.x = 790
                    elif b.y > 553:
                        explosion(b)
                        b.y = 553

            for b in self.balls:
                b.move()

            for r in self.rockets:
                if r.explosion_time == 30:
                    r.move()

            self.tank.move()
            self.tank.power_up()

            self.draw()
            if main_finished == 1:
                surf = myfont.render("Потрачено выстрелов на уничтожение цели:" + str(self.bullet_count), True, BLACK)
                self.screen.blit(surf, (115, 270))
            elif main_finished == -2:
                surf = myfont.render("Вы потеряли одну жизнь!", True, RED)
                self.screen.blit(surf, (250, 270))
            else:
                surf = myfont.render("Вы потеряли одну жизнь, но сбили цель!", True, RED)
                self.screen.blit(surf, (130, 270))
                surf = myfont.render("Потрачено выстрелов:" + str(self.bullet_count), True, BLACK)
                self.screen.blit(surf, (220, 300))
            dr.line(self.screen, BLACK, (0, 553), (800, 553), 1)
            pygame.display.update()
            i += 1


clock = pygame.time.Clock()

game = Game()
score = 0
while game.finish == 0:
    game.balls = []
    game.rockets = []
    game.bullet_count = 0
    game.main()

if game.finish == -1:
    game.screen.fill(BLACK)
    surface = myfont.render("Score:" + str(game.points), True, WHITE)
    game.screen.blit(surface, (340, 400))
    myfont = pygame.font.SysFont('Times New Roman', 69)
    surface = myfont.render("YOU DIED", True, (79, 0, 1))
    game.screen.blit(surface, (250, 240))
    pygame.display.update()
    sleep(2)
pygame.quit()
