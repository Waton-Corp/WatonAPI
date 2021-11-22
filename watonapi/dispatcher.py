import asyncio
from . import errors

class Dispatcher():
    def __init__(self, connection, listeners):
        self.connection = connection
        self.subscriptions = {}
        for listener in listeners:
            self.subscriptions[listener] = []
        self.listeners = listeners
        self.active = False
    
    def start(self):
        if not self.active:
            self.active = True
            self.task = asyncio.create_task(self.run())
    
    async def run(self):
        async for packet in self.connection.iterate():
            self.raise_event(packet['type'], packet)
        self.stop()
    
    def raise_event(self, name, data):
        try:
            for queue in self.subscriptions[name]:
                queue.put_nowait(data)
        except KeyError:
            pass

    async def retreive_listeners(self):
        if not self.active:
            raise errors.DispatcherIsStoppedError
        # Modified get_queue()
        queue = asyncio.Queue()
        for listener in self.listeners:
            self.subscriptions[listener] += [queue]
        
        while True:
            packet = await queue.get()
            if not packet:
                break
            yield packet
            queue.task_done()

    async def iterate_events(self, name):
        if not self.active:
            raise errors.DispatcherIsStoppedError
        queue = self.get_queue(name)
        while True:
            packet = await queue.get()
            if not packet:
                break
            yield packet
            queue.task_done()
    
    async def get_next_event(self, name):
        if not self.active:
            raise errors.DispatcherIsStoppedError
        queue = self.get_queue(name)
        packet = await queue.get()
        self.subscriptions[name].remove(queue)
        return packet
    
    def get_queue(self, message_type):
        queue = asyncio.Queue()
        if message_type not in self.subscriptions:
            self.subscriptions[message_type] = []
        self.subscriptions[message_type] += [queue]
        return queue
    
    def stop(self):
        if self.active:
            self.active = False
            self.task.cancel()
            self.close_all_queues()
    
    def close_all_queues(self):
        for list in self.subscriptions.values():
            for queue in list:
                queue.put_nowait(None)
