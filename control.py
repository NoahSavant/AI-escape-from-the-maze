import pygame.freetype
from pygame_functions import *


class CreateTextBox:
    def __init__(self, x, y, word, x_text, y_text):
        self.x = x
        self.y = y
        self.word = word
        self.x_text = x_text
        self.y_text = y_text

    def Create(self):
        wordBox = makeTextBox(self.x, self.y, 100, 0, self.word, 2, 24)
        showTextBox(wordBox)
        return wordBox

    def InputText(self, wordBox):
        text = textBoxInput(wordBox)
        label = CreateLaBel(self.x_text, self.y_text, text)
        label.Create()
        return text

    def IsOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + 100:
            if pos[1] > self.y and pos[1] < self.y + 40:
                return True
        return False


class CreateButton:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def Create(self, win, outline=None, word=''):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if word != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(word, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def IsOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class CreateLaBel:
    def __init__(self, x, y, text, color='red'):
        self.x = x
        self.y = y
        self.text = text
        self.color = color

    def Create(self):
        wordLabel = makeLabel(self.text, 30, self.x, self.y, self.color)
        showLabel(wordLabel)


def DrawTextBox(textbox, text=""):
    textbox.word = text
    wordBox = textbox.Create()
    return wordBox


def DrawLabel(label):
    label.Create()


def DrawButton(button, win, color, word):
    button.Create(win, color, word)
