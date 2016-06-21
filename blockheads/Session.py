import json
import requests
from datetime import datetime


class Session:
    URL_API = 'https://cloud.theblockheads.net/api'
    URL_AUTH = URL_API + '/authenticate'
    URL_SEARCH = URL_API + '/world/search'
    URL_CONNECT = URL_API + '/world/connect'

    def __init__(self, player, ic_id, d_id, force_beta=True, platform='Android/Google Play',
                 app_version='1.6.1', crystals='40'):
        self.ic_id = ic_id
        self.d_id = d_id
        self.player = player
        payload = {'icId': ic_id, 'dId': d_id, 'forceBeta': force_beta,
                   'platform': platform, 'appVersion': app_version,
                   'crystals': crystals}
        try:
            resp = requests.post(self.URL_AUTH, data=json.dumps(payload))
            data = json.loads(resp.text)
            if data['status'] != 'ok':
                raise Exception
            self.s_id = data['sId']
        except:
            raise ConnectionError

    def find_worlds(self, name='', world_ids=[], timeout=None):
        payload = {'sId': self.s_id}
        if name:
            payload['name'] = name
        if world_ids:
            payload['wIds'] = world_ids
        try:
            resp = requests.post(self.URL_SEARCH, data=json.dumps(payload), timeout=timeout)
            data = json.loads(resp.text)
            if data['status'] != 'ok':
                raise Exception
            worlds = data['worlds']
        except:
            raise ConnectionError
        return worlds

    def connect(self, client_class, w_id, timeout=None):
        start = datetime.now()
        server_info = self._get_connect_info(w_id, timeout)
        client = client_class(self, server_info['ip'], server_info['port'], server_info['key'])
        while not client.is_connected and (timeout is None or timeout > datetime.now() - start):
            client.loop(100)
        if not client.is_connected:
            client.disconnect()
            raise ConnectionError
        return client

    def _get_connect_info(self, w_id, timeout=None):
        payload = {'sId': self.s_id, 'wId': w_id, 'name': self.player.username}
        try:
            resp = requests.post(
                self.URL_CONNECT, data=json.dumps(payload), timeout=timeout)
            data = json.loads(resp.text)
            if data['status'] != 'ok':
                raise Exception()
            return data
        except TimeoutError:
            raise TimeoutError
        except:
            raise ConnectionError