## blockheads - (Very) basic client for Blockheads
This is an attempt to reverse engineer the network protocol of the game Blockheads. This project is not affiliated with Majic Jungle Software nor Noodlecake Studios.

The library consists of two main parts, Session and Client. The Session class allows you to search
worlds by name and get basic information from a world including but not limited to:
owner, player count, world id, ip, ...
The Client class allows you to connect to a Blockheads server. You can extend the class to add behaviour
when someone sends a message or a player joins/leaves. Ones connected, the client object contains a list of
all players and detailed world information.
The provided welcome_bot example is a good starting point for using this library. 

Do not use this for any malicious purposes!

This package requires [enet](https://github.com/aresch/pyenet).
