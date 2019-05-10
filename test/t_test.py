"""Test."""

import unittest

from liscript.liscript import (SF, car, cdr, cons, evalrec, globalenv,
                               loadfile, nil, objectsAreEqual, parse, show)


class TestConsCarCdr(unittest.TestCase):
    def test_carcdr(self):
        self.assertEqual(car(cons(1, 2)), 1)
        self.assertEqual(cdr(cons(1, 2)), 2)
        self.assertEqual(car(car(cons(cons(1, 2), 3))), 1)
        self.assertEqual(cdr(cdr(cons(0, cons(1, 2)))), 2)
        self.assertEqual(car(cdr(cons(0, cons(1, 2)))), 1)


class TestParse(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse('  '), None)
        self.assertEqual(parse(')'), None)
        self.assertTrue(objectsAreEqual(parse('()'), nil))

        self.assertEqual(parse(' 1 '), 1)
        self.assertEqual(parse(' 1.1 '), 1.1)
        self.assertEqual(parse("\"1.1\""), '1.1')
        self.assertEqual(parse("\"a;bc;d\""), 'a;bc;d')

        self.assertTrue(objectsAreEqual(parse("'1.1"),
                                        cons(SF.QUOTE, cons(1.1, nil))))

        v = cons(1, cons(2, nil))
        self.assertTrue(objectsAreEqual(parse(' 1 2 '), v))
        self.assertTrue(objectsAreEqual(parse(' (1 2) '), v))
        self.assertTrue(objectsAreEqual(parse(" 1;ghg\" bz zbsfb\" sd;2 "), v))
        self.assertTrue(objectsAreEqual(parse(' 1\n2 '), v))
        self.assertTrue(objectsAreEqual(parse(' (1 2 '), v))
        self.assertTrue(objectsAreEqual(parse(' 1 2))))) '), v))


class TestShow(unittest.TestCase):
    def test_show(self):
        self.assertEqual(show(nil), '()')
        self.assertEqual(show(cons(1, cons(2, nil))), '(1 2)')


class TestEvalLisp(unittest.TestCase):
    def test_evallisp(self):
        def __eval(s): return evalrec(parse(s), globalenv, 0, True)

        def __evalshow(s): return show(__eval(s))

        self.assertEqual(__eval('+ 1 2 3'), 6)

        loadfile('standard_library.liscript')

        self.assertTrue(objectsAreEqual(__eval("cdr '(0 1 2)"),
                                        cons(1, cons(2, nil))))
        self.assertEqual(__evalshow("cdr '(0 1 2)"), '(1 2)')
        self.assertEqual(__evalshow('def l (list-from-to 1 5)'), 'OK')
        self.assertEqual(__evalshow('l'), '(1 2 3 4 5)')
        self.assertEqual(__evalshow('map (lambda (x) + 1 x) l'), '(2 3 4 5 6)')


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
