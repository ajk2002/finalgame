import pygame
from settings import *

class Menu():
    def __init__(self, game, loop):
        self.loop = loop #this loop is used to indicate the menu is to run.
        self.game = game# allows you to call variables from the game class
        self.mid_w, self.mid_h = WIDTH/2, HEIGHT/2 #used to easily format where text is on the screen
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) #the square within the cursor lies
        self.offset = - 100 # so that the cursor is to the left of the options
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def draw_text(self, text, size, x, y): # used to draw the text
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def blit_screen(self): #blits it onto the screen
        self.game.display.blit(self.game.display, (0, 0))
        pygame.display.update()

class MainMenu(Menu):
    def __init__(self, game, loop):
        Menu.__init__(self, game, loop) #inherits from the menu class
        self.selected = 0 #indicates which button the cursor is on
        self.offset = -200
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.buttons = ["Start Game", "Options", "Credits"] #only one button right now, later include other buttons

    def tick(self):
        self.check_input()
        self.game.display.fill(BLACK)
        self.draw_text('Main Menu', 20, WIDTH / 2, HEIGHT / 2 - 100)
        for button_number, button in enumerate(self.buttons): #takes the position and the dat
            self.draw_text(button, 20, self.startx, self.starty + 70 * button_number)
        self.draw_cursor()
        self.blit_screen()


    def check_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.quit()
                elif event.key == pygame.K_DOWN:
                    self.selected += 1
                    if self.selected >= len(self.buttons):
                        self.selected = 0
                elif event.key == pygame.K_UP:
                    self.selected -= 1
                    if self.selected < 0:
                        self.selected = len(self.buttons) - 1
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:  # History
                        self.loop.state = "game"
                    elif self.selected == 1:  # Computer Science
                        self.loop.state = "game"
                    elif self.selected == 2:  # Maths
                        self.loop.state = "game"
    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y + 70 * self.selected)


class LevelSelectMenu(Menu):
    def __init__(self, game, loop):
        Menu.__init__(self, game, loop)
        self.selected = 0
        self.offset = - 200
        # difference 70
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.buttons = ["History", "Computer Science", "Maths", "Back"]

    def tick(self):
        self.check_input()
        self.game.display.fill(BLACK)
        self.draw_text('Level Select', 20, WIDTH / 2, HEIGHT / 2 - 100)
        for button_number, button in enumerate(self.buttons):
            self.draw_text(button, 20, self.startx, self.starty + 70 * button_number)
        self.draw_cursor()
        self.blit_screen()


    def check_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.quit()
                elif event.key == pygame.K_DOWN:
                    self.selected += 1
                    if self.selected >= len(self.buttons):
                        self.selected = 0
                elif event.key == pygame.K_UP:
                    self.selected -= 1
                    if self.selected < 0:
                        self.selected = len(self.buttons) - 1
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:  # History
                        self.loop.state = "game"
                        self.game.__init__(self.loop, "history.json")
                    elif self.selected == 1: # Computer Science
                        self.loop.state = "game"
                        self.game.__init__(self.loop, "computerscience.json")
                    elif self.selected == 2:  # Maths
                        self.loop.state = "game"
                        self.game.__init__(self.loop, "maths.json")
                    elif self.selected == 3:  # Back
                        self.loop.state = "menu"

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y + 70 * self.selected)