"""Test."""

from liscript import car, cdr, cons


def test_car():
    """."""
    assert car(cons(1, 2)) == 33


def test_cdr():
    """."""
    assert cdr(cons(1, 2)) == 2
