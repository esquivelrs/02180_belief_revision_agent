# Class to handle belief base and updates
#from src.clause import Clause       # Before .clause... didn't work?
from clause import Clause 
from sympy.abc import *
from sympy.logic.boolalg import *
from sympy import Symbol
from copy import deepcopy
import numpy as np

# TODO : Add check for contradiction (example A and ~A is added to the KB)... Doesn't work with the current implementation.
debug_mode = True

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
    

def print_debug(msg):
    if debug_mode:
        print(msg)

class Belief_base:
    def __init__(self):
        self.beliefBase = []
    
    def ASK(self, alpha):

        if self.is_tautology(alpha): # If is a tautology do nothing
            print("Alpha is a Tautology")
            return True
        
        if self.is_contradiction(alpha): # If is a tautology do nothing
            print("Alpha is a Contradiction")
            return True
        
        not_alpha = ~(alpha)
        clause_notalpha = Clause(not_alpha)
        #print_debug('ASK')
        return self._pl_resolution(self.beliefBase, clause_notalpha)
    
    def TELL(self, belief):
        # print_debug("KB ", self.beliefBase)
        # print_debug("BELIEF: ", belief)
        clause = Clause(belief)
        if not self.is_contradiction(belief) and clause not in self.beliefBase: # if the KB entails the belief, add the belief is not requiered
            
            self._revision(clause)
            
        else: 
            print("Belief is a Contradiction or already exist in the belief base... it won't be added")

    def expansion(self, clause):
        self.beliefBase.append(clause)

    def contraction(self, clause):
        self.beliefBase.sort(key=lambda x: x.belief_rank)
        temp_beliefBase = deepcopy(self.beliefBase)
        
        # Since we check for contradiction and ASK does not take a belief_base as argument,
        # we use pl_resolution with the negated, simulating ASK
        
        is_valid_rank = True
        print_debug("WHILE CONTRAC")
        while self._pl_resolution(temp_beliefBase, clause) and is_valid_rank: # While there is contradiction in the KB with the new clause
            
            for i, clause_beliefBase in enumerate(temp_beliefBase):
                print_debug(f"CONTR_Clause {clause.beliefCnf}, rank= {round(clause.belief_rank,2)}")
                
                contradiction = self._pl_resolution([clause_beliefBase], clause) # return true if empty clause, meaning contradiction
                if contradiction:
                    print_debug(f'CONTR_we have a contradiction between {clause_beliefBase} and {clause}, index={i}')
                    print_debug(temp_beliefBase)
                    #temp_beliefBase.pop(i)
                    
                    #break # go back and check if there is still a contradiction in the updated KB
                
                    if clause_beliefBase.belief_rank > clause.belief_rank:
                        is_valid_rank = False
                    else:
                        temp_beliefBase.pop(i)
                    
                    print_debug(temp_beliefBase)
                    break
                    
        if is_valid_rank:
            self.beliefBase = temp_beliefBase # No more contradiction
        else:
            print("Based on the priority the belief has a lower priotity to a contradictory clause in the KB.. It won't be added")
        return is_valid_rank

    def _revision(self, clause):
        print_debug(f"belief base {self.beliefBase}")
        print_debug(f"BELIEF: {clause}")
        print_debug(f"BELIEF CNF: {clause.CNF_clauses}")
        
        if not self.ASK(~clause.belief) or len(self.beliefBase) == 0: # This should mean the clause is not contradictory to our KB
            self.expansion(clause)
            return
        print("contraction")
        contraction = self.contraction(clause) # We are removing contradictions to the clause from our KB
        
        if contraction:
            self.expansion(clause)
        

   
    
    def is_tautology(self, belief):
        # Convert the expression to CNF
        cnf_expr = to_cnf(belief)
        # Extract the variables from the expression
        variables = list(cnf_expr.free_symbols)
        # Construct the truth table for the expression
        for values in product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            if not cnf_expr.subs(assignment):
                return False
        return True
    
    def is_contradiction(self, belief):
        # Convert the expression to CNF
        cnf_expr = to_cnf(belief)

        # Extract the variables from the expression
        variables = list(cnf_expr.free_symbols)

        # Construct the truth table for the expression
        for values in product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            if cnf_expr.subs(assignment):
                return False
        return True


    def _pl_resolve(self, clause1, clause2):
        resolvents = []
        #print_debug(f"Clause 1: {clause1} Clause 2: {clause2} --> {clause1.literals} and {clause2.literals}...")
        for literal1 in clause1.literals:
            for literal2 in clause2.literals:
                
                # print_debug(f"Resolving {literal1} and {literal2}... ", literal1==~literal2 )
                if literal1 == ~literal2:
                    new_literals = list(clause1.literals) + list(clause2.literals)
                    new_literals.remove(literal1)
                    new_literals.remove(literal2)
                    # Check that literals are not used twice in new clause
                    #if len(set(new_literals)) == len(new_literals):
                    new_clause = Clause(Or(*new_literals))
                    #print_debug(f"New clause _pl: {new_clause}")
                    
                    if new_clause not in resolvents:
                        resolvents.append(new_clause)

        return resolvents

    def _pl_resolution(self, beliefBase, notalpha):
        
        kb_list = [] # Generating list of clauses
        for clauses_E in beliefBase + [notalpha]:
            list_clause_i = clauses_E.CNF_clauses
            for clause_inner in list_clause_i:
                kb_list.append(Clause(clause_inner))
        
        
        print_debug(f"\tPLR_all clauses: {kb_list}")
   
        clauses = set(kb_list)

        while True:
            #print_debug(f"\tPLR_Current set of clauses: {clauses}")
            new_clauses = set()
            clauses_list = list(clauses)
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(len(clauses_list)) for j in range(i+1, len(clauses_list))]
            for (ci, cj) in pairs:
                #print_debug(f"Ci: {ci}  Cj: {cj}")
                resolvents = self._pl_resolve(ci, cj)
                #print_debug(f"\tPLR_resolvents: {resolvents}")
                
                for resolvent in resolvents:
                    if resolvent.beliefCnf == False:
                        #print_debug("### CONTRADICTION ####")
                        return True
                    
                    new_clauses.add(resolvent)
                    #print_debug(f"\tPLR_resolvent: {resolvent}")
                        
            # if new_clauses == set():
            #     print_debug("### CONTRADICTION 2 ####")
            #     return True
            if new_clauses.issubset(clauses):
                # print_debug(f"\tPLR_Current set of clauses (issubset): {clauses}")
                # print_debug(f"\tPLR_new_clauses: {new_clauses}")
                # print_debug("### NO CONTRADICTION ####")
                return False
                    
            clauses = clauses.union(new_clauses)





