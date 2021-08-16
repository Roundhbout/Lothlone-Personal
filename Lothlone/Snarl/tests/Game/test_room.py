import pytest

from Snarl.src.Game.room import Room


origin = (0, 0)
size = (5, 5)
doors = [(4, 2)]


def test_invalid_origin1(layout):
    with pytest.raises(ValueError):
        Room((-2, -2), size, layout, [])


def test_invalid_origin2(layout):
    with pytest.raises(ValueError):
        Room((3, -3), size, layout, [])


def test_invalid_origin3(layout):
    with pytest.raises(ValueError):
        Room((-3, 3), size, layout, [])


def test_invalid_size1(layout):
    with pytest.raises(ValueError):
        Room(origin, (-5, 5), layout, [])


def test_invalid_size2(layout):
    with pytest.raises(ValueError):
        Room(origin, (5, -3), layout, [])


def test_invalid_size3(layout):
    with pytest.raises(ValueError):
        Room(origin, (5, 4), layout, [])


def test_invalid_size4(layout):
    with pytest.raises(ValueError):
        Room(origin, (4, 5), layout, [])


def test_invalid_size5():
    with pytest.raises(ValueError):
        Room(origin, (0, 0), [], [])


def test_invalid_tile_dimensions1():
    with pytest.raises(ValueError):
        Room(origin, (2, 2), [['.', '.'], []], [])


def test_invalid_tile_dimensions2():
    with pytest.raises(ValueError):
        Room(origin, (2, 2), [[], ['.', '.']], [])


def test_invalid_tile_dimensions3():
    with pytest.raises(ValueError):
        Room(origin, (2, 2), [['.'], ['.']], [])


def test_invalid_tile_dimensions4():
    with pytest.raises(ValueError):
        Room(origin, (2, 2), [['.'], ['.', '.']], [])


def test_invalid_doors1(layout):
    with pytest.raises(ValueError):
        Room(origin, size, layout, [(3, 3)])


def test_invalid_doors2(layout):
    with pytest.raises(ValueError):
        Room(origin, size, layout, [(1, 3)])


def test_invalid_doors3(layout):
    with pytest.raises(ValueError):
        Room(origin, size, layout, [(3, 3)])


def test_render1(room1):
    render = str(room1)
    expected = '.   .   .   .   .   \n.   .   .   .   .   \n.   .   .   .   |   \n.   .   .   .   .   \n.   .   . ' \
               '  .   .   '
    assert (render == expected)


def test_render2(room3):
    render = str(room3)
    expected = '.   .   .   .   .   .   \n.   .   .   .   .   .   \n|   .   .   .   .   .   \n.   .   .   .   .   .   ' \
               '\n.   .   .   .   .   .   '
    assert (render == expected)
