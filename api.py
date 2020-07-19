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

pat = re.compile(r'[01]+')

def call_api(query):
    response = requests.post(
        'https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=***REMOVED***',
        query)
    if not pat.match(response.text):
        raise Exception('通信エラー！変なの送られてきた！ - {}'.format(response.text))
    return response.text

def mod(expr):
    return hoge

def dem0(p):
    head = p.get(2)
    if head == '00':
        return 

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
