#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**sIBL_GUI_For_Maya.py

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Maya sIBL_GUI Helper Script for Maya 2011 and higher.

**Others:**

"""

import maya.cmds as cmds
import maya.mel as mel
import os
import platform
import re
import sys

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["HDRLABS_URL",
           "WINDOWS_RELEASE_URL",
           "DARWIN_RELEASE_URL",
           "LINUX_RELEASE_URL",
           "APPLICATION_THREAD_URL",
           "open_preferences",
           "launch_application",
           "execute_loader_script",
           "delete_smart_ibl_nodes"]

HDRLABS_URL = "http://www.hdrlabs.com"
WINDOWS_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Windows"
DARWIN_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Darwin"
LINUX_RELEASE_URL = "http://kelsolaar.hdrlabs.com/?dir=./sIBL_GUI/Repository/Builds/Linux"
APPLICATION_THREAD_URL = "http://www.hdrlabs.com/cgi-bin/forum/YaBB.pl?num=1271609371"


class Environment(object):
    """
    Defines methods to manipulate environment variables.
    """

    def __init__(self, variable=None):
        """
        Initializes the class.

        :param variable: Variable to manipulate.
        :type variable: str
        """

        self._variable = variable

    def get_value(self):
        """
        Returns given environment variable value.

        :return: Variable value.
        :rtype: str
        """

        if self._variable:
            return os.environ.get(self._variable)


def _set_executable_path_option_var():
    """
    Sets **executablePath** optionVar.
    """

    _set_option_var("sIBL_GUI_executablePath", cmds.textField("Executable_Path_textField", query=True, text=True))


def _set_loader_script_path_option_var():
    """
    Sets **sIBL_GUI_loader_script_path** optionVar.
    """

    _set_option_var("sIBL_GUI_loader_script_path", cmds.textField(
        "Loader_Script_Path_textField", query=True, text=True))


def _set_command_port_option_var():
    """
    Sets **sIBL_GUI_commandPort** optionVar.
    """

    _set_option_var("sIBL_GUI_commandPort", cmds.intSliderGrp("Command_Port_intSliderGrp", query=True, value=True))


def _set_option_var(name, value):
    """
    Stores given optionVar with given value.

    :param name: OptionVar name.
    :type name: str
    :param value: OptionVar value.
    :type value: object
    """

    cmds.optionVar(sv=(name, value))


def _open_url(url):
    """
    Opens given url.

    :param url: Url to open.
    :type url: str
    """

    cmds.launch(web=url)


def _Executable_Path_button__command(state=None):
    """
    Defines the callback triggered by **Executable_Path_button** widget.

    :param state: Button state.
    :type state: bool
    """

    file_name = cmds.fileDialog2(ds=2, fileFilter="All Files (*.*)", fm=(not platform.system() == "Darwin" and 1 or 3))
    file_name = file_name and file_name[0] or None
    if not file_name:
        return

    if file_name.endswith("sIBL_GUI.exe") or re.search("sIBL_GUI[\d ]*\.app", file_name) or file_name.endswith(
            "sIBL_GUI"):
        cmds.textField("Executable_Path_textField", edit=True, text=file_name)
        _set_executable_path_option_var()
    else:
        mel.eval("warning(\"sIBL_GUI | Chosen executable path is invalid!\");")


def _Executable_Path_textField__changeCommand(value):
    """
    Defines the callback triggered by **Executable_Path_textField** widget.

    :param value: Value.
    :type value: str
    """

    if os.path.exists(value) and \
            (value.endswith("sIBL_GUI.exe") or
                 value.endswith("sIBL_GUI.app") or
                 value.endswith("sIBL_GUI")):
        _set_executable_path_option_var()
    else:
        mel.eval("warning(\"sIBL_GUI | Chosen executable path is invalid!\");")


def _Loader_Script_Path_button__command(state=None):
    """
    Defines the callback triggered by **Loader_Script_Path_button** widget.

    :param state: Button state.
    :type state: bool
    """

    file_name = cmds.fileDialog2(ds=2, fileFilter="All Files (*.*)", fm=4)
    file_name = file_name and file_name[0] or None
    if not file_name:
        return

    cmds.textField("Loader_Script_Path_textField", edit=True, text=file_name)
    _set_loader_script_path_option_var()


def _Loader_Script_Path_textField__changeCommand(value):
    """
    Defines the callback triggered by **_Loader_Script_Path_textField** widget.

    :param value: Value.
    :type value: str
    """

    if os.path.exists(value):
        _set_loader_script_path_option_var()
    else:
        mel.eval("warning(\"sIBL_GUI | Chosen Loader Script path is invalid!\");")


def _Command_Port_intSliderGrp__changeCommand(value):
    """
    Defines the callback triggered by **Command_Port_intSliderGrp** widget.

    :param value: Value.
    :type value: float
    """

    _set_command_port_option_var()


def _Command_Port_button__command(state=None):
    """
    Opens the command port.

    :param state: Button state.
    :type state: bool
    """

    try:
        cmds.commandPort(
            name="127.0.0.1:" + str(cmds.intSliderGrp("Command_Port_intSliderGrp", query=True, value=True)))
    except:
        mel.eval("warning(\"sIBL_GUI | Command port is already open or can't be opened!\");")

    _set_command_port_option_var()


def _Get_Application_button__command(state=None):
    """
    Opens Online Repository.

    :param state: Button state.
    :type state: bool
    """

    if platform.system() == "Windows" or platform.system() == "Microsoft":
        url = WINDOWS_RELEASE_URL
    elif platform.system() == "Darwin":
        url = DARWIN_RELEASE_URL
    elif platform.system() == "Linux":
        url = LINUX_RELEASE_URL

    _open_url(url)


def _HDRlabs_button__command(state=None):
    """
    Opens HDRLabs thread.

    :param state: Button state.
    :type state: bool
    """

    _open_url(HDRLABS_URL)


def _Application_Thread_button__command(state=None):
    """
    Opens sIBL_GUI thread.

    :param state: Button state.
    :type state: bool
    """

    _open_url(APPLICATION_THREAD_URL)


def _sIBL_GUI_For_Maya_window():
    """
    Launches **sIBL_GUI For Maya Preferences** window.
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
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[
        (1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
    cmds.textField("Executable_Path_textField", cc=_Executable_Path_textField__changeCommand)
    cmds.button("Executable_Path_button", label="...", al="center", command=_Executable_Path_button__command)
    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    executablePath = cmds.optionVar(q="sIBL_GUI_executablePath")
    if executablePath:
        cmds.textField("Executable_Path_textField", edit=True, text=executablePath)

    cmds.frameLayout(label="Loader Script Path", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[
        (1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
    cmds.textField("Loader_Script_Path_textField", cc=_Loader_Script_Path_textField__changeCommand)
    cmds.button("Loader_Script_Path_button", label="...", al="center", command=_Loader_Script_Path_button__command)
    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    sIBL_GUI_loader_script_path = cmds.optionVar(q="sIBL_GUI_loader_script_path")
    if sIBL_GUI_loader_script_path:
        cmds.textField("Loader_Script_Path_textField", edit=True, text=sIBL_GUI_loader_script_path)

    cmds.frameLayout(label="Command Port", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign2=["center", "center"], columnAttach=[
        (1, "both", horizontalSpacing), (2, "both", horizontalSpacing)])
    cmds.intSliderGrp("Command_Port_intSliderGrp", field=True, minValue=0, maxValue=65535,
                      value=2048, cc=_Command_Port_intSliderGrp__changeCommand)
    cmds.button("Command_Port_button", label="Open Port", al="center", command=_Command_Port_button__command)
    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    sIBL_GUI_commandPort = int(cmds.optionVar(q="sIBL_GUI_commandPort"))
    if sIBL_GUI_commandPort:
        cmds.intSliderGrp("Command_Port_intSliderGrp", edit=True, value=sIBL_GUI_commandPort)

    cmds.frameLayout(label="Online", cll=False, li=4, borderStyle="etchedOut", mh=4, mw=4)
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign3=["center", "center", "center"], columnAttach=[
        (1, "both", horizontalSpacing), (2, "both", horizontalSpacing), (3, "both", horizontalSpacing)])
    cmds.button("Get_Application_button", label="Get sIBL_GUI ...",
                al="center", command=_Get_Application_button__command)
    cmds.button("HDRlabs_button", label="Visit HDRLabs ...", al="center", command=_HDRlabs_button__command)
    cmds.button("Application_Thread_button", label="Visit sIBL_GUI Thread ...",
                al="right", command=_Application_Thread_button__command)
    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.showWindow("_sIBL_GUI_For_Maya_window")
    cmds.windowPref(enableAll=True)


def open_preferences():
    """
    Launches **sIBL_GUI For Maya - Preferences** window.
    """

    _sIBL_GUI_For_Maya_window()
    return True


def launch_application():
    """
    Launches **sIBL_GUI**.

    :return: Definition sucess.
    :rtype: bool
    """

    executable_path = cmds.optionVar(q="sIBL_GUI_executablePath")
    if executable_path:
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            os.system("start /D" + "\"" + os.path.dirname(executable_path) +
                      "\"" + " " + executable_path.replace(" ", "\" \""))
        elif platform.system() == "Darwin":
            os.system("open -a " + executable_path.replace(" ", "\ "))
        elif platform.system() == "Linux":
            os.system("\"" + executable_path.replace(" ", "\ ") + "\" &")
        return True
    else:
        mel.eval("warning(\"sIBL_GUI | No sIBL_GUI executable path defined!\");")
        cmds.confirmDialog(title="sIBL_GUI | Warning",
                           message="No sIBL_GUI executable path defined!\nPlease define one in preferences!", button=[
                "Ok"], defaultButton="Ok")
        open_preferences()


def execute_loader_script():
    """
    Executes **sIBL_GUI** Loader Script.

    :return: Definition sucess.
    :rtype: bool
    """

    loader_script_path = cmds.optionVar(q="sIBL_GUI_loader_script_path")
    if loader_script_path:
        if os.path.exists(loader_script_path):
            if re.search(r"\.mel$", loader_script_path):
                mel.eval("source \"" + loader_script_path + "\"")
            elif re.search(r"\.pyc?$", loader_script_path):
                path = os.path.dirname(loader_script_path)
                path not in sys.path and sys.path.append(path)
                module = os.path.splitext(os.path.basename(loader_script_path))[0]
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
        cmds.confirmDialog(title="sIBL_GUI | Warning",
                           message="No Loader Script found!\nPlease define one in preferences!", button=[
                "Ok"], defaultButton="Ok")
        open_preferences()


def delete_smart_ibl_nodes():
    """
    Deletes **Smart Ibl** and **Lightsmith** lights nodes.

    :return: Definition sucess.
    :rtype: bool
    """

    nodes = []
    selection = cmds.ls(sl=True, l=True, dag=True)
    if selection:
        prefixes = []
        for node in selection:
            relatives = [node]
            node_relatives = cmds.listRelatives(node, f=True, ad=True)
            node_relatives and relatives.extend(node_relatives)
            for relative in relatives:
                if re.search(r"\w*_Root$", relative):
                    if relative.replace("_Root", "_Support").split("|")[-1] in cmds.listRelatives(relative, ad=True):
                        prefixes.append(relative.replace("_Root", "").split("|")[-1])
        for prefix in prefixes:
            user_choice = cmds.confirmDialog(title="sIBL_GUI",
                                             message="Nodes with following prefix : '%s' are planned for deletion! Would you like to proceed?" % prefix,
                                             button=[
                                                 "Yes", "No"], defaultButton="Yes", cancelButton="No",
                                             dismissString="No")
            if user_choice == "Yes":
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
