#!/usr/bin/python3
# Chatbot for Blockheads. This bot uses the api of the great cleverbot and therefor
# requires the cleverbot package to be installed. The bot answers to every message send
# except these send by the server. For simplicity's sake ConnectionError exceptions
# are not caught. This is poor style and should not be done in production code.

# Basic Config
WORLD_NAME = ''
USERNAME = 'MajicBot_Public'
# Device ID, etc
IC_ID = '12345123451234512345123451234512'
D_ID = '12345123451234512345123451234512'
PLAYER_ID = '12345123451234512345123451234512'

from datetime import datetime
import blockheads
import threading
import queue
import cleverbot
from os.path import expanduser

def log(msg, head='INFO'):
    time = datetime.now().strftime('%H:%M:%S')
    print("\033[94m%s\033[0m [%s] %s" % (time, head, msg))


def run_cleverbot():
    while client.is_connected:
        msg = msg_queue.get()

class Client(blockheads.Client):
    def connected(self):
        log('Connected')

    def disconnected(self):
        log('Disconnected')

    def received_message(self, message, player, date):
        log('%s: %s' % (player.username, message), 'MSG')
        if player.username != 'SERVER':
            notmax = 1
            name = player.username.title()
            message = message.lower()
#           Triggers

#           Commands

    def player_joined(self, player):
        log('Player %s joined' % player.username)
        name = player.username.lower()
        not_custom_join_message = 1
        if name == 'wingysam':
            log('Bot: Wingzta\'s here!')
            self.send_message('Wingzta\'s here!')
            not_custom_join_message = 0
        if name in open(expanduser('~') + '/blockheads/majicbot_players').read():
            log(name.title() + ' has joined before.')
        else:
            log(name.title() + ' hasn\'t joined before.')
            open(expanduser('~') + '/blockheads/majicbot_players','a').write(name)
            if not_custom_join_message:
                log('Bot: ')
                self.send_message('')

    def player_left(self, player):
        log('Player %s left' % player.username)
USERNAME = USERNAME[:16]
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

log('%s players online.' % (world['players']))

msg_queue = queue.Queue()
bot = cleverbot.Cleverbot()
responder = threading.Thread(target=run_cleverbot)
responder.start()

while client.is_connected:
    client.loop(100)
