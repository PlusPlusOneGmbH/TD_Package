"""Info Header Start
Name : extPowderMonkey
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.31378
Info Header End"""
from functools import cache

class extPowderMonkey:

    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.UV = self.ownerComp.op('TD_uv')
        pass

    @cache
    def GetTox(self, moduleName, prefix='', package='', index=''):
        pass

    def GetGlobalComp(self, moduleName, prefix='', package='', index='', globalShortcut='', globalPath=''):
        pass