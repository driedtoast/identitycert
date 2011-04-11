import unittest
import random
import sampletest

class AllTests(unittest.TestSuite):
	def __init__(self):
		super(AllTests,self).__init__()
		self.addTest(sampletest.TestSequenceFunctions)
