from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from .extQueriedWebClient import extQueriedWebClient
    from tdi.ops.comps.baseCOMP import BaseCOMPPars as opPars
    from tdi.parTypes import *

    class CustomPars(ParCollection):
        Server: ParStr
        """
        
        Parameter Page : Settings
        """
        Header: ParDAT
        """
        
        Parameter Page : Settings
        """
        Length: ParFloat
        """
        
        Parameter Page : Settings
        """
        Includeheader: ParToggle
        """
        
        Parameter Page : Settings
        """
        Clear: ParPulse
        """
        
        Parameter Page : Settings
        """
        Processing: ParToggle
        """
        
        Parameter Page : Settings
        """
        Deploystubs: ParPulse
        """
        
        Parameter Page : Settings
        """
        Endpoint: ParStr
        """
        
        Parameter Page : Interact
        """
        Get: ParPulse
        """
        
        Parameter Page : Interact
        """
        Createcallbacks: ParPulse
        """
        
        Parameter Page : Callbacks
        """
        Callbacks: ParDAT
        """
        
        Parameter Page : Callbacks
        """
        Vcname: ParStr
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcauthor: ParStr
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcversion: ParInt
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcbuild: ParInt
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcsavetimestamp: ParStr
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcoliblink: ParStr
        """
        
        Parameter Page : Version Ctrl
        """
        Vcsaveorigin: ParStr
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcsaveversion: ParStr
        """
        Help not available.
        Parameter Page : Version Ctrl
        """
        Vcoriginal: ParToggle
        """
        Help not available.
        Parameter Page : Version Ctrl
        """

    class Typing(extQueriedWebClient, baseCOMP):
        par: Union[opPars, CustomPars]
        pass
else:

    class Typing:

        def __getattribute__(self, name):
            raise NotImplemented('This Class is only for Typehinting!')