# Agent6 = Belief_base()
# Agent6._pl_resolution([Clause(A),Clause(B)], Clause(A))

# Agent6.TELL(A >> B)
# Agent6.TELL(A)
# print_debug('KB = ', Agent6.beliefBase)
# Agent6.TELL(B)
# print_debug('KB = ', Agent6.beliefBase)
# Agent6.TELL(~B)
# print_debug('KB = ', Agent6.beliefBase)

BB = Belief_base()
# Game rules:
s1 = Symbol('s1') 
s2 = Symbol('s2') 
t1 = Symbol('t1') 
t2 = Symbol('t2') 
d1 = Symbol('d1') 
d2 = Symbol('d2') 

# BB.TELL(s1 | t1 | d1)
# BB.TELL(s2 | t2 | d2)

# print(BB.beliefBase)

# #(:t1 _ :s1) ^ (:s1 _ :d1) ^ (:d1 _ :t1)
# BB.TELL((~t1 | ~s1) & (~s1 | ~d1) & (~d1 | ~t1))
# #(:t2 _ :s2) ^ (:s2 _ :d2) ^ (:d2 _ :t2)

# BB.TELL((~t2 | ~s2) & (~s2 | ~d2) & (~d2 | ~t2))

# #(t1 _ d2) ^ (:d2 _ :t1)
# BB.TELL((t1 | d2) & (~t1 | ~d2))

# #print('Is true = ', BB.ASK(s1 & d2))

# print(BB.beliefBase)



Agent6 = Belief_base()

# [d1 | s1 | t1
#  d2 | s2 | t2
#  ~d1 | ~s1
#  ~d1 | ~t1
#  ~s1 | ~t1
#  ~d2 | ~s2
#  ~d2 | ~t2
#  ~s2 | ~t2
#  d2 | t1
#  ~d2 | ~t1]
hh = [Clause(~d2 | ~s2), 
      Clause(~d2 | ~t2), 
      Clause(~s2 | ~t2), 
      Clause(d2 | t1), 
      Clause(~d2 | ~t1)]

