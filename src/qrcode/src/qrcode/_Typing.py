from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from .extQrCode import extQrCode
    from tdi.ops.comps.baseCOMP import BaseCOMPPars as opPars
    from tdi.parTypes import *

    class CustomPars(ParCollection):
        Target: ParStr
        """
        
        Parameter Page : Custom
        """
        Generate: ParPulse
        """
        
        Parameter Page : Custom
        """
        Fieldsize: ParInt
        """
        
        Parameter Page : Custom
        """
        Bordersize: ParInt
        """
        
        Parameter Page : Custom
        """
        Fillr: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Fillg: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Fillb: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Filla: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Backgroundr: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Backgroundg: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Backgroundb: ParRGBA
        """
        
        Parameter Page : Custom
        """
        Backgrounda: ParRGBA
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
        Vcversion: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcbuild: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcoliblink: ParStr
        """
        
        Parameter Page : Version Ctrl
        """

    class Typing(extQrCode, baseCOMP):
        par: Union[opPars, CustomPars]
        pass
else:

    class Typing:

        def __getattribute__(self, name):
            raise NotImplemented('This Class is only for Typehinting!')