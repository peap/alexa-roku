import logging
from http.client import HTTPConnection
from urllib.parse import urlencode
from xml.etree import ElementTree

logger = logging.getLogger('alexa-roku')

# see the Roku External Control Guide at
# http://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide
ENDPOINTS = {
    'device-info': '/query/device-info',
    'get-icon': '/query/icon/{channel_id}',
    'input': '/input',
    'install': '/install/{channel_id}',
    'key-down': '/keydown/{key}',
    'key-up': '/keyup/{key}',
    'key-press': '/keypress/{key}',
    'launch': '/launch/{channel_id}',
    'list-channels': '/query/apps',
}

KEYS = {
    'home': 'Home',
    'reverse': 'Rev',
    'forward': 'Fwd',
    'play': 'Play',
    'select': 'Select',
    'left': 'Left',
    'right': 'Right',
    'down': 'Down',
    'up': 'Up',
    'back': 'Back',
    'instant replay': 'InstantReplay',
    'info': 'Info',
    'backspace': 'Backspace',
    'search': 'Search',
    'enter': 'Enter',
}


class RokuError(Exception):
    pass


# A Roku Channel/App
class Channel:
    def __init__(self, name, id_, version):
        self.name = name
        self.id = id_
        self.version = version

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.version)


class RokuDevice:
    """
    A single Roku player accessible over the network.
    """
    _channels = None
    _conn = None
    _device_info = None
    port = 8060

    def __init__(self, ip_addr, port=None):
        self.ip_addr = ip_addr
        if port is not None:
            self.port = port
        try:
            self.device_info
        except ConnectionRefusedError:
            raise RokuError('Connection refused to {0}!'.format(self))

    def __str__(self):
        return '{0}:{1}'.format(self.ip_addr, self.port)

    @property
    def channels(self):
        if self._channels is None:
            channels = []
            url = ENDPOINTS['list-channels']
            try:
                channel_xml = self.get(url)
            except TimeoutError:
                raise RokuError(
                    'Timed out trying to get channels for {0}!'
                    .format(self)
                )
            tree = ElementTree.fromstring(channel_xml)
            for app in tree:
                channels.append(Channel(
                    app.text,
                    app.get('id'),
                    app.get('version'),
                ))
            self._channels = sorted(channels, key=lambda c: c.name)
        return self._channels

    @property
    def connection(self):
        if self._conn is None:
            self._conn = HTTPConnection(self.ip_addr, self.port)
        return self._conn

    @property
    def device_info(self):
        if self._device_info is None:
            info = {}
            url = ENDPOINTS['device-info']
            try:
                channel_xml = self.get(url)
            except TimeoutError:
                raise RokuError(
                    'Timed out trying to get device info for {0}!'
                    .format(self)
                )
            tree = ElementTree.fromstring(channel_xml)
            for node in tree:
                info[node.tag] = node.text
            self._device_info = info
        return self._device_info

    def get(self, url, params=None):
        if params:
            url += '?{0}'.format(urlencode(params))
        self.connection.request('GET', url)
        resp = self.connection.getresponse()
        code = resp.status
        if not str(code).startswith('2'):
            raise RokuError('GET request to {0} failed: {1}'.format(url, code))
        data = resp.read()
        return data

    def get_channel(self, name):
        for channel in self.channels:
            if channel.name.lower() == name.lower():
                return channel
        return None

    def launch_channel(self, name):
        channel = self.get_channel(name)
        url = ENDPOINTS['launch'].format(channel_id=channel.id)
        self.post(url, {})

    @property
    def model(self):
        return self.device_info.get('model-name')

    @property
    def name(self):
        return self.device_info.get('user-device-name')

    def play_pause(self):
        url = ENDPOINTS['key-press'].format(key=KEYS['play'])
        self.post(url, {})

    def press_ok(self):
        url = ENDPOINTS['key-press'].format(key=KEYS['select'])
        self.post(url, {})

    def post(self, url, data, params=None):
        if params:
            url += '?{0}'.format(urlencode(params))
        enc_data = urlencode(data)
        headers = {
            'Accept': 'text/plain',
            'Content-type': 'application/x-www-form-urlencoded',
        }
        self.connection.request('POST', url, enc_data, headers)
        resp = self.connection.getresponse()
        code = resp.status
        if not str(code).startswith('2'):
            raise RokuError('POST request to {0} failed: {1}'.format(url, code))
        data = resp.read()
        return data
