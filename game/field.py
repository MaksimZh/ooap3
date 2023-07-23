from dataclasses import dataclass
from typing import Union
from ecs import *
from base import *
from graphics import ScreenPosition, ScreenSize

SPEED = 0.004

@dataclass
class FieldPosition(Component):
    x: int
    y: int

@dataclass
class FieldMotion(Component):
    direction: Direction
    progress: float

def calc_target(position: FieldPosition, direction: Direction) -> FieldPosition:
    match direction:
        case Direction.UP:
            return FieldPosition(position.x, position.y - 1)
        case Direction.DOWN:
            return FieldPosition(position.x, position.y + 1)
        case Direction.LEFT:
            return FieldPosition(position.x - 1, position.y)
        case Direction.RIGHT:
            return FieldPosition(position.x + 1, position.y)

class CameraFollow(Component):
    pass

class Frozen:
    pass

frozen = Frozen()

FieldEntry = Union[None, Entity, Frozen]

class GameField(Component):

    __size: tuple[int, int]
    __entities: list[list[FieldEntry]]

    def __init__(self, width: int, height: int) -> None:
        self.__size = (width, height)
        self.__entities = [[None for _j in range(height)] for _i in range(width)]

    def clear_cell(self, x: int, y: int) -> None:
        self.__entities[x][y] = None

    def freeze_cell(self, x: int, y: int) -> None:
        self.__entities[x][y] = frozen

    def set_cell(self, x: int, y: int, entity: Entity) -> None:
        self.__entities[x][y] = entity

    def is_cell_empty(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.__size[0]:
            return False
        if y < 0 or y >= self.__size[1]:
            return False
        return self.__entities[x][y] is None

    def is_cell_obstacle(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.__size[0]:
            return False
        if y < 0 or y >= self.__size[1]:
            return False
        entry = self.__entities[x][y]
        return entry is not None and entry is not frozen
    
    def get_cell_entity(self, x: int, y: int) -> Entity:
        entry = self.__entities[x][y]
        assert isinstance(entry, Entity)
        return entry


class MotionSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        entities = world.get_entities({FieldMotion}, set())
        while not entities.is_empty():
            entity = entities.get_entity()
            motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
            motion.progress += SPEED * frame_time
            if motion.progress >= 1:
                self.__finish_motion(world, entity)
            entities.remove_entity(entity)

    def __finish_motion(self, world: World, entity: Entity) -> None:
        field: GameField = world.get_component(world.get_global_entity(), GameField) #type: ignore
        position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
        motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
        target = calc_target(position, motion.direction)
        world.remove_component(entity, FieldMotion)
        field.clear_cell(position.x, position.y)
        position.x = target.x
        position.y = target.y
        field.set_cell(position.x, position.y, entity)


class CameraSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        cell_size = 48
        x0, y0 = self.__screen_center(world)
        camera_follow_entities = world.get_entities({CameraFollow, FieldPosition}, set())
        if camera_follow_entities.is_empty():
            return
        camera_x, camera_y = self.__exact_field_position(world, camera_follow_entities.get_entity())
        entities = world.get_entities({FieldPosition}, set())
        while not entities.is_empty():
            entity = entities.get_entity()
            x, y = self.__exact_field_position(world, entity)
            if not world.has_component(entity, ScreenPosition):
                world.add_component(entity, ScreenPosition(0, 0))
            screen_position: ScreenPosition = world.get_component(entity, ScreenPosition) #type: ignore
            screen_position.x = int(x0 + (x - camera_x - 0.5) * cell_size)
            screen_position.y = int(y0 + (y - camera_y - 0.5) * cell_size)
            entities.remove_entity(entity)

    def __screen_center(self, world: World) -> tuple[float, float]:
        screen_size: ScreenSize = world.get_component(world.get_global_entity(), ScreenSize) #type: ignore
        if world.is_status("get_component", "NO_COMPONENT"):
            return 0, 0
        return screen_size.width / 2, screen_size.height / 2
    
    def __exact_field_position(self, world: World, entity: Entity) -> tuple[float, float]:
        field_position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
        x = field_position.x
        y = field_position.y
        if world.has_component(entity, FieldMotion):
            motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
            target = calc_target(field_position, motion.direction)
            x = x * (1 - motion.progress) + target.x * motion.progress
            y = y * (1 - motion.progress) + target.y * motion.progress
        return x, y
