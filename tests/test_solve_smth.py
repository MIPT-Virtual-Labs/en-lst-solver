from solver_dummy.functions import cube, square


def test_square():
    assert square(0) == 0
    assert square(1) == 1
    assert square(2) == square(-2)
    assert square(-2) == 4


def test_cube():
    assert cube(0) == 0
    assert cube(1) == 1
    assert cube(2) == -cube(-2)
    assert cube(-2) == -8
