'''Info Header Start
Name : extPowderMonkey
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.31378
Info Header End'''

from functools import cache

class extPowderMonkey:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.UV = self.ownerComp.op("TD_uv")
	
	# We need to see if the caching actually is a good idea but it certainly is required 
	# as TD_UV as a shitty habbit of doing a quick subcall.
	# So yeah, maybe should fix it there too.
	# Non the less, GetTox gets calles evera time a comp Cook!
	@cache
	def GetTox(self, moduleName, prefix = "", package = "", index = ""):
		packageName = f"{prefix or self.ownerComp.par.Prefix.eval()}-{moduleName or package}"
		with self.ownerComp.op("TD_uv").MountModule( 
			moduleName, 
			packageName,
			additionalSettings = ["--index", index or self.ownerComp.par.Index.eval() ]) as mountedModule:
			return mountedModule.ToxFile
		
	def GetGlobalComp(self, moduleName, prefix = "", package = "", index = "", globalShortcut = "", globalPath = ""):
		_globalShortcut = globalShortcut or f"{self.ownerComp.par.Globalshortcutprefix.eval()}_{moduleName}"
		potentialGlobalComp = getattr( op, _globalShortcut, None )
		if potentialGlobalComp: return potentialGlobalComp

		_placePath = globalPath or self.ownerComp.par.Globalpath.eval()
		currentComp = op("/")
		for pathElement in _placePath.split("/"):
			currentComp = currentComp.op(pathElement) or currentComp.create(baseCOMP, pathElement)
		
		placeComp = currentComp
		localPM = placeComp.op("_PowderMonkey") or placeComp.copy( self.ownerComp, name = "_PowderMonkey")

		loadedComp = placeComp.loadTox( self.GetTox(moduleName, prefix, package, index) )
		loadedComp.par.opshortcut = _globalShortcut
		loadedComp.par.externaltox.expr = f"op('_PowderMonkey').GetTox( '{moduleName}', '{prefix or self.ownerComp.par.Prefix.eval()}', '{package}', '{index or self.ownerComp.par.Index.eval()}' )"
		return loadedComp
