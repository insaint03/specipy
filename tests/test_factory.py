import unittest
import specipy

import json, yaml

class test_factory(unittest.TestCase) :
    def test_create(self) :
        spec = specipy.spec()
        self.assertIsNotNone(spec, 'Default creation')    

    def test_pretty_print(self) :
        spec = specipy.spec()
        schema_spec = spec.expect('test')
        schema_spec.expect('version', str, True)
        spec.expect('/info/title', str, True)

        spec.pretty_print()
        self.assertTrue(True)
    
    def test_path(self) :
        test_path = 'A/B/C/D/E/F/G/h/i/j/k/L/m'
        cs = specipy.spec()
        for p in test_path.split('/') :
            cs = cs.expect(p)

        self.assertEqual('/'+test_path, cs.path())
        



