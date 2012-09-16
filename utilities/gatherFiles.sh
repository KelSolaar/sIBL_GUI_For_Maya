#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI For Maya - Files Gathering
echo ----------------------------------------------------------------

export UTILITIES=/Users/KelSolaar/Documents/Development/sIBL_GUI/utilities
export PROJECT=/Users/KelSolaar/Documents/Development/sIBL_GUI_For_Maya

export SOURCE=$PROJECT/src/
export RELEASES=$PROJECT/releases/
export BUILD=$RELEASES/build
export REPOSITORY=$RELEASES/repository

#! Gathering folder cleanup.
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD
rm -rf $REPOSITORY/*
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - End
echo ----------------------------------------------------------------

#! Extra files cleanup.
echo ----------------------------------------------------------------
echo Extra Files Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES/recursiveRemove.py ./ .DS_Store
echo ----------------------------------------------------------------
echo Extra Files Cleanup - End
echo ----------------------------------------------------------------

#! Change log gathering.
echo ----------------------------------------------------------------
echo Change Log Gathering - Begin
echo ----------------------------------------------------------------
cp $RELEASES/Change_Log.html $REPOSITORY/
echo ----------------------------------------------------------------
echo Change Log Gathering - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Files Gathering - Begin
echo ----------------------------------------------------------------
mkdir -p $BUILD/prefs/icons
mkdir -p $BUILD/prefs/shelves
mkdir $BUILD/scripts
cp $PROJECT/README $BUILD/
cp $SOURCE/prefs/icons/*.png $BUILD/prefs/icons/
cp $SOURCE/prefs/shelves/shelf_sIBL_GUI.mel $BUILD/prefs/shelves/shelf_sIBL_GUI.mel
cp $SOURCE/scripts/sIBL_GUI_For_Maya.py $BUILD/scripts/sIBL_GUI_For_Maya.py
cd $BUILD/
zip -r $REPOSITORY/sIBL_GUI_For_Maya.zip .
echo ----------------------------------------------------------------
echo Files Gathering - End
echo ----------------------------------------------------------------