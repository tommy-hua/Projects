# import socket programming library
import socket
 
# import thread module
from _thread import *
import threading
import pickle
 
 
# thread function

# built from: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
import socket
from _thread import *
import threading

import sys

sys.path.append("..")
from common.wordlist import OpponentWordList
from common.gamestate import *
from common.player import *

from typing import cast

class Server():
    """
    A class representing the server in our client-server game design/interface.
    
    This class tracks different games that can be run concurrently, mapping lobby ids
        to entire GameState objects, thus tracking also player states within each
        game.
    """
    def __init__(self, host: str, port: int): # port number in the 8000s
        """
        An initializer for the server, listening to requests and creating a store/mapping 
            between lobby_ids and GameStates.
        """
        # have a set of states
        self.states = dict()

        # create a socket, bind to localhost:port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
    
        # listen for incoming connections
        s.listen()

        print("Server now accepting connections.")
    
        # keep accepting connections! This is structured much like a POSIX API C TCP server would be
        while True:
            # https://bugs.python.org/issue41437 -> cannot CTRL+C here
            conn, addr = s.accept()
            
            # log the connection
            print('Connection from: ', addr[0], ':', addr[1])
    
            # and now spawn a thread to handle it
            start_new_thread(self.service_connection, (conn,))

    def service_connection(self, conn):
        """
        A method to recieve a connection. Handling the method is delegated to a later method,
            this one simply unwraps/deserializes the message into an easily interpretable 
            Message object.
        """
        # get header, encoded in 16 bytes
        header = conn.recv(16) 
        length = int.from_bytes(header, byteorder="big")

        # receive message in 1024 byte chunks
        data = b''
        for _ in range(0, int(length/1024) + 1):
            data += conn.recv(1024)

        # deserialize the message
        msg = pickle.loads(data)

        # handle update
        self.handle_update(conn, msg.command) 

    def send_response(self, conn, resp: str):
        """
        A method to abstract the sending of responses, which first sends a size of response, 
            followed by the response itself, chunked into 1024-byte segments.
        """
        # encode message
        msg = resp.encode("utf-8")

        # send a header encoding the length
        header = len(msg).to_bytes(16, byteorder='big')
        conn.send(header)

        # send 1024 at a time
        for i in range(0, int(len(msg)/1024) + 1):
            conn.send(msg[i:i+1024])
        
        # close
        conn.close()

    def send_to_observer(self, host, port, msg: Command):
        """
        A method to abstract away the sending of a message to a remote client's observer, in 
            the case of GameState updates. Responses, as above, are just to notify a client of
            their message/commands' successful receipt, but this is done to actually notify 
            clients of meaningful change, typically originating from the other Client/opposing
            player.
        """
        # make socket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,int(port)))

        # create cmd
        cmd = Message(f"{host}:{port}", msg)

        # create message
        msg = pickle.dumps(cmd)

        # create header
        header = len(msg).to_bytes(16, byteorder='big')

        # send header
        s.send(header)

        # send data in 1024 byte chunks
        for i in range(0, int(len(msg)/1024) + 1):
            s.send(msg[i:i+1024])

        s.close()

    def handle_update(self, conn, command: Command): # update local gamestate, and then forward to other player
        """
        Actual handling of the updates and some of the meat of the COMMAND PATTERN, as it is here 
            that the server parses and works with commands sent by users to act on the GameState.
            Responses and propagation of updates to state are also done here, as this is the central
            point of communication. 
        """
        # pick the right function to call
        if type(command) == CreateLobbyCommand:
            # create the lobby on the server side
            cmd = cast(CreateLobbyCommand, command)
            (lobby_id, lobby_state) = cmd.execute()

            # add this lobby_id mapped to the new state 
            self.states[lobby_id] = lobby_state

            # tell the user the lobby id
            self.send_response(conn, str(lobby_id))


        elif type(command) == JoinLobbyCommand:
            # handle joining on server side (vacuous operation - just unpacks command)
            cmd = cast(JoinLobbyCommand, command)
            (lobby_id, player_b) = cmd.execute()

            # if we had a valid lobby id
            if lobby_id in self.states:
                # grab the game instance's state
                my_state = self.states[lobby_id]

                # set the player id correctly
                my_state.set_player_b(player_b)

                # update the state
                my_state.set_stage('wordpick')

                # send an update to observers
                to_send = [my_state.get_player_a().get_observer(), my_state.get_player_b().get_observer()]
                for host, port in to_send:
                    # make message
                    msg = GameStartedCommand(my_state.get_player_a(), my_state.get_player_b())

                    # send it
                    self.send_to_observer(host, port, msg)

                # then send confirmation
                self.send_response(conn, 'LOBBYJOINED')

            else:
                # send failure notice
                self.send_response(conn, 'INVALIDLOBBY')


        elif type(command) == NewWordListCommand:
            # unpack command
            cmd = cast(NewWordListCommand, command)
            (lobby_id, player, wordlist) = cmd.execute()

            # get our game's state
            my_state = self.states[lobby_id]

            # assign wordlist to player
            player.set_my_list(OpponentWordList(wordlist))

            # and to opponent. we don't know which is a and b, so we grab both
            a = my_state.get_player_a()
            b = my_state.get_player_b()

            print(player.name, a.name, b.name)
            print(a.get_opponent_list(), b.get_opponent_list())
            
            # then check names
            if player.name == a.name:
                print('setting here b opponent')
                b.set_opponent_list(OpponentWordList(wordlist))
            elif player.name == b.name:
                print('setting here a opponent')
                a.set_opponent_list(OpponentWordList(wordlist))

            print(a.get_opponent_list(), b.get_opponent_list())

            # check if both lists have been given
            if a.get_opponent_list() != None and b.get_opponent_list() != None:
                # update the state
                my_state.set_stage('game')

                # get lists to send
                a_opp_list = a.get_opponent_list()
                b_opp_list = b.get_opponent_list()

                # send an update to observers
                to_send = [a.get_observer(), b.get_observer()]
                for (host, port) in to_send:
                    # make message
                    msg = GameRunningCommand(a_opp_list, b_opp_list)

                    # send it
                    self.send_to_observer(host, port, msg)

                # then send confirmation
                self.send_response(conn, 'LISTVALIDATED')
            
            # only one list provided, so just let them know
            else:
                # send confirmation
                self.send_response(conn, 'LISTVALIDATED')


        elif type(command) == CorrectGuessCommand: 
            cmd = cast(CorrectGuessCommand, command)
            
            # unwrap
            (lobby_id, player, guess) = cmd.execute()

            # grab the game instance's state
            my_state = self.states[lobby_id]

            # figure out which player sent the update
            a = my_state.get_player_a()
            b = my_state.get_player_b()

            recipient = None

            if player.name == a.name:
                # update that player
                my_state.set_player_a(player)
                recipient = b
            elif player.name == b.name:
                # update that player
                my_state.set_player_b(player)
                recipient = a

            # notify the other player
            host, port = recipient.get_observer()
            self.send_to_observer(host, port, command)

            # send confirmation
            self.send_response(conn, 'done.')


        elif type(command) == StateUpdateCommand: 
            cmd = cast(StateUpdateCommand, command)
            
            # unwrap
            (lobby_id, player, _) = cmd.execute()

            # grab the game instance's state
            my_state = self.states[lobby_id]

            # figure out which player sent the update
            a = my_state.get_player_a()
            b = my_state.get_player_b()

            recipient = None

            if player.name == a.name:
                # update that player
                my_state.set_player_a(player)
                recipient = b
            elif player.name == b.name:
                # update that player
                my_state.set_player_b(player)
                recipient = a
            
            # notify the other player
            host, port = recipient.get_observer()
            self.send_to_observer(host, port, command)

            # send confirmation
            self.send_response(conn, 'done.')


        elif type(command) == GameEndCommand: 
            cmd = cast(GameEndCommand, command)

            # unwrap
            (lobby_id, player, _) = cmd.execute()

            # grab the game instance's state
            my_state = self.states[lobby_id]

            # figure out which player sent the update
            a = my_state.get_player_a()
            b = my_state.get_player_b()

            recipient = None

            if player.name == a.name:
                # update that player
                my_state.set_player_a(player)
                recipient = b
            elif player.name == b.name:
                # update that player
                my_state.set_player_b(player)
                recipient = a
            
            # send an update to observers
            to_send = [a.get_observer(), b.get_observer()]
            for (host, port) in to_send:
                # send it
                self.send_to_observer(host, port, command)

            # then send confirmation
            self.send_response(conn, 'GAMEENDSENT')

            # remove this from states
            del self.states[lobby_id]

        elif type(command) == DumpCommand:
            # send a dump
            self.send_response(conn, str(self.states))

        else:
            print("Default")
            conn.close()

if __name__ == "__main__":
    # create server
    if len(sys.argv) != 3:
        print("Expected 2 arguments: host, port")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        Server(host, port)