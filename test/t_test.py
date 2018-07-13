"""Test."""

import unittest

from liscript.liscript import car, cdr, cons

# def test_car():
#     """."""
#     assert car(cons(1, 2)) == 1


# def test_cdr():
#     """."""
#     assert cdr(cons(1, 2)) == 2

class TestConsCarCdr(unittest.TestCase):
    """."""

    def test_car(self):
        """."""
        self.assertEqual(car(cons(1, 2)), 1)

    def test_cdr(self):
        """."""
        self.assertEqual(cdr(cons(1, 2)), 2)


class TestStringMethods(unittest.TestCase):
    """."""

    def test_upper(self):
        """."""
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        """."""
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        """."""
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
