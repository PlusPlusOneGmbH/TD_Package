__version__ = "1.9"

from pathlib import Path
ToxFile = Path( Path( __file__ ).parent, "queriedWebclient3.tox" )

# Bring it in to export for import.
# Needs deeper analysis of the targetComp.
# TBD
# from ._Typing import Typing