# Class to handle belief base and updates
from .clause import Clause
from sympy.abc import A, B, C, D, E
from sympy.logic.boolalg import *
from sympy import symbols
from copy import deepcopy


class Belief_base:
    def __init__(self):
        self.beliefBase = []
    
    def ASK(self, alpha):

        if self.is_tautology(alpha): # If is a tautology do nothing
            return True
        
        not_alpha = ~(alpha)
        clause_notalpha = Clause(not_alpha)
        #print('ASK')
        return self._pl_resolution(self.beliefBase, clause_notalpha)
    
    def TELL(self, belief):
        # print("KB ", self.beliefBase)
        # print("BELIEF: ", belief)
        if not self.ASK(belief): # if the KB entails the belief, add the belief is not requiered
            
            clause = Clause(belief)
            
            self._revision(clause)

    def expansion(self, clause):
        self.beliefBase.append(clause)

    def contraction(self, clause):
        self.beliefBase.sort(key=lambda x: x.belief_rank)
        temp_beliefBase = deepcopy(self.beliefBase)
        
        # Since we check for contradiction and ASK does not take a belief_base as argument,
        # we use pl_resolution with the negated, simulating ASK
        clause_notalpha = Clause(~(clause.belief))
        
        is_valid = True
        # print("WHILE CONTRAC")
        while self._pl_resolution(temp_beliefBase, clause) and is_valid: # While there is contradiction in the KB with the new clause
            
            for i, clause_beliefBase in enumerate(temp_beliefBase):
                # print("CONTR_Clause ", clause.beliefCnf , ", rank= ", round(clause.belief_rank,2))
                
                contradiction = self._pl_resolution([clause_beliefBase], clause) # return true if empty clause, meaning contradiction
                if contradiction:
                    # print(f'CONTR_we have a contradiction between {clause_beliefBase} and {clause}, index={i}')
                    # print(temp_beliefBase)
                    temp_beliefBase.pop(i)
                    # print(temp_beliefBase)
                    
                    break # go back and check if there is still a contradiction in the updated KB
                
                    # if clause_beliefBase.belief_rank > clause.belief_rank:
                    #     is_valid = False
                    #     break
                    # else:
                    #     temp_beliefBase.pop(i)
                    # break
                    
        self.beliefBase = temp_beliefBase # No more contradiction
        

    def _revision(self, clause):
        # print("BELIEF: ", clause)
        # print("BELIEF CNF: ", clause.CNF_clauses)
        
        if not self.ASK(~clause.belief) or len(self.beliefBase) == 0: # This should mean the clause is not contradictory to our KB
            self.expansion(clause)
            return
        
        self.contraction(clause) # We are removing contradictions to the clause from our KB
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


    def _pl_resolve(self, clause1, clause2):
        resolvents = []
        #print(f"Clause 1: {clause1} Clause 2: {clause2} --> {clause1.literals} and {clause2.literals}...")
        for literal1 in clause1.literals:
            for literal2 in clause2.literals:
                
                # print(f"Resolving {literal1} and {literal2}... ", literal1==~literal2 )
                if literal1 == ~literal2:
                    new_literals = list(clause1.literals) + list(clause2.literals)
                    new_literals.remove(literal1)
                    new_literals.remove(literal2)
                    # Check that literals are not used twice in new clause
                    #if len(set(new_literals)) == len(new_literals):
                    new_clause = Clause(Or(*new_literals))
                    #print(f"New clause _pl: {new_clause}")
                    
                    if new_clause not in resolvents:
                        resolvents.append(new_clause)

        return resolvents

    def _pl_resolution(self, beliefBase, notalpha):
        
        kb_list = [] # Generating list of clauses
        for clauses_E in beliefBase + [notalpha]:
            list_clause_i = clauses_E.CNF_clauses
            for clause_inner in list_clause_i:
                kb_list.append(Clause(clause_inner))
   
        clauses = set(kb_list)

        while True:
            # print(f"\tPLR_Current set of clauses: {clauses}")
            new_clauses = set()
            clauses_list = list(clauses)
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(len(clauses_list)) for j in range(i+1, len(clauses_list))]
            for (ci, cj) in pairs:
                resolvents = self._pl_resolve(ci, cj)
                # print(f"\tPLR_resolvents: {resolvents}")
                
                for resolvent in resolvents:
                    if resolvent.beliefCnf == False:
                        # print("### CONTRADICTION ####")
                        return True
                    
                    new_clauses.add(resolvent)
                    # print(f"\tPLR_resolvent: {resolvent}")
                        
            # if new_clauses == set():
            #     print("### CONTRADICTION 2 ####")
            #     return True
            if new_clauses.issubset(clauses):
                # print(f"\tPLR_Current set of clauses (issubset): {clauses}")
                # print(f"\tPLR_new_clauses: {new_clauses}")
                # print("### NO CONTRADICTION ####")
                return False
                    
            clauses = clauses.union(new_clauses)





