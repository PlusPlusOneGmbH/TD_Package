'''Info Header Start
Name : extPowderBrowser
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2025.30060
Info Header End'''
from functools import lru_cache
from typing import Dict 
def removePrefixes(name:str, prefixes:tuple[str]):
	for prefix in prefixes:
		name = name.removeprefix( f"-{prefix}" )
	return name

import requests

class extPowderBrowser:
	"""
	extPowderBrowser description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def IndexData(self):
		return self.fetchIndexData( 
			self.ownerComp.par.Index.eval(), 
			tuple(tdu.split( self.ownerComp.par.Prefixes.eval()))
		)
		
	@lru_cache(maxsize=1)
	def fetchIndexData(self, index, prefixes) -> Dict[str, str]:
		return { removePrefixes(project["name"], prefixes ) :{ 
				"package" : project["name"] 
			} for project in requests.get(
			index, 
			headers = {
				"Accept" : "application/vnd.pypi.simple.v1+json"
			}
		).json().get("projects", []) if project["name"].startswith(prefixes) }
	@property
	def asyncio(self):
		# Global dependencyhandling is also a topic that needs to be handled here.
		# Can we use ourself to handle thhis? Lol
		return getattr( op, "AsyncIO", self.ownerComp.op("TDAsyncIO") )

	def Place(self, name, prefix = "tdp-", package = ""):
		self.ownerComp.op("TDAsyncIO").RunAsync( self.AsyncPlace( name, prefix, package))

	async def AsyncPlace(self, name, prefix = "tdp-", package = ""):
		toBePlaced:COMP = self.ownerComp.op("_").copy(self.ownerComp.op("Proxy"), name = name)
		ui.panes.current.placeOPs([toBePlaced])
		while toBePlaced and toBePlaced.parent() == self.ownerComp.op("_"):
			await asyncio.sleep(0)
		# toBePlaced.par.externaltox.expr = f"op('{self.ownerComp.path}').Get('{name}', '{prefix}', '{package}')"
		toBePlaced.par.externaltox.expr = f"op('{self.ownerComp.path}').Get('{name}')"
		toBePlaced.par.enableexternaltoxpulse.pulse()
		toBePlaced.par.reloadcustom.val = False
		toBePlaced.par.reloadbuiltin.val = False
		toBePlaced.par.savebackup.val = False
