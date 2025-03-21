from pathlib import Path
ToxFile = Path( Path( __file__ ).parent, "Release.tox" )

from typing import Union
from extTestExtension import extTestExtension

class Typing( extTestExtension, COMP):
    pass