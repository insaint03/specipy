import unittest
import specipy

class test_cursor(unittest.TestCase) :
    def test_expect(self) :
        spec = specipy.spec()
        spec.expect('openapi')
        spec.expect(keys='openapi', datatype=str, required=True)
        self.assertTrue(True)

    def test_series_expectation(self) :
        spec = specipy.spec()
        schema_spec = spec.expect('schema', str, True)
        spec.expect('/info/title', str, True)

        self.assertEqual(spec.find('/schema'), schema_spec)
        self.assertTrue(spec.find('/info').required())

        spec.pretty_print()

    def test_upstream_requirements(self) :
        spec = specipy.spec()
        spec.expect('/hello/world/hi', str)
        spec.expect('/hello/world/hello', str)

        self.assertFalse(spec.find('/hello/world').required(), 'required false')

        spec.expect('/hello/world/bye', str, True)
        self.assertTrue(spec.find('/hello/world').required(), 'upstream required true')

        spec.pretty_print()

    def test_relative_path(self) :
        spec = specipy.spec()
        anode = spec.expect('A')
        bnode = spec.expect('B')

        child = anode.expect('aa')

        self.assertEqual(spec.find('/A/aa'), anode.find('./aa'))
        self.assertEqual(spec.find('B'), child.find('../../B'))

        spec.pretty_print()

    def test_populate(self) :
        class test_class :
            def __init__(self) :
                self.hello = 'hi'
                self.name = 'world'
                self.values = list()
                self._x = None
            @property
            def x(self) :
                return self._x
            def hi(self) :
                print(self.x)
        dv = test_class()

        spec = specipy.spec()
        spec.populate(dv, True)
        spec.pretty_print()

        self.assertTrue(True)

        self.assertIsNotNone(spec.find('hello'))

    def test_nested_populate(self) :
        class test_parent :
            X = 1
            Y = 'HI'
            C = [1,2,3]
            def __init__(self) :
                self.name = 'parent'
                self.child = None
        class test_child :
            _parent = None
            def __init__(self):
                self.name = 'child'
                self.age = 1
        p = test_parent()
        p.child = test_child()

        spec = specipy.spec()
        spec.populate(p, True)

        spec.pretty_print()

        #self.assertIsNotNone(spec.find('/child/name'))
        #self.assertEqual(spec.find('/child/name'), p.child.name)
    
    def test_instanciate(self) :
        class test_parent :
            def __init__(self) :
                self.name = 'parent'
                self.age = 30
                self.children = None
            def add_child(self, child) :
                if self.children is None :
                    self.children = list()
                self.children.append(child)
        class test_child :
            def __init__(self) :
                self._parent = None
                self.age = 10
                self.school = 'x'
                self.major = 'hi'
        p = test_parent()
        ch = test_child()
        p.add_child(ch)

        spec = specipy.spec()
        spec.populate(p, True)

        spec.pretty_print()

        ps = spec.instanciate({
            'name': 'parentX',
            'age': 55,
        })
        #self.assertEqual(ps.name, 'parentX')



        