:: las_04_canopy_raster.bat
:: dependencies
    :: CHM_RESOLUTION
    :: CHM_MAX_TIN_EDGE
    :: CLASS_VEGETATION
    :: NUM_CORES
    :: EPSG

:: make output directories
mkdir .\TEMP_FILES\18_veg
mkdir .\TEMP_FILES\13_chm\res_%CHM_RESOLUTION%\
mkdir .\OUTPUT_FILES\CHM


:: spike-free CHM following Khosravipour et al. 2016, 2015, 2014

las2las -i TEMP_FILES\10_normalized\*.laz ^
      -keep_class %CLASS_VEGETATION% ^
      -cores %NUM_CORES% ^
      -odir TEMP_FILES\18_veg\ -ocut 3 -odix _18 -olaz

las2dem -i TEMP_FILES\18_veg\*.laz ^
      -use_tile_bb ^
      -drop_class %CLASS_NOISE_GROUND% %CLASS_NOISE_CANOPY% %CLASS_GROUND% ^
      -spike_free %CHM_MAX_TIN_EDGE% ^
      -step %CHM_RESOLUTION% ^
      -kill %CHM_MAX_TIN_EDGE% ^
      -ll %GRID_ORIGIN% ^
      -cores %NUM_CORES% ^
      -odir TEMP_FILES\13_chm\res_%CHM_RESOLUTION%\ -ocut 3 -odix _spike_free_chm_%CHM_RESOLUTION%m -obil

:: merge output raster

lasgrid -i TEMP_FILES\13_chm\res_%CHM_RESOLUTION%\*.bil ^
      -merged ^
      -step %CHM_RESOLUTION% ^
      -epsg %EPSG% ^
      -ll %GRID_ORIGIN% ^
      -odir OUTPUT_FILES\CHM\ -obil