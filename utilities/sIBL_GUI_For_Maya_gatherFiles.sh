#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI For Maya - Files Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./releases/classic/*
rm -rf ./releases/qt/*
rm -rf ./releases/repository/*

#! Classic Gathering.
mkdir -p ./releases/classic/prefs/icons
mkdir -p ./releases/classic/prefs/shelves
mkdir ./releases/classic/scripts
cp ./README ./releases/classic/
cp ./src/prefs/icons/*.xpm ./releases/classic/prefs/icons/
cp ./src/prefs/shelves/shelf_sIBL_GUI.mel ./releases/classic/prefs/shelves/
cp ./src/scripts/sIBL_GUI_For_Maya.py ./releases/classic/scripts/
cd ./releases/classic/
zip ../repository/sIBL_GUI_For_Maya.zip README prefs/shelves/* prefs/icons/* scripts/*

#! Reaching Original Directory.
cd ../../

#! Classic Gathering.
mkdir -p ./releases/qt/prefs/icons
mkdir -p ./releases/qt/prefs/shelves
mkdir ./releases/qt/scripts
cp ./README ./releases/qt/
cp ./src/prefs/icons/*.png ./releases/qt/prefs/icons/
cp ./src/prefs/shelves/shelf_sIBL_GUI_Qt.mel ./releases/qt/prefs/shelves/shelf_sIBL_GUI.mel
cp ./src/scripts/sIBL_GUI_For_Maya_Qt.py ./releases/qt/scripts/sIBL_GUI_For_Maya.py
cd ./releases/qt/
zip ../repository/sIBL_GUI_For_Maya_Qt.zip README prefs/shelves/* prefs/icons/* scripts/*
