from ecs import *
from base import *
from control import Step, Target
from field import GameField, FieldPosition, FieldMotion

class Consumable(Component):
    pass

class Consumed(Component):
    pass

class ConsumeStepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        
        def process(components: ComponentDict) -> ComponentDict:
            step: Step = components[Step] #type: ignore
            target_component: Target = components[Target] #type: ignore
            target = target_component.target
            if not world.has_component(target, Consumable):
                components[FieldMotion] = FieldMotion(step.direction, 0)
                world.add_component(target, Consumed())
            return components

        world.process_entities(
            with_components={Step, FieldPosition, Target},
            no_components={FieldMotion},
            process=process)


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

