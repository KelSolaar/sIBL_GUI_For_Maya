#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sIBL_GUI_For_Maya.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Maya sIBL_GUI Helper Script For Maya 2011 And Higher.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import maya.cmds as cmds
import maya.mel as mel
import os
import platform
import re
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["HDRLABS_URL",
		"WINDOWS_RELEASE_URL",
		"DARWIN_RELEASE_URL",
		"LINUX_RELEASE_URL",
		"APPLICATION_THREAD_URL",
		"openPreferences",
		"launchesApplication",
		"executeLoaderScript",
		"deleteSmartIblNodes"]

HDRLABS_URL = "http://www.hdrlabs.com"
WINDOWS_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Windows"
DARWIN_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Darwin"
LINUX_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Linux"
APPLICATION_THREAD_URL = "http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Environment(object):
	"""
	This class provides methods to manipulate environment variables.
	"""

	def __init__(self, variable=None):
		"""
		This method initializes the class.

		:param variable: Variable to manipulate. ( String )
		"""

		self._variable = variable

	def getValue(self):
		"""
		This methods returns given environment variable value.

		:return: Variable value. ( String )
		"""

		if self._variable:
			return os.environ.get(self._variable)

def _setExecutablePathOptionVar():
	"""
	This definition sets **executablePath** optionVar.
	"""

	_setOptionVar("sIBL_GUI_executablePath", cmds.textField("Executable_Path_textField", query=True, text=True))

def _setLoaderScriptPathOptionVar():
	"""
	This definition sets **sIBL_GUI_loaderScriptPath** optionVar.
	"""

	_setOptionVar("sIBL_GUI_loaderScriptPath", cmds.textField("Loader_Script_Path_textField", query=True, text=True))

def _setCommandPortOptionVar():
	"""
	This definition sets **sIBL_GUI_commandPort** optionVar.
	"""

	_setOptionVar("sIBL_GUI_commandPort", cmds.intSliderGrp("Command_Port_intSliderGrp", query=True, value=True))

def _setOptionVar(name, value):
	"""
	This definition stores given optionVar with given value.
	
	:param name: OptionVar name. ( String )
	:param value: OptionVar value. ( Object )
	"""

	cmds.optionVar(sv=(name, value))

def _openUrl(url):
	"""
	This definition opens given url.

	:param url: Url to open. ( String )
	"""

	cmds.launch(web=url)

def _Executable_Path_button__command(state=None):
	"""
	This definition is triggered by **Executable_Path_button** widget.

	:param state: Button state. ( Boolean )
	"""

	fileName = cmds.fileDialog2(ds=2, fileFilter="All Files (*.*)", fm=(not platform.system() == "Darwin" and 1 or 3))
	fileName = fileName and fileName[0] or None
	if not fileName:
		return

	if fileName.endswith("sIBL_GUI.exe") or fileName.endswith("sIBL_GUI.app") or fileName.endswith("sIBL_GUI"):
		cmds.textField("Executable_Path_textField", edit=True, text=fileName)
		_setExecutablePathOptionVar()
	else:
		mel.eval("warning(\"sIBL_GUI | Chosen executable path is invalid!\");")

def _Executable_Path_textField__changeCommand(value):
	"""
	This definition is triggered by **Executable_Path_textField** widget.

	:param value: Value. ( String )
	"""

	if os.path.exists(value) and \
		(value.endswith("sIBL_GUI.exe") or \
		value.endswith("sIBL_GUI.app") or \
		value.endswith("sIBL_GUI")):
		_setExecutablePathOptionVar()
	else:
		mel.eval("warning(\"sIBL_GUI | Chosen executable path is invalid!\");")

def _Loader_Script_Path_button__command(state=None):
	"""
	This definition is triggered by **Loader_Script_Path_button** widget.

	:param state: Button state. ( Boolean )
	"""

	fileName = cmds.fileDialog2(ds=2, fileFilter="All Files (*.*)", fm=4)
	fileName = fileName and fileName[0] or None
	if not fileName:
		return

	cmds.textField("Loader_Script_Path_textField", edit=True, text=fileName)
	_setLoaderScriptPathOptionVar()

def _Loader_Script_Path_textField__changeCommand(value):
	"""
	This definition is triggered by **_Loader_Script_Path_textField** widget.

	:param value: Value. ( String )
	"""

	if os.path.exists(value):
		_setLoaderScriptPathOptionVar()
	else:
		mel.eval("warning(\"sIBL_GUI | Chosen Loader Script path is invalid!\");")

