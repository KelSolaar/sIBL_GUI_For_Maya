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
***		Maya sIBL_GUI Helper Script For Maya 2011 And Higher.
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
	except :
		mel.eval( "warning( \"sIBL_GUI | Command Port Is Already Open Or Can't Be Opened !\" );" )

	storeCommandPortOptionVar()

def executableFileBrowser():
	'''
	This Definition Provides A Browser.
	'''

	fileName = cmds.fileDialog2( ds = 2, fileFilter = "All Files (*.*)", fm = 1 )
	fileName = fileName and fileName[0] or None

	if fileName :
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

def sIBL_GUI_For_Maya_Preferences():
	'''
	This Definition Launchs sIBL_GUI For Maya Preferences.
	'''

	cmds.windowPref( enableAll = False )

	if ( cmds.window( "sIBL_GUI_For_Maya_Windows", exists = True ) ):
		cmds.deleteUI( "sIBL_GUI_For_Maya_Windows" )

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		height = 120
	elif platform.system() == "Darwin":
		height = 132
	elif platform.system() == "Linux":
		height = 130

	cmds.window( "sIBL_GUI_For_Maya_Windows",
		title = "sIBL_GUI For Maya Preferences",
		width = 315,
		height = height,
		sizeable = False,
		toolbox = True )

	cmds.columnLayout( adjustableColumn = True )
	cmds.frameLayout( label = "sIBL_GUI Executable Path", cll = False, li = 4, borderStyle = "etchedOut", mh = 4, mw = 4 )
	cmds.rowColumnLayout( "executablePathRowLayout", numberOfColumns = 2, cw = ( ( 1, 256 ), ( 2, 32 ) ), cs = ( ( 2, 8 ) ) )
	cmds.textField( "sIBL_ExecutablePath_TextField", cc = "sIBL_GUI_For_Maya.sIBL_ExecutablePathTextField_OnEdit()" )
	cmds.button( "fileBrowser_Button", label = "...", al = "center", command = "sIBL_GUI_For_Maya.executableFileBrowser()" )
	cmds.setParent( upLevel = True )
	cmds.setParent( upLevel = True )

	sIBL_GUI_Executable_Path = cmds.optionVar( q = "sIBL_GUI_Executable_Path" )
	if sIBL_GUI_Executable_Path != 0:
		cmds.textField( "sIBL_ExecutablePath_TextField", edit = True, text = sIBL_GUI_Executable_Path )

	cmds.frameLayout( label = "sIBL_GUI Command Port", cll = False, li = 4, borderStyle = "etchedOut", mh = 4, mw = 4 )
	cmds.rowColumnLayout( "commandPortRowLayout", numberOfColumns = 3, cw = ( ( 1, 40 ), ( 2, 140 ) ), cs = ( ( 2, 8 ), ( 3, 8 ) ) )
	cmds.intField( "sIBL_CommandPort_IntField", minValue = 0, maxValue = 65535, value = 2048, cc = "sIBL_GUI_For_Maya.sIBL_CommandPortIntField_OnEdit()" )
	cmds.intSlider( "sIBL_CommandPort_IntSlider", min = 0, max = 65535 , value = cmds.intField( "sIBL_CommandPort_IntField", query = True, value = True ) , step = 1, cc = "sIBL_GUI_For_Maya.sIBL_CommandPortIntSlider_OnEdit()" )
	cmds.button( "commandPort_Button", label = "Open Port", al = "center", command = "sIBL_GUI_For_Maya.openCommandPort()" )
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
