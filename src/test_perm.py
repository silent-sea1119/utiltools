import unittest, perm
from perm import Perm

#TODO: check get_status() of every Perm(...) like Perm(..).get_status() == 0

class TestPerm(unittest.TestCase):
   def is_rwa(self, perm1):
      self.assertEqual(perm1.has_read(), True)
      self.assertEqual(perm1.has_write(), True)
      self.assertEqual(perm1.has_admin(), True)
      self.assertEqual(perm1.has_super_admin(), False)

   def test_arr(self):
      perm1 = Perm([Perm.READ, Perm.WRITE, Perm.ADMIN])
      perm2 = Perm([Perm.WRITE, Perm.ADMIN, Perm.READ])

      stat1 = perm1.get_status()
      stat2 = perm2.get_status()

      self.is_rwa(perm1)
      self.is_rwa(perm2)

   def test_str(self):
      perm1 = Perm('arw')
      self.is_rwa(perm1)

   def test_constant(self):
      perm1 = Perm(Perm.ADMIN)
      perm2 = Perm(Perm.SUPER)
      perm3 = Perm(1 << 3) #WRITE

      self.assertEqual(perm1.has_admin(), True)
      self.assertEqual(perm2.has_super_admin(), True)
      self.assertEqual(perm3.has_write(), True)

      for x in [perm1, perm2, perm3]:
         self.assertEqual(x.has_read(), False)

   def test_or(self):
      perm_n = 0
      perm_n |= Perm.ADMIN
      perm_n |= Perm.WRITE #Perm.SUPER
      perm_n |= Perm.READ

      p = Perm(perm_n)
      self.is_rwa(p)

   def test_copy(self):
      p1 = Perm('arw')
      p2 = Perm(p1)
      self.is_rwa(p2)


   def test_errors(self):
      p = Perm([-5])
      self.assertEqual(p.get_status(), 1)
      p1 = Perm('sdfds')
      self.assertEqual(p1.get_status(), 1)
      p2 = Perm(2132)
      self.assertEqual(p2.get_status(), 3)
      p3 = Perm(p2)
      self.assertEqual(p3.get_status(), 3)
      p4 = Perm(unittest.TestCase)
      self.assertEqual(p4.get_status(), 2)

