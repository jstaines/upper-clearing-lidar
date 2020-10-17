import rastools
import laslib
import numpy as np
import os

snow_on = ["19_045", "19_050", "19_052", "19_107", "19_123"]
snow_off = ["19_149"]
all_dates = snow_on + snow_off

resolution = [".10", ".25"]

depth_to_density_intercept = dict(zip(snow_on, [183.54, 110.22, 72.50, 224.64, 223.56]))
depth_to_density_slope = dict(zip(snow_on, 100*np.array([0.1485, 1.2212, 1.5346, 1.7833, 1.2072])))

depth_to_swe_slope = dict(zip(snow_on, 100*np.array([2.695, 2.7394, 3.0604, 3.1913, 2.5946])))

depth_regression = 'swe'

# las_in_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\LAS\\<DATE>_las_proc_classified_merged_ground.las'
# dem_ref_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc_xx\\OUTPUT_FILES\\TEMPLATES\\19_149_all_point_density_r<RES>m.bil'
# dem_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\DEM\\'
# dem_file_template = '<DATE>_dem_r<RES>m_q<QUANT>.tif'
# count_file_template = '<DATE>_dem_r<RES>m_count.tif'
#
# hs_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\hs\\<DDI>-<DDJ>\\'
# hs_file_template = 'hs_<DDI>-<DDJ>_r<RES>_q<QUANT>.tif'

hs_in_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\TEMP_FILES\\15_hs\\res_<RES>\\'
hs_merged_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\HS\\'
hs_merged_file_template = '<DATE>_hs_r<RES>m.tif'

ceiling_depths = [0.87, 0.96, 0.97, 0.93, 0.98]

hs_clean_dir_template = hs_merged_dir_template + 'clean\\'
hs_clean_file_template = hs_merged_file_template.replace('.tif', '_clean.tif')

swe_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\SWE\\'
swe_file_template = 'swe_<DATE>_r<RES>m.tif'

dswe_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\<DDI>-<DDJ>\\'
dswe_file_template = 'dswe_<DDI>-<DDJ>_r<RES>m.tif'

int_dir_template = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\DEM\\interpolated\\'
int_file_template = '<DATE>_dem_r<RES>m_q<QUANT>_interpolated_t<ITN>.tif'

chm_dir_template = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\<DATE>\\<DATE>_las_proc\\OUTPUT_FILES\\CHM\\"
chm_raw_in_template = "<DATE>_spike_free_chm_r<RES>m.bil"
chm_filled_out_template = "<DATE>_spike_free_chm_r<RES>m_filled.tif"

def path_sub(path, dd=None, rr=None, qq=None, ddi=None, ddj=None, itn=None, mm=None, bb=None):
    if isinstance(path, str):
        # nest pure strings in list
        path = [path]

    for ii in range(0, len(path)):
        if dd is not None:
            path[ii] = path[ii].replace('<DATE>', dd)
        if rr is not None:
            path[ii] = path[ii].replace('<RES>', rr)
        if qq is not None:
            path[ii] = path[ii].replace('<QUANT>', str(qq))
        if ddi is not None:
            path[ii] = path[ii].replace('<DDI>', str(ddi))
        if ddj is not None:
            path[ii] = path[ii].replace('<DDJ>', str(ddj))
        if itn is not None:
            path[ii] = path[ii].replace('<ITN>', str(itn))

    return ''.join(path)

# merge dems into single output
for dd in snow_on:
    # update file paths with date
    hs_out_dir = path_sub(hs_merged_dir_template, dd=dd)

    # create DEM directory if does not exist
    if not os.path.exists(hs_out_dir):
        os.makedirs(hs_out_dir)

    for rr in resolution:
        hs_in_dir = path_sub(hs_in_dir_template, dd=dd, rr=rr)
        hs_out_file = path_sub(hs_merged_file_template, dd=dd, rr=rr)

        # calculate hs
        rastools.raster_merge(hs_in_dir, '.bil', hs_out_dir + hs_out_file, no_data="-9999")

# clean depths
for dd in snow_on:
    # update file paths with date
    hs_in_dir = path_sub(hs_merged_dir_template, dd=dd)
    hs_clean_dir = path_sub(hs_clean_dir_template, dd=dd)

    # create DEM directory if does not exist
    if not os.path.exists(hs_clean_dir):
        os.makedirs(hs_clean_dir)


    ii = 0
    for rr in resolution:
        hs_in_file = path_sub(hs_merged_file_template, dd=dd, rr=rr)

        # load file
        hs_clean_file = path_sub(hs_clean_file_template, dd=dd, rr=rr)

        # send negative values to zero
        ras = rastools.raster_load(hs_in_dir + hs_in_file)
        ras.data[(ras.data < 0) & (ras.data != ras.no_data)] = 0

        # values = np.sort(ras.data[ras.data != ras.no_data])
        # rank = (np.arange(0, len(values)) + 1) / (len(values))
        # # calculate ceiling for res = '.10'
        # ceiling = np.min(values[rank > .998])

        # send values beyond ceiling to no_data
        ras.data[ras.data > ceiling_depths[ii]] = ras.no_data

        # save
        rastools.raster_save(ras, hs_clean_dir + hs_clean_file)

        ii = ii + 1

