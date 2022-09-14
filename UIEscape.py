import pygame as pg


class UIForMaze:
    def __init__(self, _edge, _width, _height):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (20, 144, 255)
        self.GREEN = (50, 205, 50)
        self.ORANGE = (236, 135, 14)
        self.PINK = (197, 124, 172)
        self.YELLOW = (249, 244, 0)
        self.VIOLET = (81, 31, 144)
        self.edge = _edge
        self.width = _width
        self.height = _height
        screen_width = self.edge * self.width * 1.3 + 10
        self.display = pg.display.set_mode((screen_width if screen_width > 650 else 650, self.edge * self.height), 0, 32)
        self.start = self.edge * self.width + 5
        self.grid = [[0 for i in range(self.width)] for j in range(self.height)]
        self.mini_map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.text = [[0 for i in range(self.width)] for j in range(self.height)]
        self.display.fill(self.WHITE)
        pg.init()
        pg.display.set_caption("Escape")

    def color(self, x):
        switcher = {
            1: self.WHITE,  # road
            -1: self.BLACK,  # hide
            2: self.WHITE,   # agent
            0: self.BLUE,   # wall
            3: self.GREEN   # goal
        }
        return switcher.get(x, "nothing")

    def agent_color(self, x):
        switcher = {
            0: self.ORANGE,
            1: self.PINK,
            2: self.YELLOW,
            3: self.VIOLET,
            4: self.RED
        }
        return switcher.get(x, "nothing")

    def agent_size(self, x):
        switcher = {
            1: 50,
            2: 55,
            3: 60,
            4: 65,
            5: 70
        }
        return switcher.get(x, "nothing")

    def draw_maze(self, map, agents, real_map, unexplored, speed):
        for x in range(self.height):
            for y in range(self.width):
                lane_color = self.color(map[x][y])
                if map[x][y] == 1 and (x, y) in unexplored:
                    lane_color = self.RED
                self.grid[x][y] = pg.draw.rect(self.display, lane_color , (self.edge*y, self.edge*x, self.edge, self.edge))
                self.mini_map[x][y] = pg.draw.rect(self.display, self.color(real_map[x][y]), (self.edge*y*0.3 + self.start, self.edge*x*0.3, self.edge*0.3, self.edge*0.3))
                sym = ""
                _size = self.edge
                _color = self.WHITE
                if map[x][y] == 2:
                    sym = chr(215)
                    for agent in agents:
                        if agent.current_pos == (x, y):
                            _size = self.agent_size(agent.cells)
                            _color = self.agent_color(agents.index(agent))
                self.text[x][y] = pg.font.SysFont(None, _size).render(sym, True, _color)
                rect_text = self.text[x][y].get_rect()
                rect_text.centerx = self.grid[x][y].centerx
                rect_text.centery = self.grid[x][y].centery
                self.display.blit(self.text[x][y], rect_text)
            text_size = 30
            pg.draw.rect(self.display, self.WHITE, (self.start, self.edge * self.height * 0.3 + text_size * 4, 200, self.edge))
            stop_text = pg.font.SysFont(None, text_size).render("Enter to Stop", True, self.BLACK)
            pause_text = pg.font.SysFont(None, text_size).render("Space to Pause", True, self.BLACK)
            speed_up = pg.font.SysFont(None, text_size).render("(+) to Speed Up", True, self.BLACK)
            speed_down = pg.font.SysFont(None, text_size).render("(-) to Speed Down", True, self.BLACK)
            cur_speed = pg.font.SysFont(None, text_size).render("Speed: "+ str(round(1000/speed, 2)) + " FPS", True, self.BLACK)
            self.display.blit(stop_text, (self.start, self.edge * self.height * 0.3 + text_size*0))
            self.display.blit(pause_text, (self.start, self.edge * self.height * 0.3 + text_size*1))
            self.display.blit(speed_up, (self.start, self.edge * self.height * 0.3 + text_size*2))
            self.display.blit(speed_down, (self.start, self.edge * self.height * 0.3 + text_size*3))
            self.display.blit(cur_speed, (self.start, self.edge * self.height * 0.3 + text_size * 4))
        pg.display.update()
        pg.time.delay(speed)
