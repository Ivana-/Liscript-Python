"""Lesson 1"""

import re
import types  # only if cons/car/cdr done as lambdas
from enum import Enum

# CONS / CAR / CDR


# 1-st variant
# def cons(x, y): return x, y
# def car(l):     return l[0]
# def cdr(l):     return l[1]
# conslistClass = tuple

# 2-nd variant
# class ConsList:
#     def __init__(self, x, y): self.car, self.cdr = x, y

# def cons(x, y): return ConsList(x, y)
# def car(l):     return l.car
# def cdr(l):     return l.cdr
# conslistClass = ConsList

# 3-rd variant
def cons(x, y): return lambda f: f(x, y)
def car(l):     return l(lambda x, y: x)
def cdr(l):     return l(lambda x, y: y)
conslistClass = types.FunctionType


# nil is allways the same :)
nil = cons(None, None)
# def isnull(t):  return t == nil
def isnull(t):  return car(t) is None and cdr(t) is None


# TYPES / ENUMS


class BO(Enum):
    ADD, SUB, MUL, DIV, MOD, SCONCAT = range(6)

class BP(Enum):
    GT, GTE, LT, LTE, EQ, NOEQ = range(6)

class SF(Enum):
    (DEF, SET, GET, QUOTE, TYPEOF, CONS, CAR, CDR, COND, PRINT, READ,
     EVAL, EVALIN, LAMBDA, MACRO, MACROEXPAND) = range(16)

keywords_kv = {
    '+': BO.ADD,
    '-': BO.SUB,
    '*': BO.MUL,
    '/': BO.DIV,
    'mod': BO.MOD,
    '++': BO.SCONCAT,
    '>': BP.GT,
    '>=': BP.GTE,
    '<': BP.LT,
    '<=': BP.LTE,
    '=': BP.EQ,
    '/=': BP.NOEQ,
    'def': SF.DEF,
    'set!': SF.SET,
    'get': SF.GET,
    'quote': SF.QUOTE,
    'typeof': SF.TYPEOF,
    'cons': SF.CONS,
    'car': SF.CAR,
    'cdr': SF.CDR,
    'cond': SF.COND,
    'print': SF.PRINT,
    'read': SF.READ,
    'eval': SF.EVAL,
    'eval-in': SF.EVALIN,
    'lambda': SF.LAMBDA,
    'macro': SF.MACRO,
    'macroexpand': SF.MACROEXPAND
}

keywords_vk = dict(zip(keywords_kv.values(), keywords_kv.keys()))


class Symbol:
    def __init__(self, s):
        self.value = s


# READ / SHOW


def prsval(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    elif s in keywords_kv:
        return keywords_kv[s]
    else:
        try:
            return int(s)
        except Exception:
            try:
                return float(s)
            except Exception:
                return Symbol(s)


def prslist(s):
    s = s.lstrip()
    if not s:
        raise ValueError('closed \')\' is absent')
    elif s[0] == ')':
        return nil, s[1:]
    else:
        x, ss = prs(s)
        t, zz = prslist(ss)
        return cons(x, t), zz

def subs(s): return s if len(s) < 20 else s[0:20] + '...'

def prs(s):
    s = s.lstrip()
    if not s:
        return nil, ''

    c, z = s[0], s[1:]
    if c == '(':
        return prslist(z)
    elif c == ')':
        raise ValueError('extra closed \')\': ' + subs(s))
    elif c == '\"':
        try:
            a, b = re.search('\"', z).span()
            return z[0:a], z[b:]
        except Exception:
            raise ValueError('closed \'\"\' is absent: ' + subs(s))
    elif c == ';':
        try:
            a, b = re.search(';', z).span()
            return prs(z[b:])
        except Exception:
            raise ValueError('closed \';\' is absent: ' + subs(s))
    elif c == '\'':
        x, ss = prs(z)
        return cons(SF.QUOTE, cons(x, nil)), ss
    else:
        a, b = re.search('\s|\(|\)|\"|;|$', s).span()
        return prsval(s[0:a]), s[a:]


def parse(s):
    x, ss = prs(s)
    if not ss.strip():
        return x
    y, zz = prs('(' + ss + ')')
    if not zz.strip():
        return cons(x, y)
    else:
        raise ValueError('extra symbols: ' + subs(zz))



def show(o):
    if isinstance(o, conslistClass):
        r = ''
        while not isnull(o):
            r, o = r + ' ' + show(car(o)), cdr(o)
        return '(' + r.lstrip() + ')'
    elif o in keywords_vk:
        return keywords_vk[o]
    elif isinstance(o, Symbol):
        return o.value
    elif isinstance(o, bool):
        return 'true' if o else 'false'
    elif isinstance(o, str):
        return '"' + o + '"'
    else:
        return str(o)


# REPL utils


def repl():
    print('Lesson 1  - cons,car,cdr & parser')
    while True:
        s = input('>>> ').strip()
        if s == ':q':
            break
        try:
            o = parse(s)
            print(show(o))
        except Exception as ex:
            print('PARSING ERROR: ' + str(ex))

# repl()
