"""This module."""

import re
from enum import Enum

# TYPES / ENUMS


def cons(x, y):
    """."""
    return (x, y)


def car(l):
    """."""
    return l[0]


def cdr(l):
    """."""
    return l[1]


nil = (None, None)


class BO(Enum):
    """."""

    ADD, SUB, MUL, DIV, MOD, SCONCAT = range(6)


class BP(Enum):
    """."""

    GT, GTE, LT, LTE, EQ, NOEQ = range(6)


class SF(Enum):
    """."""

    (DEF, SET, GET, QUOTE, TYPEOF, CONS, CAR, CDR, COND, PRINT, READ, EVAL,
     EVALIN, LAMBDA, MACRO, MACROEXPAND) = range(16)


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
    """."""

    def __init__(self, s):
        """."""
        self.value = s


class Lambda:
    """."""

    def __init__(self, a, b, e):
        """."""
        self.args, self.body, self.env = a, b, e


class Macro:
    """."""

    def __init__(self, a, b):
        """."""
        self.args, self.body = a, b


class LambdaCall:
    """."""

    def __init__(self, l, fr):
        """."""
        self.lam, self.frame = l, fr


# READ / SHOW


def prsval(s):
    """."""
    if s == 'true':
        return True
    elif s == 'false':
        return False
    elif s in keywords_kv:
        return keywords_kv[s]
    else:
        try:
            return int(s)
        except Exception as ex:
            try:
                return float(s)
            except Exception as ex:
                return Symbol(s)


def prslist(s):
    """."""
    (x, ss) = prs(s)
    if x is None:
        return (nil, ss)
    else:
        (t, zz) = prslist(ss)
        return (cons(x, t), zz)


def prs(ss):
    """."""
    s = ss.lstrip()
    if not s:
        return (None, '')

    c, z = s[0], s[1:]
    if c == '(':
        return prslist(z)
    elif c == ')':
        return (None, z)
    elif c == '\"':
        try:
            (a, b) = re.search('\"', z).span()
        except Exception as ex:
            raise ValueError('closed \'\"\' is absent: ' +
                             (s if len(s) < 20 else s[0:20] + '...'))
        return (z[0:a], z[b:])
    elif c == ';':
        try:
            (a, b) = re.search(';', z).span()
        except Exception as ex:
            raise ValueError('closed \';\' is absent: ' +
                             (s if len(s) < 20 else s[0:20] + '...'))
        return prs(z[b:])
    elif c == '\'':
        (x, ss) = prs(z)
        return (cons(SF.QUOTE, cons(x, nil)), ss)
    else:
        (a, b) = re.search('\s|\(|\)|\"|;|$', s).span()
        return (prsval(s[0:a]), s[a:])


def parse(s):
    """."""
    (x, ss) = prs(s)
    return x if not ss.strip() else cons(x, prslist(ss)[0])


def show(o):
    """."""
    if isinstance(o, tuple):
        r = ''
        while o != nil:
            r, o = r + ' ' + show(car(o)), cdr(o)
        return '(' + r.lstrip() + ')'
    elif o in keywords_vk:
        return keywords_vk[o]
    elif isinstance(o, Symbol):
        return o.value
    elif isinstance(o, bool):
        return 'true' if o else 'false'
    elif isinstance(o, Lambda):
        return '(lambda ' + show(o.args) + ' ' + show(o.body) + ')'
    elif isinstance(o, Macro):
        return '(macro ' + show(o.args) + ' ' + show(o.body) + ')'
    elif isinstance(o, LambdaCall):
        return 'LAMBDA-CALL: ' + str(o.frame)
    elif isinstance(o, str):
        return '"' + o + '"'
    else:
        return str(o)


# ENVIRONMENT


class Env:
    """."""

    def __init__(self, m, p):
        """."""
        self.frame, self.parent = m, p

    def setvar(self, k, v):
        """."""
        e = self
        while e is not None:
            if k in e.frame:
                e.frame[k] = v
                break
            e = e.parent

    def getvar(self, k, s):
        """."""
        e = self
        while e is not None:
            if k in e.frame:
                return e.frame[k]
            e = e.parent
        return s if isinstance(s, Symbol) else Symbol(k)

    def defvar(self, k, v):
        """."""
        self.frame[k] = v


# EVAL utils


def objectsAreEqual(x, y):
    """."""
    if isinstance(x, (int, float, complex)) and isinstance(
            y, (int, float, complex)):
        return x == y
    elif type(x) != type(y):
        return False
    elif isinstance(x, Symbol):
        return x.value == y.value
    elif isinstance(x, tuple):
        while not x == nil and not y == nil:
            if not objectsAreEqual(car(x), car(y)):
                return False
            x, y = cdr(x), cdr(y)
        return x == nil and y == nil
    else:
        return x == y


