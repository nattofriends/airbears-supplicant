from distutils.core import setup
import py2exe, os, sys
sys.path.append(".")

try:
    import wx
except ImportError:
    print "wxPython is required to build AirBearsSupplicant."
    sys.exit(-1)
    
if wx.VERSION[0:2] < (2, 9):
    print "wxPython 2.9 or above is required.")
    sys.exit(-1)

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>TagQueryClient</description>
<dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b" />
    </dependentAssembly>
  </dependency>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

setup(
options = {
	'py2exe': {	
        'bundle_files': 1, 
		'optimize': 2,
        'excludes': ['wlan_darwin'],
        'dll_excludes': ['w9xpopen.exe'],
        "ascii": True,
        "excludes": ['doctest', 'pdb', 'unittest', 'difflib', 'inspect', 'pyreadline', 'optparse', 'pickle', 'tcl', 'Tkconstants', 'Tkinter', 'curses', 'email', 'bz2', '_scproxy', 'email.utils', 'win32ui']
    }},
windows = [{
	"script": 'main.py', 
    "dest_base": "airbears_supplicant",
	"icon_resources": [(1, 'assets/tag.ico')],
	"other_resources": [(24, 1, manifest),
                       # (u"DefaultConfig", 1, open("DefaultConfig.tqconf").read())
                       ]
	}],
# version = ver,
# data_files = [("Microsoft.VC90.CRT", ["msvcr90.dll"])],
zipfile = None)