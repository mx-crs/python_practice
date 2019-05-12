import pygame
import random
import math


SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):  # сумма двух векторов
        return Vec2d((self.x[0] + other.x[0], self.x[1] + other.x[1]))

    def __sub__(self, other):  # разность двух векторов
        return Vec2d((self.x[0] - other.x[0], self.x[1] - other.x[1]))

    def __mul__(self, k):  # умножение вектора на число или скалярное умножение векторов
        if isinstance(k, Vec2d):
            return self.x[0] * k.x[0] + self.x[1] * k.x[1]
        return Vec2d((self.x[0] * k, self.x[1] * k))

    def __divmod__(self, k): # деление вектора на число
        return Vec2d((self.x[0] / k, self.x[1] / k))

    def __len__(self):  # длинна вектора
        return math.sqrt(self.x[0] * self.x[0] + self.x[1] * self.x[1])

    def __getitem__(self, item):
        return self.x[item]

    def nearly_equal(self, other, length=10):
        return (abs((self - other).x[0]) <= length and
                abs((self - other).x[1]) <= length)

    def int_pair(self):
        return int(self.x[0]), int(self.x[1])


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.speedX = 1

    # Добавление и исключение в ломаную и из ломаной точки со скоростью
    def add_remove_point_speed(self, point, speed):
        sign = 0
        for i in range(len(self.points)):
            if self.points[i].nearly_equal(point):
                self.points.pop(i)
                self.speeds.pop(i)
                sign = 1
                break
        if sign == 0:
            self.points.append(point)
            self.speeds.append(speed * self.speedX)

    # Персчитывание координат опорных точек
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d((- self.speeds[p][0], self.speeds[p][1]))
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d((self.speeds[p][0], -self.speeds[p][1]))

    # "Отрисовка" точек
    def draw_points(self, gameDisplay, points=None, style="points", width=3, clr=(255, 255, 255)):
        if points is None:
            points = self.points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, clr, (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, clr,
                                   (int(p[0]), int(p[1])), width)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    # Сделать большей скорость перемещения точек
    def do_faster(self):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i] * 1.5
        self.speedX += 1.5

    # Сделать меньшей скорость перемещения точек
    def do_slower(self):
        for i in range(len(self.speeds)):
            self.speeds[i] = self.speeds[i].__divmod__(1.5)
        self.speedX -= 1.5 if self.speedX > 1.5 else 0


class Knot(Polyline):
    def get_knot(self, obj, count):
        if len(obj.points) < 3:
            return []
        res = []
        for i in range(-2, len(obj.points) - 2):
            ptn = []
            ptn.append((obj.points[i] + obj.points[i + 1]) * 0.5)
            ptn.append(obj.points[i + 1])
            ptn.append((obj.points[i + 1] + obj.points[i + 2]) * 0.5)

            res.extend(super().get_points(ptn, count))
        return res


class Solver:
    def __init__(self):
        pygame.init()
        self.scr_dim = (800, 600)
        self.gameDisplay = pygame.display.set_mode(self.scr_dim)
        pygame.display.set_caption("MyScreenSaver")

        self.steps = 35
        self.working = True
        self.polyline = Polyline()
        self.knot = Knot()
        self.show_help = False
        self.pause = True

        self.hue = 0
        self.color = pygame.Color(0)

    def run(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.polyline = Polyline()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0
                    if event.key == pygame.K_UP:
                        self.polyline.do_faster()
                    if event.key == pygame.K_DOWN:
                        self.polyline.do_slower()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pnt = Vec2d(event.pos)
                    spd = Vec2d((random.random() * 2, random.random() * 2))
                    self.polyline.add_remove_point_speed(pnt, spd)

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.polyline.draw_points(self.gameDisplay)
            self.polyline.draw_points(self.gameDisplay, self.knot.get_knot(self.polyline, self.steps),
                                    "line", 3, self.color)
            if not self.pause:
                self.polyline.set_points()
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        exit(0)

    # Отрисовка справки
    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])
        data.append(["Add point", "Click on free space"])
        data.append(["Remove point", "Click on/near the point"])
        data.append(["UpArrow", "Make points run faster"])
        data.append(["DownArrow", "Make points run slower"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
                          (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (300, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    solver = Solver()

    solver.run()
    solver.quit()
