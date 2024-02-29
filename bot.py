import websockets
import aiohttp
from enum import StrEnum, IntEnum
import asyncio
from asyncio import CancelledError, create_task, sleep
import json
import inspect
from random import random

class GatewayOpcodes(IntEnum):
    EVENT = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_OFFLINE_MEMBERS = 8
    INVALIDATED = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

class GatewayError(IntEnum):
    UNKNOWN = 4000
    INVALID_OPCODE = 4001
    INVALID_PAYLOAD = 4002
    NO_AUTH = 4003
    INVALID_TOKEN = 4004
    EXISTING_AUTH = 4005
    INVALID_RESUME_SEQUENCE = 4007
    RATELIMIT = 4008
    SESSION_TIMEOUT = 4009
    BAD_SHARD = 4011
    INVALID_API = 4011
    DISABLED_INTENTS = 4012

class GatewayMessage:
    def from_received(recv):
        if isinstance(recv, str):
            recv = json.loads(recv)
        return GatewayMessage(recv['op'], recv['d'], recv['t'], recv['s'])

    def __init__(self, opcode, data, event, seq):
        self.opcode = opcode
        self.data = data
        if opcode != GatewayOpcodes.EVENT:
            self.event = None
            self.sequence = None
        else:
            self.event = event
            self.sequence = seq
    def payload(self):
        return {'d': self.data, 'op': self.opcode, 't': self.event, 's': self.sequence}
    async def send(self, ws, ret=True):
        await ws.send(json.dumps(self.payload()))
        resp = json.loads(await ws.recv())
        if ret:
            mesg = GatewayMessage(resp['op'], resp['d'], resp['t'], resp['s'])
            return mesg

def is_receivable(code):
    if code == GatewayOpcodes.EVENT: return True
    if code == GatewayOpcodes.RECONNECT: return True
    if code > GatewayOpcodes.REQUEST_OFFLINE_MEMBERS: return True
    return False

class OnlineMode(StrEnum):
    NORMAL = 'linux'
    MOBILE = 'Discord Android'

class InvalidReceiveOpcode(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)

API_VERSION = 10
class Bot:
    def __init__(self, token, onm=OnlineMode.NORMAL):
        self._token = token
        self._onm = onm
        self._presence = None
        self.heartbeats = 0
        self.pulse = -1
        self._eventListener = {}
        self._heartbeat_task = None 

    async def _heartbeat(self):
        try:
            while True:
                self.heartbeats += 1
                jitter = 1
                if self.heartbeats == 1:
                    jitter = random()

                p = self.pulse / 1000
                print(p * jitter)
                await sleep(p * jitter)
                await GatewayMessage(GatewayOpcodes.HEARTBEAT, None, None, None).send(self._client)
                print("heartbeat")
                print()
        except CancelledError:
            print("Stopping heartbeat task")
            await self._heartbeat_task.cancel()

    async def _call_event(self, event_name, *args):
        if not (event_name in self._eventListener):
            self._eventListener[event_name.lower()] = {}
        listenersList = self._eventListener[event_name.lower()]
        for listener in listenersList:
            if not inspect.isawaitable(listener):
                listener(args)
            else:
                await listener(args)
    
    def event(self, func):
        def wrapper(event_type, once=False):
            if once:
                old_func = func
                def func(*args):
                    old_func(args)
                    idx = -1
                    for event_listener in self._eventListener[event_type]:
                        idx += 1
                        if event_listener[event_type] == func:
                            self._eventListener[event_type][idx] = None
            self._eventListener[event_type].append(func)
        return wrapper

    async def _recv(self, mesg):
        print()
        print("RECEIVED")
        print(mesg.payload())
        print(mesg.opcode)
        print(mesg.opcode != 0)
        print()
        op = mesg.opcode
        data = mesg.data
        await self._call_event("intercept_" + str(op), data)
        if op != 0:
            if op == GatewayOpcodes.HELLO:
                print('hi!')
                self._heartbeat_task = asyncio.create_task(self._heartbeat())
        else:
            event = mesg.event
            await self._call_event(event, data)
            await self._call_event("any", data)


    def run(self):
        async def connect_to_gateway():
            self._session = aiohttp.ClientSession()
            async with self._session.get(f'https://discord.com/api/v{API_VERSION}/gateway/bot', headers={'Authorization':'Bot ' + self._token}) as data:
                data = await data.json()
                print(data)
                url = data['url']
                shards = data['shards']
            GATEWAY_URL = f'{url}?v={API_VERSION}&encoding=json'
            self._gwurl = GATEWAY_URL
            conn = await websockets.connect(GATEWAY_URL)
            shardArray = None
            self._client = conn
            if shards > 0:
                shardArray = [shards - 1, shards]
            data = {
                'token': self._token,
                'intents': 513,
                'properties': {
                    'os': self._onm,
                    'browser': 'dislib',
                    'device': self._onm
                },
                'shard': shardArray
            }
            mesg = GatewayMessage(GatewayOpcodes.IDENTIFY, data, None, None)

            hello = GatewayMessage.from_received(await conn.recv())
            data = hello.data
            self.pulse = data['heartbeat_interval']
            await self._recv(hello)

            event = await mesg.send(conn)
            data = event.data
            await self._recv(event)
            while True:
                event = await self._client.recv()
                await self._recv(GatewayMessage.from_received(event))
        try:
            asyncio.get_event_loop().run_until_complete(connect_to_gateway())
        except KeyboardInterrupt:
            asyncio.get_event_loop().run_until_complete(self.stop())
    async def stop(self):
        print()
        await self._client.close()
        await self._session.close()
        await self._heartbeat_task.cancel()

if __name__ == "__main__":
    token = 'no'
    bot = Bot(token)
    bot.run()
