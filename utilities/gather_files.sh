#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI For Maya - Files Gathering
echo ----------------------------------------------------------------

export PROJECT_DIRECTORY=$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)

export SOURCE_DIRECTORY=$PROJECT_DIRECTORY/src/
export RELEASES_DIRECTORY=$PROJECT_DIRECTORY/releases/
export BUILD_DIRECTORY=$RELEASES_DIRECTORY/build
export REPOSITORY_DIRECTORY=$RELEASES_DIRECTORY/repository
export UTILITIES_DIRECTORY=$PROJECT_DIRECTORY/utilities

#! Gathering folder cleanup.
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - Begin
echo ----------------------------------------------------------------
rm -rf $BUILD_DIRECTORY
rm -rf $REPOSITORY_DIRECTORY/*
echo ----------------------------------------------------------------
echo Gathering Folder Cleanup - End
echo ----------------------------------------------------------------

#! Extra files cleanup.
echo ----------------------------------------------------------------
echo Extra Files Cleanup - Begin
echo ----------------------------------------------------------------
python $UTILITIES_DIRECTORY/recursiveRemove.py ./ .DS_Store
echo ----------------------------------------------------------------
echo Extra Files Cleanup - End
echo ----------------------------------------------------------------

#! Change log gathering.
echo ----------------------------------------------------------------
echo Change Log Gathering - Begin
echo ----------------------------------------------------------------
cp $RELEASES_DIRECTORY/Change_Log.html $REPOSITORY_DIRECTORY/
echo ----------------------------------------------------------------
echo Change Log Gathering - End
echo ----------------------------------------------------------------

echo ----------------------------------------------------------------
echo Files Gathering - Begin
echo ----------------------------------------------------------------
mkdir -p $BUILD_DIRECTORY/prefs/icons
mkdir -p $BUILD_DIRECTORY/prefs/shelves
mkdir $BUILD_DIRECTORY/scripts
cp $PROJECT_DIRECTORY/README $BUILD_DIRECTORY/
cp $SOURCE_DIRECTORY/prefs/icons/*.png $BUILD_DIRECTORY/prefs/icons/
cp $SOURCE_DIRECTORY/prefs/shelves/shelf_sIBL_GUI.mel $BUILD_DIRECTORY/prefs/shelves/shelf_sIBL_GUI.mel
cp $SOURCE_DIRECTORY/scripts/sIBL_GUI_For_Maya.py $BUILD_DIRECTORY/scripts/sIBL_GUI_For_Maya.py
cd $BUILD_DIRECTORY/
zip -r $REPOSITORY_DIRECTORY/sIBL_GUI_For_Maya.zip .
echo ----------------------------------------------------------------
echo Files Gathering - End
echo ----------------------------------------------------------------