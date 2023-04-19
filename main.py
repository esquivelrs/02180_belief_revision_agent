from sympy.abc import A, B, C, D
from sympy import And, Or, Not
from sympy.logic.boolalg import to_cnf, to_dnf
from sympy.logic.boolalg import is_cnf



# Build Boolean expressions with the standard python operators & (And), | (Or), ~ (Not):

# print((A >> B).equals(~B >> ~A))
# print(Not(And(A, B, C)).equals(And(Not(A), Not(B), Not(C))))
# print(Not(And(A, Not(A))).equals(Or(B, Not(B))))


# print(to_cnf(~(A & B & C))) #Convert to CNF
# print(to_cnf(A >> B)) #Convert to CNF
# print(to_cnf((A | B) & (A | ~A), True)) #Simplify the result
# print(to_dnf((A >> (B | C)) & ((B | C) >> A)))

# eq = (A >> (B | C)) & ((B | C) >> A)
# print("test")
# print(to_cnf(eq))
# print(to_cnf(eq).args)


eq1 = A >> (C & B)
print("test")

if isinstance(to_cnf(eq1), And) == True:
    eq_cnf = to_cnf(eq1).args
else:
    eq_cnf = to_cnf(eq1)

print(eq_cnf)




