import pygame as pg
from control import *
from MapDesign import *

GRAY = (160, 160, 160)
UNKNOW = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PINK = (197, 124, 172)
ORANGE = (236, 135, 14)

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
NUM_BLOCK_HEIGHT = ""
NUM_BLOCK_WIDTH = ""
NUMBER_AGENT = ""
BLOCK_SIZE = 40


class EnterSize:
    def __init__(self):
        pg.init()
        self.screen_size = screenSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.button_set = CreateButton(BLUE, 440, 500, 100, 50)
        self.button_rand = CreateButton(BLUE, 260, 500, 100, 50)
        self.button_quit = CreateButton(BLUE, 70, 500, 100, 50)
        self.textbox_width = CreateTextBox(70, WINDOW_HEIGHT / 2, "", 90, WINDOW_HEIGHT / 2 + 5)
        self.textbox_height = CreateTextBox(250, WINDOW_HEIGHT / 2, "", 275, WINDOW_HEIGHT / 2 + 5)
        self.textbox_num_agent = CreateTextBox(430, WINDOW_HEIGHT / 2, "[1,5]", 460, WINDOW_HEIGHT / 2 + 5)
        self.label_form = CreateLaBel(220, 100, "ENTER SIZE")
        self.label_maxsize = CreateLaBel(100, 200, "MAX SIZE = 25x15, MIN SIZE = 5x5")
        self.label_width = CreateLaBel(90, WINDOW_HEIGHT / 2 + 60, "Width")
        self.label_height = CreateLaBel(265, WINDOW_HEIGHT / 2 + 60, "Height")
        self.label_num_agent = CreateLaBel(400, WINDOW_HEIGHT / 2 + 60, "Number Agent")
        self.label_error = CreateLaBel(240, 430, "Error Value", "black")
        self.wordbox_width = ""
        self.wordbox_height = ""
        self.wordbox_num_agent = ""

    def Draw(self):
        self.wordbox_width = DrawTextBox(self.textbox_width, NUM_BLOCK_WIDTH)
        self.wordbox_height = DrawTextBox(self.textbox_height, NUM_BLOCK_HEIGHT)
        self.wordbox_num_agent = DrawTextBox(self.textbox_num_agent, NUMBER_AGENT)
        DrawButton(self.button_set, self.screen_size, WHITE, 'Set Map')
        DrawButton(self.button_quit, self.screen_size, WHITE, 'Quit')
        DrawButton(self.button_rand, self.screen_size, WHITE, 'Rand Map')
        DrawLabel(self.label_form)
        DrawLabel(self.label_maxsize)
        DrawLabel(self.label_width)
        DrawLabel(self.label_height)
        DrawLabel(self.label_num_agent)
        DrawLabel(self.label_error)

    def IsNumber(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def Run(self):
        global NUM_BLOCK_HEIGHT
        global NUM_BLOCK_WIDTH
        global NUMBER_AGENT

        while True:
            self.Draw()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.textbox_width.IsOver(pos):
                        user_result = self.textbox_width.InputText(self.wordbox_width)
                        if self.IsNumber(user_result) and int(user_result) <= 25 and int(user_result) >= 5:
                            self.label_error.color = "black"
                            NUM_BLOCK_WIDTH = user_result
                        else:
                            self.label_error.color = "red"
                            NUM_BLOCK_WIDTH = ""
                    elif self.textbox_height.IsOver(pos):
                        user_result = self.textbox_height.InputText(self.wordbox_height)
                        if self.IsNumber(user_result) and int(user_result) <= 15 and int(user_result) >= 5:
                            self.label_error.color = "black"
                            NUM_BLOCK_HEIGHT = user_result
                        else:
                            self.label_error.color = "red"
                            NUM_BLOCK_HEIGHT = ""
                    elif self.textbox_num_agent.IsOver(pos):
                        user_result = self.textbox_num_agent.InputText(self.wordbox_num_agent)
                        if self.IsNumber(user_result) and int(user_result) <= 5 and int(user_result) >= 1:
                            self.label_error.color = "black"
                            NUMBER_AGENT = user_result
                        else:
                            self.label_error.color = "red"
                            NUMBER_AGENT = ""
                    elif self.button_set.IsOver(pos):
                        if self.IsNumber(NUM_BLOCK_WIDTH) and self.IsNumber(NUM_BLOCK_HEIGHT) and self.IsNumber(NUMBER_AGENT):
                            pg.quit()
                            return int(NUMBER_AGENT), SetPath(int(NUM_BLOCK_WIDTH) + 2, int(NUM_BLOCK_HEIGHT) + 2).Run()
                    elif self.button_rand.IsOver(pos):
                        if self.IsNumber(NUM_BLOCK_WIDTH) and self.IsNumber(NUM_BLOCK_HEIGHT) and self.IsNumber(NUMBER_AGENT):
                            pg.quit()
                            return int(NUMBER_AGENT), rand_maze(int(NUM_BLOCK_WIDTH), int(NUM_BLOCK_HEIGHT), 90)
                    elif self.button_quit.IsOver(pos):
                        pygame.quit()
                        return None ,False
                if event.type == pygame.MOUSEMOTION:
                    if self.button_set.IsOver(pos):
                        self.button_set.color = RED
                    elif self.button_quit.IsOver(pos):
                        self.button_quit.color = RED
                    elif self.button_rand.IsOver(pos):
                        self.button_rand.color = RED
                    else:
                        self.button_set.color = GREEN
                        self.button_quit.color = GREEN
                        self.button_rand.color = GREEN


class SetPath:
    def __init__(self, width, height, real_map=None):
        self.width = width
        self.height = height
        pg.init()
        self.screen_path = pg.display.set_mode((self.width * BLOCK_SIZE + 260, self.height * BLOCK_SIZE + 60))
        pg.display.set_caption('Chose Path')
        self.screen_path.fill(BLUE)
        if real_map:
            self.real_map = real_map
        else:
            self.real_map = [[-2 if x == 0 or y == 0 or y == height - 1 or x == width - 1 else 0 for x in range(width)] for
                         y in range(height)]
        self.button_next = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 - 40, 100, 50)
        self.button_back = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 + 40, 100, 50)
        # self.font = pg.font.Font(pg.font.get_default_font(), 20)
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        self.text = [[None for i in range(self.width)] for j in range(self.height)]

    def Draw(self):
        self.Create_Map()
        DrawButton(self.button_back, self.screen_path, WHITE, 'Back')
        DrawButton(self.button_next, self.screen_path, WHITE, 'Next')
        # text_chose_path = self.font.render('Click on Box to Chose your path', True, BLUE)
        # self.screen_path.blit(text_chose_path, dest=(140, 30))

    def CheckGrid(self, pos):
        x = int((pos[1] - 30) / BLOCK_SIZE)
        y = int((pos[0] - 30) / BLOCK_SIZE)
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            return False
        return [x, y]

    def Create_Map(self):
        for x in range(self.height):
            for y in range(self.width):
                color = GRAY
                symbol = ""
                if self.real_map[x][y] == 1:
                    color = WHITE
                elif self.real_map[x][y] == -2:
                    symbol = "X"
                self.grid[x][y] = pg.draw.rect(self.screen_path, color,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE))
                self.grid[x][y] = pg.draw.rect(self.screen_path, WHITE,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE), 1)
                self.text[x][y] = pg.font.SysFont(None, 20).render(symbol, True, RED)
                rect_text = self.text[x][y].get_rect()
                rect_text.centerx = self.grid[x][y].centerx
                rect_text.centery = self.grid[x][y].centery
                self.screen_path.blit(self.text[x][y], rect_text)

    def Run(self):
        while True:
            self.Draw()
            pos = pygame.mouse.get_pos()
            # print(pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    index = self.CheckGrid(pos)
                    if self.button_back.IsOver(pos):
                        pg.quit()
                        return EnterSize().Run()
                    elif self.button_next.IsOver(pos):
                        pg.quit()
                        return SetGoal(self.width, self.height, self.real_map).Run()
                    elif index:
                        self.real_map = set_lane(self.real_map, index)[0]

                if event.type == pygame.MOUSEMOTION:
                    if self.button_next.IsOver(pos):
                        self.button_next.color = RED
                    elif self.button_back.IsOver(pos):
                        self.button_back.color = RED
                    else:
                        self.button_next.color = GREEN
                        self.button_back.color = GREEN

            pygame.display.update()


