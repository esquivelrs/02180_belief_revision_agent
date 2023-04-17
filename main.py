from sympy.abc import A, B, C, D
from sympy import And, Or, Not
from sympy.logic.boolalg import to_cnf



# Build Boolean expressions with the standard python operators & (And), | (Or), ~ (Not):

print((A >> B).equals(~B >> ~A))
print(Not(And(A, B, C)).equals(And(Not(A), Not(B), Not(C))))
print(Not(And(A, Not(A))).equals(Or(B, Not(B))))


print(to_cnf(~(A | B) | D)) #Convert to CNF
print(to_cnf(A >> B)) #Convert to CNF
print(to_cnf((A | B) & (A | ~A), True)) #Simplify the result

