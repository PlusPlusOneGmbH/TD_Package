from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    from .extTestExtension import extTestExtension
    from tdi.ops.comps.baseCOMP import BaseCOMPPars
    from tdi.parTypes import *


    class CustomPars(ParCollection):
        Fooo : ParInt
        """
            This is a parameter and an INT.
        """
        Bar : ParCHOP
        """
            This is a CHOP based parameter.
        """


    class Typing( extTestExtension, COMP):
        par : Union[BaseCOMPPars, CustomPars]
        pass
else:
    class Typing:
        pass
    