# SWE products
for dd in snow_on:
    # update file paths with date
    swe_dir = path_sub(swe_dir_template, dd=dd)

    # create SWE directory if does not exist
    if not os.path.exists(swe_dir):
        os.makedirs(swe_dir)

    for rr in resolution:
        # update file paths with resolution
        hs_file = path_sub([hs_clean_dir_template, hs_clean_file_template], dd=dd, rr=rr)
        swe_file = path_sub([swe_dir_template, swe_file_template], dd=dd, rr=rr)

        # calculate swe
        ras = rastools.raster_load(hs_file)
        valid_cells = np.where(ras.data != ras.no_data)
        depth = ras.data[valid_cells]

        # juggle regression types
        if depth_regression == 'density':
            mm = depth_to_density_slope[dd]
            bb = depth_to_density_intercept[dd]
            swe = depth * (mm * depth + bb)
        elif depth_regression == 'swe':
            mm = depth_to_swe_slope[dd]
            swe = mm * depth
        else:
            raise Exception('Invalid specification for depth_regression.')

        ras.data[valid_cells] = swe
        rastools.raster_save(ras, swe_file)

# differential SWE products
for ii in range(0, len(snow_on)):
    ddi = snow_on[ii]
    for jj in range(ii + 1, len(snow_on)):
        ddj = snow_on[jj]
        # update file paths with dates
        dswe_dir = path_sub(dswe_dir_template, ddi=ddi, ddj=ddj)

        # create SWE directory if does not exist
        if not os.path.exists(dswe_dir):
            os.makedirs(dswe_dir)

        for rr in resolution:
            ddi_in = path_sub([swe_dir_template, swe_file_template], dd=ddi, rr=rr)
            ddj_in = path_sub([swe_dir_template, swe_file_template], dd=ddj, rr=rr)
            dswe_out = path_sub([dswe_dir_template, dswe_file_template], ddi=ddi, ddj=ddj, rr=rr)

            hs = rastools.raster_dif(ddj_in, ddi_in, inherit_from=2, dif_out=dswe_out)

# interpolated products
for dd in snow_off:
    print(dd, end='')
    # update file paths with date
    int_dir = path_sub(int_dir_template, dd)

    # create DEM directory if does not exist
    if not os.path.exists(int_dir):
        os.makedirs(int_dir)

    for rr in resolution:
        ras_template = path_sub(dem_ref_template, rr=rr)
        dem_file = path_sub([dem_dir_template, dem_file_template], dd=dd, rr=rr, qq=dem_quantile)
        count_file = path_sub([dem_dir_template, count_file_template], dd=dd, rr=rr)
        int_file = path_sub([int_dir_template, int_file_template], dd=dd, rr=rr, qq=dem_quantile, itn=interpolation_threshold)

        # interpolate dem
        rastools.delauney_fill(dem_file, int_file, ras_template, n_count=count_file, n_threshold=interpolation_threshold)
        print(' -- ' + rr, end='')
    print('\n')

# fill chm with zeros where dem in not nan
# only for dates and resolutions where chm exists
for dd in all_dates:
    for rr in resolution:
        # update file paths with resolution
        chm_in = path_sub([chm_dir_template, chm_raw_in_template], dd=dd, rr=rr)
        if os.path.exists(chm_in):
            # update file paths
            count_file = path_sub([dem_dir_template, count_file_template], dd=dd, rr=rr)
            chm_out = path_sub([chm_dir_template, chm_filled_out_template], dd=dd, rr=rr)

            # load rasters
            chm = rastools.raster_load(chm_in)
            counts = rastools.gdal_raster_reproject(count_file, chm_in)[:, :, 0]

            # fill in chm nan values with 0 where dem count > 0
            chm.data[(chm.data == chm.no_data) & (counts > 0)] = 0

            # save to chm_out
            rastools.raster_save(chm, chm_out)


# # point sample HS products to merge with snow surveys
# initial_pts_file = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\surveys\\all_ground_points_UTM11N_uid_flagged_cover.csv"
# for rr in resolution:
#     pts_file_in = initial_pts_file
#     pts_file_out = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\all_ground_points_dhs_r" + rr + ".csv"
#     for ii in range(0, date.__len__()):
#         ddi = date[ii]
#         for jj in range(ii + 1, date.__len__()):
#             ddj = date[jj]
#
#             ras_sample = path_sub([dhs_dir_template, dhs_file_template], ddi=ddi, ddj=ddj, rr=rr)
#             colname = str(ddi) + '-' + str(ddj)
#             rastools.csv_sample_raster(ras_sample, pts_file_in, pts_file_out, "xcoordUTM11", "ycoordUTM11", colname, sample_no_data_value='')
#             pts_file_in = pts_file_out

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.plot(rank, values)



nn = len(rank)
v1 = np.convolve(values, np.ones(int(nn/100000)), 'valid')/int(nn/100000)
r1 = np.arange(0, len(v1))/len(v1)
nn = len(r1)

plt.plot(r1, v1)

v2 = v1[1:nn] - v1[0:nn-1]
r2 = r1[0:nn-1]
plt.plot(r2, v2)