import PySimpleGUI as sg

class CreateLobby:
    def __init__(self):
        #id gets passed to server
        self.lobbyid = None

    def create_lobby(self):
        #UI
        sg.theme('LightBrown1')   # Add a touch of color tan: #e8dccc
        pfont = ('_', 20, 'bold')

        lobby = sg.Input('', key='id', font=('_', 20), size=(10, 1), border_width=1, expand_x=True)

        frame_layout = [
                        [lobby],
                        [sg.Button('back', font=pfont, expand_x=True, enable_events=True, key='BACK'), sg.Button('create', font=pfont, expand_x=True, enable_events=True, key='CREATE')],
                        ]

        layout = [  [sg.Text('create lobby', font=('_', 50, 'bold'), justification='c')],
                    [sg.Text('Create a lobby for you and your friends to join', font=pfont, justification='c', pad=(0, (20, 30)))],
                    [sg.Frame('enter lobby id', frame_layout, font=pfont, border_width=2, expand_x=True)],
                    [sg.Text('Waiting for players to join...', font=('_', 20, 'italic'), pad=(0, (30, 30)), key='HID', visible=False)],
                    [sg.Button('cancel', font=pfont, size=(10, 1), enable_events=True, key='CANCEL', visible=False)],
                    ]
        
        window = sg.Window('lobby',layout, element_justification='center', size=(500, 500))
        
        while True:
            event, values = window.read()

            if event == 'CREATE':
                self.lobbyid = values['id']
                sg.popup(f'lobby #{self.lobbyid} created', title='lobby created', font=pfont, button_justification='c')
                window['HID'].update(visible=True)
                window['CANCEL'].update(visible=True)

            elif event == 'CANCEL':
                window['HID'].update(visible=False)
                window['CANCEL'].update(visible=False)
                
            elif event == 'BACK' or event == sg.WIN_CLOSED:
                break
        
        window.close()
        
        return