def bo(op, a, b):
    """."""
    if op == BO.ADD:
        return a + b
    elif op == BO.SUB:
        return a - b
    elif op == BO.MUL:
        return a * b
    elif op == BO.DIV:
        return a / b
    elif op == BO.MOD:
        return a % b
    elif op == BO.SCONCAT:
        return (a if isinstance(a, str) else show(a)) + (b if isinstance(
            b, str) else show(b))
    else:
        return None


def foldbo(op, t, e, d):
    """."""
    if t == nil:
        raise ValueError('no operands for ariphmetic operation: ' + op)
    r, t = evalrec(car(t), e, d, True), cdr(t)
    while t != nil:
        r, t = bo(op, r, evalrec(car(t), e, d, True)), cdr(t)
    return r


def bp(op, a, b):
    """."""
    if op == BP.GT:
        return a > b
    elif op == BP.GTE:
        return a >= b
    elif op == BP.LT:
        return a < b
    elif op == BP.LTE:
        return a <= b
    elif op == BP.EQ:
        return objectsAreEqual(a, b)  # a == b
    elif op == BP.NOEQ:
        return not objectsAreEqual(a, b)  # a != b
    else:
        return None


def foldbp(op, t, e, d):
    """."""
    if t == nil:
        return True
    a, t = evalrec(car(t), e, d, True), cdr(t)
    while t != nil:
        b = evalrec(car(t), e, d, True)
        if not bp(op, a, b):
            return False
        a, t = b, cdr(t)
    return True


def evalListToArray(t, e, d):
    """."""
    m = []
    while t != nil:
        m.append(evalrec(car(t), e, d, True))
        t = cdr(t)
    return m


def objectEvalToSymbolName(o, e, d):
    """."""
    if isinstance(o, Symbol):
        return o.value
    elif isinstance(o, str):
        return o
    else:
        s = show(evalrec(o, e, d, True))
        return s[1:-1] if s[0] == '"' and s[-1] == '"' else s


def getBody(o):
    """."""
    return car(o) if (isinstance(o, tuple) and not o == nil
                      and cdr(o) == nil) else o


def getMapNamesValues(ns, bs, e, d, evalFlag):
    """."""
    r = {}
    while not ns == nil and not bs == nil:
        if cdr(ns) == nil and not cdr(bs) == nil:
            if evalFlag:
                m, v = evalListToArray(bs, e, d), nil
                for x in reversed(m):
                    v = cons(x, v)
            else:
                v = bs
        else:
            v = evalrec(car(bs), e, d, True) if evalFlag else car(bs)
        r[car(ns).value], ns, bs = v, cdr(ns), cdr(bs)
    return r


def macroSubst(body, kv):
    """."""
    if isinstance(body, Symbol):
        return kv.get(body.value, body)
    elif isinstance(body, tuple):
        return nil if body == nil else cons(
            macroSubst(car(body), kv), macroSubst(cdr(body), kv))
    else:
        return body


def macroexpand(m, t, e, d):
    """."""
    return macroSubst(m.body, getMapNamesValues(m.args, t, e, d, False))


def getTypeName(o):
    """."""
    return 'ConsList' if isinstance(o, tuple) else type(o).__name__


# EVAL recursive

evalCalls, maxStack, TCOFlag, showStatFlag = 0, 0, True, False
symbolOK = Symbol('OK')


