# class to represent a clause
from sympy.abc import A, B, C, D
from sympy.logic.boolalg import to_cnf

class Clause:
    def __init__(self, ID, belief):
        self.ID = ID
        self.belief = belief
        
        self.beliefCnf = to_cnf(belief)
        self.beliefCnf_negated = ~self.beliefCnf
        self.literals = list(self.beliefCnf.args)

    def __repr__(self):
        return str(self.beliefCnf)
