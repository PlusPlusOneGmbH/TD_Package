'''Info Header Start
Name : autoComplete_Example
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''
with mod.Import.MountModule("SimpleTest"):
    from SimpleTest.extTestExtension import extTestExtension

from typing import Union
targetComp:Union[COMP, extTestExtension] = op("base1")
targetComp.Foobar()