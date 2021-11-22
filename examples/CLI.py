# WATON API --------------

# Example: Command Line Interface

# Communicate with the server through the command line
# Messages will appear in the command line
# To send a message, type your message and press enter
#
# REQUIRED FIELDS:
#   server_ip
#   token

# ------------------------

from watonapi.server import *
import asyncio

server_ip = ""
token = ""

async def async_input():
    return await asyncio.get_event_loop().run_in_executor(None, input)

async def take_input(server):
    while True:
        msg = await async_input()
        await server.send_msg('Waton CLI', msg)

async def main(server):
    await server.add_listener("minecraft_msg") # Begin listening for a "minecraft_msg" packet
    await server.add_listener("player_join") # Begin listening for a "player_join" packet
    await server.add_listener("player_leave") # Begin listening for a "player_leave" packet
    
    authorized = False
    try:
        authorized = await server.connect(token)
    except Exception as e:
        print(f"Couldn't connect to server ( ERROR: {e} )")
    
    if authorized:
        input_handler = asyncio.create_task(take_input(server))
        async for packet in server.get_listeners():
            if packet["type"] == "minecraft_msg":
                print(f"<{packet['user']}> {packet['content']}")
            elif packet["type"] == "player_join":
                print(f"{packet['user']} joined the game!")
            elif packet["type"] == "player_leave":
                print(f"{packet['user']} left the game!")
        input_handler.cancel() 
        print("Lost Connection")

server = Server(server_ip)
asyncio.run(main(server))