print(Agent6._pl_resolution(hh, Clause(~d2 | ~t1)))


#print_debug(Agent6.is_contradiction(A))
#Agent6._pl_resolution([Clause(A | B)], Clause(A))

# Agent6 = Belief_base()
# Agent6._pl_resolution([Clause(A),Clause(B)], Clause(A))

#print_debug(to_cnf(Or([])))

# #Test case 8
# # print_debug("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# # print_debug('tell it something again')
# Agent6.TELL(~A)
# # #Agent6.TELL(B & C)
# # #Agent6.TELL(C)

# print_debug('tell it something again')
# Agent6.TELL(A)

# print_debug('KB = ', Agent6.beliefBase)


# # Test case 1
# print_debug("TEST CASE 1")
# Agent1 = Belief_base()
# Agent1.TELL(A)



# alpha = A 

# # print_debug(Agent1.beliefBase[0].literals)
# print_debug(Agent1.ASK(alpha))  # Expected output: True


# # Test case 2
# print_debug("TEST CASE 2")
# Agent2 = Belief_base()
# Agent2.TELL(A | B)
# Agent2.TELL(C | D)
# Agent2.TELL(~C | ~D)

# print_debug('KB = ', Agent2.beliefBase)

# alpha = A


# print_debug(Agent2.ASK(alpha))   # Expected output: False


#clause_1 = Clause(0, ~A >> B)
#clause_2 = Clause(0, B >> A)
#clause_3 = Clause(0, A >> (C & D))

#Agent1 = belief_base()
#Agent1.TELL(clause_1)
#Agent1.TELL(clause_2)
#Agent1.TELL(clause_3)
#print_debug('KB = ', Agent1.beliefBase)

#alpha = Clause(0, ~(~A | C & D))        # TODO alpha cannot as of now be a sentence (multiple clauses)... Lucas fix this (e.g. by creating a list of alpha-clauses we loop over)
#print_debug('alpha litterals = ', alpha.literals)

#pl_resolution(Agent1.beliefBase, alpha)




# Test PL_resolve:
# clause_1 = Clause(0, A | B | ~C)
# clause_2 = Clause(0, A | B | C)
# print_debug(pl_resolve(clause_1, clause_2))


# # Test case 3
# print_debug("TEST CASE 3")
# Agent3 = Belief_base()
# Agent3.TELL(A & B)
# Agent3.TELL(C & D)

# print_debug('KB = ', Agent3.beliefBase)

# alpha = ~A

# print_debug(Agent3.ASK(alpha))  # Expected output: False



# # Test case 4
# print_debug("TEST CASE 4")
# Agent4 = Belief_base()
# Agent4.TELL(A | B)
# Agent4.TELL(C | D)

# print_debug('KB = ', Agent4.beliefBase)

# alpha = E

# print_debug(Agent4.ASK(alpha))   # Expected output: False


# # Test case 5
# print_debug("TEST CASE 5")
# Agent5 = Belief_base()
# Agent5.TELL(~A>>B)
# Agent5.TELL(B>>A)
# Agent5.TELL(A >> (C & D))

# print_debug('KB = ', Agent5.beliefBase)

# alpha = A&C&D

# print_debug(Agent5.ASK(alpha))   # Expected output: False



# # Test case 6
# print_debug("TEST CASE 2")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | B)
# Agent6.TELL(A | ~B)

# print_debug('KB = ', Agent6.beliefBase)

# alpha = ~B

# print_debug(Agent6.ASK(alpha))   # Expected output: False


# # Test case 7
# print_debug("TEST CASE 2")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | B)
# Agent6.TELL(A | ~B)

# print_debug('KB = ', Agent6.beliefBase)

# alpha = A | ~A

# print_debug(Agent6.ASK(alpha))   # Expected output: True


# #Test case 8
# print_debug("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | C)
# Agent6.TELL(B & C)

# print_debug('KB = ', Agent6.beliefBase)

# alpha = (A & B) | (~A & C)

# print_debug(Agent6.ASK(alpha))   # Expected output: True


# # Test case 8
# print_debug("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | C)
# Agent6.TELL(B & C)


# print_debug('KB = ', Agent6.beliefBase)

# alpha = D

# print_debug(Agent6.ASK(alpha))   # Expected output: True




