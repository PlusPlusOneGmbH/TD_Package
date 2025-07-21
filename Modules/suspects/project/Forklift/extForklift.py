'''Info Header Start
Name : extForklift
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2025.30060
Info Header End'''


from tempfile import TemporaryDirectory
from pathlib import Path
import json
import sys
from uuid import uuid4
import inspect
from itertools import chain

from CustomTypingsAstParser import createTypingModuleString

class extForklift:
	"""
	extForklift description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def _bindAssign(self, parentParName, targetParName, targetComp):
		if targetComp.parent().par[parentParName]: targetComp.par[targetParName].bindExpr = f"parent().par['{parentParName}']"

	def createMetaComp(self, targetComp):
		metaComp:COMP = targetComp.copy(self.ownerComp.op("Package_Meta_Prefab"), name = "Package_Meta")
		self._bindAssign( "Vcname", "Name", metaComp)
		self._bindAssign( "Vcversion", "Version1", metaComp)
		self._bindAssign( "Vcbuild", "Version2", metaComp)
		ui.messageBox("New Setup", "It seems like you are preparing a COMP. Please take a moment to fill out some Meta-Data")
		newPane = ui.panes.createFloating()
		newPane.owner = targetComp
		newPane.home( op = metaComp )
		raise Exception("No Initialised!")
		return metaComp


	def Rundown(self, targetComp, TempOutput = True):
		with TemporaryDirectory() as _buildDir:
			if not TempOutput:
				_buildDir = Path("TDImportCache", str(uuid4()))
				_buildDir.mkdir( parents=True, exist_ok = False)
			self.Prepare( targetComp )
			self.Export( targetComp, _buildDir)
			self.Build( _buildDir )
			self.Publish( _buildDir )
			# self.ownerComp.op("logger").Log("Finished", _buildDir)

	def Prepare(self, targetComp:COMP):
		metaComp = targetComp.op("Package_Meta") or self.createMetaComp(targetComp)
		metaComp.par.clone.val = self.ownerComp.op("Package_Meta_Prefab")
		metaComp.par.enablecloningpulse.pulse()
		metaComp.par.clone.val = ""
		for linkTarget in [
			("Vcname", "Name"),
			("Vcversion", "Version1"),
			("Vcbuild", "Version2"),
		]:
			if hasattr( targetComp.par, linkTarget[0]):
				metaComp.par[linkTarget[1]].bindExpr = f"parent().par['{linkTarget[0]}']"
	

	def cleanExternalDependencies(self, targetComp, parName):
		for childComp in targetComp.findChildren( parName = parName):
			if "KeepExternal" in childComp.tags or childComp.par[parName].mode != ParMode.CONSTANT: continue
			childComp.par[parName].val = ""
	
	def fetchDatDepdencies(self, moduleOp:textDAT ):
		returnData = []
		try:
			returnData += [
				op(_member[1].__module__) for _member in inspect.getmembers( mod(moduleOp) ) 
				if (
					_member[0] not in {"mod", "me", moduleOp.name} and 
					hasattr(_member[1], "__module__") and 
					op(_member[1].__module__) is not None and 
					op(_member[1].__module__) is not moduleOp
				)
			]
		except tdError as e:
			# TBH not sure why but there is some strange behaviour when releasing Forklift itself? I suppose it is sensible to just skip stuff then.
			pass
			# debug("Error while fetching dependencies", e)
		
		try:
			returnData +=[
				op(_member[1]) for _member in inspect.getmembers( mod(moduleOp) ) 
				if (
					_member[0] not in {"mod", "me", moduleOp.name} and 
					op(_member[1]) is not None and 
					op(_member[1]) is not moduleOp
				)
			]
		except tdError as e:
			# TBH not sure why but there is some strange behaviour when releasing Forklift itself? I suppose it is sensible to just skip stuff then.
			pass
			# debug("Error while fetching dependencies", e)

		

		return returnData + list(chain.from_iterable([self.fetchDatDepdencies( _dependencyModule ) for _dependencyModule in returnData]))


	def fetchExtDependencies(self, compWithExtensions:COMP):
		return [
			op(extension.__module__) for extension in compWithExtensions.extensions
		]

	def SaveComp(self, targetComp:COMP, targetDir:Path):
		# First we find all textDats that might be interresting for typehinting reasons. 
		self.cleanExternalDependencies( targetComp, "externaltox")
		self.cleanExternalDependencies( targetComp, "file")

		# Lets iterate over all dependency modules
		extensionDats = self.fetchExtDependencies( targetComp )

		# All future refferences t external files are now in relation to the position of the tox file. At least they should.
		targetComp.par.relpath.menuIndex = 2

		for moduleDat in set(extensionDats + list(chain.from_iterable( [ self.fetchDatDepdencies( extensionDat ) for extensionDat in extensionDats] ))) :
			# Lets also actually set the refference!
			

			# There are some strange issues where the algo fetches old refferences I assume when copying.
			# Lets check that we are actually in the targetComp.
			if not moduleDat.path.startswith( targetComp.path ): continue
	
			savePath = moduleDat.save(
				Path( 
					targetDir, 
					*targetComp.relativePath( moduleDat ).split("/")[1:]
				).with_name( moduleDat.name ).with_suffix( f".{moduleDat.par.extension.eval()}"),
				createFolders=True
			)
			# If that makes sense, to be testes. 
			# We are basicly externalising all the python dependencies. Yaih!

			moduleDat.par.file.val = Path( savePath ).relative_to( targetDir )
		
		return Path( targetComp.save( Path(targetDir, targetComp.name).with_suffix(".tox")) )


	def validateMeta(self, targetComp:COMP):
		pass

	def Export(self, _targetComp:COMP, _buildDir):
		schleuse = op("/sys").op("Schleuse") or op("/sys").copy( self.ownerComp.op("Schleuse") )
		for child in schleuse.findChildren( depth = 1):
			child.destroy()
			
		targetComp = schleuse.copy( _targetComp )
		metaComp = targetComp.op("Package_Meta")
		metaComp.op("PreExportScriptRepo").Repo.run()
		
		(metaComp.op("pre_release") or self.ownerComp.op("empty")).run()

		buildDir = Path( _buildDir )
		buildDir.mkdir(exist_ok=True, parents=True)
		metaComp.op("LicenseRepo").Repo.save(
			Path(buildDir, "LICENSE")
		)
		metaComp.op("ManifestRepo").Repo.save(
			Path(buildDir, "MANIFEST.in")
		)
		metaComp.op("ReadmeRepo").Repo.save(
			Path(buildDir, "README.md")
		)

		# Lets find TD_UV and silently add the dependencies!
		for child in targetComp.findChildren(depth = 1):
			if child.par.Vcname.eval() == "TD_Uv" and child.par.Vcversion.eval() >= 0 and child.par.Vcbuild.eval() >= 35:
				child.InstallDependencyTable( additional_settings = "--freeze" )

		with Path(buildDir, "pyproject.toml").open("+wt") as projectToml:
			projectToml.write(
				self.ownerComp.op("prefabPyProject").text.format(**{
					"Name" : f"{self.ownerComp.par.Prefix.eval()}{metaComp.par.Name.eval()}",
					"Version" : f"{metaComp.par.Version1}.{metaComp.par.Version2}",
					"Dependencies" : json.dumps([
						cell.val for cell in ( 
							targetComp.op("dependencies") or 
							self.ownerComp.op("empty")
						).col(0)
					]),
					"Authors" : json.dumps([{
						"name" : block.par.Name.eval(), "email" : block.par.Email.eval()
					} for block in metaComp.seq.Authors]).replace(":", "="), #Oh my god. Why python WHY? Why use TOML, not have a writer in hand and then NOT AHDEAR TO JSON!!!
					"Description" : metaComp.par.Description.eval(),
					"License" : metaComp.par.License.eval(),
					"PythonVersion" : f">={sys.version_info.major}.{sys.version_info.minor}",
					"Keywords" : json.dumps(["TouchDesigner", app.build] + [
						block.par.Keyword.eval() for block in metaComp.seq.Keywords
					]),
					"URLs" : f"\n".join([
						f'{block.par.Name.eval()}="{block.par.Url.eval()}"' for block in metaComp.seq.Urls
					]),
					"Build" : app.build
				})
			)

		srcFolder = Path(buildDir, "src", metaComp.par.Name.eval() )
		srcFolder.mkdir( parents=True, exist_ok=True)
		savedTox = self.SaveComp( targetComp, srcFolder )
		
		with Path( srcFolder , "__init__.py").open("+wt") as initFile:
			initFile.write(
				self.ownerComp.op("prefabInit").text.format(**{
					"Filename" : savedTox.name,
					"Version" : f"{metaComp.par.Version1}.{metaComp.par.Version2}"
				})
			)

		with Path( srcFolder , "_Typing.py").open("+wt") as typingFile:
			typingFile.write(
				createTypingModuleString( targetComp )
			)
		# 
		targetComp.destroy()
		return buildDir
		
	def Build(self, buildDir:Path):
		self.ownerComp.op("TD_uv").Run([ 
			"build", str(buildDir), 
			 "--index-strategy", 
			 "unsafe-best-match" ]
		)


	def Publish(self, buildDir:Path):
		"""
			Actually Upload to the repository using twine.
			Right now actually uses cloudsmith. Wold 
		"""
		self.ownerComp.op("TD_uv").Run([ "publish", 
								  "--directory", str(buildDir), 
								  "--publish-url", self.ownerComp.par.Index.eval() ] + (
									[ "--token", self.ownerComp.par.Token.eval() ] * bool( self.ownerComp.par.Token.eval() )
									)
								)
		return
