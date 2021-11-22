# WatonAPI
<p align="center">
    <img src="logo.png" width="400" alt="WatonAPI Logo">
</p>

## Python API for WatonPlugin
WatonAPI is an API used to connect to spigot servers with the WatonPlugin to communicate.
You can send messages to the server and read messages, making it useful for cross-chat programs.

Some examples of possible use cases are:
* Minecraft Chat CLI
* Cross Chat Discord Bot

#### And many more

## How to use

### Documentation will be released soon

WatonAPI is an async library, meaning that it has to be run with asyncio. 
You can look in the examples directory to find example programs using the WatonAPI.
#### CLI Example
```py
from watonapi.server import *
import asyncio

server_ip = ""
token = ""

async def async_input():
    return await asyncio.get_event_loop().run_in_executor(None, input)

async def take_input(server):
    while True:
        msg = await async_input()
        await server.send_msg('Waton CLI', msg) # When input is received, send it to the server

async def main(server):
    await server.add_listener("minecraft_msg") # Begin listening for a "minecraft_msg" packet
    await server.add_listener("player_join") # Begin listening for a "player_join" packet
    await server.add_listener("player_leave") # Begin listening for a "player_leave" packet
    
    authorized = False
    try:
        # If this doesn't fail, the token was correct and the connection authorized
        authorized = await server.connect(token)
    except Exception as e:
        print(f"Couldn't connect to server ( ERROR: {e} )")
    
    if authorized:
        input_handler = asyncio.create_task(take_input(server)) # Start an async task to get user input
        async for packet in server.get_listeners(): # Get all of the packets that we are listening for
            if packet["type"] == "minecraft_msg":
                print(f"<{packet['user']}> {packet['content']}")
            elif packet["type"] == "player_join":
                print(f"{packet['user']} joined the game!")
            elif packet["type"] == "player_leave":
                print(f"{packet['user']} left the game!")
        input_handler.cancel() # If it gets to here, the connection was lost
        print("Lost Connection")

server = Server(server_ip) # Create a server object using the server ip
asyncio.run(main(server)) # Run the main function

```
