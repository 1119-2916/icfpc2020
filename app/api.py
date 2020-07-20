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
    eval,
)
from reader import (
    isNumerical,
)
from util import (
    mod,
    dem,
)

pat = re.compile(r'[01]+')

def call_api(query):
    response = requests.post(
        'https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=***REMOVED***',
        query)
    if not pat.match(response.text):
        raise Exception('通信エラー！変なの送られてきた！ - {}'.format(response.text))
    return response.text

def send_message(expr):
    query = mod(expr)
    print("send: {}".format(query))
    raw = call_api(query)
    answer = dem(raw)
    print("recieved: {}".format(raw))
    return answer

if __name__ == '__main__':
    print(mod(dem('1101100001111101100010110110001100110110010000')))