class SetGoal:
    def __init__(self, width, height, real_map):
        self.width = width
        self.height = height
        pg.init()
        self.screen_goal = pg.display.set_mode((self.width * BLOCK_SIZE + 260, self.height * BLOCK_SIZE + 60))
        pg.display.set_caption('Chose Goal')
        self.screen_goal.fill(BLUE)
        self.last_map = [[col for col in row] for row in real_map]
        self.real_map = to_goal_map(get_lane(real_map))
        self.button_next = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 - 40, 100, 50)
        self.button_back = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 + 40, 100, 50)
        # self.font = pg.font.Font(pg.font.get_default_font(), 20)
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        self.text = [[None for i in range(self.width)] for j in range(self.height)]
        self.goal_pos = None

    def Draw(self):
        self.Create_Map()
        DrawButton(self.button_back, self.screen_goal, WHITE, 'Back')
        DrawButton(self.button_next, self.screen_goal, WHITE, 'Next')
        # text_chose_path = self.font.render('Click on Box to Chose your path', True, BLUE)
        # self.screen_path.blit(text_chose_path, dest=(140, 30))

    def CheckGrid(self, pos):
        x = int((pos[1] - 30) / BLOCK_SIZE)
        y = int((pos[0] - 30) / BLOCK_SIZE)
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            return False
        return [x, y]

    def Create_Map(self):
        for x in range(self.height):
            for y in range(self.width):
                color = GRAY
                symbol = ""
                text_color = RED
                if self.real_map[x][y] == 1:
                    color = WHITE
                elif self.real_map[x][y] == 3:
                    if self.goal_pos and self.goal_pos == [x, y]:
                        symbol = "G"
                        text_color = BLACK
                    color = GREEN
                if self.real_map[x][y] != 3:
                    symbol = "X"
                self.grid[x][y] = pg.draw.rect(self.screen_goal, color,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE))
                self.grid[x][y] = pg.draw.rect(self.screen_goal, WHITE,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE), 1)
                self.text[x][y] = pg.font.SysFont(None, 30).render(symbol, True, text_color)
                rect_text = self.text[x][y].get_rect()
                rect_text.centerx = self.grid[x][y].centerx
                rect_text.centery = self.grid[x][y].centery
                self.screen_goal.blit(self.text[x][y], rect_text)

    def Run(self):
        while True:
            self.Draw()
            pos = pygame.mouse.get_pos()
            # print(pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    index = self.CheckGrid(pos)
                    if self.button_back.IsOver(pos):
                        pg.quit()
                        return SetPath(self.width, self.height, self.last_map).Run()
                    elif self.button_next.IsOver(pos):
                        if self.goal_pos:
                            pg.quit()
                            return SetStart(self.width, self.height, self.last_map, self.goal_pos).Run()
                    elif index:
                        if set_goal(self.real_map, index):
                            self.goal_pos = index

                if event.type == pygame.MOUSEMOTION:
                    if self.button_next.IsOver(pos):
                        self.button_next.color = RED
                    elif self.button_back.IsOver(pos):
                        self.button_back.color = RED
                    else:
                        self.button_next.color = GREEN
                        self.button_back.color = GREEN

            pygame.display.update()


