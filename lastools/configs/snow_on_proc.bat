
:: _____DIRECTORY CONFIG_____

:: folder containing batch files
SET DIR_BAT=C:\Users\Cob\index\educational\usask\research\masters\repos\upper-clearing-lidar\lastools
:: folder containing lastools and license
SET DIR_LASTOOLS=C:\Users\Cob\index\educational\usask\research\masters\code_lib\lastools\LAStools\bin;
:: folder containing site polygons
SET SITE_MASK=C:\Users\Cob\index\educational\usask\research\masters\data\LiDAR\site_library\50_site_poly.shp


:: _____PARAMETER CONFIG_____
:: PROJECTION
SET EPSG=32611
SET GRID_ORIGIN=628004 5646470

:: CLASSES
SET CLASS_GROUND=2
SET CLASS_VEGETATION=5
SET CLASS_NOISE=7


:: _____PROJECT CONFIG_____
SET DATE_LIST=19_045 19_050 19_052 19_107 19_123

for %%d in (%DATE_LIST%) do (

	SET PRODUCT_ID=%%d_snow_on
	:: folder in which temp and output files will be saved to
	SET DIR_WORKING=C:\Users\Cob\index\educational\usask\research\masters\data\LiDAR\%%d
	SET FILE_IN=C:\Users\Cob\index\educational\usask\research\masters\data\LiDAR\%%d\%%d_all_WGS84_utm11N.las

	:: _____SET UP [0]_____
	call %DIR_BAT%\las_00_dir_setup.bat


	:: _____QUALIT CONTROL [1]_____
	SET ORIGINAL_SCALE_FACTOR=0.00025
	SET NUM_CORES=4
	SET TILE_SIZE=25
	SET TILE_BUFFER=5

	::call %DIR_BAT%\las_01_quality_control.bat


	:: _____CLASSIFICATION [2]_____
	SET NOISE_ISOLATION=10
	SET NOISE_STEP=1

	:: optimized for snow-on DEM
	SET GROUND_STEP=1.0
	SET GROUND_OFFSET=.03

	::call %DIR_BAT%\las_02_classification.bat


	:: _____DEM [3]_____
	SET DEM_RESOLUTION=.04
	SET DEM_THIN_RESOLUTION=.02
	SET DEM_MAX_TIN_EDGE=.12
	call %DIR_BAT%\las_03_dem.bat

	SET DEM_RESOLUTION=.10
	SET DEM_THIN_RESOLUTION=.05
	SET DEM_MAX_TIN_EDGE=.30
	call %DIR_BAT%\las_03_dem.bat

	SET DEM_RESOLUTION=.25
	SET DEM_THIN_RESOLUTION=.125
	SET DEM_MAX_TIN_EDGE=.75
	call %DIR_BAT%\las_03_dem.bat

	SET DEM_RESOLUTION=.50
	SET DEM_THIN_RESOLUTION=.25
	SET DEM_MAX_TIN_EDGE=1.50
	call %DIR_BAT%\las_03_dem.bat

	SET DEM_RESOLUTION=1.00
	SET DEM_THIN_RESOLUTION=.50
	SET DEM_MAX_TIN_EDGE=3.00
	call %DIR_BAT%\las_03_dem.bat
)
::
:::: _____CANOPY [4]_____
::SET NOISE_HEIGHT_THRESHOLD_LOW=-1
::SET NOISE_HEIGHT_THRESHOLD_HIGH=35
::SET VEGETATION_HEIGHT_THRESHOLD_LOW=2
::SET CHM_RESOLUTION=.25
::SET CHM_MAX_TIN_EDGE=.75
::SET CHM_LAYER_LIST= 0 2 5 10 15 20 25
::
::call %DIR_BAT%\las_04_canopy.bat
::
::
:::: _____COMPILE [5]_____
::