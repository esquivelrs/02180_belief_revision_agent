from src.belief_base import Belief_base
from src.clause import Clause
from sympy import Symbol
import unittest
from sympy.abc import *
from unittest import TestCase


class TestBeliefBase(TestCase):

    def test_single_clause(self):
        bb = Belief_base()
        bb.TELL(A)
        self.assertTrue(bb.ASK(A))
        self.assertFalse(bb.ASK(~A))
        self.assertFalse(bb.ASK(E))
        #print("TRUE")

    def test_multiple_clauses(self):
        bb = Belief_base()
        bb.TELL(A | B)
        bb.TELL(~A | B)
        bb.TELL(A | ~B)
        self.assertFalse(bb.ASK(~B))
        self.assertTrue(bb.ASK(B))
        #print("TRUE")
        
    def test_equiv(self):
        bb = Belief_base()
        bb.TELL(A | B)
        bb.TELL(~A | C)
        bb.TELL(B & C)
        self.assertTrue(bb.ASK((A & B) | (~A & C)))


    def test_implication(self):
        bb = Belief_base()
        bb.TELL(~A>>B)
        bb.TELL(B>>A)
        bb.TELL(A >> (C & D))
        self.assertTrue(bb.ASK(A&C&D))
        
    
    def test_implication(self):
        bb = Belief_base()
        bb.TELL(~A>>B)
        bb.TELL(B>>A)
        bb.TELL(A >> (C & D))
        #print("##### HERE ### ", bb.beliefBase)
        self.assertTrue(bb.ASK(A&C&D))
        
   
    
    # Tests that ASK returns True for a tautology. 
    def test_ASK_tautology(self):
        bb = Belief_base()
        assert bb.ASK(A | ~A) == True

    # Tests that ASK returns False for a contradiction. 
    def test_ASK_contradiction(self):
        bb = Belief_base()
        bb.TELL(A)
        assert bb.ASK(~A) == False

    # Tests that TELLs a contradiction. 
    def test_TELL_contradiction(self):
        bb = Belief_base()
        bb.TELL(A & ~A)
        #print("BBBBBB ", bb.beliefBase)
        assert len(bb.beliefBase) == 0       
    

    # Tests that TELL with a single literal adds a new clause to the belief base. 
    def test_TELL_single_literal(self):
        bb = Belief_base()
        bb.TELL(A)
        assert len(bb.beliefBase) == 1

    # Tests that _pl_resolve returns the correct resolvents. 
    def test_pl_resolve(self):
        bb = Belief_base()
        clause1 = Clause(A | B | ~C)
        clause2 = Clause(A | B | C)
        resolvents = bb._pl_resolve(clause1, clause2)
        assert len(resolvents) == 1
        assert resolvents[0].beliefCnf == A | B

    # Tests that TELL with a single clause adds a new clause to the belief base. 
    def test_TELL_single_clause(self):
        bb = Belief_base()
        bb.TELL(A | B)
        assert len(bb.beliefBase) == 1

    # Tests that TELL with a conjunction of literals adds a new clause to the belief base. 
    def test_TELL_conjunction_literals(self):
        bb = Belief_base()
        bb.TELL(A & B)
        assert len(bb.beliefBase) == 1

    # Tests that TELL with a disjunction of literals adds a new clause to the belief base. 
    def test_TELL_implication_literals(self):
        bb = Belief_base()
        bb.TELL(A >> B)
        assert len(bb.beliefBase) == 1

    # Tests that TELL with a negation of a single literal adds a new clause to the belief base. 
    def test_TELL_negation_literal(self):
        bb = Belief_base()
        bb.TELL(~A)
        assert len(bb.beliefBase) == 1



    # Tests that _pl_resolution returns False for no contradiction. 
    def test_pl_resolution_no_contradiction(self):
        bb = Belief_base()
        clause1 = Clause(A | B)
        clause2 = Clause(~A | C)
        resolvents = bb._pl_resolve(clause1, clause2)
        assert len(resolvents) == 1
        assert bb._pl_resolution([clause1, clause2], Clause(D)) == False


    # # Tests that ASK with an empty belief base returns True.  
    # def test_ASK_empty_belief_base(self):
    #     bb = Belief_base()
    #     assert bb.ASK(Symbol('A')) == True

    # Tests that _revision adds a new clause to the belief base when there is no contradiction.   
    def test_revision_no_contradiction(self):
        bb = Belief_base()
        bb.TELL(A)
        bb.TELL(B)
        bb.TELL(C)
        bb.TELL(A | B)
        bb.TELL(B | C)
        bb.TELL(C | A)
        bb.TELL(A | B | C)        
        assert len(bb.beliefBase) == 7
        bb.TELL(D)  
        assert len(bb.beliefBase) == 8
        #print("######### KB" , bb.beliefBase)

    # Tests that _revision removes contradictions to the clause from the belief base.   
    def test_revision_contradiction(self):
        bb = Belief_base()
        bb.TELL(A)
        bb.TELL(B)
        bb.TELL(C)
        bb.TELL(A | B)
        bb.TELL(B | C)
        bb.TELL(C | A)
        bb.TELL(A | B | C)  
        assert len(bb.beliefBase) == 7
        #print("BBBBBBBB ", bb.beliefBase)
        bb.TELL(~(A | B))
        #print("BBBBBBBB ", bb.beliefBase)
        assert len(bb.beliefBase) == 5

    # Tests that _revision handles duplicate clauses in belief base.   
    def test_revision_duplicate_clauses(self):
        bb = Belief_base()
        bb.TELL(A)
        bb.TELL(B)
        bb.TELL(C)
        bb.TELL(A | B)
        bb.TELL(B | C)
        bb.TELL(C | A)
        bb.TELL(A | B | C) 
        assert len(bb.beliefBase) == 7
        bb.TELL(A | B | C)
        assert len(bb.beliefBase) == 7

    # Tests that _revision handles clauses with multiple literals.    
    def test_revision_multiple_literals(self):
        bb = Belief_base()
        bb.TELL(A & B)
        bb.TELL(C | D)
        bb.TELL(E)
        bb.TELL(F)
        bb.TELL(G)
        bb.TELL(H)
        bb.TELL(I)
        bb.TELL(J)
        bb.TELL(K)
        bb.TELL(L)
        bb.TELL(M)
        bb.TELL(N)
        bb.TELL(O)
        bb.TELL(P)
        bb.TELL(Q)
        bb.TELL(R)
        bb.TELL(S)
        bb.TELL(T)
        bb.TELL(U)
        bb.TELL(V)
        bb.TELL(W)
        bb.TELL(X)
        bb.TELL(Y)
        bb.TELL(Z)

        assert len(bb.beliefBase) == 24

        # Contradiction
        bb.TELL(~A & ~B & ~C & ~D & ~E & ~F & ~G & ~H & ~I & ~J & ~K & ~L & ~M & ~N & ~O & ~P & ~Q & ~R & ~S & ~T & ~U & ~V & ~W & ~X & ~Y & ~Z)

        assert len(bb.beliefBase) == 1

    # Tests that _revision handles nested expressions in clauses.    
    def test_revision_nested_expressions(self):
        bb = Belief_base()
        bb.TELL((A | B) & (C | D))
        bb.TELL((E | F) & (G | H))
        bb.TELL((I | J) & (K | L))
        bb.TELL((M | N) & (O | P))
        bb.TELL((Q | R) & (S | T))
        bb.TELL((U | V) & (W | X))
        bb.TELL((Y | Z))

        assert len(bb.beliefBase) == 7
        
        bb.TELL(~A & ~B )

        assert len(bb.beliefBase) == 7
        # Contradiction
        bb.TELL(~C & ~D & ~E & ~F & ~G & ~H & ~I & ~J & ~K & ~L & ~M & ~N & ~O & ~P & ~Q & ~R & ~S & ~T & ~U & ~V & ~W & ~X & ~Y & ~Z)

        assert len(bb.beliefBase) == 2

    def test_revision_belief_Low_rank(self):
        bb = Belief_base()
        bb.TELL(A)
        bb.TELL(B)
        bb.TELL(C)
        bb.TELL(A | B)
        bb.TELL(B | C)
        bb.TELL(C | A)
        bb.TELL(A | B | C)  
        assert len(bb.beliefBase) == 7
        #print("BBBBBBBB ", bb.beliefBase)
        clause = Clause(~(A | B))
        clause.belief_rank = 0
        bb._revision(clause)
        #print("BBBBBBBB ", bb.beliefBase)
        assert len(bb.beliefBase) == 7

    def test_revision_belief_High_rank(self):
        bb = Belief_base()
        bb.TELL(A)
        bb.TELL(B)
        bb.TELL(C)
        bb.TELL(A | B)
        bb.TELL(B | C)
        bb.TELL(C | A)
        bb.TELL(A | B | C)  
        assert len(bb.beliefBase) == 7
        #print("BBBBBBBB ", bb.beliefBase)
        clause = Clause(~(A | B))
        clause.belief_rank = 10000
        bb._revision(clause)
        #print("BBBBBBBB ", bb.beliefBase)
        assert len(bb.beliefBase) == 5



class TestAll(unittest.TestCase):
    def test_belief_base(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBeliefBase)
        unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()