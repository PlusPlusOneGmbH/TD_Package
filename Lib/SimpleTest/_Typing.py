from typing import Union
from extTestExtension import extTestExtension
from tdi.ops.comps.baseCOMP import BaseCOMPPars
from tdi.parTypes import *


class CustomPars(ParCollection):
    Fooo : ParInt
    Bar : ParCHOP


class Typing( extTestExtension, COMP):
    par : Union[BaseCOMPPars, CustomPars]
    pass
