#!/usr/bin/env python3

# Basic Config
WORLD_NAME = 'love god'
USERNAME = 'MajicBot'
# Device ID, etc
IC_ID = 'f58686de5772f8f018342827987d2efd'
D_ID = '9c14d288d93569c42997d47262481cfd'
PLAYER_ID = '58884f9fd7bd0366e1ada7e6b5dd28fd'

from datetime import datetime
import blockheads
import threading
import queue
import cleverbot


def log(msg, head='INFO'):
    time = datetime.now().strftime('%H:%M:%S')
    print("\033[94m%s\033[0m [%s] %s" % (time, head, msg))

def bot(msg, head='BOT'):
    time = datetime.now().strftime('%H:%M:%S')
    print("\033[94m%s\033[0m [%s] %s" % (time, head, msg))

def send(msg):
    bot(msg)
    client.send_message(msg)
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
        if player.username != 'SERVER.':
            notmax = 1
            name = player.username.title()
            msg = message.lower()
#           Triggers

#           Commands

        if msg[:4] == '?rev':
            if msg[5:][::-1][:1] != '/':
                send(message[5:][::-1])
            else:
                send('Command execution failed.')
        if msg[:5] == '?echo':
            if msg[6:][:1] != '/':
                send(message[6:])
            else:
                send('Command execution failed.')
        if msg == '?help':
            send('Help\n?echo - Echo something in chat\n?rev - Reverse something in chat\n?help - Display this message')

# All caps detection
        if msg.upper() == message:
            if any(c.isalpha() for c in message):
                send('Please do not chat in all caps, ' + name + '.')

    def player_joined(self, player):
        log('Player %s joined' % player.username)
        name = player.username.lower()
        not_custom_join_message = 1
        if name == 'wingysam':
            send('Wingzta\'s here!')
            not_custom_join_message = 0
        if name in open('/home/sam/blockheads/majicbot_players').read():
            log(name.title() + ' has joined before.')
        else:
            log(name.title() + ' hasn\'t joined before.')
            open('/home/sam/blockheads/majicbot_players','a').write(name)
            if not_custom_join_message:
                send('New player welcome message unset.')

    def player_left(self, player):
        log('Player %s left' % player.username)
USERNAME = USERNAME[:16]
player = blockheads.Player(USERNAME, PLAYER_ID)
session = blockheads.Session(player, IC_ID, D_ID)
worlds = session.find_worlds(WORLD_NAME)
if len(worlds) == 0:
    exit('No world found')
world = worlds[0]
if 'players' in world:
    if world['players'] == 16:
        exit('Player limit reached')
else:
    exit('Players attribute not found.')

log('Connecting to world %s from %s' % (world['name'], world['owner']))
client = session.connect(Client, world['wId'])

log('%s players online.' % (world['players']))

msg_queue = queue.Queue()
#bot = cleverbot.Cleverbot()
responder = threading.Thread(target=run_cleverbot)
responder.start()

while client.is_connected:
    client.loop(100)
