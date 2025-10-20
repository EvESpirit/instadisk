# InstaDisk


A tiny Python script designed to be ran from an executable, allowing for RAMDisk creation with two clicks. Uses [ImDisk](https://sourceforge.net/projects/imdisk-toolkit/files/latest/download) under the hood, so it must be installed before using this.


This tool is set to NTFS, 8GB by ***default***, if you want a different filesystem or want the RAMDisk shortcut to be smaller or bigger, please, edit the script's ```CONFIG``` section at the very top to your preferences,
and then use [AutoPyToExe](https://pypi.org/project/auto-py-to-exe/) to package the script back into an executable.




### Usage:
Download the rd.exe file from this repository's releases.

>*(Optional) Verify with a free tool like File Hasher (available on the Microsoft Store) or using PowerShell's inbuilt ```Get-FileHash rd.exe``` capabilities.*

```SHA256 for the 1.0 release: 6692303315A187ECE178F23B34733062F5AC189259EA6A9A3191CD951C83FAC9```

Run it. That's it.




### Terminal usage:
Download the rd.py file from this repository or copy it's source code.

>*(Optional) Edit the edit the script's ```CONFIG``` section at the very top to your preferences.*

Open CMD or PowerShell in the folder where you put the script and run it with ```python md5.py```
