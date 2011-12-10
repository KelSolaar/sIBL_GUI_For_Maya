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

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOADER_SCRIPTS_DIRECTORY = "HDRLabs/sIBL_GUI/io/loaderScripts/"
LOADER_SCRIPT = "sIBL_Maya_Import.mel"
HDRLABS_URL = "http://www.hdrlabs.com"
WINDOWS_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Windows"
DARWIN_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Darwin"
LINUX_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Linux"
APPLICATION_THREAD_URL = "http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Environment( object ):
	"""
	This Class Provides Methods To Manipulate Environment Variables.
	"""

	def __init__( self, variable = None ):
		"""
		This Method Initializes The Class.

		:param variable: Variable To Manipulate. ( String )
		"""

		# --- Setting Class Attributes. ---
		self._variable = variable

	def getPath( self ):
		"""
		This Method Gets The Chosen Environment Variable Path As A String.

		:return: Variable Path. ( String )
		"""

		if self._variable:
			for param in os.environ:
				if( self._variable == param ): return os.environ[param]

def getSystemApplicationDataDirectory():
	"""
	This Definition Gets The System Application Data Directory.

	:return: User Application Data Directory. ( String )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		environmentVariable = Environment( "APPDATA" )
		return environmentVariable.getPath()

	elif platform.system() == "Darwin":
		environmentVariable = Environment( "HOME" )
		return os.path.join( environmentVariable.getPath(), "Library/Preferences" )

	elif platform.system() == "Linux":
		environmentVariable = Environment( "HOME" )
		return environmentVariable.getPath()

def storeCommandPortOptionVar():
	"""
	This Definition Stores The Command Port In An Option Var.
	"""

	cmds.optionVar( iv = ( "sIBL_GUI_Command_Port", cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )

def storeExecutablePathOptionVar():
	"""
	This Definition Stores sIBL_GUI Executable Path In An Option Var.
	"""

	cmds.optionVar( sv = ( "sIBL_GUI_Executable_Path", cmds.textField( "sIBL_ExecutablePath_TextField", query = True, text = True ) ) )

def openCommandPort():
	"""
	This Definition Opens The Command Port.
	"""

	try:
		cmds.commandPort( name = "127.0.0.1:" + str( cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )
		cmds.commandPort( name = ":" + str( cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )
	except:
		mel.eval( "warning( \"sIBL_GUI | Command Port Is Already Open Or Can't Be Opened!\" );" )

	storeCommandPortOptionVar()

def executableFileBrowser():
	"""
	This Definition Provides A Browser.
	"""

	filePath = cmds.fileBrowserDialog( m = 0, fc = getExecutablePath, ft = "", an = "sIBL_GUI_Executable", wt = "Choose sIBL_GUI Executable" )

def getExecutablePath( fileName, fileType ):
	"""
	This Definition Gets sIBL_GUI Executable Path.

	:param fileName: File Name. ( String )
	:param fileType: File Type. ( String )
	"""

	if platform.system() == "Darwin":
		if "sIBL_GUI.app" in fileName:
			fileName = "sIBL_GUI.app" in fileName and fileName.split( "sIBL_GUI.app" )[0] + "sIBL_GUI.app"
		else:
			mel.eval( "warning( \"sIBL_GUI | On Mac Os X, You Need To Choose 'sIBL_GUI' File Inside 'sIBL_GUI.app/Contents/MacOS' Folder, The Helper Script Will Then Construct The Path Itself!\" );" )

	if fileName.endswith( "sIBL_GUI.exe" ) or fileName.endswith( "sIBL_GUI.app" ) or fileName.endswith( "sIBL_GUI" ):
		cmds.textField( "sIBL_ExecutablePath_TextField", edit = True, text = fileName )
		storeExecutablePathOptionVar()
	else:
		mel.eval( "warning( \"sIBL_GUI | Chosen Executable Path Is Invalid!\" );" )

def sIBL_CommandPortIntSlider_OnEdit():
	"""
	This Definition Is Triggered By sIBL_CommandPortIntSlider Edit.
	"""

	cmds.intField( "sIBL_CommandPort_IntField", edit = True, value = cmds.intSlider( "sIBL_CommandPort_IntSlider", query = True, value = True ) )

	storeCommandPortOptionVar()

def sIBL_CommandPortIntField_OnEdit():
	"""
	This Definition Is Triggered By sIBL_CommandPortIntField Edit.
	"""

	cmds.intSlider( "sIBL_CommandPort_IntSlider", edit = True, value = cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) )

	storeCommandPortOptionVar()

def sIBL_ExecutablePathTextField_OnEdit():
	"""
	This Definition Is Triggered By sIBL_ExecutablePathTextField Edit.
	"""

	textFieldContent = cmds.textField( "sIBL_ExecutablePath_TextField", query = True, text = True )
	if textFieldContent.endswith( "sIBL_GUI.exe" ) or textFieldContent.endswith( "sIBL_GUI.app" ) or  textFieldContent.endswith( "sIBL_GUI" ):
		storeExecutablePathOptionVar()
	else:
		mel.eval( "warning( \"sIBL_GUI | Chosen Executable Path Is Invalid!\" );" )

def openUrl( url ):
	"""
	This Definition Opens HDRLabs Thread.

	:param url: Url To Open. ( String )
	"""
	cmds.launch( web = url )

def getApplication_Button_OnClicked():
	"""
	This Definition Opens Online Repository.
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		url = WINDOWS_RELEASE_URL
	elif platform.system() == "Darwin":
		url = DARWIN_RELEASE_URL
	elif platform.system() == "Linux":
		url = LINUX_RELEASE_URL

	openUrl( url )

