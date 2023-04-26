# class to represent a clause
from sympy.abc import A, B, C, D
from sympy.logic.boolalg import *
import random as rnd
import numpy as np

class Clause:
    next_id = 0
    
    def __init__(self, belief):
        self.ID = Clause.next_id
        Clause.next_id += 1
        self.belief = belief
        self.beliefCnf = to_cnf(self.belief)

        
        self.CNF_clauses = []
        #self.belief_rank = rnd.random()
        self.belief_rank = self.ID
        self.split_clauses()
        self.literals = []
        self.get_literals()
   
    def split_clauses(self):
        belief_cnf = to_cnf(self.belief)
        if isinstance(belief_cnf, And):
            self.CNF_clauses = list(belief_cnf.args)
        else:
            self.CNF_clauses = [belief_cnf]
            
    
    def get_literals(self):
        if len(self.belief.atoms()) == 1:
            self.literals = [to_cnf(self.belief)]
        
        else:
            #print(self.CNF_clauses)
            #split_by_clauses = np.array([clause.args if isinstance(clause, Or) else clause for clause in self.CNF_clauses ]).flatten()
            split_by_clauses = []
            for clause in self.CNF_clauses:
                #print(f"Clause {clause}")
                if isinstance(clause, Or):
                    #print(f"Has an OR ", clause.args)
                    split_by_clauses += clause.args
                else:
                    split_by_clauses.append(clause)
            
            #print(split_by_clauses)
            split_by_literals = list(split_by_clauses)
            self.literals = split_by_literals
   
    

    def __repr__(self):
        return str(self.beliefCnf)
    
    # def __str__(self):
    #     return str(self.beliefCnf) + "_" + str(self.belief_rank)
    
    def __eq__(self, other):
        return self.beliefCnf == other.beliefCnf
    
    def __hash__(self):
        return hash(self.beliefCnf)
    
    
# print(Clause(~A>>(B&~(C|D))).literals)

# print(Clause(~A).literals)

#print(Clause(~(A >> (C & D))).literals)

