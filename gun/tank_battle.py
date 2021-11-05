import math
import pygame.draw as dr
import pygame.key as key
import pygame.font
from time import sleep
from random import choice

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
Движение первого танка можно осуществлять  клавишами A и D, движение второго - стрелочками. 
При зажатии левой кнопки мыши происходит "зарядка" пушки, и при отпускании клавишы происходит выстрел шарами.
Танки стреляют поочередно, но двигаться могут всегда.
У такнка 3 жизни, при потере всех трёх игра заканчивается. В одной жизни 100 единиц здоровья,
одно попадание бомбы отнимает 10 единиц здоровья. Важным моментом явяляется то, что танк может подбить сам себя.
Я ограничил угол наклона пушки от вертикали, так как иначе можно стрелять просто по горизонтали, 
что не позволяет увернуться, а так неинтересно.
"""


def distance(coord1, coord2):
    """
    Находит расстояние между двумя точками.
    :param coord1: координаты первой точки.
    :param coord2: координаты второй точки.
    :return: расстояние между точками.
    """
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5


class Ball:
    def __init__(self, screen, x, y):
        """
        Конструктор класса Ball.
        :param screen: экран, на котором рисуются мячи.
        :param x: начальная x-координата мяча, вылетающего из пушки.
        :param y: начальная y-координата мяча, вылетающего из пушки.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = 15
        self.live = 30
        self.activity = 1
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
        self.x += self.vx
        self.y += self.vy
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


