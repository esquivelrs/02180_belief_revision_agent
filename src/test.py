from sympy.abc import A, B, C, D
from sympy.logic.boolalg import *
import random as rnd
import numpy as np

CNF_clauses = [A, ~C | ~D]
print(CNF_clauses)
split_by_clauses = [clause.args if isinstance(clause, Or) else clause for clause in CNF_clauses ]#).flatten()
print(split_by_clauses)


split_by_clauses = []
for clause in CNF_clauses:
    print(f"Clause {clause}")
    if isinstance(clause, Or):
        print(f"Has an OR ", clause.args)
        split_by_clauses += clause.args
    else:
        split_by_clauses.append(clause)
print(split_by_clauses)

