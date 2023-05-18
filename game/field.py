from dataclasses import dataclass
from ecs import *
from graphics import ScreenPosition, ScreenSize


@dataclass
class FieldPosition(Component):
    x: int
    y: int

class CameraFollow(Component):
    pass

class CameraSystem(System):

    def __init__(self) -> None:
        pass

    def run(self, world: World, frame_time: Timems) -> None:
        cell_size = 48
        screen_size_entities = world.get_entities({ScreenSize}, set())
        if screen_size_entities.is_empty():
            return
        screen_size_entity = screen_size_entities.get_entity()
        screen_size: ScreenSize = world.get_component(screen_size_entity, ScreenSize) #type: ignore
        x0 = screen_size.width / 2
        y0 = screen_size.height / 2
        camera_follow_entities = world.get_entities({CameraFollow, FieldPosition}, set())
        if camera_follow_entities.is_empty():
            return
        camera_follow_entity = camera_follow_entities.get_entity()
        camera_field_position: FieldPosition = world.get_component(camera_follow_entity, FieldPosition) #type: ignore
        entities = world.get_entities({FieldPosition}, set())
        while not entities.is_empty():
            entity = entities.get_entity()
            field_position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
            if not world.has_component(entity, ScreenPosition):
                world.add_component(entity, ScreenPosition(0, 0))
            screen_position: ScreenPosition = world.get_component(entity, ScreenPosition) #type: ignore
            screen_position.x = int(x0 + (field_position.x - camera_field_position.x - 0.5) * cell_size)
            screen_position.y = int(y0 + (field_position.y - camera_field_position.y - 0.5) * cell_size)
            sp: ScreenPosition = world.get_component(entity, ScreenPosition) #type: ignore
            entities.remove_entity(entity)

    def clean(self) -> None:
        pass

    def requests_quit(self) -> bool:
        return False
