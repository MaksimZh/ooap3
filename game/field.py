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
        screen_size_entity = world.get_single_entity({ScreenSize})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        screen_size: ScreenSize = world.get_component(screen_size_entity, ScreenSize) #type: ignore
        x0 = screen_size.width / 2
        y0 = screen_size.height / 2
        camera_follow_entity = world.get_single_entity({CameraFollow, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        camera_field_position: FieldPosition = world.get_component(camera_follow_entity, FieldPosition) #type: ignore
        camera_x = camera_field_position.x
        camera_y = camera_field_position.y
        if world.has_component(camera_follow_entity, FieldMotion):
            motion: FieldMotion = world.get_component(camera_follow_entity, FieldMotion) #type: ignore
            target = calc_target(camera_field_position, motion)
            camera_x = camera_x * (1 - motion.progress) + target.x * motion.progress
            camera_y = camera_y * (1 - motion.progress) + target.y * motion.progress
        entities = world.get_entities({FieldPosition}, set())
        while not entities.is_empty():
            entity = entities.get_entity()
            field_position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
            x = field_position.x
            y = field_position.y
            if world.has_component(entity, FieldMotion):
                motion: FieldMotion = world.get_component(entity, FieldMotion) #type: ignore
                target = calc_target(field_position, motion)
                x = x * (1 - motion.progress) + target.x * motion.progress
                y = y * (1 - motion.progress) + target.y * motion.progress
            if not world.has_component(entity, ScreenPosition):
                world.add_component(entity, ScreenPosition(0, 0))
            screen_position: ScreenPosition = world.get_component(entity, ScreenPosition) #type: ignore
            screen_position.x = int(x0 + (x - camera_x - 0.5) * cell_size)
            screen_position.y = int(y0 + (y - camera_y - 0.5) * cell_size)
            sp: ScreenPosition = world.get_component(entity, ScreenPosition) #type: ignore
            entities.remove_entity(entity)
