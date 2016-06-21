# Simple client for Blockheads. It welcomes every player that joins and logs
# send messages and joined players. For simplicity's sake ConnectionError exceptions
# are not caught. This is poor style and should not be done in production code.

from datetime import datetime
import blockheads


def log(msg, head='INFO'):
    time = datetime.now().strftime('%H:%M:%S')
    print("\033[94m%s\033[0m [%s] %s" % (time, head, msg))


# Extend the blockheads.Client class and override the methods you need.
class Client(blockheads.Client):
    def connected(self):
        log('Connected')

    def disconnected(self):
        log('Disconnected')

    def received_message(self, message, player, date):
        log('%s: %s' % (player.username, message), 'MSG')

    def player_joined(self, player):
        log('Player %s joined' % player.username)
        self.send_message('Hi %s!' % player.username.title())

    def player_left(self, player):
        log('Player %s left' % player.username)


# iCloud, device and player id can be any unique 32 long hex string.
# These parameters are bound to an account. Change all three and you have yourself a new account.
# Every server you connect to receive these parameters in plain text, so yeah very secure :P
IC_ID = '0123456789abcdef0123456789abcdef'
D_ID = 'fedcba9876543210fedcba9876543210'
PLAYER_ID = '12345678912345678912345678912345'
# Username can be any non taken username
USERNAME = 'WELCOMEBOT'
# The name of the world you like to connect to. When the world name is empty, a world will
# be chosen at random.
WORLD_NAME = ''

# Open a session.
player = blockheads.Player(USERNAME, PLAYER_ID)
session = blockheads.Session(player, IC_ID, D_ID)
# Find all worlds with the given name (or close to). Every element of the returned list is a dictionary
# with the properties of the world (wId, name, owner, player count, ...).
worlds = session.find_worlds(WORLD_NAME)
if len(worlds) == 0:
    exit('No world found')
world = worlds[0]
log('Connecting to world %s from %s' % (world['name'], world['owner']))

# Connect to the world with the given world id. Session.connect(...) will return a new Client object
# initialized with the given client class.
client = session.connect(Client, world['wId'])
# Execute client loop as long as it is connected.
while client.is_connected:
    # Loop will wait at most 10 milliseconds for a new packet. This function has to be called reguraly.
    # The given wait time should not be too long, so the send buffer doesn't become too large.
    client.loop(10)
