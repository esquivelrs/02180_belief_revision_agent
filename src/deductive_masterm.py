from belief_base import Belief_base
from clause import Clause
from sympy import Symbol
from sympy.abc import *

def deductiveMastermind():
    # Tulips:       A = t1, B = t2
    # Daisies:      C = d1, D = d2
    # Sunflowers:   E = s1, F = s2

    BB = Belief_base()
    # Game rules:
    BB.TELL(A | C | E)  # There must be one flower in first position
    BB.TELL(B | D | F)  # There must be one flower in second position
    BB.TELL((~A | ~C) & (~A | ~E) & (~C | ~E))  # There cannot be more than one flower in first position
    BB.TELL((~B | ~D) & (~B | ~F) & (~D | ~F))  # There cannot be more than one flower in second position

    print("BB: ", BB.beliefBase)

    # Move 1:
    print("Move 1")
    #BB.TELL((A | D) & (~A | ~D))    # Either tulip or daisy in first position
    BB.TELL(A | D)
    print("Move 1.a")
    BB.TELL(~A | ~D)
    print("BB: ", BB.beliefBase)
    # Move 2:
    print("Move 2")
    BB.TELL(~A & ~B)                # Tulip cannot be in any position
    print("BB: ", BB.beliefBase)
    # Move 3:
    print("Move 3")
    BB.TELL((C & ~D) | (~C & D))    # Only one daisy is present - in either first or second position
    
    print(f"Result: {BB.beliefBase}")
    
deductiveMastermind()