def hdrlabs_Button_OnClicked():
	"""
	This Definition Opens HDRLabs Thread.
	"""

	openUrl( HDRLABS_URL )

def applicationThread_Button_OnClicked():
	"""
	This Definition Opens sIBL_GUI Thread.
	"""

	openUrl( APPLICATION_THREAD_URL )

def openPreferences():
	"""
	This Definition Launchs sIBL_GUI For Maya Preferences.
	"""

	cmds.windowPref( enableAll = False )

	if ( cmds.window( "sIBL_GUI_For_Maya_Window", exists = True ) ):
		cmds.deleteUI( "sIBL_GUI_For_Maya_Window" )

	cmds.window( "sIBL_GUI_For_Maya_Window",
		title = "sIBL_GUI For Maya - Preferences",
		width = 8,
		height = 8,
		rtf = True,
		toolbox = True )

	horizontalSpacing = 8
	verticalSpacing = 16

	cmds.columnLayout( adjustableColumn = True, rowSpacing = verticalSpacing, columnOffset = ["both", horizontalSpacing ] )
	cmds.frameLayout( label = "sIBL_GUI Executable Path", labelAlign = "center", cll = False, li = 4, borderStyle = "etchedOut", mh = 4, mw = 4 )
	cmds.rowLayout( "executablePathRowLayout", numberOfColumns = 2, adjustableColumn = 1, columnAlign2 = ["center", "center"], columnWidth = [2, 25], columnAttach = [( 1, "both", horizontalSpacing ), ( 2, "both", horizontalSpacing )] )
	cmds.textField( "sIBL_ExecutablePath_TextField", cc = "sIBL_GUI_For_Maya.sIBL_ExecutablePathTextField_OnEdit()" )
	cmds.button( "fileBrowser_Button", label = "...", al = "center", command = "sIBL_GUI_For_Maya.executableFileBrowser()" )
	cmds.setParent( upLevel = True )
	cmds.setParent( upLevel = True )

	sIBL_GUI_Executable_Path = cmds.optionVar( q = "sIBL_GUI_Executable_Path" )
	if sIBL_GUI_Executable_Path != 0:
		cmds.textField( "sIBL_ExecutablePath_TextField", edit = True, text = sIBL_GUI_Executable_Path )

	cmds.frameLayout( label = "sIBL_GUI Command Port", labelAlign = "center", cll = False, li = 4, borderStyle = "etchedOut", mh = 4, mw = 4 )
	cmds.rowLayout( "commandPortRowLayout", numberOfColumns = 3, adjustableColumn = 2, columnAlign3 = ["center", "center", "center"], columnAttach = [( 1, "both", horizontalSpacing ), ( 2, "both", horizontalSpacing ), ( 3, "both", horizontalSpacing )] )
	cmds.intField( "sIBL_CommandPort_IntField", minValue = 0, maxValue = 65535, value = 2048, cc = "sIBL_GUI_For_Maya.sIBL_CommandPortIntField_OnEdit()" )
	cmds.intSlider( "sIBL_CommandPort_IntSlider", min = 0, max = 65535 , value = cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) , step = 1, cc = "sIBL_GUI_For_Maya.sIBL_CommandPortIntSlider_OnEdit()" )
	cmds.button( "commandPort_Button", label = "Open Port", al = "center", command = "sIBL_GUI_For_Maya.openCommandPort()" )
	cmds.setParent( upLevel = True )
	cmds.setParent( upLevel = True )

	cmds.frameLayout( label = "Online", labelAlign = "center", cll = False, li = 4, borderStyle = "etchedOut", mh = 4, mw = 4 )
	cmds.rowLayout( "onlineRowLayout", numberOfColumns = 3, adjustableColumn = 3, columnAlign3 = ["center", "center", "center"], columnAttach = [( 1, "both", horizontalSpacing ), ( 2, "both", horizontalSpacing ), ( 3, "both", horizontalSpacing )] )
	cmds.button( "getApplication_Button", label = "Get sIBL_GUI", al = "center", command = "sIBL_GUI_For_Maya.getApplication_Button_OnClicked()" )
	cmds.button( "hdrlabs_Button", label = "Visit HDRLabs", al = "center", command = "sIBL_GUI_For_Maya.hdrlabs_Button_OnClicked()" )
	cmds.button( "applicationThread_Button", label = "Visit sIBL_GUI Thread", al = "right", command = "sIBL_GUI_For_Maya.applicationThread_Button_OnClicked()" )
	cmds.setParent( upLevel = True )
	cmds.setParent( upLevel = True )

	sIBL_GUI_Command_Port = int( cmds.optionVar( q = "sIBL_GUI_Command_Port" ) )
	if sIBL_GUI_Command_Port != 0:
		cmds.intField( "sIBL_CommandPort_IntField", edit = True, value = sIBL_GUI_Command_Port )

	cmds.showWindow( "sIBL_GUI_For_Maya_Window" )
	cmds.windowPref( enableAll = True )

