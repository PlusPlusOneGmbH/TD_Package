from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from .extExampleExtension import extExampleExtension
    from tdi.ops.comps.baseCOMP import BaseCOMPPars as opPars
    from tdi.parTypes import *

    class CustomPars(ParCollection):
        Float: ParFloat
        """
        
        Parameter Page : Custom
        """
        Float2: ParFloat
        """
        
        Parameter Page : Custom
        """
        Object: ParObject
        """
        
        Parameter Page : Custom
        """
        Op: ParOP
        """
        
        Parameter Page : Custom
        """
        Vcname: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcauthor: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcversion: ParInt
        """
        
        Parameter Page : Version Ctrl
        """
        Vcbuild: ParInt
        """
        
        Parameter Page : Version Ctrl
        """
        Vcsavetimestamp: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcsaveorigin: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcsaveversion: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcoriginal: ParToggle
        """
        
        Parameter Page : Version Ctrl
        """
        Vcgroup: ParStr
        """
        
        Parameter Page : Version Ctrl
        """

    class Typing(extExampleExtension, baseCOMP):
        par: Union[opPars, CustomPars]
        pass
else:

    class Typing:

        def __getattribute__(self, name):
            raise NotImplemented('This Class is only for Typehinting!')