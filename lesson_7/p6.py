class BaseFigure():
    n_dots = None

    def __init__(self):
        self.validate()

    def area(self):
        raise NotImplementedError("Method area is not implemented")

    def validate(self):
        raise NotImplementedError("Method validate is not implemented")

class Triangle(BaseFigure):
    n_dots=3
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def validate(self):
        sides = [self.a,self.b,self.c]
        max_side = max(sides)
        if max_side >= sum(sides) - max_side:
            raise ValueError('triangle inequality does not hold')
        else:
            return (self.a, self.b, self.c)
        for i, _ in enumerate(sides):
            sides_copy = sides.copy()
            test_side = sides_copy.pop(i)
            if test_side >= sum(sides_copy):
                raise ValueError('triangle inequality does not hold')
            else:
                return (self.a, self.b, self.c)

    def area(self):
        p = (self.a + self.b + self.c) / 2
        S = (p * (p - self.a) * (p - self.b) * (p - self.c))**0.5
        return S

class Rectangle(BaseFigure):
    n_dots = 4

    def __init__(self, a,b):
        self.a = a
        self.b = b
        super().__init__()

    def validate(self):
        return (self.a, self.b)

    def area(self):
        return self.a * self.b

tr_1 = Triangle(1,2,4)
tr_2 = Triangle(1,2,2.9)

square_1 = tr_1.area()
square_2 = tr_2.area()