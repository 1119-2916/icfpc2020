import requests
import sys
from reader import (
    
)
from util import (
    mod,
    dem,
    to_expr,
)

def send(request):
    res = requests.post(server_url, data=request)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    print('Server response:', res.text)
    return dem(res.text)

def makeJoinRequest(playerKey):
    return mod(to_expr([2, playerKey]))

def makeStartRequest(playerKey, gameResponse, x0, x1, x2, x3):
    # x3 should be >= 1
    return mod(to_expr([3, playerKey, [x0, x1, x2, x3]]))

def makeCommandsRequest(playerKey, gameResponse):
    return mod(to_expr([4, playerKey, makeCommand(gameResponse)]))

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
    (1, gameStage, staticGameInfo, gameState) = gameResponse
    return gameStage == 2

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    joinRequest = makeJoinRequest(playerKey)
    gameResponse = send(serverUrl, joinRequest)

    startRequest = makeStartRequest(playerKey, gameResponse, 1, 1, 1, 1)
    gameResponse = send(serverUrl, startRequest)

    while not isGameEnd(gameResponse):
        commandsRequest = makeCommandsRequest(playerKey, gameResponse)
        gameResponse = send(serverUrl, commandsRequest)

    res = requests.post(server_url, data=player_key)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    print('Server response:', res.text)

if __name__ == '__main__':
    main()
