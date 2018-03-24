from . import accepts
from . import expects

import types

class spec(object) :

    @staticmethod
    def populate_values(ret, data) :
        obj = ret() if type(ret) is type else ret
        cls_names = obj.__class__.__dict__.keys()
        obj_names = obj.__dict__.keys()

        for k,v in data.items() :
            if k in cls_names :
                if isinstance(obj.__class__.__dict__[k], expects.expect) :
                    obj.__class__.__dict__[k].__set__(obj, v)
                elif k in obj.__class__.__dict__ or k in obj.__dict__ :
                    pass
                else :
                    raise AttributeError('Can not set (%s, %s)'%(k,v))
            else :
                setattr(obj, k, v)

        return obj

    @staticmethod
    def dump_values(instance) :
        d = dict()
        cls_data = instance.__class__.__dict__.items()
        obj_data = instance.__dict__.items()

        for k,v in cls_data :
            if k.startswith('_') or type(v) in (type, types.FunctionType) : continue
            d[k] = getattr(instance, k)
        return d
        

    def __init__(self) :
        pass

    def validate(self) :
        # expect will be in class; its func decorator
        for name,fn in self.__class__.__dict__.items() :
            if not isinstance(fn, expects.expect) : continue
            if not fn.required : continue
            if fn.__get__(self) is None :
                return False
        return True

    def populate(self, data):
        spec.populate_values(self, data)


    def dump(self) :
        return spec.dump_values(self)

    
    

    
