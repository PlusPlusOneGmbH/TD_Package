
from typing import Union
class extTestExtension:
	"""
	extTestExtension description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp:Union[extTestExtension, COMP] = ownerComp

	def Foobar(self):
		""" 
			This function does nothing. LOL
		"""
		debug("SIKE!")