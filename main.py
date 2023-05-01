from sympy.abc import *
from src.belief_base import Belief_base
from src.clause import Clause



belief_base = Belief_base()

list_of_beliefs = [A&B,A] 
alpha = (B)

for belief in list_of_beliefs:
    belief_base.TELL(belief)


print(f"Belief base: {belief_base.beliefBase}")
print(f"This belief base entails {alpha} : {belief_base.ASK(alpha)}")
    


