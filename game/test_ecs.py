import unittest

import ecs


class A(ecs.Component):
    pass

class B(ecs.Component):
    pass

class C(ecs.Component):
    pass

def to_set(s: ecs.EntitySet) -> set[ecs.Entity]:
    result = set[ecs.Entity]()
    while not s.is_empty():
        e = s.get_entity()
        result.add(e)
        s.remove_entity(e)
    return result

class Test_World(unittest.TestCase):

    def test_component_fill(self):
        world = ecs.World()
        a = world.new_entity()
        b = world.new_entity()
        self.assertFalse(world.has_component(a, A))
        world.add_component(a, A())
        self.assertTrue(world.has_component(a, A))
        world.add_component(b, B())
        self.assertTrue(world.has_component(a, A))
        self.assertFalse(world.has_component(a, B))
        self.assertFalse(world.has_component(b, A))
        self.assertTrue(world.has_component(b, B))
        world.add_component(a, B())
        self.assertTrue(world.has_component(a, A))
        self.assertTrue(world.has_component(a, B))
        self.assertFalse(world.has_component(a, C))
        self.assertFalse(world.has_component(b, A))
        self.assertTrue(world.has_component(b, B))
        self.assertFalse(world.has_component(b, C))
        world.add_component(a, A())
        self.assertTrue(world.is_status("add_component", "ALREADY_EXISTS"))

    def test_get_component(self):
        world = ecs.World()
        a = world.new_entity()
        b = world.new_entity()
        aa = A()
        world.add_component(a, aa)
        ab = B()
        world.add_component(a, ab)
        bb = B()
        world.add_component(b, bb)
        t = world.get_component(a, A)
        self.assertTrue(world.is_status("get_component", "OK"))
        self.assertIs(t, aa)
        t = world.get_component(a, B)
        self.assertTrue(world.is_status("get_component", "OK"))
        self.assertIs(t, ab)
        t = world.get_component(b, B)
        self.assertTrue(world.is_status("get_component", "OK"))
        self.assertIs(t, bb)
        t = world.get_component(a, C)
        self.assertTrue(world.is_status("get_component", "NO_COMPONENT"))

    def test_remove_component(self):
        world = ecs.World()
        a = world.new_entity()
        b = world.new_entity()
        world.add_component(a, A())
        world.add_component(a, B())
        world.add_component(b, A())
        world.add_component(b, B())
        self.assertTrue(world.has_component(a, A))
        self.assertTrue(world.has_component(a, B))
        self.assertTrue(world.has_component(b, A))
        self.assertTrue(world.has_component(b, B))
        world.remove_component(a, A)
        self.assertTrue(world.is_status("remove_component", "OK"))
        self.assertFalse(world.has_component(a, A))
        self.assertTrue(world.has_component(a, B))
        self.assertTrue(world.has_component(b, A))
        self.assertTrue(world.has_component(b, B))
        world.remove_component(a, C)
        self.assertTrue(world.is_status("remove_component", "NO_COMPONENT"))

    def test_get_entities(self):
        world = ecs.World()
        a = world.new_entity()
        world.add_component(a, A())
        b = world.new_entity()
        world.add_component(b, B())
        c = world.new_entity()
        world.add_component(c, C())
        ab = world.new_entity()
        world.add_component(ab, A())
        world.add_component(ab, B())
        bc = world.new_entity()
        world.add_component(bc, B())
        world.add_component(bc, C())
        ac = world.new_entity()
        world.add_component(ac, C())
        world.add_component(ac, A())
        abc = world.new_entity()
        world.add_component(abc, A())
        world.add_component(abc, B())
        world.add_component(abc, C())
        
        s = world.get_entities({A}, set())
        self.assertEqual(to_set(s), {a, ab, ac, abc})

        s = world.get_entities({A}, {B})
        self.assertEqual(to_set(s), {a, ac})

        s = world.get_entities({A, B}, set())
        self.assertEqual(to_set(s), {ab, abc})

        s = world.get_entities(set(), {B, C})
        self.assertEqual(to_set(s), {a})

        s = world.get_entities({A, B}, {C})
        self.assertEqual(to_set(s), {ab})


class Test_ExtendableEntitySet(unittest.TestCase):

    def test_fill_empty(self):
        world = ecs.World()
        a = world.new_entity()
        b = world.new_entity()
        c = world.new_entity()
        s = ecs.ExtendableEntitySet()
        self.assertTrue(s.is_empty())
        s.get_entity()
        self.assertTrue(s.is_status("get_entity", "EMPTY"))
        s.add_entity(a)
        self.assertTrue(s.is_status("add_entity", "OK"))
        self.assertFalse(s.is_empty())
        e = s.get_entity()
        self.assertTrue(s.is_status("get_entity", "OK"))
        self.assertIs(e, a)
        s.add_entity(b)
        self.assertTrue(s.is_status("add_entity", "OK"))
        e = s.get_entity()
        self.assertIn(e, {a, b})
        s.add_entity(c)
        self.assertTrue(s.is_status("add_entity", "OK"))
        e = s.get_entity()
        self.assertIn(e, {a, b, c})
        s.add_entity(a)
        self.assertTrue(s.is_status("add_entity", "ALREADY_EXISTS"))

        x = s.get_entity()
        self.assertTrue(s.is_status("get_entity", "OK"))
        s.remove_entity(x)
        self.assertTrue(s.is_status("remove_entity", "OK"))
        y = s.get_entity()
        self.assertTrue(s.is_status("get_entity", "OK"))
        s.remove_entity(y)
        self.assertTrue(s.is_status("remove_entity", "OK"))
        z = s.get_entity()
        self.assertTrue(s.is_status("get_entity", "OK"))
        s.remove_entity(z)
        self.assertTrue(s.is_status("remove_entity", "OK"))
        self.assertTrue(s.is_empty())
        self.assertEqual({x, y, z}, {a, b, c})


if __name__ == '__main__':
    unittest.main()
