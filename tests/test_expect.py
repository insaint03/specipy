import unittest
from specipy import expect, accepts

class Author :
    def __init__(self) :
        self._name = None
        self._age = None
        self._email = None
        self._desc = None

    @expect(accept=accepts.primitive, required=True)
    def name(self, v=None) :
        if v is not None : self._name = v
        return self._name
    @expect(accept=accepts.email, required=True)
    def email(self, v=None) :
        if v is not None : self._email = v
        return self._email

    @expect(accept=accepts.integer)
    def age(self, v=None) :
        if v is not None : self._age = v
        return self._age

    @property
    def description(self) :
        return self._desc

    @description.setter
    def description(self, v) :
        self._desc = v
    
class test_expect(unittest.TestCase) :
    def setUp(self) :
        me = Author()
        self.assertIsNotNone(me)

        values = {
            'name': 'Song, Yong-Geun',
            'email': 'insaint03@gmail.com',
            'desciption': 'sr.Data Engineer',
            'age': 20
        }
        for k,v in values.items() :
            setattr(me, k, v)
            self.assertEqual(getattr(me, k), v)

        self.me = me

    def test_simple(self) :
        me = self.me

        me.name = 1234
        self.assertTrue(type(me.name) is str)
        self.assertEqual(me.name, '1234')

    def test_assertion(self) :
        with self.assertRaises(TypeError) :
            self.me.age = 'Unknown'
    