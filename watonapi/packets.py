from . import errors
from . import codec
import asyncio

class PacketStream:
  def __init__(self, stream):
    self.reader, self.writer = stream

  async def get_packets(self):
    while True:
      try:
        size = await codec.read_varint(self)
      except errors.DisconnectedError:
        break
      except errors.InvalidFormatError:
        # If you dont know where this one ends you 
        # cant know where the others begin
        raise errors.CorruptedStreamError
      yield await self.read_bytes(size)

  async def read_bytes(self, amount):
    try:
      return await self.reader.readexactly(amount)
    except asyncio.IncompleteReadError:
      raise errors.DisconnectedError

  async def write_packet(self, payload_bytes):
    type_field = codec.to_varint(0)
    length_field = codec.to_varint(len(type_field) + len(payload_bytes))
    self.writer.write(length_field + type_field + payload_bytes)
    await self.writer.drain()
  
  async def close(self):
    self.writer.close()
    await self.writer.wait_closed()