def evalrec(o, e, stacklevel, strict):
    """."""
    global evalCalls, maxStack
    evalCalls, maxStack, d = evalCalls + \
        1, max(maxStack, stacklevel + 1), stacklevel + 1

    if isinstance(o, Symbol):
        return e.getvar(o.value, o)
    elif isinstance(o, tuple):
        if o == nil:
            return o
        t = cdr(o)
        h = evalrec(car(o), e, d, strict if t == nil else True)

        if isinstance(h, BO):
            return foldbo(h, t, e, d)
        elif isinstance(h, BP):
            return foldbp(h, t, e, d)
        elif isinstance(h, SF):

            if h == SF.DEF or h == SF.SET:
                while not t == nil and not cdr(t) == nil:
                    s, v = objectEvalToSymbolName(car(t), e, d), evalrec(
                        car(cdr(t)), e, d, True)
                    e.defvar(s, v) if h == SF.DEF else e.setvar(s, v)
                    t = cdr(cdr(t))
                return symbolOK

            elif h == SF.GET:
                s = car(t)
                return e.getvar(objectEvalToSymbolName(s, e, d), s)

            elif h == SF.QUOTE:
                return car(t)

            elif h == SF.TYPEOF:
                return getTypeName(evalrec(car(t), e, d, True))

            elif h == SF.CONS:
                m, v, lst = evalListToArray(t, e, d), nil, True
                for x in reversed(m):
                    v, lst = x if lst and isinstance(x, tuple) else cons(
                        x, v), False
                return v

            elif h == SF.CAR:
                a = evalrec(car(t), e, d, True)
                return car(a) if isinstance(a, tuple) else a

            elif h == SF.CDR:
                a = evalrec(car(t), e, d, True)
                return cdr(a) if isinstance(a, tuple) else nil

            elif h == SF.COND:
                while not t == nil and not cdr(t) == nil:
                    if evalrec(car(t), e, d, True):
                        return evalrec(car(cdr(t)), e, d, strict)
                    t = cdr(cdr(t))
                return nil if t == nil else evalrec(car(t), e, d, strict)

            elif h == SF.PRINT or h == SF.READ:
                m, s = evalListToArray(t, e, d), ''
                for x in m:
                    s += x if isinstance(x, str) else show(x)
                if h == SF.PRINT:
                    print(s)
                    return symbolOK
                else:
                    return parse(input(s))

            elif h == SF.EVAL:
                return evalrec(evalrec(car(t), e, d, True), e, d, True)

            elif h == SF.EVALIN:
                a = evalrec(car(t), e, d, True)
                return evalrec(getBody(cdr(t)), a.env, d, True) if isinstance(
                    a, Lambda) else None

            elif h == SF.LAMBDA:
                return Lambda(car(t), getBody(cdr(t)), e)

            elif h == SF.MACRO:
                return Macro(car(t), getBody(cdr(t)))

            elif h == SF.MACROEXPAND:
                a = evalrec(car(t), e, d, True)
                return macroexpand(a, cdr(t), e,
                                   d) if isinstance(a, Macro) else None

            else:
                raise ValueError('Unrecognized special form \'' + h + '\'')
                return None

        elif isinstance(h, Lambda):
            if not TCOFlag:
                return evalrec(
                    h.body, Env(
                        getMapNamesValues(h.args, t, e, d, True), h.env), d,
                    True)
            else:
                v = LambdaCall(h, getMapNamesValues(h.args, t, e, d, True))
                if strict:
                    while isinstance(v, LambdaCall):
                        v = evalrec(v.lam.body, Env(v.frame, v.lam.env), d,
                                    False)
                return v
        elif isinstance(h, Macro):
            return evalrec(macroexpand(h, t, e, d), e, d, True)
        else:
            v = h
            while t != nil:
                v, t = evalrec(
                    car(t), e, d, strict if cdr(t) == nil else True), cdr(t)
            return v
    else:
        return o


# REPL utils


def evallisp(s):
    """."""
    global evalCalls, maxStack
    evalCalls, maxStack = 0, 0
    try:
        o = parse(s)
    except Exception as ex:
        print('PARSING ERROR: ' + str(ex))
        return
    # print(show(o))
    try:
        r = evalrec(o, globalenv, 0, True)
    except Exception as ex:
        print('EVAL ERROR: ' + str(ex))
        return
    print(show(r))
    if showStatFlag:
        print('max stack: ' + str(maxStack) + ', eval calls: ' +
              str(evalCalls))


def loadfile(filename):
    """."""
    try:
        with open(filename) as f:
            s = f.read()
    except IOError as err:
        print('FILE ERROR: ' + str(err))
        return
    evallisp(s)


def replcmd(s):
    """."""
    global TCOFlag, showStatFlag
    m = s.split()
    cmd = m[0]
    if cmd == ':l':
        loadfile(m[1])
    elif cmd == ':':
        evalinput(lastInput)
    elif cmd == ':help':
        loadfile('help.liscript')
    elif cmd == ':tco':
        TCOFlag = not TCOFlag
    elif cmd == ':stat':
        showStatFlag = not showStatFlag
    else:
        print('bad REPL command: ' + cmd)


def evalinput(s):
    """."""
    if s:
        replcmd(s) if s[0] == ':' else evallisp(s)


lastInput = ''
globalenv = Env({}, None)


def repl():
    """."""
    global lastInput
    loadfile('standard_library.liscript')
    # loadfile('demo2.liscript')
    while True:
        s = input(('t' if TCOFlag else 'n') + ' >>> ').strip()
        if s == ':q':
            break
        if s != ':':
            lastInput = s
        evalinput(s)


# repl()
