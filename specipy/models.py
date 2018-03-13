class model :
    def __init__(self, cursor) :
        self._cursor = cursor
        self._data = None

    @property
    def cursor(self) :
        return self._cursor

    @property
    def data(self) :
        return self._data

    @data.setter
    def data(self, values) :
        self.populate(self, values)

    # data to model instance
    def instanciate(self) :
        pass

    # values to 
    def populate(self, values) :
        pass