def _Command_Port_intSliderGrp__changeCommand(value):
	"""
	This definition is triggered by **Command_Port_intSliderGrp** widget.

	:param value: Value. ( Float )
	"""

	_setCommandPortOptionVar()

def _Command_Port_button__command(state=None):
	"""
	This definition opens the command port.

	:param state: Button state. ( Boolean )
	"""

	try:
		cmds.commandPort(name="127.0.0.1:" + str(cmds.intSliderGrp("Command_Port_intSliderGrp", query=True, value=True)))
	except:
		mel.eval("warning(\"sIBL_GUI | Command port is already open or can't be opened!\");")

	_setCommandPortOptionVar()

def _Get_Application_button__command(state=None):
	"""
	This definition opens Online Repository.

	:param state: Button state. ( Boolean )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		url = WINDOWS_RELEASE_URL
	elif platform.system() == "Darwin":
		url = DARWIN_RELEASE_URL
	elif platform.system() == "Linux":
		url = LINUX_RELEASE_URL

	_openUrl(url)

def _HDRlabs_button__command(state=None):
	"""
	This definition opens HDRLabs thread.

	:param state: Button state. ( Boolean )
	"""

	_openUrl(HDRLABS_URL)

def _Application_Thread_button__command(state=None):
	"""
	This definition opens sIBL_GUI thread.

	:param state: Button state. ( Boolean )
	"""

	_openUrl(APPLICATION_THREAD_URL)

def _sIBL_GUI_For_Maya_window():
	"""
	This definition launches **sIBL_GUI For Maya Preferences** window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("_sIBL_GUI_For_Maya_window", exists=True)):
		cmds.deleteUI("_sIBL_GUI_For_Maya_window")

	cmds.window("_sIBL_GUI_For_Maya_window",
		title="sIBL_GUI For Maya - Preferences",
		sizeable=False)

	horizontalSpacing = 8

	cmds.columnLayout(adjustableColumn=True)

	cmds.picture(image="sIBL_GUI_Small_Logo.png")

	cmds.frameLayout(label="sIBL_GUI Executable Path", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
	cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[(1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
	cmds.textField("Executable_Path_textField", cc=_Executable_Path_textField__changeCommand)
	cmds.button("Executable_Path_button", label="...", al="center", command=_Executable_Path_button__command)
	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	executablePath = cmds.optionVar(q="sIBL_GUI_executablePath")
	if executablePath:
		cmds.textField("Executable_Path_textField", edit=True, text=executablePath)

	cmds.frameLayout(label="Loader Script Path", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
	cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[(1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
	cmds.textField("Loader_Script_Path_textField", cc=_Loader_Script_Path_textField__changeCommand)
	cmds.button("Loader_Script_Path_button", label="...", al="center", command=_Loader_Script_Path_button__command)
	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	sIBL_GUI_loaderScriptPath = cmds.optionVar(q="sIBL_GUI_loaderScriptPath")
	if sIBL_GUI_loaderScriptPath:
		cmds.textField("Loader_Script_Path_textField", edit=True, text=sIBL_GUI_loaderScriptPath)

	cmds.frameLayout(label="Command Port", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
	cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[(1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
	cmds.intSliderGrp("Command_Port_intSliderGrp", field=True, minValue=0, maxValue=65535, value=2048, cc=_Command_Port_intSliderGrp__changeCommand)
	cmds.button("Command_Port_button", label="Open Port", al="center", command=_Command_Port_button__command)
	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	sIBL_GUI_commandPort = int(cmds.optionVar(q="sIBL_GUI_commandPort"))
	if sIBL_GUI_commandPort:
		cmds.intSliderGrp("Command_Port_intSliderGrp", edit=True, value=sIBL_GUI_commandPort)

	cmds.frameLayout(label="Online", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
	cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign3=["center", "center", "center"], columnAttach=[(1, "both", horizontalSpacing), (2, "both", horizontalSpacing), (3, "both", horizontalSpacing)])
	cmds.button("Get_Application_button", label="Get sIBL_GUI ...", al="center", command=_Get_Application_button__command)
	cmds.button("HDRlabs_button", label="Visit HDRLabs ...", al="center", command=_HDRlabs_button__command)
	cmds.button("Application_Thread_button", label="Visit sIBL_GUI Thread ...", al="right", command=_Application_Thread_button__command)
	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.showWindow("_sIBL_GUI_For_Maya_window")
	cmds.windowPref(enableAll=True)

def openPreferences():
	"""
	This definition launches **sIBL_GUI For Maya - Preferences** window.
	"""

	_sIBL_GUI_For_Maya_window()
	return True

def launchApplication():
	"""
	This definition launches **sIBL_GUI**.

	:return: Definition sucess. ( Boolean )
	"""

	executablePath = cmds.optionVar(q="sIBL_GUI_executablePath")
	if executablePath:
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			os.system("start /D" + "\"" + os.path.dirname(executablePath) + "\"" + " " + executablePath.replace(" ", "\" \""))
		elif platform.system() == "Darwin":
			os.system("open -a " + executablePath)
		elif platform.system() == "Linux":
			os.system("\"" + executablePath + "\" &")
		return True
	else:
		mel.eval("warning(\"sIBL_GUI | No sIBL_GUI executable path defined!\");")
		cmds.confirmDialog(title="sIBL_GUI | Warning", message="No sIBL_GUI executable path defined!\nPlease define one in preferences!", button=["Ok"], defaultButton="Ok")
		openPreferences()

def executeLoaderScript():
	"""
	This definition executes **sIBL_GUI** Loader Script.

	:return: Definition sucess. ( Boolean )
	"""

	loaderScriptPath = cmds.optionVar(q="sIBL_GUI_loaderScriptPath")
	if loaderScriptPath:
		if os.path.exists(loaderScriptPath):
			if re.search(r"\.mel$", loaderScriptPath):
				mel.eval("source \"" + loaderScriptPath + "\"")
			elif re.search(r"\.pyc?$", loaderScriptPath):
				path = os.path.dirname(loaderScriptPath)
				path not in sys.path and sys.path.append(path)
				module = os.path.splitext(os.path.basename(loaderScriptPath))[0]
				import_ = __import__(module)
				reload(import_)
				if hasattr(import_, "Setup"):
					setup = import_.Setup()
					setup.execute()
			return True
		else:
			mel.eval("error(\"sIBL_GUI | Loader Script doesn't exists!\");")
	else:
		mel.eval("warning(\"sIBL_GUI | No Loader Script found!\");")
		cmds.confirmDialog(title="sIBL_GUI | Warning", message="No Loader Script found!\nPlease define one in preferences!", button=["Ok"], defaultButton="Ok")
		openPreferences()

def deleteSmartIblNodes():
	"""
	This definition deletes **Smart Ibl** and **Lightsmith** lights nodes.
	
	:return: Definition sucess. ( Boolean )
	"""

	nodes = []
	selection = cmds.ls(sl=True, l=True, dag=True)
	if selection:
		prefixes = []
		for node in selection:
			relatives = [node]
			nodeRelatives = cmds.listRelatives(node, f=True, ad=True)
			nodeRelatives and relatives.extend(nodeRelatives)
			for relative in relatives:
				if re.search(r"\w*_Root$", relative):
					if relative.replace("_Root", "_Support").split("|")[-1] in cmds.listRelatives(relative, ad=True):
						prefixes.append(relative.replace("_Root", "").split("|")[-1])
		for prefix in prefixes:
			userChoice = cmds.confirmDialog(title="sIBL_GUI", message="Nodes with following prefix : '%s' are planned for deletion! Would you like to proceed?" % prefix, button=["Yes", "No"], defaultButton="Yes", cancelButton="No", dismissString="No")
			if userChoice == "Yes":
				nodes.extend(sorted(cmds.ls(prefix + "*", l=True)))
	else:
		result = cmds.promptDialog(title="sIBL_GUI | Nodes Deletion",
	                message="Enter scene 'Smart Ibl' Nodes prefix ( 'sIBL' ):",
	                text="sIBL",
	                button=["Ok", "Cancel"],
	                defaultButton="Ok",
	                cancelButton="Cancel",
	                dismissString="Cancel")

		if result == "Ok":
			prefix = cmds.promptDialog(query=True, text=True)
			nodes.extend(sorted(cmds.ls("%s*" % prefix, l=True)))

	for node in nodes:
		if cmds.objExists(node):
			print("sIBL_GUI | Deleting node: '%s'!" % node)
			cmds.delete(node)

	return True
