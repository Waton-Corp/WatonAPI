from . import errors

#Encodes a number using the varint format
#https://wiki.vg/Protocol#VarInt_and_VarLong
def to_varint(num):
  result = []
  while True:
    byte = num & 0b01111111
    num >>= 7
    if num == 0:
      result += [byte]
      break
    else:
      result += [byte | 0b10000000]
  return bytes(result)

async def read_varint(stream):
  bytes_read = 0
  result = 0
  while True:
    byte = (await stream.read_bytes(1))[0]
    value = byte & 0b01111111
    result |= value << (7 * bytes_read)
    bytes_read += 1
    if bytes_read > 5:
      raise errors.InvalidFormatError('Varint is too big')
    if byte & 0b1000_0000 == 0:
      return result

def encode_string(string):
  str_bytes = string.encode()
  length = len(str_bytes)
  return to_varint(length) + str_bytes
