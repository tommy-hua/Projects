NAMES:
- Pranav Subramanian
- Tommy Hua

LANGUAGE VERSION:
- Python 3.9.7

INSTRUCTIONS:
- servers and clients listen on ports for updates. Pick a port for the server, and both clients. The IPs will likely be 127.0.0.1.
- run the client from the client folder. To run, run a command of the form `python client.py CLIENT_IP CLIENT_PORT SERVER_IP SERVER_PORT PLAYER_NAME`. For example, `python client.py 127.0.0.1 9000 127.0.0.1 8000 player_a`
- run the server from the server folder. To run, run a command of the form `python server.py SERVER_IP SERVER_PORT`. For example, `python server.py 127.0.0.1 8000`.
- the best way to run this is to run 3 different terminals on a single host. Then, on each terminal, enter the following (one of these lines per terminal window):
    - `python client.py 127.0.0.1 9000 127.0.0.1 8000 player_a`
    - `python client.py 127.0.0.1 9001 127.0.0.1 8000 player_b`
    - `python server.py 127.0.0.1 8000`
- to run and inspect the UI itself, run `python gamescreen.py`.