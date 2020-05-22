mkdir .\OUTPUT_FILES\RAS

:: all return point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -drop_class %CLASS_NOISE_GROUND% %CLASS_NOISE_CANOPY% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _last_return_point_density_%RAS_RESOLUTION%m

:: 1st return point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -keep_first ^
            -drop_class %CLASS_NOISE_GROUND% %CLASS_NOISE_CANOPY% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _1st_return_point_density_%RAS_RESOLUTION%m

:: last return point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -keep_last ^
            -drop_class %CLASS_NOISE_GROUND% %CLASS_NOISE_CANOPY% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _last_return_point_density_%RAS_RESOLUTION%m

:: single return point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -keep_single ^
            -drop_class %CLASS_NOISE_GROUND% %CLASS_NOISE_CANOPY% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _last_return_point_density_%RAS_RESOLUTION%m

:: ground point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -keep_class %CLASS_GROUND% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _ground_point_density_%RAS_RESOLUTION%m

:: vegetation point density
lasgrid -i TEMP_FILES\11_no_buffer\*.laz ^
            -keep_class %CLASS% ^
            -merged ^
            -step %RAS_RESOLUTION% ^
            -epsg %EPSG% ^
            -point_density ^
            -odir OUTPUT_FILES\RAS\ -obil -ocut 3 -odix _veg_point_density_%RAS_RESOLUTION%m

:: analysis of height-normalized point cloud

:: mean height of 1st returns
:: mean height of last returns
:: standard deviation of all returns