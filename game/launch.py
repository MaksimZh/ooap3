import sys
import pygame as pg

import ecs
import engine as eg
from input import InputSystem
from graphics import Sprite, GraphicsSystem
from field import FieldPosition, CameraFollow, CameraSystem

game_path = sys.path[0]
sprites = pg.image.load(game_path + "/sprites.png")


world = ecs.World()

def add_wall(x: int, y: int):
    e = world.new_entity()
    world.add_entity(e)
    world.add_component(e, Sprite(sprites, pg.Rect(0, 48, 48, 48)))
    world.add_component(e, FieldPosition(x, y))

e = world.new_entity()
world.add_entity(e)
world.add_component(e, Sprite(sprites, pg.Rect(0, 0, 48, 48)))
world.add_component(e, FieldPosition(15, 15))
world.add_component(e, CameraFollow())
add_wall(14, 16)
add_wall(15, 16)
add_wall(16, 16)
systems = ecs.SystemList()
systems.add(InputSystem())
systems.add(CameraSystem())
systems.add(GraphicsSystem())
engine = eg.Engine(world, systems)
engine.run()
