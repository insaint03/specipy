from .datatypes import datatypes
#from .models import models
import sys, types
class cursor :
    def __init__(self, document, parent, key, datatype=None, required=False) :
        self._key = key
        self._parent = parent
        self._root = document
        self._datatype = datatype
        self._required = required
        self._children = None
        self._defaultValue = None
        self._value = None

        if parent is not None :
            if parent._children is None : parent._children = dict()
            parent._children[key] = self

    def __find_iter(self, cs, k_idx, k_strs, createIfNotExists, datatype, required) :
        key_str = k_strs[k_idx].strip()

        # upstream required option set
        if required and not cs._required :
            cs._required = True

        # create
        if len(key_str)<=0 :
            cs = cs._root
        elif key_str=='.':
            cs = cs
        elif key_str=='..':
            cs = cs._parent
        elif key_str.startswith('$'):
            pass
        elif cs._children is not None and key_str in cs._children :
            cs = cs._children[key_str]
        else :
            if createIfNotExists :
                if cs._children is None : cs._children = dict()
                dt = datatype if k_idx+1 >= len(k_strs) else None
                cs = cursor(self._root, cs, key_str, dt, required)
            else :
                raise KeyError('Can not find key %s at %s '%(key_str, cs.path()))

        return cs
    
    def _find(self, keys='', createIfNotExists=False, datatype=None, required=False) :
        ks = keys.split('/')
        kl = len(ks)
        cs = self
        for ki in range(0, kl) :
            cs = self.__find_iter(cs, ki, ks, createIfNotExists, datatype, required)
                
        return cs
    
    def find(self, keys='') :
        return self._find(keys)
        
    def __str__(self) :
        if self._parent is None : 
            # dummy root
            return '!!'
        else :
            return '%s %s%s%s %s'%(
                '+' if self._children is not None else '-',
                self._key, '*' if self._required else '',
                '(%s)'%(self._datatype) if self._datatype is not None else '',
                ':'%(str(self._defaultValue)) if self._defaultValue is not None else '')

    @property
    def key(self) :
        return self._key

    @property
    def datatype(self) :
        return self._datatype

    def pretty_print(self, write_stream=sys.stdout) :
        stack = [(self, 0)]
        while 0<len(stack) :
            (cs,lv) = stack.pop(0)
            indent = ' '*lv
            write_stream.write('%s%s\n'%(indent, cs))
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
            cs = cs._parent
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
    
    def _populate_instance(self, stack, label, value, with_structure) :
        if label.startswith('_') \
        or type(value) is types.FunctionType :
            return
        else :
            next_cursor = self._find(label, with_structure, type(value))
            if type(value) in (list, tuple, dict, set, frozenset) :
                # internal collection
                pass
            elif type(value) is property :
                # 
                pass
            elif type(value) in (int, str, float, bool) :
                # 
                pass
            else :
                stack.append((next_cursor, value))


    def populate(self, instance, with_structure=False) :
        # build current model
        stack = [(self, instance)]
        stack_record = list()
        while 0<len(stack) :
            #try :
            (cs, instance) = stack.pop(0)
            # to avoid loops
            if instance in stack_record : continue
            stack_record.append(instance)

            for label,value in instance.__class__.__dict__.items() :
                cs._populate_instance(stack, label, value, with_structure)
            for label,value in vars(instance).items() :
                cs._populate_instance(stack, label, value, with_structure)
            # except Exception as ex :
            #     print(ex)

    def instanciate(self, values) :
        # no child no more
        if self._children is None or values is None : 
            return (None, None)

        sheet = self._datatype() if self._datatype is not None else object()
        #print((self._datatype(), sheet))
        # for label,nc in self._children.items() :
        #     if label in values :
        #         val = None
        #         if nc._datatype in (bool,int,float,str,set,frozenset,tuple,list,dict) :
        #             val = nc._datatype(values[label])
        #         else :
        #             val = nc._instanciate_template(self, values[label])
        #         if val is not None :
        #             setattr(sheet, label, val)
        
        # for label,val in values.items() :
        #     if hasattr(sheet, label) : continue
        #     if type(val) is dict : continue
        #     setattr(sheet, label, val)
        
        
        return sheet

