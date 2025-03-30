'''Info Header Start
Name : extPowderMonkey
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.31378
Info Header End'''
import requests
from functools import lru_cache
import asyncio

class extPowderMonkey:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		
	@property
	def IndexData(self):
		return self.fetchIndexData( 
			self.ownerComp.par.Index.eval(), 
			tuple(tdu.split( self.ownerComp.par.Prefixes.eval()))
		)
	
	@lru_cache(maxsize=1)
	def fetchIndexData(self, index, prefixes):
		return [ project["name"] for project in requests.get(
			index, 
			headers = {
				"Accept" : "application/vnd.pypi.simple.v1+json"
			}
		).json().get("projects", []) if project["name"].startswith(prefixes)]
	
	def Get(self, name, prefix = "tdp-", package = ""):
		with self.ownerComp.op("td_pip").MountModule( name, package or f"{prefix}{name}") as mountedModule:
			return mountedModule.ToxFile
	
	async def AsyncPlace(self, name, prefix = "tdp-", package = ""):
		toBePlaced:COMP = self.ownerComp.op("_").copy(self.ownerComp.op("Proxy"), name = name)
		ui.panes.current.placeOPs([toBePlaced])
		while toBePlaced and toBePlaced.parent() == self.ownerComp.op("_"):
			await asyncio.sleep(0)
		toBePlaced.par.externaltox.expr = f"op('{self.ownerComp.path}').Get('{name}', '{prefix}', '{package}')"
		toBePlaced.par.enableexternaltoxpulse.pulse()
		toBePlaced.par.reloadcustom.val = False
		toBePlaced.par.reloadbuiltin.val = False
		toBePlaced.par.savebackup.val = False

	@property
	def asyncio(self):
		# Global dependencyhandling is also a topic that needs to be handled here.
		# Can we use ourself to handle thhis? Lol
		return getattr( op, "AsyncIO", self.ownerComp.op("TDAsyncIO") )

	def Place(self, name, prefix = "tdp-", package = ""):
		self.ownerComp.op("TDAsyncIO").RunAsync( self.AsyncPlace( name, prefix, package))