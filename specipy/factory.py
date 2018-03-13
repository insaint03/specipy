#from . import decorators
from .cursor import cursor

class factory(cursor) :
    def __init__(self, schema=None, version=None) :
        super().__init__(self, None, schema)
        self._schema = schema
        self._version = version