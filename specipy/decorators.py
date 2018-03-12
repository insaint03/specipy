
# parameterized class method
def parameterized_method(*argv) :
    def wrapper(fn) :
        names = tuple([str(a) for a in argv])
        def class_method_wrapper(self, *argv,**kwargv) :
            params = None
            if argv is not None and 0<len(argv) :
                rg = range(0, len(names))
                ag = range(0, len(argv))
                params = {names[i]:argv[i] if i in ag else None for i in range(0, len(names))}
            if kwargv is not None and 0<len(kwargv) :
                params = {n:kwargv[n] if n in kwargv else None for n in names}
            fn(self,params)
        return class_method_wrapper
    return wrapper

        
        
