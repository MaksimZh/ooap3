from abc import ABC, abstractmethod
from typing import NewType, Type
from tools import Status, status

Timems = NewType("Timems", int)

Entity = NewType("Entity", int)

class Component(ABC):
    pass

class World(Status):
    
    __next_id: int
    __entities: dict[Entity, dict[Type[Component], Component]]

    #CONSTRUCTOR
    def __init__(self) -> None:
        super().__init__()
        self.__next_id = 0
        self.__entities = dict()

    
    # COMMANDS
    
    # Add new entity
    # PRE: `entity` is not in the world
    # POST: `entity` added to the world without components
    @status("OK", "ALREADY_EXISTS")
    def add_entity(self, entity: Entity) -> None:
        if self.has_entity(entity):
            self._set_status("add_entity", "ALREADY_EXISTS")
            return
        self.__entities[entity] = dict()
        if int(entity) >= self.__next_id:
            self.__next_id = int(entity) + 1
        self._set_status("add_entity", "OK")

    # Add component to entity in the world
    # PRE: `entity` is in the world
    # PRE: `entity` has no component of this type
    # POST: `component` added to `entity`
    @status("OK", "NO_ENTITY", "ALREADY_EXISTS")
    def add_component(self, entity: Entity, component: Component) -> None:
        if not self.has_entity(entity):
            self._set_status("add_component", "NO_ENTITY")
            return
        if self.has_component(entity, type(component)):
            self._set_status("add_component", "ALREADY_EXISTS")
            return
        self._set_status("add_component", "OK")
        self.__entities[entity][type(component)] = component

    # Remove entity from the world
    # PRE: `entity` is in the world
    @status("OK", "NO_ENTITY")
    def remove_entity(self, entity: Entity) -> None:
        if not self.has_entity(entity):
            self._set_status("remove_entity", "NO_ENTITY")
            return
        del self.__entities[entity]
        self._set_status("remove_entity", "OK")

    # Remove component form the entity in the world
    # PRE: `entity` is in the world
    # PRE: component of type `component_type` belongs to `entity`
    @status("OK", "NO_ENTITY", "NO_COMPONENT")
    def remove_component(self, entity: Entity, component_type: Type[Component]) -> None:
        if not self.has_entity(entity):
            self._set_status("remove_component", "NO_ENTITY")
            return
        if not self.has_component(entity, component_type):
            self._set_status("remove_component", "NO_COMPONENT")
            return
        del self.__entities[entity][component_type]
        self._set_status("remove_component", "OK")

    
    # QUERIES

    # Check if world is empty
    def is_empty(self) -> bool:
        return len(self.__entities) == 0
    
    # Check if entity belongs to world
    def has_entity(self, entity: Entity) -> bool:
        return entity in self.__entities

    # Return new entity that is definitely not in the world
    # Note that new entity is not added to the world 
    def new_entity(self) -> Entity:
        return Entity(self.__next_id)
    
    # Check if `entity` has component of type `component_type`
    # PRE: `entity` is in the world
    @status("OK", "NO_ENTITY")
    def has_component(self, entity: Entity, component_type: Type[Component]) -> bool:
        if not self.has_entity(entity):
            self._set_status("has_component", "NO_ENTITY")
            return False
        self._set_status("has_component", "OK")
        return component_type in self.__entities[entity]
    
    # Get component of given entity
    @status("OK", "NO_ENTITY", "NO_COMPONENT")
    def get_component(self, entity: Entity, component_type: Type[Component]) -> Component:
        if not self.has_entity(entity):
            self._set_status("get_component", "NO_ENTITY")
            return Component()
        if not self.has_component(entity, component_type):
            self._set_status("get_component", "NO_COMPONENT")
            return Component()
        self._set_status("get_component", "OK")
        return self.__entities[entity][component_type]


class EntitySet(Status):

    # COMMANDS

    # Remove entity from the set
    # PRE: `entity` is in the set
    @abstractmethod
    @status("OK", "NO_ENTITY")
    def remove_entity(self, entity: Entity) -> None:
        assert False

    
    # QUERIES

    # Check if set is empty
    @abstractmethod
    def is_empty(self) -> bool:
        assert False

    # Check if entity is in the set
    @abstractmethod
    def has_entity(self, entity: Entity) -> bool:
        assert False

    # Get any entity from the set
    @abstractmethod
    @status("OK", "EMPTY")
    def get_entity(self) -> Entity:
        assert False


class ExtendableEntitySet(EntitySet):

    __entities: set[Entity]

    # CONSTRUCTOR
    # POST: empty set is created
    def __init__(self) -> None:
        super().__init__()
        self.__entities = set()

    # COMMANDS

    # Add entity to the set
    # PRE: `entity` is not in the set
    @status("OK", "ALREADY_EXISTS")
    def add_entity(self, entity: Entity) -> None:
        if self.has_entity(entity):
            self._set_status("add_entity", "ALREADY_EXISTS")
            return
        self.__entities.add(entity)
        self._set_status("add_entity", "OK")

    # Remove entity from the set
    # PRE: `entity` is in the set
    @status("OK", "NO_ENTITY")
    def remove_entity(self, entity: Entity) -> None:
        if not self.has_entity(entity):
            self._set_status("remove_entity", "NO_ENTITY")
            return
        self.__entities.remove(entity)
        self._set_status("remove_entity", "OK")

    
    # QUERIES

    # Check if set is empty
    def is_empty(self) -> bool:
        return len(self.__entities) == 0

    # Check if entity is in the set
    def has_entity(self, entity: Entity) -> bool:
        return entity in self.__entities

    # Get any entity from the set
    @status("OK", "EMPTY")
    def get_entity(self) -> Entity:
        if self.is_empty():
            self._set_status("get_entity", "EMPTY")
            return Entity(0)
        self._set_status("get_entity", "OK")
        return next(iter(self.__entities))


class System(ABC):
    
    @abstractmethod
    def run(self, world: World, frame_time: Timems) -> None:
        assert False