class Tank:
    """
    Класс танка.
    """

    def __init__(self, screen, color, x):
        """
        Конструктор класса Tank.
        :param screen: экран, на котором рисуется пушка.
        """
        self.screen = screen
        self.power = 5
        self.f2_on = 0
        self.angle = -math.pi / 2
        self.color = GREY
        self.location = [x, 520]
        self.health = 100
        self.lives = 3
        self.body_color = color
        self.moving = 0

    def move(self):
        """
        Метод, отвечающий за перемещение танка по земле. Перемещение осуществляется клавишами A и D или стрелочками.
        """
        keys = key.get_pressed()
        if self.moving == 1:
            if self.location[0] < 765 and keys[pygame.K_d]:
                self.location[0] += 8
            if self.location[0] > 35 and keys[pygame.K_a]:
                self.location[0] -= 8
        elif self.moving == 2:
            if self.location[0] < 765 and keys[pygame.K_RIGHT]:
                self.location[0] += 8
            if self.location[0] > 35 and keys[pygame.K_LEFT]:
                self.location[0] -= 8

    def loading_start(self):
        """
        Начало "заряжания" пушки.
        """
        self.f2_on = 1

    def loading_end(self):
        """
        Выстрел снарядом.
        Происходит при отпускании кнопки мыши. Запускается шарик при нажатиии левой кнопокй мыши,
        ракета - при нажатии правой. Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        new_bullet = Ball(self.screen, 60 * math.cos(self.angle) + self.location[0],
                          60 * math.sin(self.angle) + self.location[1])
        new_bullet.vx = self.power * math.cos(self.angle)
        new_bullet.vy = self.power * math.sin(self.angle)
        new_bullet.x -= new_bullet.vx
        new_bullet.y -= new_bullet.vy
        self.f2_on = 0
        self.power = 5
        return new_bullet

    def targetting(self, event):
        """
        Прицеливание, происходящее при движении мыши.
        :param event: событие движения мыши.
        """
        if event:
            self.angle = math.atan2((event.pos[1] - self.location[1]), (event.pos[0] - self.location[0]))
            if -math.pi / 3 < self.angle <= math.pi / 2:
                self.angle = -math.pi / 3
            elif math.pi / 2 < self.angle <= math.pi or -math.pi < self.angle <= -2 * math.pi / 3:
                self.angle = -2 * math.pi / 3

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

        dr.rect(self.screen, self.body_color, (self.location[0] - 15, self.location[1] - 4, 30, 10))
        dr.rect(self.screen, BLACK, (self.location[0] - 15, self.location[1] - 4, 30, 10), 1)

        points = [[-15, 6], [-35, 15], [-35, 25], [35, 25], [35, 15], [15, 6]]
        for i in range(6):
            points[i][0] += self.location[0]
            points[i][1] += self.location[1]
        dr.polygon(self.screen, self.body_color, points)
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
        self.balls_1tank = []
        self.balls_2tank = []
        self.tanks = [Tank(self.screen, (0, 40, 0), 50), Tank(self.screen, (0, 0, 80), 750)]

    def draw(self):
        """
        Метод вырисовывает все действующие объекты на экране.
        """
        self.screen.fill(WHITE)
        for i in range(2):
            self.tanks[i].draw()

        for b in self.balls_1tank[:]:
            if b.live > 0:
                b.draw()
            else:
                self.balls_1tank.remove(b)

        for b in self.balls_2tank[:]:
            if b.live > 0:
                b.draw()
            else:
                self.balls_2tank.remove(b)

        for i in range(2):
            surf = myfont.render("Health" + str(i + 1) + ": " + str(self.tanks[i].health), True, BLACK)
            self.screen.blit(surf, (30, 30 * i))
            surf = myfont.render("Lives" + str(i + 1) + ": ", True, BLACK)
            self.screen.blit(surf, (250, 30 * i))
            for j in range(self.tanks[i].lives):
                dr.circle(self.screen, RED, (360 + 25 * j, 15 + 30 * i), 10)
                dr.circle(self.screen, BLACK, (360 + 25 * j, 15 + 30 * i), 10, 1)
        dr.line(self.screen, BLACK, (0, 553), (800, 553), 1)
        dr.rect(self.screen, (25, 15, 0), (0, 554, 800, 46))

    def move_tanks(self):
        """
        Функция определяет, должны ли танки двигаться. И если да, то двигает ихю
        """
        keys = key.get_pressed()

        if (keys[pygame.K_d] and self.tanks[1].location[0] - self.tanks[0].location[0] > 70) or keys[pygame.K_a]:
            self.tanks[0].moving = 1
        else:
            self.tanks[0].moving = 0

        if keys[pygame.K_RIGHT] or (keys[pygame.K_LEFT] and
                                    self.tanks[1].location[0] - self.tanks[0].location[0] > 70):
            self.tanks[1].moving = 2
        else:
            self.tanks[1].moving = 0

        for i in range(2):
            self.tanks[i].move()
            self.tanks[i].power_up()

    def main(self):
        """
        Метод, отвечающий за саму игру. Разбит на два цикла: в первом происходсят основные действия, во втором после
        попадания потери жизни одним танком на экране на 2.1 секунды выводится надпись,
        новые снаряды и бомбы при этом не выпускаются, старые снаряды не взаимодействуют с танками.
        """

        leader = 0  # Переменная, отвечающая за то, какой танк сейчас стреляет.
        main_finished = 0
        while main_finished == 0 and self.finish == 0:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.tanks[leader].loading_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if leader == 0:
                        self.balls_1tank.append(self.tanks[0].loading_end())
                    else:
                        self.balls_2tank.append(self.tanks[1].loading_end())
                    leader = (leader + 1) % 2
                elif event.type == pygame.MOUSEMOTION:
                    self.tanks[leader].targetting(event)

            self.move_tanks()

            for b in self.balls_1tank:
                b.move()
                if abs(b.x - self.tanks[1].location[0]) < 35 + b.r / 2 \
                        and (-4 - b.r / 2 < b.y - self.tanks[1].location[1] < 25 + b.r / 2) and b.activity:
                    self.tanks[1].health -= 10
                    b.activity = 0
            for b in self.balls_2tank:
                b.move()
                if abs(b.x - self.tanks[0].location[0]) < 35 + b.r / 2 \
                        and (-4 - b.r / 2 < b.y - self.tanks[0].location[1] < 25 + b.r / 2) and b.activity:
                    self.tanks[0].health -= 10
                    b.activity = 0

            for i in range(2):
                if self.tanks[i].health == 0:
                    self.tanks[i].lives -= 1
                    if self.tanks[i].lives == 0:
                        self.finish -= i + 1
                    else:
                        main_finished += i + 1

            self.draw()
            pygame.display.update()

        if main_finished == 1:
            self.tanks[0].health = 100
        elif main_finished == 2:
            self.tanks[1].health = 100
        elif main_finished == 3:
            self.tanks[0].health = self.tanks[1].health = 100

        i = 0
        while not self.finish and i < 70:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.tanks[leader].loading_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.tanks[leader].f2_on = 0
                    self.tanks[leader].power = 5
                elif event.type == pygame.MOUSEMOTION:
                    self.tanks[leader].targetting(event)

            self.move_tanks()

            for b in self.balls_1tank:
                b.move()
            for b in self.balls_2tank:
                b.move()

            self.draw()
            pygame.display.update()

            if main_finished == 1:
                surf = myfont.render("Танк 2 подбил Танк 1!", True, RED)
                self.screen.blit(surf, (250, 270))
            elif main_finished == 2:
                surf = myfont.render("Танк 1 подбил Танк 2!", True, RED)
                self.screen.blit(surf, (250, 270))
            else:
                surf = myfont.render("Танки подбили друг-друга!", True, RED)
                self.screen.blit(surf, (250, 270))

            dr.line(self.screen, BLACK, (0, 553), (800, 553), 1)
            pygame.display.update()
            i += 1


clock = pygame.time.Clock()

game = Game()
while game.finish == 0:
    game.tanks[0].location[0] = 50
    game.tanks[1].location[0] = 750
    game.balls_1tank = game.balls_2tank = []
    game.main()

if game.finish != 1:
    myfont = pygame.font.SysFont('calibri', 40)
    if game.finish == -1:
        surface = myfont.render("Танк 2 победил!", True, RED)
        game.screen.blit(surface, (250, 240))
    elif game.finish == -2:
        surface = myfont.render("Танк 1 победил!", True, RED)
        game.screen.blit(surface, (250, 240))
    else:
        surface = myfont.render("Ничья!", True, RED)
        game.screen.blit(surface, (350, 240))
    pygame.display.update()
    sleep(2)
pygame.quit()
