from . import accepts

class Expect(property) :
    def __init__(self, fn,
            accept=accepts.primitive,
            required=False,
            defaultValue=None,
            referable=None) :
        super().__init__(fget=fn,fset=fn)
        self.keyname = fn.__name__
        self._accepts = accept
        self.required = required
        self.defaultValue = defaultValue
        self.referable = referable

    def __get__(self, obj, objType=None) :
        return self._accepts.decode(self.fget(obj, None))

    def __set__(self, obj, val) :
        return self.fset(obj, self._accepts.encode(val))

def expect(accept=accepts.primitive, \
        required=False, \
        defaultValue=None, \
        referable=None, \
        fget=None,fset=None,fdel=None,doc=None) :
    def expected_wrapper(fn) :
        return Expect(fn, accept,required,defaultValue,referable)
        
    return expected_wrapper
        


# tester
if __name__ == '__main__' :
    class Author(object) :
        def __init__(self):
            self._name = 'Hello world'
            self.email = 'insaint03@gmail.com'
            self.country = 'Korea, Republic of'
        
        @expect(accepts.string, True)
        def name(self, val=None) :
            if val is not None :
                self._name = val
            return self._name
    me = Author()

    me.name = 'Song, Yong-Geun',
    print(me.name)
