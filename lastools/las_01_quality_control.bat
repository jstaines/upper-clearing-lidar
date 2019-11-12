:: las_01_quality_control.bat
:: dependencies
     :: DIR_WORKING
     :: DIR_LASTOOLS
     :: DIR_SITE_LIBRARY
     :: PRODUCT_ID
     :: FILE_IN
     :: ORIGINAL_SCALE_FACTOR
     :: NUM_CORES
     :: TILE_SIZE
     :: TILE_BUFFER


:: include LAStools in PATH to allow running script from here
set PATH=%PATH%;%DIR_LASTOOLS%

:: initial setup
pushd %DIR_WORKING%

:: make product folder
mkdir .\%PRODUCT_ID%
cd %PRODUCT_ID%

:: make temp folder
mkdir .\TEMP_FILES


:: make output folders
cd TEMP_FILES
mkdir .\01_precision
mkdir .\02_clip
mkdir .\03_tile
mkdir .\04_duplicate
cd ..

:: ----------PROTOCOL----------

:: should check each file prior to rescaling to verify actual precision
lasprecision -i %FILE_IN% ^
          -rescale %ORIGINAL_SCALE_FACTOR% %ORIGINAL_SCALE_FACTOR% %ORIGINAL_SCALE_FACTOR% ^
          -odir TEMP_FILES\01_precision\ -o %PRODUCT_ID%_01.laz

:: clip las by shpfile
lasclip -i TEMP_FILES\01_precision\%PRODUCT_ID%_01.laz ^
          -poly C:\Users\Cob\index\educational\usask\research\masters\data\LiDAR\site_library\site_poly.shp ^
          -odir TEMP_FILES\02_clip\ -ocut 3 -odix _02 -olaz

:: tile las for memory management
lastile -i TEMP_FILES\02_clip\%PRODUCT_ID%_02.laz ^
          -set_classification 0 -set_user_data 0 ^
          -tile_size %TILE_SIZE% -buffer %TILE_BUFFER% ^
          -odir TEMP_FILES\03_tile\ -o %PRODUCT_ID%.laz

:: remove xyz duplicate points
lasduplicate -i TEMP_FILES\03_tile\*.laz ^
                -unique_xyz ^
                -cores %NUM_CORES% ^
                -odir TEMP_FILES\04_duplicate\ -olaz -odix _04