from .factory import factory


def spec(schema=None, version=None) :
    return factory(schema, version)
