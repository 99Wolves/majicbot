import enet
import plistlib
import zlib
from datetime import datetime
import threading
from blockheads.Player import Player


class Client:
    def connected(self):
        pass

    def disconnected(self):
        pass

    def received_message(self, message, player, date):
        pass

    def player_joined(self, player):
        pass

    def player_left(self, player):
        pass

    def __init__(self, session, ip, port, server_key):
        self.session = session
        self.server_key = server_key
        self.ip = ip
        self.port = port
        self.players = {}
        self.world_info = {}
        self.is_connected = False
        self._send_lock = threading.Lock()
        self._host = enet.Host(None, 1, 0xff, 0, 0)
        try:
            self._peer = self._host.connect(enet.Address(ip, port), 0xff, 0)
        except:
            raise ConnectionError

    def __del__(self):
        try:
            self.disconnect()
        except:
            return

    def disconnect(self):
        self.is_connected = False
        self._peer.disconnect()
        self._host.service(0)

    def send(self, data):
        with self._send_lock:
            self._peer.send(0, enet.Packet(data, enet.PACKET_FLAG_RELIABLE))

    def send_message(self, message, username=''):
        if not username:
            username = self.session.player.username
        pl = dict(
            alias=username,
            message=message,
            playerID=self.session.player.player_id,
            date=datetime.utcnow(),
        )
        self.send(bytes([self._ID_MESSAGE]) + plistlib.dumps(pl))

    def loop(self, wait_time):
        with self._send_lock:
            event = self._host.service(wait_time)
        if event.type == enet.EVENT_TYPE_DISCONNECT:
            self.is_connected = False
            self.disconnected()
        elif event.type == enet.EVENT_TYPE_RECEIVE:
            self._handle_packet(event.packet.data)

    def _handle_packet(self, packet):
        if len(packet) == 0:
            return
        packet_id = packet[0]
        data = packet[1:]
        if packet_id in self._packet_handlers:
            self._packet_handlers[packet_id](self, data)

    def _handle_world_info(self, data):
        try:
            decoded = plistlib.loads(data[1:])
        except:
            return
        self.world_info.update(decoded)
        pl = dict(
            alias=self.session.player.username,
            cloudKey=self.server_key,
            iCloudID=self.session.ic_id,
            local=True,
            micOrSpeakerOn=True,
            minorVersion=2,
            playerID=self.session.player.player_id,
            udidNew=self.session.d_id,
            voiceConnected=False,
        )
        if self.session.player.photo:
            pl['photo'] = self.session.player.photo
        self.send(bytes([self._ID_LOGIN]) + plistlib.dumps(pl))

    def _handle_world_info_long(self, data):
        try:
            decoded = plistlib.loads(
                zlib.decompress(data, 16 + zlib.MAX_WBITS)
            )
        except:
            return
        self.world_info.update(decoded)
        self.is_connected = True
        self.connected()

    def _handle_player_data(self, data):
        try:
            decoded = plistlib.loads(data)
        except:
            return
        usernames = []
        for player_data in decoded:
            username = player_data['alias']
            usernames.append(username)
            if username in self.players:
                if 'mod' in player_data and player_data['mod'] != self.players[username].mod:
                    self.players[username].mod = player_data['mod']
            else:
                if 'photo' in player_data:
                    photo = player_data['photo']
                else:
                    photo = ''
                if 'mod' in player_data:
                    mod = player_data['mod']
                else:
                    mod = ''
                player = Player(username, player_data['playerID'], photo, mod)
                self.players[username] = player
                if self.is_connected:
                    self.player_joined(player)

        left_players = set(self.players.keys()) - set(usernames)
        for username in left_players:
            player = self.players[username]
            del self.players[username]
            self.player_left(player)

    def _handle_message(self, data):
        try:
            decoded = plistlib.loads(data)
        except:
            return
        if all(k in decoded for k in ('date', 'playerID', 'alias', 'message')):
            username = decoded['alias']
            if username in self.players:
                player = self.players[username]
            else:
                player = Player(username, decoded['playerID'])
            self.received_message(decoded['message'], player, decoded['date'])

    _ID_WORLD_INFO = 0x23
    _ID_LOGIN = 0x1f
    _ID_WORLD_INFO_LONG = 0x01
    _ID_MESSAGE = 0x24
    _ID_PLAYER_DATA = 0x1e

    _packet_handlers = {
        _ID_WORLD_INFO: _handle_world_info,
        _ID_MESSAGE: _handle_message,
        _ID_WORLD_INFO_LONG: _handle_world_info_long,
        _ID_PLAYER_DATA: _handle_player_data,
    }