import sys
import pygame as pg

import ecs
import engine as eg
from input import InputSystem, PlayerControl
from graphics import Sprite, GraphicsSystem
from field import GameField, FieldPosition, CameraFollow, CameraSystem, MotionSystem
from control import ControlSystem, StepSystem

game_path = sys.path[0]
sprites = pg.image.load(game_path + "/sprites.png")


world = ecs.World()
field = GameField(10, 10)
e = world.new_entity()
world.add_entity(e)
world.add_component(e, field)

def add_to_field(x: int, y: int) -> ecs.Entity:
    e = world.new_entity()
    world.add_entity(e)
    world.add_component(e, FieldPosition(x, y))
    field.set_cell(x, y, e)
    return e

def add_wall(x: int, y: int) -> ecs.Entity:
    e = add_to_field(x, y)
    world.add_component(e, Sprite(sprites, pg.Rect(0, 48, 48, 48)))
    return e

e = add_to_field(5, 5)
world.add_component(e, Sprite(sprites, pg.Rect(0, 0, 48, 48)))
world.add_component(e, PlayerControl())
add_wall(4, 6)
e = add_wall(5, 6)
world.add_component(e, CameraFollow())
add_wall(6, 6)
systems = ecs.SystemList()
systems.add(MotionSystem())
systems.add(InputSystem())
systems.add(ControlSystem())
systems.add(StepSystem())
systems.add(CameraSystem())
systems.add(GraphicsSystem())
engine = eg.Engine(world, systems)
engine.run()
