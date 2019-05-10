"""Lesson 4"""

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

class Lambda:
    def __init__(self, a, b, e):
        self.args, self.body, self.env = a, b, e

class Macro:
    def __init__(self, a, b):
        self.args, self.body = a, b

class LambdaCall:
    def __init__(self, l, fr):
        self.lam, self.frame = l, fr


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
    def __init__(self, m, p):
        self.frame, self.parent = m, p

    def setvar(self, k, v):
        e = self
        while e is not None:
            if k in e.frame:
                e.frame[k] = v
                break
            e = e.parent

    def getvar(self, k, s):
        e = self
        while e is not None:
            if k in e.frame:
                return e.frame[k]
            e = e.parent
        return s if isinstance(s, Symbol) else Symbol(k)

    def defvar(self, k, v):
        self.frame[k] = v


# EVAL utils


def objectsAreEqual(x, y):
    if isinstance(x, (int, float, complex)) and isinstance(y, (int, float, complex)):
        return x == y
    elif type(x) != type(y):
        return False
    elif isinstance(x, Symbol):
        return x.value == y.value
    elif isinstance(x, conslistClass):
        while not isnull(x) and not isnull(y):
            if not objectsAreEqual(car(x), car(y)):
                return False
            x, y = cdr(x), cdr(y)
        return isnull(x) and isnull(y)
    else:
        return x == y


def bo(op, a, b):
    if   op == BO.ADD: return a + b
    elif op == BO.SUB: return a - b
    elif op == BO.MUL: return a * b
    elif op == BO.DIV: return a / b
    elif op == BO.MOD: return a % b
    elif op == BO.SCONCAT: return (a if isinstance(a, str) else show(a)) + (b if isinstance(b, str) else show(b))
    else: return None


def foldbo(op, t, e, d):
    if isnull(t):
        raise ValueError('no operands for ariphmetic operation: ' + op)
    r, t = evalrec(car(t), e, d, True), cdr(t)
    while not isnull(t):
        r, t = bo(op, r, evalrec(car(t), e, d, True)), cdr(t)
    return r


def bp(op, a, b):
    if   op == BP.GT:   return a > b
    elif op == BP.GTE:  return a >= b
    elif op == BP.LT:   return a < b
    elif op == BP.LTE:  return a <= b
    elif op == BP.EQ:   return objectsAreEqual(a, b)  # a == b
    elif op == BP.NOEQ: return not objectsAreEqual(a, b)  # a != b
    else:               return None


def foldbp(op, t, e, d):
    if isnull(t):
        return True
    a, t = evalrec(car(t), e, d, True), cdr(t)
    while not isnull(t):
        b = evalrec(car(t), e, d, True)
        if not bp(op, a, b):
            return False
        a, t = b, cdr(t)
    return True


def evalListToArray(t, e, d):
    m = []
    while not isnull(t):
        m.append(evalrec(car(t), e, d, True))
        t = cdr(t)
    return m


def objectEvalToSymbolName(o, e, d):
    if isinstance(o, Symbol):
        return o.value
    elif isinstance(o, str):
        return o
    else:
        s = show(evalrec(o, e, d, True))
        return s[1:-1] if s[0] == '"' and s[-1] == '"' else s


def getBody(o):
    return car(o) if (isinstance(o, conslistClass) and not isnull(o) and isnull(cdr(o))) else o


def getMapNamesValues(ns, bs, e, d, evalFlag):
    r = {}
    while not isnull(ns) and not isnull(bs):
        if isnull(cdr(ns)) and not isnull(cdr(bs)):
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
    if isinstance(body, Symbol):
        return kv.get(body.value, body)
    elif isinstance(body, conslistClass):
        return nil if isnull(body) else cons(macroSubst(car(body), kv), macroSubst(cdr(body), kv))
    else:
        return body


def macroexpand(m, t, e, d):
    return macroSubst(m.body, getMapNamesValues(m.args, t, e, d, False))


def getTypeName(o):
    return 'ConsList' if isinstance(o, conslistClass) else type(o).__name__


# EVAL recursive

evalCalls, maxStack, TCOFlag, showStatFlag = 0, 0, True, False
symbolOK = Symbol('OK')


def evalrec(o, e, stacklevel, strict):
    global evalCalls, maxStack
    evalCalls, maxStack, d = evalCalls + 1, max(maxStack, stacklevel + 1), stacklevel + 1

    if isinstance(o, Symbol):
        return e.getvar(o.value, o)
    elif isinstance(o, conslistClass):
        if isnull(o):
            return o
        t = cdr(o)
        h = evalrec(car(o), e, d, strict if isnull(t) else True)

        if isinstance(h, BO):
            return foldbo(h, t, e, d)
        elif isinstance(h, BP):
            return foldbp(h, t, e, d)
        elif isinstance(h, SF):

            if h == SF.DEF or h == SF.SET:
                while not isnull(t) and not isnull(cdr(t)):
                    s, v = objectEvalToSymbolName(car(t), e, d), evalrec(car(cdr(t)), e, d, True)
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
                    v, lst = x if lst and isinstance(x, conslistClass) else cons(x, v), False
                return v

            elif h == SF.CAR:
                a = evalrec(car(t), e, d, True)
                return car(a) if isinstance(a, conslistClass) else a

            elif h == SF.CDR:
                a = evalrec(car(t), e, d, True)
                return cdr(a) if isinstance(a, conslistClass) else nil

            elif h == SF.COND:
                while not isnull(t) and not isnull(cdr(t)):
                    if evalrec(car(t), e, d, True):
                        return evalrec(car(cdr(t)), e, d, strict)
                    t = cdr(cdr(t))
                return nil if isnull(t) else evalrec(car(t), e, d, strict)

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
                return evalrec(getBody(cdr(t)), a.env, d, True) if isinstance(a, Lambda) else None

            elif h == SF.LAMBDA:
                return Lambda(car(t), getBody(cdr(t)), e)

            elif h == SF.MACRO:
                return Macro(car(t), getBody(cdr(t)))

            elif h == SF.MACROEXPAND:
                a = evalrec(car(t), e, d, True)
                return macroexpand(a, cdr(t), e, d) if isinstance(a, Macro) else None

            else:
                raise ValueError('Unrecognized special form \'' + h + '\'')
                # return None

        elif isinstance(h, Lambda):
            if not TCOFlag:
                return evalrec(
                    h.body, Env(getMapNamesValues(h.args, t, e, d, True), h.env), d, True)
            else:
                v = LambdaCall(h, getMapNamesValues(h.args, t, e, d, True))
                if strict:
                    while isinstance(v, LambdaCall):
                        v = evalrec(v.lam.body, Env(v.frame, v.lam.env), d, False)
                return v
        elif isinstance(h, Macro):
            return evalrec(macroexpand(h, t, e, d), e, d, True)
        else:
            v = h
            while not isnull(t):
                v, t = evalrec(car(t), e, d, strict if isnull(cdr(t)) else True), cdr(t)
            return v
    else:
        return o


# REPL utils


def evallisp(s):
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
    try:
        with open(filename) as f:
            s = f.read()
    except IOError as err:
        print('FILE ERROR: ' + str(err))
        return
    evallisp(s)


def replcmd(s):
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
    if s: replcmd(s) if s[0] == ':' else evallisp(s)


lastInput = ''
globalenv = Env({}, None)


def repl():
    global lastInput
    print('Lesson 4  - Macro & repl commands & standard library ------- TCO & eval-in & different cons variants & etc.')
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
