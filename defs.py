class Expr:
    def __init__(self):
        self.Evaluated = None


class Atom(Expr):
    def __init__(self, Name):
        super().__init__()
        self.Name = Name


class Ap(Expr):
    def __init__(self, Fun, Arg):
        super().__init__()
        self.Fun = Fun
        self.Arg = Arg


class Vect:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


nil = Atom("nil")
