# Class to handle belief base and updates
from clause import Clause
from sympy.abc import A, B, C, D, E
from sympy.logic.boolalg import *
from sympy import symbols


class Belief_base:
    def __init__(self):
        self.beliefBase = []
    
    
    def TELL(self, belief):
        
        clause = Clause(belief)
        self.beliefBase.append(clause)
        return clause.CNF_clauses


    def ASK(self, alpha):
        # Check if belief is a tautology
        not_alpha = ~(alpha)
        #print(to_cnf(not_alpha))
        res = self.is_tautology(not_alpha)
        if res:
            return True
        
        # Create the clause we want to query
        #query_clause = Clause(~belief)
        query_list = []
        if isinstance(to_cnf(not_alpha), And):
            clauses = to_cnf(not_alpha).args
            for clause in clauses:
                query_list.append(Clause(clause))
        else:
            query_list.append(Clause(not_alpha))
        
        #print("alpha", query_list)
        # Resolve by contradiction
        return self._pl_resolution(query_list)
   
    
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
        # print(f"Clause 1: {clause1} Clause 2: {clause2} --> {clause1.literals} and {clause2.literals}...")
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
                    # print(f"New clause: {new_clause}")
                    
                    if new_clause not in resolvents:
                        resolvents.append(new_clause)

        return resolvents

    #pl_resolve(Clause(A|B), Clause(A|~B))

    def _pl_resolution(self, notalpha):
        clauses = set(self.beliefBase + notalpha)

        while True:
            # print(f"Current set of clauses: {clauses}")
            new_clauses = set()
            clauses_list = list(clauses)
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(len(clauses_list)) for j in range(i+1, len(clauses_list))]
            for (ci, cj) in pairs:
                #if ci != cj:
                resolvents = self._pl_resolve(ci, cj)
                for resolvent in resolvents:
                    if resolvent.beliefCnf == False:
                        return True
                    
                    new_clauses.add(resolvent)
                            
                    #print(f"resolvents: {resolvents}")
                        
            if new_clauses.issubset(clauses):
                #print(f"Current set of clauses (issubset): {clauses}")
                #print(f"new_clauses: {new_clauses}")
                return False
                    
            clauses = clauses.union(new_clauses)


# # Test case 1
# print("TEST CASE 1")
# Agent1 = Belief_base()
# Agent1.TELL(A)


# print('KB = ', Agent1.beliefBase)

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


# # Test case 8
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




