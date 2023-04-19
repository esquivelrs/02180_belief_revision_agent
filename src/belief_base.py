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
    for literal in clause1.litterals:
        if ~literal not in clause2.litterals:
            resulting_literals.append(literal)
    # Return new clause
    return resulting_literals



def pl_resolution(KB, alpha):
    # Given a knowledge base KB and a query alpha, return True if alpha can be inferred from KB, and False otherwise
    for clause in KB:
        litterals = pl_resolve(alpha.beliefCnf_negated, clause)     # TODO alpha is inconsistent (not negated)






# Test PL_resolve:
clause_1 = Clause(0, A | B | ~C)
clause_2 = Clause(0, A | B | C)
print(pl_resolve(clause_1, clause_2))


# # Test TELL:
# Agent1 = belief_base()
# Agent1.TELL(~(A & B & C))
# Agent1.TELL(A >> (C & B))
# print(Agent1.beliefBase)

# Test ASK:























    # def resolve_by_contradiction(self, belief_base, query_clause):
    #     # Create new belief base
    #     new_belief_base = belief_base.copy()
    #     # Resolve until no more clauses can be resolved
    #     while True:
    #         # Get all possible pairs of clauses
    #         pairs = self.get_all_pairs(new_belief_base)
    #         # Resolve all pairs
    #         for pair in pairs:
    #             # Resolve pair
    #             new_clause = self.PL_resolve(pair[0], pair[1])
    #             # Check if new clause is empty
    #             if new_clause.beliefCnf == True:
    #                 # Return True
    #                 return True
    #             # Check if new clause is already in the belief base
    #             if new_clause not in new_belief_base:
    #                 # Add new clause to belief base
    #                 new_belief_base.append(new_clause)
    #         # Check if no new clauses were added
    #         if len(new_belief_base) == len(belief_base):
    #             # Return False
    #             return False
    #         # Update belief base
    #         belief_base = new_belief_base.copy()


    # def get_all_pairs(self, belief_base):
    #     # Create list of all pairs
    #     pairs = []
    #     # Get all possible pairs of clauses
    #     for i in range(len(belief_base)):
    #         for j in range(i+1, len(belief_base)):
    #             pairs.append([belief_base[i], belief_base[j]])
    #     # Return list of all pairs
    #     return pairs
        


    # def PL_resolve(self, clause1, clause2):
    #     # Create new clause
    #     new_clause = Clause(0, None)
    #     # Add literals from clause1
    #     for literal in clause1.beliefCnf.args:
    #         new_clause.beliefCnf.args.append(literal)
    #     # Add literals from clause2
    #     for literal in clause2.beliefCnf.args:
    #         new_clause.beliefCnf.args.append(literal)
    #     # Remove duplicates
    #     new_clause.beliefCnf.args = list(set(new_clause.beliefCnf.args))
    #     # Return new clause
    #     return new_clause

            

# Test PL_resolve:
# Agent1 = belief_base()
# Agent1.TELL(~(A & B & C))
# Agent1.TELL(A >> B)
# print(Agent1.beliefBase)
# print(Agent1.PL_resolve(Agent1.beliefBase[0], Agent1.beliefBase[1]))