def launchApplication():
	"""
	This Definition Launchs sIBL_GUI.
	"""

	sIBL_GUI_Executable_Path = cmds.optionVar( q = "sIBL_GUI_Executable_Path" )
	if sIBL_GUI_Executable_Path != 0:
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			os.system( "start /D" + "\"" + os.path.dirname( sIBL_GUI_Executable_Path ) + "\"" + " " + sIBL_GUI_Executable_Path.replace( " ", "\" \"" ) )
		elif platform.system() == "Darwin":
			os.system( "open -a " + sIBL_GUI_Executable_Path )
		elif platform.system() == "Linux":
			os.system( "\"" + sIBL_GUI_Executable_Path + "\" &" )
	else:
		mel.eval( "warning( \"sIBL_GUI | No sIBL_GUI Executable Path Defined!\" );" )

def executeLoaderScript():
	"""
	This Definition Executes sIBL_GUI Maya Loader Script.
	"""

	systemApplicationDataDirectory = getSystemApplicationDataDirectory()

	if systemApplicationDataDirectory:
		loaderScript = os.path.normpath( os.path.join( systemApplicationDataDirectory, LOADER_SCRIPTS_DIRECTORY, LOADER_SCRIPT ) )

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			loaderScript = loaderScript.replace( "\\", "\\\\" )

		if os.path.exists( loaderScript ):
			mel.eval( "source \"" + loaderScript + "\"" )
		else:
			mel.eval( "warning( \"sIBL_GUI | No Maya Loader Script Found!\" );" )

def deleteSmartIblNodes():
	"""
	This Definition Deletes Smart Ibl And Lightsmith Lights Nodes.
	"""

	nodes = []
	selection = cmds.ls(sl = True, l = True)
	if selection:
		prefixes = []
		for node in selection:
			relatives = [node]
			relatives.extend(cmds.listRelatives(node, f = True, ad = True))
			for relative in relatives:
				if re.search(r"\w*_Root$", relative):
					if relative.replace("_Root", "_Support").split("|")[-1] in cmds.listRelatives(relative, ad = True):
						prefixes.append(relative.replace("_Root", "").split("|")[-1])
		for prefix in prefixes:
			userChoice = cmds.confirmDialog(title="sIBL_GUI", message="Nodes With Following Prefix : '%s' Are Planned For Deletion! Would You Like To Proceed?" % prefix, button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
			if userChoice == "Yes":
				nodes.extend(sorted(cmds.ls(prefix + "*", l = True)))
	else:
		userChoice = cmds.confirmDialog(title="sIBL_GUI", message="Smart Ibl Nodes Are Planned For Deletion! Would You Like To Proceed?", button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
		if userChoice == "Yes":
			nodes.extend(sorted(cmds.ls("sIBL*", l = True)))

	for node in nodes:
		if cmds.objExists(node):
			print("sIBL_GUI | Deleting Node: '%s'!" % node)
			cmds.delete(node)
