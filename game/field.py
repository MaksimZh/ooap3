from dataclasses import dataclass
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

def calc_target(position: FieldPosition, motion: FieldMotion) -> FieldPosition:
    match motion.direction:
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
        position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
        motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
        target = calc_target(position, motion)
        world.remove_component(entity, FieldMotion)
        position.x = target.x
        position.y = target.y


class CameraSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        cell_size = 48
        x0, y0 = self.__screen_center(world)
        camera_follow_entity = world.get_single_entity({CameraFollow, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        camera_x, camera_y = self.__exact_field_position(world, camera_follow_entity)
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
        screen_size_entity = world.get_single_entity({ScreenSize})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return 0, 0
        screen_size: ScreenSize = world.get_component(screen_size_entity, ScreenSize) #type: ignore
        return screen_size.width / 2, screen_size.height / 2
    
    def __exact_field_position(self, world: World, entity: Entity) -> tuple[float, float]:
        field_position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
        x = field_position.x
        y = field_position.y
        if world.has_component(entity, FieldMotion):
            motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
            target = calc_target(field_position, motion)
            x = x * (1 - motion.progress) + target.x * motion.progress
            y = y * (1 - motion.progress) + target.y * motion.progress
        return x, y
