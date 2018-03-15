from . import accepts
from . import expects

class spec(object) :   
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
        cls_names = self.__class__.__dict__.keys()
        obj_names = self.__dict__.keys()

        for k,v in data.items() :
            if k in cls_names :
                if isinstance(self.__class__.__dict__[k], expects.expect) :
                    self.__class__.__dict__[k].__set__(self, v)
                else :
                    raise AttributeError('Can not set (%s, %s)'%(k,v))
            else :
                setattr(self, k, v)


    def dump(self) :
        pass

    
    

    
