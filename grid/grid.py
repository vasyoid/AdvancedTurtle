import random
import turtle
import time

_MARGIN = 40
_SCREEN_WIDTH = 640
_SCREEN_HEIGHT = 640
_CELL_SIZE = 40


class Turtle:
    def __init__(self):
        tr = _screen.tracer()
        _screen.tracer(0)
        self._t = turtle.Turtle("turtle")
        self._t.up()
        self._t.setpos(-_SCREEN_WIDTH // 2 + _CELL_SIZE // 2, -_SCREEN_HEIGHT // 2 + _CELL_SIZE // 2)
        _screen.tracer(tr)
        _screen.update()

    def _current_cell(self):
        return self._cell(*map(int, self._t.pos()))

    def _next_cell(self):
        cx, cy = self._current_cell()
        shift = [(1, 0), (0, 1), (-1, 0), (0, -1)][self._current_direction()]
        return cx + shift[0], cy + shift[1]

    def _prev_cell(self):
        cx, cy = self._current_cell()
        shift = [(1, 0), (0, 1), (-1, 0), (0, -1)][(self._current_direction() + 2) % 4]
        return cx + shift[0], cy + shift[1]

    def _cell(self, x, y):
        return (x + _SCREEN_WIDTH // 2) // _CELL_SIZE, (y + _SCREEN_HEIGHT // 2) // _CELL_SIZE

    def _current_direction(self):
        return int(self._t.heading()) // 90

    def can_go_forward(self):
        return _grid.in_field(*self._next_cell())

    def can_go_backward(self):
        return _grid.in_field(*self._prev_cell())

    def has_enemy_forward(self):
        return _grid.has_enemy(*self._next_cell())

    def has_enemy_backward(self):
        return _grid.has_enemy(*self._prev_cell())

    def nearest_food_forward(self):
        return _grid.nearest_food(*self._current_cell(), self._current_direction())

    def forward(self):
        if self.can_go_forward():
            self._t.forward(_CELL_SIZE)
            _grid.update(*self._current_cell())
        else:
            self._shake()

    def backward(self):
        if self.can_go_backward():
            self._t.backward(_CELL_SIZE)
            _grid.update(*self._current_cell())
        else:
            self._shake()

    def _shake(self):
        s = self._t.speed()
        self._t.speed(6)
        self._t.left(10)
        for _ in range(5):
            self._t.right(20)
            self._t.left(20)
            pass
        self._t.right(10)
        self._t.speed(s)

    def left(self):
        self._t.left(90)

    def right(self):
        self._t.right(90)

    def color(self, color):
        return self._t.color(color)

    def speed(self, speed=None):
        return self._t.speed(speed)

    def down(self):
        return self._t.down()

    def up(self):
        return self._t.up()

    def isdown(self):
        return self._t.isdown()

    def onclick(self, fun, btn=1, add=None):
        return self._t.onclick(fun, btn, add)

    def clear(self):
        return self._t.clear()


class Obstacle:
    def __init__(self):
        self._t = turtle.Turtle("circle")
        self._t.speed(0)
        self._t.up()
        self._t.hideturtle()
        self._cx = -1
        self._cy = -1
        self.ttl = 0

    def setpos(self, cx, cy, ttl, instantly=True):
        tr = _screen.tracer()
        if instantly:
            _screen.tracer(0)
        self._cx = cx
        self._cy = cy
        self._t.setpos(-_SCREEN_WIDTH // 2 + cx * _CELL_SIZE + _CELL_SIZE // 2,
                       -_SCREEN_HEIGHT // 2 + cy * _CELL_SIZE + _CELL_SIZE // 2)
        self._t.showturtle()
        self.ttl = ttl
        if instantly:
            _screen.tracer(tr)

    def hide(self):
        self._t.hideturtle()
        self._cx = -1
        self._cy = -1
        self.ttl = 0


class Food(Obstacle):
    def __init__(self):
        super().__init__()
        self._t.color("green")


class Enemy(Obstacle):
    def __init__(self):
        super().__init__()
        self._t.color("red")


class Grid:
    def __init__(self, width, height, food=1, enemies=0):
        self.width = width
        self.height = height
        self._grid = [[None for _ in range(width)] for _ in range(height)]
        self._score = 0
        _screen.title(f"Score: {self._score}")
        self._food = [Food() for _ in range(food)]
        self._enemies = [Enemy() for _ in range(enemies)]
        for _ in range(food):
            self.add_food(0, 0)
        for _ in range(enemies):
            self.add_enemy(0, 0)

    def draw(self):
        tr = _screen.tracer()
        _screen.tracer(0)
        _drawer.width(2)
        _drawer.color("lightgray")
        for i in range(self.height + 1):
            _drawer.up()
            cell_y = -_SCREEN_HEIGHT // 2 + i * _CELL_SIZE
            _drawer.setpos(-_SCREEN_WIDTH // 2, cell_y)
            _drawer.down()
            _drawer.setpos(_SCREEN_WIDTH // 2, cell_y)

        for i in range(self.width + 1):
            _drawer.up()
            cell_x = -_SCREEN_WIDTH // 2 + i * _CELL_SIZE
            _drawer.setpos(cell_x, -_SCREEN_HEIGHT // 2)
            _drawer.down()
            _drawer.setpos(cell_x, _SCREEN_HEIGHT // 2)
        _screen.tracer(tr)

    def in_field(self, cx, cy):
        return 0 <= cx < self.width and 0 <= cy < self.height

    def _get_free_cell(self, tx, ty):
        while True:
            cx = random.randint(0, self.width - 1)
            cy = random.randint(0, self.height - 1)
            if self._grid[cy][cx] is None and (cx, cy) != (tx, ty):
                return cx, cy

    def add_food(self, tx, ty):
        self._add_obstacle(tx, ty, self._food)

    def add_enemy(self, tx, ty):
        self._add_obstacle(tx, ty, self._enemies)

    def _add_obstacle(self, tx, ty, obstacles):
        cx, cy = self._get_free_cell(tx, ty)
        obstacle = obstacles.pop()
        wh = self.width + self.height
        obstacle.setpos(cx, cy, ttl=random.randint(wh, wh + 10), instantly=False)
        self._grid[cy][cx] = obstacle

    def remove_food(self, cx, cy):
        self._remove_obstacle(cx, cy, self._food)

    def remove_enemy(self, cx, cy):
        self._remove_obstacle(cx, cy, self._enemies)

    def has_food(self, cx, cy):
        return self.in_field(cx, cy) and isinstance(self._grid[cy][cx], Food)

    def has_enemy(self, cx, cy):
        return self.in_field(cx, cy) and isinstance(self._grid[cy][cx], Enemy)

    def nearest_food(self, cx, cy, direction):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
        distance = 1

        nx, ny = cx + dx, cy + dy
        while self.in_field(nx, ny):
            if self.has_food(nx, ny):
                return distance
            nx += dx
            ny += dy
            distance += 1

        return 0

    def _remove_obstacle(self, cx, cy, obstacles):
        obstacle: Obstacle = self._grid[cy][cx]
        obstacle.hide()
        self._grid[cy][cx] = None
        obstacles.append(obstacle)

    def _game_over(self, text):
        _screen.title(text)
        _screen.clear()
        _drawer.setpos(0, 0)
        _screen.tracer(0)
        _drawer.color("black")
        _drawer.write(f"{text}\nScore: {self._score}", align="center",
                      font=("Arial", 32, "normal"))
        _screen.update()
        time.sleep(3)
        _screen.bye()

    def update(self, tx, ty):
        global _steps
        if _steps > 0:
            _steps -= 1
            if _steps == 0:
                self._game_over("Finished")
                return
        tr = _screen.tracer()
        _screen.tracer(0)
        if self.has_food(tx, ty):
            self._score += 1
            _screen.title(f"Score: {self._score}")
            self.remove_food(tx, ty)
            self.add_food(tx, ty)
        elif self.has_enemy(tx, ty):
            self._game_over("Game Over")
            return

        for cy in range(self.height):
            for cx in range(self.width):
                obstacle: Obstacle = self._grid[cy][cx]
                if isinstance(obstacle, Obstacle) and obstacle.ttl > 0:
                    obstacle.ttl -= 1
                    if obstacle.ttl == 0:
                        obstacles = self._food if obstacle is Food else self._enemies
                        self._remove_obstacle(cx, cy, obstacles)
                        self._add_obstacle(cx, cy, obstacles)
        _screen.tracer(tr)


def level1(steps=-1, seed=None):
    _new_game(1, steps, seed)


def level2(steps=-1, seed=None):
    _new_game(2, steps, seed)


def level3(steps=-1, seed=None):
    _new_game(3, steps, seed)


def _new_game(level, steps, seed):
    global _grid, _steps
    _steps = steps
    tr = _screen.tracer()
    _screen.tracer(0)
    random.seed(seed)
    food, enemies = 0, 0
    if level == 1:
        food, enemies = 10, 0
    elif level == 2:
        food, enemies = 10, 5
    elif level == 3:
        food, enemies = 1, 5
    _grid = Grid(_SCREEN_WIDTH // _CELL_SIZE, _SCREEN_HEIGHT // _CELL_SIZE, food, enemies)
    _grid.draw()
    _screen.tracer(tr)


def mainloop():
    _screen.mainloop()


def tracer(n):
    _screen.tracer(n)


def update():
    _screen.update()


def onkey(fun, key):
    _screen.onkey(fun, key)


def getscreen():
    return _screen


def onkeypress(fun, key=None):
    return _screen.onkeypress(fun, key)


def ontimer(fun, t=0):
    return _screen.ontimer(fun, t)


_screen = turtle.Screen()
_screen.setup(_SCREEN_WIDTH + _MARGIN, _SCREEN_HEIGHT + _MARGIN)
_screen.title("Score: 0")

_drawer = turtle.Turtle()
_drawer.hideturtle()

_steps = 0
_grid: Grid = None
