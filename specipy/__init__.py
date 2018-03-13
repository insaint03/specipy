from .factory import factory

__version__ = '0.0.1'

__all__ = [
    factory
]

def spec(schema=None, version=None) :
    return factory(schema, version)