class SetStart:
    def __init__(self, width, height, real_map, goal_pos):
        self.width = width
        self.height = height
        pg.init()
        self.screen_start = pg.display.set_mode((self.width * BLOCK_SIZE + 260, self.height * BLOCK_SIZE + 60))
        pg.display.set_caption('Chose Goal')
        self.screen_start.fill(BLUE)
        self.last_map = [[col for col in row] for row in real_map]
        self.real_map = to_goal_map(get_lane(real_map))
        replace(self.real_map, 3, 0)
        self.real_map[goal_pos[0]][goal_pos[1]] = 3
        self.button_next = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 - 40, 100, 50)
        self.button_back = CreateButton(GREEN, self.width * BLOCK_SIZE + 80, self.height * BLOCK_SIZE / 2 + 40, 100, 50)
        # self.font = pg.font.Font(pg.font.get_default_font(), 20)
        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        self.text = [[None for i in range(self.width)] for j in range(self.height)]
        self.start_pos = None

    def Draw(self):
        self.Create_Map()
        DrawButton(self.button_back, self.screen_start, WHITE, 'Back')
        DrawButton(self.button_next, self.screen_start, WHITE, 'Next')
        # text_chose_path = self.font.render('Click on Box to Chose your path', True, BLUE)
        # self.screen_path.blit(text_chose_path, dest=(140, 30))

    def CheckGrid(self, pos):
        x = int((pos[1] - 30) / BLOCK_SIZE)
        y = int((pos[0] - 30) / BLOCK_SIZE)
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            return False
        return [x, y]

    def Create_Map(self):
        for x in range(self.height):
            for y in range(self.width):
                color = GRAY
                symbol = ""
                text_color = RED
                if self.real_map[x][y] == 1:
                    if self.start_pos and self.start_pos == [x, y]:
                        symbol = "S"
                        text_color = BLACK
                    color = WHITE
                elif self.real_map[x][y] == 3:
                    color = GREEN
                if self.real_map[x][y] != 1:
                    symbol = "X"
                self.grid[x][y] = pg.draw.rect(self.screen_start, color,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE))
                self.grid[x][y] = pg.draw.rect(self.screen_start, WHITE,
                                               (y * BLOCK_SIZE + 30, x * BLOCK_SIZE + 30, BLOCK_SIZE, BLOCK_SIZE), 1)
                self.text[x][y] = pg.font.SysFont(None, 30).render(symbol, True, text_color)
                rect_text = self.text[x][y].get_rect()
                rect_text.centerx = self.grid[x][y].centerx
                rect_text.centery = self.grid[x][y].centery
                self.screen_start.blit(self.text[x][y], rect_text)

    def Run(self):
        while True:
            self.Draw()
            pos = pygame.mouse.get_pos()
            # print(pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    index = self.CheckGrid(pos)
                    if self.button_back.IsOver(pos):
                        pg.quit()
                        return SetGoal(self.width, self.height, self.last_map).Run()
                    elif self.button_next.IsOver(pos):
                        if self.start_pos:
                            pg.quit()
                            return get_init(self.real_map, self.start_pos)
                    elif index:
                        if set_init(self.real_map, index):
                            self.start_pos = index

                if event.type == pygame.MOUSEMOTION:
                    if self.button_next.IsOver(pos):
                        self.button_next.color = RED
                    elif self.button_back.IsOver(pos):
                        self.button_back.color = RED
                    else:
                        self.button_next.color = GREEN
                        self.button_back.color = GREEN

            pygame.display.update()


