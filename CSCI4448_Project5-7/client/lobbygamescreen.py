import PySimpleGUI as sg

from createlobbyui import CreateLobby
from joinlobbyui import JoinLobby

'''
This is the UI for the Lobby Screen
the lobby screen has the attributes of CreateLobby and JoinLobby which are the UI for creating and joining lobbies respectively
'''

class LobbyGameScreen:
    def __init__(self):
        #create and join lobby UI and lobbyid that gets passed to server from create or join
        self.CreateLobby = CreateLobby()
        self.JoinLobby = JoinLobby()
        self.lobbyID = None

        #Lobby Screen UI
        sg.theme('LightBrown1')
        pfont = ('_', 20, 'bold')

        layout = [  [sg.Text('mongoose', font=('_', 50, 'bold'))],
                    [sg.Button('Create Lobby', font=pfont, size=(10, 2), key='cl', enable_events=True)],
                    [sg.Button('Join Lobby', font=pfont, size=(10, 2), key='jl', enable_events=True)],
                    [sg.Button('Quit', font=pfont, size=(10, 2))]
                ]

        window = sg.Window('Lobby', layout, element_justification='center', size=(500, 500))

        while True:
            event, values = window.read()
            if event == 'cl':
                window.hide()
                self.CreateLobby.create_lobby()
                window.UnHide()
                              
            elif event == 'jl':
                window.hide()
                self.JoinLobby.join_lobby()
                window.UnHide()

            elif event == sg.WIN_CLOSED or event == 'Quit':
                break
            
        window.close()