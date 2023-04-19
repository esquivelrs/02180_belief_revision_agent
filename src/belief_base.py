# Class to handle belief base and updates
from clause import Clause
from sympy.abc import A, B, C, D
from sympy.logic.boolalg import to_cnf, And

class belief_base:
    def __init__(self):
        self.beliefBase = []
        self.currentID = 1
    
    def TELL(self, belief):
    
        if isinstance(to_cnf(belief), And):
            clauses = to_cnf(belief).args
            for clause in clauses:
                self.beliefBase.append(Clause(self.currentID, clause))
                self.currentID += 1
        else:
            self.beliefBase.append(Clause(self.currentID, belief))
            self.currentID += 1


    def ASK(self, belief):
        # Create the clause we want to query
        query_clause = Clause(0, belief)
        # Negate (done in Clause)
        # Convert to CNF (done in Clause)

        # Add new clause to belief base
        temp_belief_base = self.beliefBase.copy()
        temp_belief_base.append(query_clause)

        # Resolve by contradiction
        return self.resolve_by_contradiction(temp_belief_base)




def pl_resolve(clause1, clause2):
    # Create new clause
    resulting_literals = []
    # Add literals from clause1
    for literal in clause1.literals:
        if ~literal not in clause2.literals:
            resulting_literals.append(literal)
    # Return new clause
    return resulting_literals



def pl_resolution(KB, alpha):
    # Given a knowledge base KB and a query alpha, return True if alpha can be inferred from KB, and False otherwise

    while len(alpha.literals) is not 0:
        for clause in KB:
            alpha.literals = pl_resolve(alpha, clause)     # TODO alpha should be negated for input
            print(alpha.literals)
        break




clause_1 = Clause(0, ~A >> B)
clause_2 = Clause(0, B >> A)
clause_3 = Clause(0, A >> (C & D))

Agent1 = belief_base()
Agent1.TELL(clause_1)
Agent1.TELL(clause_2)
Agent1.TELL(clause_3)
print('KB = ', Agent1.beliefBase)

alpha = Clause(0, ~(~A | C & D))        # TODO alpha cannot as of now be a sentence (multiple clauses)... Lucas fix this (e.g. by creating a list of alpha-clauses we loop over)
print('alpha litterals = ', alpha.literals)

pl_resolution(Agent1.beliefBase, alpha)




# Test PL_resolve:
# clause_1 = Clause(0, A | B | ~C)
# clause_2 = Clause(0, A | B | C)
# print(pl_resolve(clause_1, clause_2))


# # Test TELL:
# Agent1 = belief_base()
# Agent1.TELL(~(A & B & C))
# Agent1.TELL(A >> (C & B))
# print(Agent1.beliefBase)

# Test ASK:


            

# Test PL_resolve:
# Agent1 = belief_base()
# Agent1.TELL(~(A & B & C))
# Agent1.TELL(A >> B)
# print(Agent1.beliefBase)
# print(Agent1.PL_resolve(Agent1.beliefBase[0], Agent1.beliefBase[1]))






