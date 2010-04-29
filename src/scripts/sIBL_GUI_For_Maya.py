#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	sIBL_GUI_For_Maya.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Maya sIBL_GUI Helper Script.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os
import maya.cmds as cmds
import maya.mel as mel
import platform

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOADER_SCRIPTS_DIRECTORY = "HDRLabs/sIBL_GUI/io/loaderScripts/"
LOADER_SCRIPT = "sIBL_Maya_Import.mel"
HDRLABS_URL = "http://www.hdrlabs.com"
WINDOWS_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Windows"
DARWIN_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Darwin"
LINUX_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Linux"
APPLICATION_THREAD_URL = "http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371"

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Environment( object ):
	'''
	This Class Provides Methods To Manipulate Environment Variables.
	'''

	def __init__( self, variable = None ):
		'''
		This Method Initializes The Class.

		@param variable: Variable To Manipulate. ( String )
		'''

		# --- Setting Class Attributes. ---
		self._variable = variable

	def getPath( self ):
		'''
		This Method Gets The Chosen Environment Variable Path As A String.

		@return: Variable Path. ( String )
		'''

		if self._variable :
			for param in os.environ.keys():
				if( self._variable == param ): return os.environ[param]

def getSystemApplicationDatasDirectory():
	'''
	This Definition Gets The User Application Datas Directory.

	@return: User Application Datas Directory. ( String )
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft" :
		environmentVariable = Environment( "APPDATA" )
		return environmentVariable.getPath()

	elif platform.system() == "Darwin" :
		environmentVariable = Environment( "HOME" )
		return os.path.join( environmentVariable.getPath(), "Library/Preferences" )

	elif platform.system() == "Linux" :
		environmentVariable = Environment( "HOME" )
		return environmentVariable.getPath()

def storeCommandPortOptionVar():
	'''
	This Definition Stores The Command Port In An Option Var.
	'''

	cmds.optionVar( iv = ( "sIBL_GUI_Command_Port", cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )

def storeExecutablePathOptionVar():
	'''
	This Definition Stores sIBL_GUI Executable Path In An Option Var.
	'''

	cmds.optionVar( sv = ( "sIBL_GUI_Executable_Path", cmds.textField( "sIBL_ExecutablePath_TextField", query = True, text = True ) ) )

def openCommandPort():
	'''
	This Definition Opens The Command Port.
	'''

	try:
		cmds.commandPort( name = "127.0.0.1:" + str( cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )
		cmds.commandPort( name = ":" + str( cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) ) )
	except :
		mel.eval( "warning( \"sIBL_GUI | Command Port Is Already Open Or Can't Be Opened !\" );" )

	storeCommandPortOptionVar()

def executableFileBrowser():
	'''
	This Definition Provides A Browser.
	'''

	filePath = cmds.fileBrowserDialog( m = 0, fc = getExecutablePath, ft = '', an = 'Ok', om = 'Choose sIBL_GUI Executable' )

def getExecutablePath( fileName, fileType ):
	'''
	This Definition Gets sIBL_GUI Executable Path.

	@param fileName: File Name. ( String )
	@param fileType: File Type. ( String )
	'''

	if fileName.endswith( "sIBL_GUI" ) or fileName.endswith( "sIBL_GUI.exe" ) :
		cmds.textField( "sIBL_ExecutablePath_TextField", edit = True, text = fileName )
		storeExecutablePathOptionVar()
	else:
		mel.eval( "warning( \"sIBL_GUI | Chosen Executable Path Is Invalid !\" );" )

def sIBL_CommandPortIntSlider_OnEdit():
	'''
	This Definition Is Triggered By sIBL_CommandPortIntSlider Edit.
	'''

	cmds.intField( "sIBL_CommandPort_IntField", edit = True, value = cmds.intSlider( "sIBL_CommandPort_IntSlider", query = True, value = True ) )

	storeCommandPortOptionVar()

def sIBL_CommandPortIntField_OnEdit():
	'''
	This Definition Is Triggered By sIBL_CommandPortIntField Edit.
	'''

	cmds.intSlider( "sIBL_CommandPort_IntSlider", edit = True, value = cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) )

	storeCommandPortOptionVar()

def sIBL_ExecutablePathTextField_OnEdit():
	'''
	This Definition Is Triggered By sIBL_ExecutablePathTextField Edit.
	'''

	textFieldContent = cmds.textField( "sIBL_ExecutablePath_TextField", query = True, text = True )
	if textFieldContent.endswith( "sIBL_GUI" ) or textFieldContent.endswith( "sIBL_GUI.exe" ) :
		storeExecutablePathOptionVar()
	else:
		mel.eval( "warning( \"sIBL_GUI | Chosen Executable Path Is Invalid !\" );" )

def openUrl( url ) :
	'''
	This Definition Opens HDRLabs Thread.

	@param url: Url To Open. ( String )
	'''
	cmds.launch( web = url )

def getApplication_Button_OnClicked() :
	'''
	This Definition Opens Online Repository.
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		url = WINDOWS_RELEASE_URL
	elif platform.system() == "Darwin":
		url = DARWIN_RELEASE_URL
	elif platform.system() == "Linux":
		url = LINUX_RELEASE_URL

	openUrl( url )

def hdrlabs_Button_OnClicked():
	'''
	This Definition Opens HDRLabs Thread.
	'''

	openUrl( HDRLABS_URL )

def applicationThread_Button_OnClicked() :
	'''
	This Definition Opens sIBL_GUI Thread.
	'''

	openUrl( APPLICATION_THREAD_URL )

def sIBL_GUI_For_Maya_Preferences():
	'''
	This Definition Launchs sIBL_GUI For Maya Preferences.
	'''

	cmds.windowPref( enableAll = False )

	if ( cmds.window( "sIBL_GUI_For_Maya_Windows", exists = True ) ):
		cmds.deleteUI( "sIBL_GUI_For_Maya_Windows" )

	cmds.window( "sIBL_GUI_For_Maya_Windows",
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

	cmds.showWindow( "sIBL_GUI_For_Maya_Windows" )
	cmds.windowPref( enableAll = True )

def sIBL_GUI_For_Maya_Launch():
	'''
	This Definition Launchs sIBL_GUI.
	'''

	sIBL_GUI_Executable_Path = cmds.optionVar( q = "sIBL_GUI_Executable_Path" )
	if sIBL_GUI_Executable_Path != 0:
		if platform.system() == "Windows":
			os.system( "start /D" + "\"" + os.path.dirname( sIBL_GUI_Executable_Path ) + "\"" + " " + sIBL_GUI_Executable_Path.replace( " ", "\" \"" ) )
		else :
			os.system( "\"" + sIBL_GUI_Executable_Path + "\" &" )
	else:
		mel.eval( "warning( \"sIBL_GUI | No sIBL_GUI Executable Path Defined !\" );" )

def sIBL_GUI_ExecuteLoaderScript():
	'''
	This Definition Executes sIBL_GUI Maya Loader Script.
	'''

	systemApplicationDatasDirectory = getSystemApplicationDatasDirectory()

	if systemApplicationDatasDirectory :
		loaderScript = os.path.normpath( os.path.join( systemApplicationDatasDirectory, LOADER_SCRIPTS_DIRECTORY, LOADER_SCRIPT ) )

		if platform.system() == "Windows" or platform.system() == "Microsoft" :
			loaderScript = loaderScript.replace( "\\", "\\\\" )

		if os.path.exists( loaderScript ) :
			mel.eval( "source \"" + loaderScript + "\"" )
		else:
			mel.eval( "warning( \"sIBL_GUI | No Maya Loader Script Found !\" );" )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
