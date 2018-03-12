# argv, kwargv decorator
from . import decorators

class cursor :
    def __init__(self, document, parent, key, datatype=None, required=False) :
        self._key = key
        self._parent = parent
        self._root = document
        self._datatype = datatype
        self._required = required
        self._children = None
        #self._aliases = None
        self._defaultValue = None
        self._value = None

        if parent is not None :
            if parent._children is None : parent._children = dict()
            parent._children[key] = self

    def _find(self, keys='', createIfNotExists=False, datatype=None, required=False) :
        ks = keys.split('/')
        cs = self
        for k in ks :
            if len(k)<=0 :
                cs = self._root
            elif k=='.' :
                cs = self
            elif k=='..':
                cs = self._parent
            elif cs._children is not None and k in cs._children :
                return cs._children[k]
            else :
                if cs._children is None : cs._children = dict()
                cs = cursor(self._root, cs, k, datatype, required)
        return cs

    
    def find(self, keys='') :
        return self._find(keys)
        

    def __str__(self) :
        if self._parent is None : return '!!'
        else :
            return '%s %s%s %s'%(
                '+' if self._children is not None else '-',
                self._key + '*' if self._required else '',
                '(%s)'%(self._datatype) if self._datatype is not None else '',
                ':'%(str(self._defaultValue)) if self._defaultValue is not None else '')


    def pretty_print(self) :
        stack = [(self, 0)]
        while 0<len(stack) :
            (cs,lv) = stack.pop(0)
            indent = ' '*lv
            print('%s%s'%(indent, cs))
            if cs._children is not None :
                for ck, c in cs._children.items() :
                    if ck is not None : stack.insert(0, (c, lv+1))


    # def alias(self, aliases) :
    #     if self._aliases is None :
    #         self._aliases = list()
    #     for al in aliases :
    #         sval = str(al)
    #         if sval not in self._aliases :
    #             self._aliases.append(sval)
    
    def value(self, set_value=None) :
        if set_value is not None :
            self._value = set_value
        return self._value if self._value is not None else self._defaultValue

    def required(self, set_required=None) :
        if set_required is not None :
            self._required = set_required
        return self._required

    def defaultValue(self, set_default_value=None) :
        if set_default_value is not None :
            self._defaultValue = set_default_value
        return self._defaultValue

    def expect(self, keys, datatype=None, required=False) :
        return self._find(keys, True, datatype, required)

    def path(self) :
        cs = self
        path = ''
        while cs._parent is not None and cs != cs._root :
            path = '/%s'%(cs._key) + path
        return path
    
    def is_valid(self) :
        stack = [self]
        while 0<len(stack) :
            cs = stack.pop(0)
            # check requirements
            for ch in cs._children :
                if ch._required and ch._value is None and ch._defaultValue is None :
                    # required None
                    raise ValueError('Required %s not fulfilled'%(cs.path()))
                    # TODO: value type error
        return True

    def instanciate(self) :
        pass

class factory(cursor) :
    def __init__(self, schema=None, version=None) :
        super().__init__(self, None, schema)
        self._schema = schema
        self._version = version

    

    
