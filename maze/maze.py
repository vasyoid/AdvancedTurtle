import random
import turtle

_MARGIN = 40
_SCREEN_WIDTH = 680
_SCREEN_HEIGHT = 680
_CELL_SIZE = 40


class Turtle:
    def __init__(self):
        tr = _screen.tracer()
        _screen.tracer(0)
        self._t = turtle.Turtle("turtle")
        self._t.up()
        cx = random.randint(0, _SCREEN_WIDTH // _CELL_SIZE - 1)
        cy = random.randint(0, _SCREEN_HEIGHT // _CELL_SIZE - 1)
        self._t.setpos(-_SCREEN_WIDTH // 2 + cx * _CELL_SIZE + _CELL_SIZE // 2, -_SCREEN_HEIGHT // 2 + cy * _CELL_SIZE + _CELL_SIZE // 2)
        _screen.tracer(tr)
        _screen.update()

    def _current_cell(self):
        x, y = map(int, self._t.pos())
        return (x + _SCREEN_WIDTH // 2) // _CELL_SIZE, (y + _SCREEN_HEIGHT // 2) // _CELL_SIZE

    def _current_direction(self):
        return int(self._t.heading()) // 90

    def has_wall_forward(self):
        return _maze.has_wall(*self._current_cell(), self._current_direction())

    def has_wall_left(self):
        return _maze.has_wall(*self._current_cell(), (self._current_direction() + 1) % 4)

    def has_wall_right(self):
        return _maze.has_wall(*self._current_cell(), (self._current_direction() + 3) % 4)

    def paint_cell(self, color):
        _maze.paint_cell(*self._current_cell(), color)

    def cell_color(self):
        return _maze.cell_color(*self._current_cell())

    def forward(self):
        if self.has_wall_forward():
            s = self._t.speed()
            self._t.speed(6)
            self._t.left(10)
            for _ in range(5):
                self._t.right(20)
                self._t.left(20)
                pass
            self._t.right(10)
            self._t.speed(s)
        else:
            self._t.forward(_CELL_SIZE)

    def backward(self):
        self._t.backward(_CELL_SIZE)

    def left(self):
        self._t.left(90)

    def right(self):
        self._t.right(90)

    def color(self, *args, **kwargs):
        return self._t.color(*args, **kwargs)

    def speed(self, *args, **kwargs):
        return self._t.speed(*args, **kwargs)

    def down(self):
        return self._t.down()

    def up(self):
        return self._t.up()


class Maze:
    _DX = [0, 1, 0, -1]
    _DY = [-1, 0, 1, 0]
    _OPPOSITE = [2, 3, 0, 1]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._grid = [[0b1111 for _ in range(width)] for _ in range(height)]
        self._colors = [["white" for _ in range(width)] for _ in range(height)]
        self._visited = [[False for _ in range(width)] for _ in range(height)]
        self._generate()
        self._colors[random.randint(0, self.height - 1)][random.randint(0, self.width - 1)] = "green"

    def _generate(self, cx=0, cy=0):
        self._visited[cy][cx] = True
        directions = list(range(4))
        random.shuffle(directions)

        for direction in directions:
            nx, ny = cx + Maze._DX[direction], cy + Maze._DY[direction]
            if 0 <= nx < self.width and 0 <= ny < self.height and not self._visited[ny][nx]:
                self._grid[cy][cx] &= ~(1 << direction)
                self._grid[ny][nx] &= ~(1 << Maze._OPPOSITE[direction])
                self._generate(nx, ny)

    def has_wall(self, cx, cy, direction):
        dir = [1, 2, 3, 0][direction]
        return self._grid[cy][cx] & (1 << dir) != 0

    def paint_cell(self, cx, cy, color):
        self._colors[cy][cx] = color
        self._draw_cell(cx, cy)

    def cell_color(self, cx, cy):
        return self._colors[cy][cx]

    def _draw_cell(self, cx, cy):
        tr = _screen.tracer()
        _screen.tracer(0)
        _drawer.width(2)
        cell_value = self._grid[cy][cx]
        cell_x = -_SCREEN_WIDTH // 2 + cx * _CELL_SIZE
        cell_y = -_SCREEN_HEIGHT // 2 + cy * _CELL_SIZE

        _drawer.color(self._colors[cy][cx])
        _drawer.setheading(0)
        _drawer.up()
        _drawer.setpos(cell_x, cell_y)
        _drawer.begin_fill()
        for _ in range(4):
            _drawer.forward(_CELL_SIZE)
            _drawer.left(90)
        _drawer.end_fill()

        _drawer.color("black")
        for direction in range(4):
            if cell_value & (1 << direction):
                _drawer.up()

                if direction == 0:  # North
                    _drawer.setpos(cell_x, cell_y)
                    _drawer.setheading(0)  # East
                elif direction == 1:  # East
                    _drawer.setpos(cell_x + _CELL_SIZE, cell_y)
                    _drawer.setheading(90)  # North
                elif direction == 2:  # South
                    _drawer.setpos(cell_x, cell_y + _CELL_SIZE)
                    _drawer.setheading(0)  # East
                elif direction == 3:  # West
                    _drawer.setpos(cell_x, cell_y)
                    _drawer.setheading(90)  # North

                _drawer.down()
                _drawer.forward(_CELL_SIZE)
        _screen.tracer(tr)

    def draw(self):
        tr = _screen.tracer()
        _screen.tracer(0)
        for cy in range(self.height):
            for cx in range(self.width):
                self._draw_cell(cx, cy)
        _screen.tracer(tr)

    def drop_walls(self, n):
        for _ in range(n):
            while True:
                if random.getrandbits(1):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 2)
                    if self._grid[y][x] & ~(1 << 2):
                        self._grid[y][x] &= ~(1 << 2)
                        self._grid[y + 1][x] &= ~(1 << 0)
                        break
                else:
                    x = random.randint(0, self.width - 2)
                    y = random.randint(0, self.height - 1)
                    if self._grid[y][x] & (1 << 1):
                        self._grid[y][x] &= ~(1 << 1)
                        self._grid[y][x + 1] &= ~(1 << 3)
                        break


def new_maze(seed=None):
    global _maze
    random.seed(seed)
    _maze = Maze(_SCREEN_WIDTH // _CELL_SIZE, _SCREEN_HEIGHT // _CELL_SIZE)
    _maze.draw()


def new_cyclic_maze(seed=None):
    global _maze
    random.seed(seed)
    _maze = Maze(_SCREEN_WIDTH // _CELL_SIZE, _SCREEN_HEIGHT // _CELL_SIZE)

    _maze.drop_walls(100)
    _maze.draw()


def mainloop():
    _screen.mainloop()


def tracer(n):
    _screen.tracer(n)

_screen = turtle.Screen()
_screen.setup(_SCREEN_WIDTH + _MARGIN, _SCREEN_HEIGHT + _MARGIN)

_drawer = turtle.Turtle()
_drawer.hideturtle()

_maze: Maze = None
