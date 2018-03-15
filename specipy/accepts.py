import re
from datetime import date, time, datetime

_DATA_TYPES_PRIMITIVES = (bool,int,float,str)
_DATA_TYPES_COLLECTIONS = (tuple,list,set,dict,object) 

class accept(object) :
    def __init__(self, datatype, allowance) :
        self._datatype = datatype
        self._allowance = allowance

    def encode(self, val) :
        if type(val) is self._datatype :
            return val
        elif type(val) in self._allowance :
            try :
                return self._datatype(val)
            except :
                raise TypeError
        else :
            raise TypeError

    def decode(self, val) :
        return val


class accept_pattern(accept) :
    def __init__(self, pattern, replace=None) :
        global _DATA_TYPES_PRIMITIVES
        super().__init__(str, _DATA_TYPES_PRIMITIVES)
        self._pattern = re.compile(pattern)
        self._replace = replace

    def encode(self, v) :
        val = super().encode(v)
        if self._pattern.match(val) :
            if self._replace is not None :
                return self._pattern.replace(val, self._replace)
            else :
                return val
        else :
            raise ValueError('Pattern not matched')

class accept_timestamp(accept) :
    def __init__(self, parse, format, allowance=(str,int,float)) :
        super().__init__(float, allowance, defaultValue)

        if parse is not None :
            self.__parse = parse
        if format is not None :
            self.__format = format

    def encode(self, v) :
        return super._encode(self.__parse(v))

    def decode(self, v) :
        return self.__format(super._decode(v))

    def __parse(self, v):
        #if type(v) in (int, float) :
        return v
    def __format(self, v) :
        return v
        

""" basic types """
primitive = accept(str, _DATA_TYPES_PRIMITIVES)
string = primitive
integer = accept(int, _DATA_TYPES_PRIMITIVES)
number = accept(float, _DATA_TYPES_PRIMITIVES)
""" pattern string """
uri = accept_pattern('^(?P<protocol>\w+)://(?P<host>[^/]+)(?P<path>(/[^/#\?]*)*)?(?P<query>\?(&?[^&\?\=#]+=[^&\?#]*)*)?(?P<hashtag>#.+)?$')
version = accept_pattern('^v?(?P<major>\d+)(\.(?P<minor>\d+)(\.(?P<subminor>\w+)?)?)?$')
email = accept_pattern('(?P<uname>[-_\.\+\w]+)@(?P<hostname>[-_\.\w]+\.\w+)')
""" collections """
array = accept(list, (tuple, list))
category = accept(set, (tuple, list, set))
map = accept(dict, (dict, object))
""" datatime """


