import PySimpleGUI as sg

class JoinLobby:
    def __init__(self):
        #lobbyid variable that gets passed to the server
        self.lobbyid = None

    def join_lobby(self):
        #UI
        sg.theme('LightBrown1')     #e8dccc
        pfont = ('_', 20, 'bold')

        lobby = sg.Input('', key='id', font=('_', 20), size=(10, 1), border_width=1, expand_x=True)

        frame_layout = [
                        [lobby],
                        [sg.Button('back', font=pfont, expand_x=True, enable_events=True, key='BACK'), sg.Button('join', font=pfont, expand_x=True, enable_events=True, key='JOIN')],
                        ]
        layout = [  [sg.Text('join lobby', font=('_', 50, 'bold'), justification='c')],
                    [sg.Text('join a lobby with your friend, or enemy', font=pfont, justification='c', pad=(0, (20, 30)))],
                    [sg.Frame('enter lobby id', frame_layout, font=pfont, border_width=2, expand_x=True)],
                    [sg.Text('', font=('_', 20, 'italic'), pad=(0, (30, 30)), key='HID', visible=False)],
                    [sg.Button('cancel', font=pfont, size=(10, 1), enable_events=True, key='CANCEL', visible=False)],
                    ]
        
        window = sg.Window('lobby',layout, element_justification='center', size=(500, 500))
        
        while True:
            event, values = window.read()

            if event == 'JOIN':
                self.lobbyid = values['id']
                window['HID'].update(f'Searching for lobby #{self.lobbyid}...', visible=True)
                window['CANCEL'].update(visible=True)

            elif event == 'CANCEL':
                window['HID'].update(visible=False)
                window['CANCEL'].update(visible=False)
                
            elif event == 'BACK' or event == sg.WIN_CLOSED:
                break
        
        window.close()

        return
