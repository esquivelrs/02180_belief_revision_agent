from unittest import TestCase
from sympy.abc import A, B, C, D, E
from sympy.logic.boolalg import *
from belief_base import Belief_base
from clause import Clause

class TestBeliefBase(TestCase):
    def setUp(self):
        self.bb = Belief_base()

    def test_tautology(self):
        self.assertTrue(self.bb.ASK(A | ~A))
        
    def test_single_clause(self):
        self.bb.TELL(A)
        self.assertTrue(self.bb.ASK(A))
        self.assertFalse(self.bb.ASK(~A))
        self.assertFalse(self.bb.ASK(E))
        #print("TRUE")

    def test_multiple_clauses(self):
        self.bb.TELL(A | B)
        self.bb.TELL(~A | B)
        self.bb.TELL(A | ~B)
        self.assertFalse(self.bb.ASK(~B))
        self.assertTrue(self.bb.ASK(B))
        #print("TRUE")
        
    def test_equiv(self):
        self.bb.TELL(A | B)
        self.bb.TELL(~A | C)
        self.bb.TELL(B & C)
        self.assertTrue(self.bb.ASK((A & B) | (~A & C)))


    def test_implication(self):
        self.bb.TELL(~A>>B)
        self.bb.TELL(B>>A)
        self.bb.TELL(A >> (C & D))
        self.assertTrue(self.bb.ASK(A&C&D))


import unittest

class TestAll(unittest.TestCase):
    def test_belief_base(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBeliefBase)
        unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()