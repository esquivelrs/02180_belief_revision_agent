from sympy.abc import *
from sympy import And, Or, Not
from sympy.logic.boolalg import to_cnf, to_dnf
from sympy.logic.boolalg import is_cnf
from src.belief_base import Belief_base



belief_base = Belief_base()

list_of_beliefs = [] # ADD belief that can be contradicted each other and the Belief base should deal with the contradictions

for belief in list_of_beliefs:
    belief_base.TELL(belief)
    
print(belief_base.beliefBase)
    


