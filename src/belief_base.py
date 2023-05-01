# Class to handle belief base and updates
from src.clause import Clause       # Before .clause... didn't work?
from sympy.abc import *
from sympy.logic.boolalg import *
from sympy import Symbol
from copy import deepcopy
import numpy as np

debug_mode = False

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