#Agent6 = Belief_base()
#Agent6._pl_resolution([Clause(A | B)], Clause(A))

# Agent6 = Belief_base()
# Agent6._pl_resolution([Clause(A),Clause(B)], Clause(A))

#print(to_cnf(Or([])))

# #Test case 8
# # print("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# # print('tell it something again')
# Agent6.TELL(~A)
# # #Agent6.TELL(B & C)
# # #Agent6.TELL(C)

# print('tell it something again')
# Agent6.TELL(A)

# print('KB = ', Agent6.beliefBase)


# # Test case 1
# print("TEST CASE 1")
# Agent1 = Belief_base()
# Agent1.TELL(A)



# alpha = A 

# # print(Agent1.beliefBase[0].literals)
# print(Agent1.ASK(alpha))  # Expected output: True


# # Test case 2
# print("TEST CASE 2")
# Agent2 = Belief_base()
# Agent2.TELL(A | B)
# Agent2.TELL(C | D)
# Agent2.TELL(~C | ~D)

# print('KB = ', Agent2.beliefBase)

# alpha = A


# print(Agent2.ASK(alpha))   # Expected output: False


#clause_1 = Clause(0, ~A >> B)
#clause_2 = Clause(0, B >> A)
#clause_3 = Clause(0, A >> (C & D))

#Agent1 = belief_base()
#Agent1.TELL(clause_1)
#Agent1.TELL(clause_2)
#Agent1.TELL(clause_3)
#print('KB = ', Agent1.beliefBase)

#alpha = Clause(0, ~(~A | C & D))        # TODO alpha cannot as of now be a sentence (multiple clauses)... Lucas fix this (e.g. by creating a list of alpha-clauses we loop over)
#print('alpha litterals = ', alpha.literals)

#pl_resolution(Agent1.beliefBase, alpha)




# Test PL_resolve:
# clause_1 = Clause(0, A | B | ~C)
# clause_2 = Clause(0, A | B | C)
# print(pl_resolve(clause_1, clause_2))


# # Test case 3
# print("TEST CASE 3")
# Agent3 = Belief_base()
# Agent3.TELL(A & B)
# Agent3.TELL(C & D)

# print('KB = ', Agent3.beliefBase)

# alpha = ~A

# print(Agent3.ASK(alpha))  # Expected output: False



# # Test case 4
# print("TEST CASE 4")
# Agent4 = Belief_base()
# Agent4.TELL(A | B)
# Agent4.TELL(C | D)

# print('KB = ', Agent4.beliefBase)

# alpha = E

# print(Agent4.ASK(alpha))   # Expected output: False


# # Test case 5
# print("TEST CASE 5")
# Agent5 = Belief_base()
# Agent5.TELL(~A>>B)
# Agent5.TELL(B>>A)
# Agent5.TELL(A >> (C & D))

# print('KB = ', Agent5.beliefBase)

# alpha = A&C&D

# print(Agent5.ASK(alpha))   # Expected output: False



# # Test case 6
# print("TEST CASE 2")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | B)
# Agent6.TELL(A | ~B)

# print('KB = ', Agent6.beliefBase)

# alpha = ~B

# print(Agent6.ASK(alpha))   # Expected output: False


# # Test case 7
# print("TEST CASE 2")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | B)
# Agent6.TELL(A | ~B)

# print('KB = ', Agent6.beliefBase)

# alpha = A | ~A

# print(Agent6.ASK(alpha))   # Expected output: True


# #Test case 8
# print("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | C)
# Agent6.TELL(B & C)

# print('KB = ', Agent6.beliefBase)

# alpha = (A & B) | (~A & C)

# print(Agent6.ASK(alpha))   # Expected output: True


# # Test case 8
# print("TEST CASE 8")
# Agent6 = Belief_base()
# Agent6.TELL(A | B)
# Agent6.TELL(~A | C)
# Agent6.TELL(B & C)


# print('KB = ', Agent6.beliefBase)

# alpha = D

# print(Agent6.ASK(alpha))   # Expected output: True




