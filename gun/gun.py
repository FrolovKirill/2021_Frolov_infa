import math
import pygame.draw as dr
import pygame.font
from random import choice
from random import randint

FPS = 30

pygame.init()
pygame.font.init()

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

myfont = pygame.font.SysFont('calibri', 30)


def distance(coord1, coord2):
    """
    Находит расстояние между двумя точками.
    :param coord1: координаты первой точки.
    :param coord2: координаты второй точки.
    :return: расстояние между точками.
    """
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5


def ball_repulse(obj):
    """
    Отражает мячи(ядра пушки) от стенок с потерей энергии.
    :param obj: объект класса Ball
    """
    if obj.x <= obj.r or obj.x >= 800 - obj.r:
        obj.vx = -0.65 * obj.vx
    if obj.x <= obj.r:
        obj.x = obj.r
    elif obj.x >= 800 - obj.r:
        obj.x = 800 - obj.r
    if obj.y >= 520 - obj.r:
        obj.vy = -0.65 * obj.vy
        obj.vx = 0.65 * obj.vx
        obj.y = 520 - obj.r

    if obj.vx ** 2 < 1:
        obj.vx = 0

    if obj.vy ** 2 < 1:
        obj.vy = 0


def target_repulse(obj):
    """
    Отражает мишени от границ области, в которой они могут находиться.
    :param obj: объект класса Target
    """
    if obj.x <= 300 or obj.x >= 800 - obj.r:
        obj.vx = -obj.vx
    if obj.x <= 300:
        obj.x = 300
    elif obj.x >= 800 - obj.r:
        obj.x = 800 - obj.r

    if obj.y <= obj.r or obj.y >= 520:
        obj.vy = -obj.vy
    if obj.y <= obj.r:
        obj.y = obj.r
    elif obj.y >= 520:
        obj.y = 520


class Ball:
    """
    Класс мячей, вылетающих из пушки.
    """

    def __init__(self, screen: pygame.Surface, x, y):
        """
        Конструктор класса Ball.
        :param screen: экран, на котором рисуются мячи.
        :param x: начальная x-координата мяча, вылетающего из пушки.
        :param y: начальная y-координата мяча, вылетающего из пушки.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30  # Параметр отвечает за время жизни мяча после остановки (30 кадров = 1 с)

    def move(self):
        """
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += 1.5
        self.x += self.vx
        self.y += self.vy
        ball_repulse(self)
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

    def hittest(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        :param obj: объекти класса Target
        :return: True - если произошло поражение цели, False - иначе.
        """
        if distance((self.x, self.y), (obj.x, obj.y)) <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    """
    Класс пушки.
    """
    def __init__(self, screen):
        """
        Конструктор класса Ball.
        :param screen: экран, на котором рисуется пушка.
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 0
        self.color = GREY

    def fire2_start(self):
        """
        Начало "заряжания" пушки.
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        :param event: событие отпускания кнопки мыши.
        """
        new_ball = Ball(self.screen, (11 + 8 / 9 * self.f2_power) * math.cos(self.angle) + 20,
                        (11 + 8 / 9 * self.f2_power) * math.sin(self.angle) + 450)
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = (8 / 10 * self.f2_power) * math.cos(self.angle) * 0.7
        new_ball.vy = (8 / 10 * self.f2_power) * math.sin(self.angle) * 0.7
        self.f2_on = 0
        self.f2_power = 10
        return new_ball

    def targetting(self, event):
        """
        Прицеливание, происходящее при движении мыши.
        :param event: событие движения мыши.
        """
        if event:
            self.angle = math.atan2((event.pos[1] - 450), (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """
        Метод вырисовывает объект этого класса на экране.
        """
        coords = ((3 * math.sin(self.angle) + 20, -3 * math.cos(self.angle) + 450),
                  ((11 + 8 / 9 * self.f2_power) * math.cos(self.angle) + 3 * math.sin(self.angle) + 20,
                   (11 + 8 / 9 * self.f2_power) * math.sin(self.angle) - 3 * math.cos(self.angle) + 450),
                  ((11 + 8 / 9 * self.f2_power) * math.cos(self.angle) - 3 * math.sin(self.angle) + 20,
                   (11 + 8 / 9 * self.f2_power) * math.sin(self.angle) + 3 * math.cos(self.angle) + 450),
                  (-3 * math.sin(self.angle) + 20, 3 * math.cos(self.angle) + 450))
        dr.polygon(
            self.screen,
            self.color,
            coords
        )
        dr.aalines(
            self.screen,
            self.color,
            True,
            coords
        )

    def power_up(self):
        """
        Процесс заряжания пушки.
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = BLACK
        else:
            self.color = GREY


class Target:
    """
    Класс мишеней.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Конструктор класса Target.
        :param screen: экран, на котором рисуются мячи.
        """
        self.screen = screen
        self.points = 0
        self.x = randint(400, 780)
        self.y = randint(200, 520)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.r = randint(5, 35)
        self.color = choice([RED, BLUE, YELLOW])

    def move(self):
        """
        Переместить мишень по прошествии единицы времени.
        """
        self.x += self.vx
        self.y += self.vy
        target_repulse(self)

    def hit(self, points=1):
        """
        Попадание шарика в мишень.
        """
        self.points += points

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


class Game:
    """
    Класс игры.
    """
    def __init__(self):
        """
        Конструктор класса Game.
        """
        self.points = 0
        self.finish = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bullet = 0
        self.balls = []
        self.targets = []
        self.gun = Gun(self.screen)

    def main(self):
        """
        Метод, отвечающий за саму игру. Разбит на два цикла: в первом происходсят основные действия, во втором после
        попадания в мишень на экране на 2.1 секунды выводится надпись, новые мячи при этом не выпускаются.
        """
        for _ in range(3 - len(self.targets)):
            self.targets.append(Target(self.screen))

        main_finished = False

        while not main_finished and not self.finish:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.balls.append(self.gun.fire2_end(event))
                    self.bullet += 1
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)

            for t in self.targets:
                t.move()
            for b in self.balls:
                b.move()
                for t in self.targets[:]:
                    if b.hittest(t):
                        t.points = self.points
                        t.hit()
                        self.points = t.points
                        self.targets.remove(t)
                        main_finished = True

            self.gun.power_up()

            self.screen.fill(WHITE)
            self.gun.draw()
            for t in self.targets:
                if t != 0:
                    t.draw()
            for b in self.balls[:]:
                if b.live > 0:
                    b.draw()
                else:
                    self.balls.remove(b)

            surf = myfont.render("Score:" + str(self.points), True, BLACK)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()

        i = 0
        while not self.finish and i < 70:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.gun.f2_on = 0
                    self.gun.f2_power = 10
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)

            for t in self.targets:
                t.move()
            for b in self.balls:
                b.move()

            self.gun.power_up()

            self.screen.fill(WHITE)
            self.gun.draw()
            for t in self.targets:
                if t != 0:
                    t.draw()
            for b in self.balls[:]:
                if b.live > 0:
                    b.draw()
                else:
                    self.balls.remove(b)

            surf = myfont.render("Score:" + str(self.points), True, BLACK)
            self.screen.blit(surf, (0, 0))
            surf = myfont.render("Потрачено выстрелов на уничтожение цели:" + str(self.bullet), True, BLACK)
            self.screen.blit(surf, (115, 280))
            pygame.display.update()

            i += 1


clock = pygame.time.Clock()

game = Game()
score = 0
while not game.finish:
    game.balls = []
    game.bullet = 0
    game.main()

pygame.quit()
