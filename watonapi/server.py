import asyncio
from . import connection
from . import dispatcher
from . import address

class Server:
    """
    MAIN SERVER CLASS
    Interface for other classes
    """
    def __init__(self, ipaddr):
        """
        Setup server class
        Define ip, port, and an empty listeners list
        """
        self.ip, self.port = address.get_ip_port(ipaddr)
        self.listeners = []

    async def connect(self, token):
        """
        Connect to the server though the connection class in the connection file
        Checks authorization token to connect to the server
        Begins the dispatcher to start receiving data if the token is correct
        """
        
        self.connection = await connection.connect(self.ip, self.port)
        await self.connection.send({'type': 'handshake', 'token': token})
        async for packet in self.connection.iterate():
            if packet["type"] == "authorize_response" and packet["response"] == True:
                self.keepalive_task = asyncio.create_task(self.keepalive())
                self.dispatcher = dispatcher.Dispatcher(self.connection, self.listeners)
                self.dispatcher.start()
                return True
            else:
                await self.connection.disconnect()
  
    async def keepalive(self, interval=25):
        while True:
            await self.connection.send({'type': 'keepalive'})
            await asyncio.sleep(interval)
  
    async def send_msg(self, user, content):
        await self.connection.send({
            'type': 'discord_msg', 
            'user': user, 
            'content': content
        })
    async def add_listener(self, listener_type):
        self.listeners.append(listener_type)

    async def get_listeners(self):
        async for packet in self.dispatcher.retreive_listeners():
            yield packet

    async def get_packet(self, type_):
        async for packet in self.dispatcher.iterate_events(type_):
            yield packet
    
    async def disconnect(self):
        self.dispatcher.stop()
        self.keepalive_task.cancel()
        await self.connection.disconnect()
