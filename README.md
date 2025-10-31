
# This Repo has been rolled up in to : https://github.com/PlusPlusOneGmbH/tdp-MVP and is archived. No further implementations and or changes will occur.



![Firefly a euro palette full of different crates and boxes filled to the brim with bananas 20284](https://github.com/user-attachments/assets/f99a642a-b3c6-42c8-9f2a-f17d1e444678)

# A proposal for PackageManagement in TouchDesigner

Runs on TouchDesigner 2025 Experimental Builds

## TDP - A Standart for TouchDesigner Packaging
TDP is short TouchDesignerPackage and defines a simple standart in which TouchDesigner components should be packaged so they are easily accessable for Developers, but also non-dev users of the platform.

In general, we should try to adher to the following baseline:
- One Module per Package.
- One .tox File per Module.
- A seperated PackageType for collections. (TDC ?)
- Components should be built in a way that changes of the internal workings are not necesarry.
- Data needs to be cept outside of the components.
- Components should work standalone without dependencies to external files once installed. (?)
- Components are not allowed to rely or inject elements in to the Global Namespace like GlobalOP-Shortcuts.

The OnePer-Rule allows for a simpler management of Versioning and makes it easyier for users to search and understand what they are doing. Bundling several Components in to a single Module makes automated processing much harder.

### File-Layout
A TDP should implement two attributes at minimum. ToxFile and Typing.

#### ToxFile
```python
from pathlib import Path
ToxFile = Path(__file__).parent / "Release.tox"
```
Release-Tox in this case is a Placeholder Name and should be substituted with the actual name of the File. 
The file needs to be next to the ```__init__.py``` for this to work
#### Typing
```python
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
        def __getattribute__(self, name):
            raise NotImplemented( "This Class is only for Typehinting!")
```

This allows use now to do two things. 
- Given that the Module is already mounted, we can make use of the Module on Demand method in TD and pass the refference to the Externaltox-Parameter:
```mod.MyPackage.ToxFile```
- If we need to rely on tools like TD_PIP we can use the ImportModule() method to the same result.
- We can add typehinting to our code.
```python
from MyPackageModule import Typing as MyPackageComp
myOperator:MyPackageComp = op("Foobar")
```
This allows us to also add typehinting for Parameters and Methods from Extensions.
Using the if TYPE_CHECKING clause keeps users from trying to import the actual package.

## Forklift
Forklift is packaging tool that creates and uploads ready packages to indizes like Pip from a Component inside TouchDesigner.

It utilises TD_UV to allow for a handsoff, internal approach. The output is a legal package that follows the rules of TDP defined above. 

It makes use of a PackageMeta component that allows for modification of behaviour if required.

It should do the following things:
- Make sure that the Component does not used external files by removing refferences to external files.
- Listen to specified tags to allow for keeping external refferences. This refferences should then either be handles by a DependencyManagementCOMP or by CustomPars on the TopLevel.
- Analyze and export Modules from inside TD for typecompletion.
- Generate the Typing-Part of the exported module programtically.
- Upload the content to a defined repository making use of .pypirc files.
- Allow for customisation on how this behaviour executes.
- Add dependencies from a dependency tableDAT inside of the release component to the package.

## PowderMonkey
PowderMonkey is a Dependencymanager inside of TD and should do:
- Allow Searching and Installation of TDP from a defined Index like PIP via a UI.
- Be able to manage the importing and provisioning of the modules.
- Run headless.
- Export and document external dependencies. 
