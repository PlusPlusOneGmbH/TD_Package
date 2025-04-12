"""Info Header Start
Name : extForklift
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.31378
Info Header End"""
from tempfile import TemporaryDirectory
from pathlib import Path
import json
import sys
from uuid import uuid4
import inspect
from itertools import chain
from typingsAstParser import createTypingModuleString

class extForklift:
    """
	extForklift description
	"""

    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        pass

    def _bindAssign(self, parentParName, targetParName, targetComp):
        pass

    def createMetaComp(self, targetComp):
        pass

    def Rundown(self, targetComp, TempOutput=True):
        pass

    def Prepare(self, targetComp: COMP):
        pass

    def cleanExternalDependencies(self, targetComp, parName):
        pass

    def fetchDatDepdencies(self, moduleOp: textDAT):
        pass

    def fetchExtDependencies(self, compWithExtensions: COMP):
        pass

    def SaveComp(self, targetComp: COMP, targetDir: Path):
        pass

    def validateMeta(self, targetComp: COMP):
        pass

    def Export(self, _targetComp: COMP, _buildDir):
        pass

    def Build(self, buildDir: Path):
        pass

    def Publish(self, buildDir: Path):
        """
			Actually Upload to the repository using twine.
			Right now actually uses cloudsmith. Wold 
		"""
        pass