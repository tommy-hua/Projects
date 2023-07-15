import PySimpleGUI as sg

from lobbygamescreen import LobbyGameScreen
from ingamescreen import InGameScreen
from endgamescreen import EndGameScreen

'''
We utilized a facade pattern for the ui
the facade class is GameScreen, and it has 3 attributes: LobbyGameScreen, InGameScreen, and EndGameScreen
'''

#facade class
class GameScreen:
    def __init__(self):
        #initialize the 3 screens
        self.lobby_gs = LobbyGameScreen()
        self.ingame_gs = InGameScreen()
        self.endgame_gs = EndGameScreen()

    #method to send updates to the relevant game screens
    def send_updates():
        pass

    
####################################################################################################

# for testing purposes/demonstration
if __name__ == '__main__':
    demo_wl = ['WORDS', 'SERUM', 'COUNT', 'ABYSS', 'SLEEP', 'SOUND']
    demo_wa = [('WORDS', True), ('SERUM', False), ('COUNT', True), ('ABYSS', True), ('SLEEP', True), ('SOUND', False)]
    demo_score, demo_opp_score = 23, 12

    #LobbyGameScreen()
    InGameScreen(demo_wl).run_game()
    #EndGameScreen(demo_score, demo_opp_score, demo_wa).end_game()
    

