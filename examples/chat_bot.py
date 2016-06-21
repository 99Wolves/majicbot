# Chatbot for Blockheads. This bot uses the api of the great cleverbot and therefor
# requires the cleverbot package to be installed. The bot answers to every message send
# except these send by the server. For simplicity's sake ConnectionError exceptions
# are not caught. This is poor style and should not be done in production code.

from datetime import datetime
import blockheads
import threading
import queue
import cleverbot


def log(msg, head='INFO'):
    time = datetime.now().strftime('%H:%M:%S')
    print("\033[94m%s\033[0m [%s] %s" % (time, head, msg))


def run_cleverbot():
    while client.is_connected:
        msg = msg_queue.get()
        resp = bot.ask(msg)
        log('%s: %s' % ('Bot', resp))
        client.send_message(resp)


class Client(blockheads.Client):
    def connected(self):
        log('Connected')

    def disconnected(self):
        log('Disconnected')

    def received_message(self, message, player, date):
        log('%s: %s' % (player.username, message), 'MSG')
        if player.username != 'SERVER':
            msg_queue.put(message)

    def player_joined(self, player):
        log('Player %s joined' % player.username)

    def player_left(self, player):
        log('Player %s left' % player.username)

IC_ID = 'f58686de5772f8f018342827987d2efd'
D_ID = '9c14d288d93569c42997d47262481cfd'
PLAYER_ID = '58884f9fd7bd0366e1ada7e6b5dd28fd'
USERNAME = 'NOTSOCLEVER'
WORLD_NAME = ''

player = blockheads.Player(USERNAME, PLAYER_ID)
session = blockheads.Session(player, IC_ID, D_ID)
worlds = session.find_worlds(WORLD_NAME)
if len(worlds) == 0:
    exit('No world found')
world = worlds[0]
if world['players'] == 16:
    exit('Player limit reached')

log('Connecting to world %s from %s' % (world['name'], world['owner']))
client = session.connect(Client, world['wId'])

msg_queue = queue.Queue()
bot = cleverbot.Cleverbot()
responder = threading.Thread(target=run_cleverbot)
responder.start()

while client.is_connected:
    client.loop(100)
