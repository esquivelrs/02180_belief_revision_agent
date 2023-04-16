from sympy.abc import A, B, C
from sympy import And, Or, Not


print((A >> B).equals(~B >> ~A))
print(Not(And(A, B, C)).equals(And(Not(A), Not(B), Not(C))))
print(Not(And(A, Not(A))).equals(Or(B, Not(B))))