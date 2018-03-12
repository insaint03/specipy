import unittest
import specipy

import json, yaml

class test_specipy(unittest.TestCase) :
    def test_create(self) :
        spec = specipy.spec()
        self.assertIsNotNone(spec, 'Default creation')

    def test_create_with_modules(self) :
        json_spec = specipy.spec()
        yaml_spec = specipy.spec(yaml, 'test.yaml')

        self.assertIsNotNone(json_spec, 'JSON create')
        self.assertIsNotNone(yaml_spec, 'YAML create')

    def test_expect(self) :
        spec = specipy.spec()
        spec.expect('openapi')
        spec.expect(keys='openapi', datatype=str, required=True)
        self.assertTrue(True)

    def test_pretty_print(self) :
        spec = specipy.spec()
        schema_spec = spec.expect('test_schema', str, False)
        schema_spec.expect('version', str, True)
        spec.expect('/info/title', str, True)

        spec.pretty_print()

        self.assertTrue(True)

    def test_seriese_expectation(self) :
        spec = specipy.spec()
        schema_spec = spec.expect('schema', str, True)
        spec.expect('/info/title', str, True)

        self.assertEqual(spec.find('/schema'), schema_spec)
        self.assertTrue(spec.find('/info').required())


