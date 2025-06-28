import random
import turtle

_SCREEN_WIDTH = 600
_SCREEN_HEIGHT = 600

_screen = turtle.Screen()
_screen.setup(_SCREEN_WIDTH, _SCREEN_HEIGHT)
_screen.tracer(0)

_numbers = []
_selectors = []


def _draw_rect(x, y, w, h, value, highlighted):
    _drawer.color("orange" if highlighted else "lightgreen")
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
    _drawer.write(value, align="center", font=("Arial", 15, "normal"))


def _draw_numbers(highlighted=-1):
    _drawer.clear()
    w = _SCREEN_WIDTH // len(_numbers)
    d = w // 6
    for i in range(len(_numbers)):
        _selectors[i].setpos(w * i + w // 2 - _SCREEN_WIDTH // 2, _SCREEN_HEIGHT // 4 - 60)
        _draw_rect(w * i + d // 2 - _SCREEN_WIDTH // 2, _SCREEN_HEIGHT // 4 - 30, w - d,
                   _numbers[i] * _SCREEN_HEIGHT // 80 + 20, _numbers[i], highlighted == i)
    _screen.update()


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
        _numbers[i] = random.randint(1, 20)
    _draw_numbers()


def _init():
    for i in range(10):
        _numbers.append(0)
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


def setup(sum, min, max, min_pos, max_pos, swap, sort):
    ts = []
    for i in range(8):
        t = turtle.Turtle("turtle")
        t.up()
        t.setpos(-_SCREEN_WIDTH // 2 + 20, -40 * i)
        ts.append(t)

    _write_nice(ts[0], "sum")
    _write_nice(ts[1], "min")
    _write_nice(ts[2], "max")
    _write_nice(ts[3], "show min")
    _write_nice(ts[4], "show max")
    _write_nice(ts[5], "swap")
    _write_nice(ts[6], "sort")
    _write_nice(ts[7], "refresh")

    ts[0].onclick(lambda x, y: _write_with_clear_and_update(ts[0], f"sum: {sum(_numbers)}"))
    ts[1].onclick(lambda x, y: _write_with_clear_and_update(ts[1], f"min: {min(_numbers)}"))
    ts[2].onclick(lambda x, y: _write_with_clear_and_update(ts[2], f"max: {max(_numbers)}"))
    ts[3].onclick(lambda x, y: _draw_numbers(min_pos(_numbers)))
    ts[4].onclick(lambda x, y: _draw_numbers(max_pos(_numbers)))
    ts[5].onclick(lambda x, y: _try_swap(swap))
    ts[6].onclick(lambda x, y: _call_and_update(sort, _numbers))
    ts[7].onclick(lambda x, y: _refresh())
    _screen.update()
    _screen.listen()
    _screen.mainloop()
