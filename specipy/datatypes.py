class datatypes :
    @staticmethod
    def search(dt):
        return datatype_string

    def accept(self, value) :
        return True

    def save(self, value) :
        return value
    


class datatype_string(datatypes) :
    def __init__(self) :
        super().__init__()

    def instanciate(self, cursor) :
        pass

    def populate(self, cursor, value) :
        pass


