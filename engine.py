import pygame as pg

FPS = 30
BACKGROUND_COLOR = (0, 0, 32)


class Engine:

    __screen: pg.Surface

    def __init__(self) -> None:
        pg.init()
        self.__screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    def run(self) -> None:
        running = True
        clock = pg.time.Clock()
        while running:
            clock.tick(FPS)
            self.__screen.fill(BACKGROUND_COLOR)
            self.frame(clock.get_time())
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
        pg.quit()

    def frame(self, time: int) -> None:
        print(time)

Engine().run()
