import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import json
import random


class Game(Player):
    def __init__(self, loop, file="maths.json"):
        self.loop = loop
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.display = self.screen  # for menu screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.question = -1
        self.game_over = False
        self.load_data(file)
        self.show_question = True
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.score_value = 0
        self.timer = 0
        self.point_coords = []
        self.correct_answer = 0
        self.countdown = 15
        self.new()

    game_over_image = pg.image.load(path.join('assets', 'gameoverscreen.png'))

    def load_data(self, file="maths.json"):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map.txt'))
        with open(file) as load_questions:#opens and then closes json file after usage.
            self.questions = json.load(load_questions)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.points = pg.sprite.Group()
        self.point_list = [Point(self, 0), Point(self, 1), Point(self, 2)]

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

                if tile == 'D':
                    self.point_coords.append((col, row))

        print(self.point_coords)
        # self.camera = Camera(self.map.width, self.map.height)
        #self.playing = True
        self.new_question()

    def tick(self):
        # game loop - set self.playing = False to end the
        self.dt = self.clock.tick(FPS) / 1000

        self.timer += self.dt
        self.events()
        self.update()
        self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        if self.game_over is True:
            pass
        else:
            self.all_sprites.update()
            # self.camera.update(self.player)  # can put any sprite you want for camera to track

            if self.show_question:
                # putting it in show question allows user to know right answer even after the game has finished
                if self.countdown <= 0:
                    # update question screen
                    pass
            else:
                 #draw answer


                self.new_question()

                     #shows, new question after 0.5 seconds
                pass

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw_question(self):
        current_question = self.questions["questions"][self.questions["order"][self.question]]["question"]
        answers = self.questions["questions"][self.questions["order"][self.question]]["answer"]
        questions_text = self.font.render(current_question, True, WHITE)
        self.screen.blit(questions_text, (WIDTH // 2 - questions_text.get_width()//2, 0))
        answers = answers[3 - self.correct_answer:3] + answers[0:3 - self.correct_answer] # randomizes the answer selection, self.correct_answer = correct index
        for answer in range(len(answers)):
            answers_text = self.font.render(answers[answer], True, WHITE)
            self.screen.blit(answers_text, (answer * WIDTH // len(answers) + 100, HEIGHT - TILESIZE * 2))
        print (answers)


    def new_question(self):
        self.show_question = True
        self.question += 1 #"order" in json will go up by one.
        self.correct_answer = random.randrange(3)
        current_choice = random.sample(self.point_coords, 3)
        for x in range(3):
            self.point_list[x].move_point(current_choice[x])

    def next_question(self, choice):
        if self.show_question == True:
            self.show_question = False
            if choice == self.correct_answer:
                self.score_value += 1
                self.countdown += 5
            else:
                self.score_value -= 1
            print(self.score_value)


    def draw(self):

        if self.countdown <= 0 and self.show_question is True or self.game_over is True:
            finalscore = self.font.render(str(self.score_value), True, YELLOW)

            self.screen.blit(self.game_over_image, [0, 0])
            self.screen.blit(finalscore, [400, 500])  # MOVE TO THE CORRECT POSITION
            self.game_over = True


        else:
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            for sprite in self.all_sprites:
                # self.screen.blit(sprite.image, self.camera.apply(sprite))
                self.screen.blit(sprite.image, sprite)
                # iterates over each sprite, applying transformation to them.
            self.draw_UI()
        pg.display.flip()

    def draw_UI(self):
        # countdown timer

        self.countdown -= self.dt
        displaycountdown = math.trunc(self.countdown)
        # scorepointer
        text = self.font.render('Score: ' + str(self.score_value), True, GREEN)
        textRect = text.get_rect()
        countdowntext = self.font.render(str(displaycountdown), True, GREEN)

        pg.draw.rect(self.screen, BLACK, (0, 0, WIDTH, TILESIZE * 3))
        pg.draw.rect(self.screen, BLACK, (0, HEIGHT - TILESIZE * 3, WIDTH, TILESIZE * 3))
        pg.draw.rect(self.screen, BLUE, (0, HEIGHT - TILESIZE * 3, 200, 200))
        pg.draw.rect(self.screen, RED, (400, HEIGHT - TILESIZE * 3, 200, 200))
        pg.draw.rect(self.screen, LIGHTGREY, (750, HEIGHT - TILESIZE * 3, 200, 200))

        self.screen.blit(text, textRect)
        self.screen.blit(countdowntext, [980, 1])

        if self.show_question:
            # draw the question
            self.draw_question()
        else:
            # draws correct answer
            pass

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.key == pg.K_RETURN and self.game_over is True:
                    self.loop.state = "menu"
