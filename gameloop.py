from mazee import Game
from menu import MainMenu, LevelSelectMenu
class Loop:
    def __init__(self):
        self.state = "menu"
        self.game_state = Game(self)
        self.mainmenu_state = MainMenu(self.game_state, self)
        self.levelselect_state = LevelSelectMenu(self.game_state, self)



    def main(self):

        while True:
            if self.state == "game":
                # run game updates
                self.game_state.tick()
            elif self.state == "menu":
                self.mainmenu_state.tick()
            elif self.state == "levelSelect":
                self.levelselect_state.tick()

