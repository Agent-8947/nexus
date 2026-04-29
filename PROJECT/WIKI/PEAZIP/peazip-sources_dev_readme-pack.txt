Contains data to help creation of packages of PeaZip for various package management systems.
It does not replaces or duplicates the function of sources package peazip-x.y.z.src, as it is simply meant to help packaging the application for a specific distribution system, rather than compiling and building the binaries of the application.
Please refer to the readme file in .src package to understand how content is organized in PeaZip installable and portable packages.


BSD

To edit BDS packages, which are portable, simply extract PeaZip for BSD package as plain archive file, and edit the content referring to .src package's readme instructions.
Basically, you can start from re-compiling and replacing the app's binaries targeting your own CPU architecture and favourite widgetset.


LINUX

DEB folder in this package contains DEB package folders for Linux (current GTK2 and Qt5 builds).

RPM folder in this package contains RPM folders and specs folder for Linux (current GTK2 and Qt5 builds).

To edit Portable packages, extract the TAR.GZ archive containing the package, update binaries and resources, and simply re-compress it in TAR.GZ or any other suitable archive format supported by the target distribution(s).


MACOS

To edit macOS packages it is simply needed one of the pre-built DMG files for Darwin/macOS.
To open the peazip.app folder inside the DMG use "Show package content" from Finder, or use an alternative file manager as PeaZip itself.
You can update resources and binaries in the folder the original package was extracted to, and finally re-build the DMG package from Disk Utility (File > New Image > From folder, selecting the folder of the updated package).
As alternative to DMG format, the folder of the updated package can simply be compressed and distributed as ZIP file, which can be used on legacy OSX systems not supporting DMG packages.


WINDOWS

To customize Windows installable packages you can start updating binaries and resources in the folder where the application is installed.
Configuration files, which are stored in user profile's path, will be created on the fly running the application and are not needed in installable packages.
Installers (.exe) are created by the InnoSetup .iss scripts (Pascal -like dialect) available in the "installer" folder of the source package.

To edit Windows Portable packages, extract the ZIP archive containing the package, update binaries and resources, and simply re-compress it ZIP format.