sIBL_GUI For Maya - Helper Script
=================================

Installation
------------

Extract "sIBL_GUI For Maya.zip" content into your Maya Preferences folder, for example on Windows: "C:\Documents and Settings\$USER\Mes documents\maya\2011\". Start Maya, and you should find a new "sIBL_GUI" shelf.
You can add the following lines into your "userSetup.mel" if you want the Socket Port to be opened automatically on Maya startup::

	commandPort -n ( "127.0.0.1:"  + `optionVar -q "sIBL_GUI_commandPort"` );

Usage
-----

-  "p" icon launches "sIBL_GUI For Maya Preferences" window where you define "sIBL_GUI" executable path, Loader Script path and Remote Connection Port.
-  "O" icon launches "sIBL_GUI".
-  "e" icon executes the "Loader Script".
-  "e" icon launches the cleanup function.

About
-----

| **sIBL_GUI For Maya** by Thomas Mansencal - 2008 - 2014
| **sIBL_GUI** by Thomas Mansencal - 2008 - 2014
| Copyright © 2008 - 2014 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_