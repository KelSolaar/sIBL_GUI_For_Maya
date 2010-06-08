#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI For Maya - Files Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf ./releases/classic/*
rm -rf ./releases/qt/*
rm -rf ./releases/repository/*
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - End
echo ----------------------------------------------------------------

#! Extra Files Cleanup.
echo ----------------------------------------------------------------
echo Extra Files Cleanup - Begin
echo ----------------------------------------------------------------
python ../sIBL_GUI/utilities/sIBL_GUI_recursiveRemove.py ./ .DS_Store
echo ----------------------------------------------------------------
echo Extra Files Cleanup - End
echo ----------------------------------------------------------------

#! Change Log Gathering.
echo ----------------------------------------------------------------
echo Change Log Gathering - Begin
echo ----------------------------------------------------------------
cp ./releases/Change\ Log.html ./releases/repository/
echo ----------------------------------------------------------------
echo Change Log Gathering - End
echo ----------------------------------------------------------------

#! Classic Gathering.
echo ----------------------------------------------------------------
echo Classic Gathering - Begin
echo ----------------------------------------------------------------
mkdir -p ./releases/classic/prefs/icons
mkdir -p ./releases/classic/prefs/shelves
mkdir ./releases/classic/scripts
cp ./README ./releases/classic/
cp ./src/prefs/icons/*.xpm ./releases/classic/prefs/icons/
cp ./src/prefs/shelves/shelf_sIBL_GUI.mel ./releases/classic/prefs/shelves/
cp ./src/scripts/sIBL_GUI_For_Maya.py ./releases/classic/scripts/
cd ./releases/classic/
zip -r ../repository/sIBL_GUI_For_Maya.zip .
echo ----------------------------------------------------------------
echo Classic Gathering - End
echo ----------------------------------------------------------------

#! Reaching Original Directory.
cd ../../

echo ----------------------------------------------------------------
echo Qt Gathering - Begin
echo ----------------------------------------------------------------
#! Qt Gathering.
mkdir -p ./releases/qt/prefs/icons
mkdir -p ./releases/qt/prefs/shelves
mkdir ./releases/qt/scripts
cp ./README ./releases/qt/
cp ./src/prefs/icons/*.png ./releases/qt/prefs/icons/
cp ./src/prefs/shelves/shelf_sIBL_GUI_Qt.mel ./releases/qt/prefs/shelves/shelf_sIBL_GUI.mel
cp ./src/scripts/sIBL_GUI_For_Maya_Qt.py ./releases/qt/scripts/sIBL_GUI_For_Maya.py
cd ./releases/qt/
zip -r ../repository/sIBL_GUI_For_Maya_Qt.zip .
echo ----------------------------------------------------------------
echo Qt Gathering - End
echo ----------------------------------------------------------------