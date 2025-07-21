'''Info Header Start
Name : extExampleExtension
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2025.30060
Info Header End'''

class extExampleExtension:
	"""
	extExampleExtension description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Foobar(self):
		""" Does lieraly nothing """
		pass
		
	def Hello(self, str) -> COMP:
		return self.ownerComp
