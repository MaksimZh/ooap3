import pygame as pg
from ecs import *

class InputSystem(System):

    __requests_quit: bool

    def __init__(self) -> None:
        self.__requests_quit = False

    def run(self, world: World, frame_time: Timems) -> None:
        for event in pg.event.get():
            self.__requests_quit = self.__requests_quit or event.type == pg.QUIT

    def clean(self) -> None:
        pass

    def requests_quit(self) -> bool:
        return self.__requests_quit
