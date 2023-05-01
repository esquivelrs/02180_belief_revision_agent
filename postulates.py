from sympy.abc import A, B, C, D
from sympy.logic.boolalg import *
import random as rnd
import numpy as np
import copy as copy
from src.belief_base import Belief_base
from src.clause import Clause

BB = Belief_base()
BB.TELL((A & B))
print('Initial belief base: ', BB.beliefBase)


# AGM postulate 1: Closure
# The result of the revision of BB by A is a belief set and is not empty
def AGM_postulate_closure(BB, query):
    BB.TELL(query)
    print('Tell: ', query)
    print('New BB: ', BB.beliefBase)
    if isinstance(BB.beliefBase, list) and BB.beliefBase != []:
        print('Closure holds')
        return True
    else:
        print('Closure does not hold')
        return False

# AGM postulate 2: Success
# After revision by A of BB with A, A is in BB'
def AGM_postulate_success(BB, query):
    BB.TELL(query)
    print('Tell: ', query)
    print('New BB: ', BB.beliefBase)
    if BB.ASK(query):
        print('Success holds')
        return True
    else:
        print('Success does not hold')
        return False

# AGM postulate 3: Inclusion
# After revision by A of BB with A, BB' is a subset of BB
def AGM_postulate_inclusion(BB, query):
    BB_test = copy.deepcopy(BB)
    BB_test.expansion(Clause(query))
    print('Expanded BB set: ', set(BB_test.beliefBase))

    BB.TELL(query)
    print('New BB set: ', set(BB.beliefBase))

    if set(BB.beliefBase).issubset(set(BB_test.beliefBase)):
        print('Inclusion holds')
        return True
    else:
        print('Inclusion does not hold')
        return False


# AGM postulate 4: Vacuity
# If A is not contradictory with BB, then revising BB by A with A simply adds A to BB
def AGM_postulate_vacuity(BB, query):
    expected_belief_base = copy.deepcopy(BB)
    expected_belief_base.expansion(Clause(query))
    BB.TELL(query)
    print('New belief base: ', BB.beliefBase)
    print('Expected belief base: ', expected_belief_base.beliefBase)

    if BB.beliefBase == expected_belief_base.beliefBase:
        print('Vacuity holds')
        return True
    else:
        print('Vacuity does not hold')
        return False

# AGM postulate 5: Consistency
# If BB and A is consistent, then revision by A of BB with A is consistent
def AGM_postulate_consistency(BB, query):
    alpha = Clause(query)

    # Checking for consistency in input sentence/belief
    temp_BB = []
    for clause in alpha.CNF_clauses:
        temp_BB.append(Clause(clause))
    print('input sentence: ', alpha)
    input_consistent = not BB._pl_resolution(temp_BB, alpha)

    # Checking for consistency in new belief base
    BB.TELL(query)
    print('New BB after tell: ', BB.beliefBase)
    BB_consistent = not BB._pl_resolution(BB.beliefBase, alpha) 

    if input_consistent and BB_consistent:
        print('Consistency holds')
        return True
    elif not input_consistent:
        print('Input sentence is not consistent')
        return True
    else:
        print('Consistency does not hold')
        return False




    # BB.TELL(query)
    # print(BB.beliefBase)
    # if BB.beliefBase.is_Consistent:
    #     print('Consistency holds')
    #     return True
    # else:
    #     print('Consistency does not hold')
    #     return False

# AGM postulate 6: Extensionality
# If A and B are logically equivalent, then revision by A of BB with A is logically equivalent to revision by B of BB with A
def AGM_postulate_extensionality(BB, query1, query2):
    revised_bb_1 = copy.deepcopy(BB)
    revised_bb_2 = copy.deepcopy(BB)
    revised_bb_1.TELL(query1)
    revised_bb_2.TELL(query2)
    print('Revision 1: ', revised_bb_1.beliefBase)
    print('Revision 2: ', revised_bb_2.beliefBase)

    if Clause(query1).CNF_clauses == Clause(query2).CNF_clauses and revised_bb_1.beliefBase == revised_bb_2.beliefBase:
        print('Extensionality holds')
        return True
    elif Clause(query1).CNF_clauses != Clause(query2).CNF_clauses:
        print('Input sentences are not logically equivalent')
        return True
    else:
        print('Extensionality does not hold')
        return False

  



#### TESTS ####

print('\n--- AGM postulate 1: Closure ---')
BB = Belief_base()
AGM_postulate_closure(BB, C)

print('\n--- AGM postulate 2: Success ---')
BB = Belief_base()
AGM_postulate_success(BB, C)

print('\n--- AGM postulate 3: Inclusion ---')
BB = Belief_base()
BB.TELL(A & B)
AGM_postulate_inclusion(BB, C)

print('\n--- AGM postulate 4: Vacuity ---')
BB = Belief_base()
BB.TELL(A)
AGM_postulate_vacuity(BB, C)

print('\n--- AGM postulate 5: Consistency ---')
BB = Belief_base()
BB.TELL(~C & ~B)
AGM_postulate_consistency(BB, (C))

print('\n---AGM postulate 6: Extensionality---')
BB = Belief_base()
BB.TELL(A & B)
AGM_postulate_extensionality(BB, C | D, D | C)