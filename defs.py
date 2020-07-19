class Expr:
    def __init__(self):
        self.Evaluated = None


class Atom(Expr):
    def __init__(self, Name):
        super().__init__()
        self.Name = str(Name)

    def __str__(self):
        return "Atom('{}')".format(self.Name)


class Ap(Expr):
    def __init__(self, Fun, Arg):
        super().__init__()
        self.Fun = Fun
        self.Arg = Arg

    def __str__(self):
        return "Ap({}, {})".format(self.Fun, self.Arg)

class Vect:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return "Vect({}, {})".format(self.X, self.Arg)


nil = Atom("nil")
