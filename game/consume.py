from ecs import *
from base import *
from control import Step
from field import GameField, FieldPosition, FieldMotion, calc_target

class Consumable(Component):
    pass

class Consumed(Component):
    pass

class ConsumeStepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        field: GameField = world.get_component(world.get_global_entity(), GameField) #type: ignore
        if world.is_status("get_component", "NO_COMPONENT"):
            return
        heroes = world.get_entities({Step, FieldPosition}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        if world.has_component(hero, FieldMotion):
            return
        position: FieldPosition = world.get_component(hero, FieldPosition) #type: ignore
        step: Step = world.get_component(hero, Step) #type: ignore
        target_position = calc_target(position, step.direction)
        if not field.is_cell_obstacle(target_position.x, target_position.y):
            return
        target = field.get_cell_entity(target_position.x, target_position.y)
        if not world.has_component(target, Consumable):
            return
        world.add_component(hero, FieldMotion(step.direction, 0))
        world.add_component(target, Consumed())


class ConsumeSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        field: GameField = world.get_component(world.get_global_entity(), GameField) #type: ignore
        entities = world.get_entities({Consumed, FieldPosition}, set())
        while not entities.is_empty():
            entity = entities.get_entity()
            entities.remove_entity(entity)
            position: FieldPosition = world.get_component(entity, FieldPosition) #type: ignore
            field.clear_cell(position.x, position.y)
            world.clean_entity(entity)

