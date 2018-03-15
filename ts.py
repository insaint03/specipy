from specipy import expect, accepts

class A :
    alpha=1
    beta=2
    def __init__(self) :
        self.x = 1
        self.y = 2

    @expect
    def yx(self, v=None) :
        pass

print(('CLS', A.__dict__))

a = A()
print(('OBJ', a.__dict__))
print(('OBJ-CLS', a.__class__.__dict__))