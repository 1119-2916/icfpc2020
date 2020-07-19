# coding: utf-8
import requests
import re
from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
from parse import (
    asNum,
)
from reader import (
    isNumerical,
)
from preamble import (
    to_list,
    to_expr,
)

pat = re.compile(r'[01]+')

def call_api(query):
    response = requests.post(
        'https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=c6dcbd02334345a88a93a7bd0ee7a07a',
        query)
    if not pat.match(response.text):
        raise Exception('通信エラー！変なの送られてきた！ - {}'.format(response.text))
    return response.text

def mod_num(num):
    if num == 0:
        return '010'
    res = ''
    if num < 0:
        num = -num
        res += '10'
    else:
        res += '01'
    ln = 1
    pln = 4
    nowMax = 2 ** 4
    while nowMax <= num:
        ln += 1
        pln += 4
        nowMax *= 2 ** 4
    res += '1' * ln + '0'
    numstr = ''
    for i in range(pln):
        numstr += str(num % 2)
        num = num // 2
    return res + numstr[::-1]


def mod(expr):
    if type(expr) is Atom:
        if isNumerical(expr.Name):
            return mod_num(asNum(expr))
        raise Exception('parse error: mod: illegal num: {}'.format(expr.Name))
    return "".join(["11" + mod(el) for el in to_list(expr)]) + "1100"

def dem_len_num(p):
    ln = 0
    while True:
        if p.isEnd():
            raise Exception('parse error: illegal number')
        if p.get() == '0':
            break
        ln += 4

    num = 0
    for i in range(ln):
        num *= 2
        num += int(p.get())

    return num


def dem0(p):
    head = p.get(2)
    if head == '00':
        return nil
    elif head == '01':
        return Atom(str(dem_len_num(p)))
    elif head == '10':
        return Atom(str(-1 * dem_len_num(p)))
    elif head == '11':
        ls = []
        while True:
            if p.peek(2) == '11':
                p.get(2)
            if p.peek(2) == '00':
                p.get(2)
                return to_expr(ls)
            ls.append(dem0(p))
    raise Exception('parse error: dem0')

def dem(bitseq):
    p = Parser(bitseq)
    return dem0(p)

def send_message(expr):
    query = mod(expr)
    answer = dem(call_api(query))
    return answer


class Parser:
    def __init__(self, ls):
        self.ls = ls
        self.ptr = 0

    def isEnd(self):
        return len(self.ls) <= self.ptr

    def peek(self, n=1):
        return self.ls[self.ptr : self.ptr+n]

    def get(self, n=1):
        s = self.ls[self.ptr : self.ptr+n]
        self.ptr += n
        return s


if __name__ == '__main__':
    print(mod(dem('1101100001110110010011011000101110100100111110110001010001110111001000000100011011100001001111001100')))
