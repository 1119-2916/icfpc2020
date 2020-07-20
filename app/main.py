import requests
import sys
from util import (
    mod,
    dem,
    to_expr,
)
sys.setrecursionlimit(1000000)

def send(server_url, request):
    print(request)
    res = requests.post(server_url + "/aliens/send", data=request)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    print('Server response:', res.text)
    return dem(res.text)

def makeJoinRequest(player_key):
    return mod(to_expr([2, player_key]))

def makeStartRequest(player_key, gameResponse, x0, x1, x2, x3):
    # x3 should be >= 1
    return mod(to_expr([3, player_key, [x0, x1, x2, x3]]))

def makeCommandsRequest(player_key, gameResponse):
    return mod(to_expr([4, player_key, makeCommands(gameResponse)]))

def makeCommands(gameResponse):
    # 一切コマンド作らず、動かない
    return []

def makeAccelerateCommand(gameResponse, shipId, vector):
    return [0, shipId, vector]

def makeDenoteCommand(gameResponse, shipId):
    return [1, shipId]

def makeShootCommand(gameResponse, shipId, target, x3):
    return [2, shipId, target, x3]

def isGameEnd(gameResponse):
    [x1, gameStage, staticGameInfo, gameState] = gameResponse
    return gameStage == 2

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('server_url: %s; player_key: %s' % (server_url, player_key))

    joinRequest = makeJoinRequest(player_key)
    gameResponse = send(server_url, joinRequest)

    startRequest = makeStartRequest(player_key, gameResponse, 1, 1, 1, 1)
    gameResponse = send(server_url, startRequest)

    while not isGameEnd(gameResponse):
        commandsRequest = makeCommandsRequest(player_key, gameResponse)
        gameResponse = send(server_url, commandsRequest)

    res = requests.post(server_url, data=player_key)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    print('Server response:', res.text)

if __name__ == '__main__':
    main()
