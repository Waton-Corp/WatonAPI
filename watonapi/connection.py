import asyncio
from . import packets
from . import codec
import json

async def connect(ip, port):
  stream = await asyncio.open_connection(ip, port)
  return Connection(packets.PacketStream(stream))

class Connection:
  def __init__(self, stream):
    self.stream = stream

  async def iterate(self):
    async for packet in self.stream.get_packets():
      yield json.loads(packet[1:])
  
  async def send(self, obj):
    protocol_version = codec.to_varint(69420)
    string = codec.encode_string(json.dumps(obj))
    unused_fields = bytes([0,0,1])
    packet = protocol_version + string + unused_fields
    await self.stream.write_packet(packet)

  async def disconnect(self):
    await self.stream.close()
