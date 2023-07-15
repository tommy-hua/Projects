import PySimpleGUI as sg

'''
This is the UI for the End Game Screen
The End Game Screen is a culmination of the games data and displays the final score, the words correct, and the opponent's score
The end game screen receives this data from the server
'''

class EndGameScreen:
    def __init__(self, score, opp_score, words_correct):
        self.final_score = score
        self.words_acc = words_correct
        self.opp_score = opp_score
        #self.opp_acc = opp_acc
        self.win = None

    def end_game(self):
        #end game screen UI
        sg.theme('LightBrown1')   # Add a touch of color tan: #e8dccc
        pfont = ('_', 20, 'bold')

        end_text = ''

        #figure out who won
        if self.final_score > self.opp_score:
            self.win = True
            end_text = 'you won!'
        elif self.final_score < self.opp_score:
            self.win = False
            end_text = 'you lost!'
        else:
            self.win = None
            end_text = 'you tied!'

        word_layout = [ [sg.Text('Word List:', font=pfont, justification='c', pad=(0, (5, 0)))],
                        [sg.HSep()],
                        [sg.Button(f'{self.words_acc[0][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[0][1], pad=(1,1))],
                        [sg.Button(f'{self.words_acc[1][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[1][1], pad=(1,1))],
                        [sg.Button(f'{self.words_acc[2][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[2][1], pad=(1,1))],
                        [sg.Button(f'{self.words_acc[3][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[3][1], pad=(1,1))],
                        [sg.Button(f'{self.words_acc[4][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[4][1], pad=(1,1))],
                        [sg.Button(f'{self.words_acc[5][0]}', font=pfont, size=(10, 1), button_color='red', disabled_button_color='green', disabled=self.words_acc[5][1], pad=(1,1))],
                       ]

        layout = [  [sg.Text(end_text, font=('_', 50, 'bold'), justification='c')],
                    [sg.Text('Final Scores', font=('_', 24), justification='c', pad=(0, (10, 5)))],
                    [sg.Text(f'Your Score: {self.final_score}', font=pfont), sg.VSep(), sg.Text(f'Opps Score: {self.opp_score}', font=pfont)],
                    [word_layout],
                    [sg.HSep()],
                    [sg.Button('play again', font=pfont, size=(10, 1), pad=(5, (15, 0)), enable_events=True, key='AGAIN'), sg.Button('quit game', font=pfont, size=(10, 1), pad=(0, (15, 0)), enable_events=True, key='EXIT')],
                    ]
        
        window = sg.Window('end screen',layout, element_justification='center', size=(500, 500))

        while True:
            event, values = window.read()
            if event == 'EXIT' or event == sg.WIN_CLOSED:
                break
            elif event == 'AGAIN':
                break
        
        window.close()

        return