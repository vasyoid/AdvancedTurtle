import math
import random
import time
import turtle


class ListElement:
    def __init__(self, value=0):
        self.value = value
        self.shift = (0, 0)
        self.highlighted = None

    def _highlight_and_draw(self, other):
        self.highlighted = "orange"
        if isinstance(other, ListElement):
            other.highlighted = "orange"
        _draw_numbers()
        self.highlighted = None
        if isinstance(other, ListElement):
            other.highlighted = None
        time.sleep(0.5)

    def __lt__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value >= other.value
        return self.value >= other

    def __eq__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        self._highlight_and_draw(other)
        if isinstance(other, ListElement):
            return self.value != other.value
        return self.value != other

    def __add__(self, other):
        if isinstance(other, ListElement):
            return self.value + other.value
        return self.value + other

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return self.value.__repr__()


class MyList(list[ListElement]):
    def swap(self, a, b):
        if a > b:
            a, b = b, a
        self[a].highlighted = self[b].highlighted = "orange"
        w = _SCREEN_WIDTH // len(_numbers)
        r = w * (b - a) // 2
        for i in range(101):
            angle = math.pi / 100 * i
            self[a].shift = ((1 - math.cos(angle)) * r, math.sin(angle) * r)
            self[b].shift = ((math.cos(angle) - 1) * r, -math.sin(angle) * r)
            _draw_numbers()
            time.sleep(0.005)
        self[a].highlighted = self[b].highlighted = None
        self[a].shift = self[b].shift = (0, 0)
        self[a], self[b] = self[b], self[a]
        _draw_numbers()


_SCREEN_WIDTH = 600
_SCREEN_HEIGHT = 600

_screen = turtle.Screen()
_screen.setup(_SCREEN_WIDTH, _SCREEN_HEIGHT)
_screen.tracer(0)

_numbers = MyList()
_selectors = []


def _draw_rect(x, y, w, h, element: ListElement):
    _drawer.color(element.highlighted or "lightgreen")
    _drawer.setpos(x, y)
    _drawer.setheading(0)
    _drawer.down()
    _drawer.begin_fill()
    for _ in range(2):
        for d in w, h:
            _drawer.forward(d)
            _drawer.left(90)
    _drawer.end_fill()
    _drawer.up()
    _drawer.forward(w // 2)
    _drawer.color("black")
    _drawer.write(element, align="center", font=("Arial", 15, "normal"))


def _draw_numbers():
    _drawer.clear()
    w = _SCREEN_WIDTH // len(_numbers)
    d = w // 6
    for i in range(len(_numbers)):
        sx, sy = _numbers[i].shift
        _selectors[i].setpos(w * i + w // 2 - _SCREEN_WIDTH // 2, _SCREEN_HEIGHT // 4 - 60)
        _draw_rect(w * i + d // 2 - _SCREEN_WIDTH // 2 + sx, _SCREEN_HEIGHT // 4 - 30 + sy, w - d,
                   _numbers[i].value * _SCREEN_HEIGHT // 80 + 20, _numbers[i])
    _screen.update()


def _highlight_and_draw(pos):
    _numbers[pos].highlighted = "orange"
    _draw_numbers()
    _numbers[pos].highlighted = None


_drawer = turtle.Turtle()
_drawer.hideturtle()
_drawer.up()


def _toggle_color(t):
    t.color("yellow" if t.color()[0] == "black" else "black")
    _screen.update()


def _init_onclick(t):
    t.onclick(lambda x, y: _toggle_color(t))


def _refresh():
    for i in range(len(_numbers)):
        _numbers[i] = ListElement(random.randint(1, 20))
    _draw_numbers()


def _init():
    for i in range(10):
        _numbers.append(ListElement())
        t = turtle.Turtle("turtle")
        t.up()
        t.setheading(90)
        _init_onclick(t)
        _selectors.append(t)
    _refresh()
    _screen.listen()


_init()


def _write_nice(t, text):
    x, y = t.pos()
    t.setpos(x + 30, y - 10)
    t.write(text, font=("Arial", 15, "normal"))
    t.setpos(x, y)


def _write_with_clear_and_update(t, text):
    t.clear()
    _write_nice(t, text)
    _screen.update()


def _try_swap(swap):
    selected = []
    for i in range(len(_selectors)):
        if _selectors[i].color()[0] == "yellow":
            selected.append(i)
    if len(selected) != 2:
        return
    swap(_numbers, *selected)
    for i in selected:
        _selectors[i].color("black")
    _draw_numbers()


def _call_and_update(fun, *args):
    fun(*args)
    _draw_numbers()


def _nums_list():
    return [el.value for el in _numbers]


def _sort():
    values = sorted(_nums_list())
    for i in range(len(_numbers)):
        _numbers[i].value = values[i]
    _draw_numbers()


def _search(binary_search, t):
    x = random.randint(1, 20)
    _write_with_clear_and_update(t, f"search {x}")
    pos = binary_search(_numbers, x)
    if pos is None:
        return
    if pos < len(_numbers) and _numbers[pos].value == x:
        _numbers[pos].highlighted = "green"
    else:
        _numbers[pos].highlighted = "red"
    _draw_numbers()
    _numbers[pos].highlighted = None


def setup(sum, min, max, min_pos, max_pos, swap, bubble_sort, insertion_sort, selection_sort, binary_search):
    ts = []
    for i in range(6):
        t = turtle.Turtle("turtle")
        t.up()
        t.setpos(-_SCREEN_WIDTH // 2 + 20, -40 * i)
        ts.append(t)

    for i in range(6, 12):
        t = turtle.Turtle("turtle")
        t.up()
        t.setpos(20, 240 - 40 * i)
        ts.append(t)

    _write_nice(ts[0], "sum")
    _write_nice(ts[1], "min")
    _write_nice(ts[2], "max")
    _write_nice(ts[3], "show min")
    _write_nice(ts[4], "show max")
    _write_nice(ts[5], "swap")
    _write_nice(ts[6], "bubble sort")
    _write_nice(ts[7], "insertion sort")
    _write_nice(ts[8], "selection sort")
    _write_nice(ts[9], "refresh")
    _write_nice(ts[10], "quick sort")
    _write_nice(ts[11], "search")

    ts[0].onclick(lambda x, y: _write_with_clear_and_update(ts[0], f"sum: {sum(_nums_list())}"))
    ts[1].onclick(lambda x, y: _write_with_clear_and_update(ts[1], f"min: {min(_nums_list())}"))
    ts[2].onclick(lambda x, y: _write_with_clear_and_update(ts[2], f"max: {max(_nums_list())}"))
    ts[3].onclick(lambda x, y: _highlight_and_draw(min_pos(_nums_list())))
    ts[4].onclick(lambda x, y: _highlight_and_draw(max_pos(_nums_list())))
    ts[5].onclick(lambda x, y: _try_swap(swap))
    ts[6].onclick(lambda x, y: _call_and_update(bubble_sort, _numbers))
    ts[7].onclick(lambda x, y: _call_and_update(insertion_sort, _numbers))
    ts[8].onclick(lambda x, y: _call_and_update(selection_sort, _numbers))
    ts[9].onclick(lambda x, y: _refresh())
    ts[10].onclick(lambda x, y: _sort())
    ts[11].onclick(lambda x, y: _search(binary_search, ts[11]))

    _screen.update()
    _screen.listen()
    _screen.mainloop()
