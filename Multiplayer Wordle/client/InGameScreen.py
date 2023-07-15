import PySimpleGUI as sg
import copy

"""
    https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Game_Wordle.py

    The basis for this code is from PySimpleGUI (link above). It has been modified to fit our needs.

    This is the In Game Screen that consists of the actual gameplay of wordle and the UI for it.
    This class InGameScreen gets passed a wordlist from the server and uses it to execute the game.
    This class will then send updates to the server side on game progress, player score, and words correct.
    This class has the methods run_game() which runs the game and wordle() which is the implementation of the game.
"""

class InGameScreen:
    def __init__(self, wordlist):
        #variables to be sent to the server
        self.score = 0
        self.words_correct = []
        self.wordlist = wordlist
        self.game_count = 0
        #list of allowed words
        #self.allowed_wordlist = allowed_wordlist
    
    #run game method that executes the wordle() gameplay 
    def run_game(self):
        for i in range(len(self.wordlist)):
            game_data = self.wordle(self.wordlist[i], i, self.words_correct, self.score)
            self.score += game_data[0]
            self.words_correct.append((game_data[1], game_data[2]))

    #the wordle() method takes in a word from the wordlist to use as the answer, the current number of games that have been played, the number of previous words correct, and the current score
    #the wordle() method returns the updated score and number of words correct
    def wordle(self, word, gc, c, scr):
        #helper function
        def TextChar(value, key):
            return sg.Input(value, key=key, font=('_', 28), size=(2, 4), pad=(0,0), disabled_readonly_background_color='light gray', border_width=2,  p=1, enable_events=True, disabled=True, justification='center')
        
        #Wordle game UI
        sg.theme('LightBrown1')

        #data needed for the game
        answer = word
        game_count = gc
        score = 0
        cur_score = scr
        last_c = c

        #game progess UI
        guess_count = [sg.Button(str(j+1),font=('_', 20, 'bold'), key=(j, -1), size=(2,1), border_width=1.75, disabled=True, button_color='tan', pad=(0,(0, 5)), focus=False) for j in range(6)]

        #Wordle grid UI
        frame = [[TextChar('', (row, col)) for col in range(5)] for row in range(6)]

        layout = [
                [sg.Text('wordle', font=('_', 50, 'bold'), pad=(0, (0, 5)))],
                [sg.Text(f'score: {cur_score}', font=('_', 20), pad=(0,(0, 10)), key='SCORE')],
                [guess_count],
                [sg.Frame('', frame, border_width=1, relief='sunken', element_justification='center', pad=(0, (10, 5)))],
                [sg.B('enter', font=('_', 20, 'bold'), size=(10, 1), bind_return_key=True, pad=(0, 0), visible=True)],
                [sg.Button('next word', font=('_', 20, 'bold'), pad=(0, 5), visible=False)],
                ]

        window = sg.Window("mongoose.", layout, finalize=True, size=(500, 500), element_justification='center')

        cur_row, correct = 0, False
        [window[(cur_row, col)].update(disabled=False) for col in range(5)]
        window[(cur_row, 0)].set_focus()
        window.bind('<BackSpace>', '-BACKSPACE-')

        #updates the game progress UI
        for i in range(len(last_c)):
            if last_c[i][0]:
                window[(i, -1)].update(button_color='green')
            else:
                window[(i, -1)].update(button_color='red')

        #game execution
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                cur_row = 6
                break
            
            if isinstance(event, tuple):
                if len(values[event]):
                    row, col = event
                    char_input = values[event][-1]
                    if not char_input.isalpha():    # if not a character input, remove the input
                        window[event].update('')
                    else:
                        window[event].update(char_input.upper()[0])     # convert to uppercase
                        if col < 4:
                            window[(row, col+1)].set_focus()    # Move to next position
                
            elif event == 'enter':
                guess = ''.join([values[(cur_row, j)] for j in range(5)])

                #checks for valid guess
                if len(guess) < 5:
                    sg.popup('please guess a 5-letter word.', title='error.',  font='_ 12', keep_on_top=True, button_justification='center')
                    continue
                # if guess not in self.allowed_wordslist:
                #     sg.popup('WORD NOT IN WORDLIST', title='error.',  font='_ 12', keep_on_top=True, button_justification='center')
                #     continue

                #letter coloring functionality
                answer2 = [answer[i] for i in range(0, len(answer))]
                for i in range (0, len(guess)):
                    if guess[i] == answer2[i]:
                        window[(cur_row, i)].update(background_color='green', text_color='white')
                        answer2[i] = '*'

                    elif guess[i] in answer2:
                        window[(cur_row, i)].update(background_color='#C9B359', text_color='white')
                        answer2[i] = '*'

                    else:
                        window[(cur_row, i)].update(background_color='gray', text_color='white')

                if guess == answer:
                    correct = True
                    break

                cur_row += 1    # Move to the next row
                if cur_row > 5:     # If we passed the last row, end the game
                    break
                
                [window[(cur_row, col)].update(disabled=False) for col in range(5)]     # Enable inputs on next row
                window[(cur_row, 0)].set_focus()     # Move to first position on row

            #ability to backspace on keyboard
            elif event == '-BACKSPACE-':
                current_focus = window.find_element_with_focus()
                current_key = current_focus.Key
                if isinstance(current_key, tuple):
                    window[current_key].update('')
                    if current_key[1] > 0:
                        window[(current_key[0], current_key[1]-1)].set_focus()
                        window[(current_key[0], current_key[1]-1)].update('')

        if correct:
            sg.popup('correct!', title='good job', font=('_', 20), keep_on_top=True, button_justification='center')
        else:
            sg.popup(f'Sorry... the word was {answer}', title='L', font=('_', 14), keep_on_top=True, button_justification='center')

        window.close()

        score = 6 - cur_row     #calculates score

        return score, correct, answer   #returns game data


