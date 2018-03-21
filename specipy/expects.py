from . import accepts

from . import spec

class expect(object) :
    def __init__(self, 
            accept=accepts.primitive,
            required=False,
            defaultValue=None,
            referable=None) :
        self._accepts = accept
        self.required = required
        self.defaultValue = defaultValue
        self.referable = referable

    def __get__(self, obj, objType=None) :
        return self._accepts.decode(self.fget(obj))

    def __set__(self, obj, val) :
        return self.fset(obj, self._accepts.encode(val))
    
    def __call__(self, fn) :
        self.fget = fn
        self.fset = fn
        self.keyname = fn.__name__

        return self
        

# tester
if __name__ == '__main__' :
    class Author(object) :
        def __init__(self):
            self._name = 'Hello world'
            self.email = 'insaint03@gmail.com'
            self.country = 'Korea, Republic of'
        
        @expect(accepts.string, True)
        def name(self, v=None) :
            if v is not None : self._name = v
            return self._name
    me = Author()

    #me.name = 'Song, Yong-Geun',
    print(me.name)
