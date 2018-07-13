"""Test."""

from liscript import car, cdr, cons


def test_car():
    """."""
    assert car(cons(1, 2)) == 1


def test_cdr():
    """."""
    assert cdr(cons(1, 2)) == 2
