
![Firefly a euro palette full of different crates and boxes filled to the brim with bananas 20284](https://github.com/user-attachments/assets/f99a642a-b3c6-42c8-9f2a-f17d1e444678)

Extremly rough testingground for a PythonPackage based distribution and import pattern for TouchDesigner.
The system is based TD_PIP in its core, localized in the local/modules of the project, to allow a quick and easy way of refferencing a package.
A package should contain a simple initfile, pointing to the ToxFile using the ```__file__``` property.
```python
from pathlib import Path
ToxFile = Path( Path( __file__ ).parent, "Release.tox" )
```
Next to the init we have the ToxFile named Release.tox

We can now use TD_PIP pointing at that library to Import the package on demand and returning the ToxFile attribute.
```python
def Tox(packageName, pipPackageName = ""):
    with op("td_pip").MountModule( packageName, pipPackageName = pipPackageName ) as mountedPackage:
        return mountedPackage.ToxFile
```



We can now streight up use ```mod.Import.Tox("SimpleTest")``` in any Comp to get the path to the ToxFile.

![grafik](https://github.com/user-attachments/assets/8dc356c3-7c4d-4510-b35a-c8e00a9b6292)


### thoughts
TD_PIP is designed as an on-demand packagemanager.
Idealy we would have a package-browser which could install and write the package to a package.json like file, just like npm-install does (which is so much better then everything PIP is doing, fight me!)
We could then, for deployment, use that package.json to preinstall all dependencies without having to rely on the on-demand nature of TD-PIP as is right now.

It would also be extremly important that we can define an external library on a per-project basis naively in TD, without having to rely on elements like TD_PIP, so we could import Extension for type-completion free of charge! 
Right now this requires the Mounting-paradigm of TD-Pip to work, which is pretty cumbersome (but works!)
![grafik](https://github.com/user-attachments/assets/ff06c57c-061c-4441-ba0e-ef4b07799025)

For this to work we need unified tooling to Export a COMP with extension and the correct ```__init__``` file and refferences. 
And a browser.
And a package.json.
And an external installer/manager (+ the internal browser)
And a package repository to work off of!

It is too late, I have to go to bed....
