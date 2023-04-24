# class to represent a clause
from sympy.abc import A, B, C, D
from sympy.logic.boolalg import *

class Clause:
    next_id = 0
    
    def __init__(self, belief):
        self.ID = Clause.next_id
        Clause.next_id += 1
        self.belief = belief
        
        self.beliefCnf = to_cnf(belief)
        self.beliefCnf_negated = ~self.beliefCnf
        self.literals = tuple(self.get_literals())
    
        
    def get_literals(self):
        new_list = []
        args_to_check = list(self.beliefCnf.args)
        #print("self.belief",self.belief)
        if len(self.belief.atoms()) == 1:
            return [to_cnf(self.belief)]
        #print(args_to_check)
        while(0 < len(args_to_check)):
            new_elements = []
            for i,arg in enumerate(args_to_check):
                if (isinstance(arg, And) == True) or (isinstance(arg, Or) == True):
                    args_to_check.remove(arg)
                    new_elements += arg.args
                else:
                    args_to_check.remove(arg)
                    new_list.append(arg)
            
            args_to_check += new_elements
        new_list = list( dict.fromkeys(new_list))
        return new_list
                    
    
    def __repr__(self):
        return str(self.beliefCnf)
    
    def __eq__(self, other):
        return self.beliefCnf == other.beliefCnf
    
    def __hash__(self):
        return hash(self.beliefCnf)
    
    
# print(Clause(~A>>(B&~(C|D))).literals)

# print(Clause(~A).literals)

#print(Clause(A)==Clause(A))

