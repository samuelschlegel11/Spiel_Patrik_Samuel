import pygame, sys
from pygame.locals import *

class Spiel:
    def __init__(self, groesse):
        self.felder = [[0 for x in range(groesse)]for y in range(groesse)]

