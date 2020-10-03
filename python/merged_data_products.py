def merge_data_products(ddict, hemi_data_in, file_out):
    import pandas as pd
    import rastools
    import numpy as np

    data = rastools.pd_sample_raster_gdal(ddict)

    data.dce = np.rint(data.dce * 10)/10

    # merge with hemisfer outputs
    print('Merging with hemi_data... ', end='')
    hemi_data = pd.read_csv(hemi_data_in)
    merged = data.merge(hemi_data, how='left', left_on='hemi_id', right_on='id')
    merged = merged.drop(columns='id')
    print('done')


    # save to file
    print('saving to file... ', end='')
    merged.to_csv(file_out, index=False)
    print('done')


# first item in ddict is parent by default
# subsequent items are sampled at non-null parent cell centers
ddict = {
    ('er_001_mean', 'er_001_median', 'er_001_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\RSM\\19_149_expected_returns_res_.25m_0-0_t_1.tif',
    'swe_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\SWE\\19_045\\swe_19_045_r.25m_q0.25.tif',
    'count_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\DEM\\19_045_dem_r.25m_count.tif',
    'swe_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\SWE\\19_050\\swe_19_050_r.25m_q0.25.tif',
    'count_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\DEM\\19_050_dem_r.25m_count.tif',
    'swe_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\SWE\\19_052\\swe_19_052_r.25m_q0.25.tif',
    'count_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\DEM\\19_052_dem_r.25m_count.tif',
    'swe_19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\SWE\\19_107\\swe_19_107_r.25m_q0.25.tif',
    'count_19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_107\\19_107_las_proc\\OUTPUT_FILES\\DEM\\19_107_dem_r.25m_count.tif',
    'swe_19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\SWE\\19_123\\swe_19_123_r.25m_q0.25.tif',
    'count_19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_123\\19_123_las_proc\\OUTPUT_FILES\\DEM\\19_123_dem_r.25m_count.tif',
    'count_19_149': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DEM\\19_149_dem_r.25m_count.tif',
    'dnt': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DNT\\19_149_spike_free_chm_r.10m_kho_distance_.10m.tif',
    'dce': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DCE\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_DCE.tiff',
    'chm': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\CHM\\19_149_spike_free_chm_r.25m_filled.tif',
    'lpmf5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a5_r0.25m.tif',
    'lpml5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a5_r0.25m.tif',
    'lpmc5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a5_r0.25m.tif',
    'lpmf10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a10_r0.25m.tif',
    'lpml10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a10_r0.25m.tif',
    'lpmc10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a10_r0.25m.tif',
    'lpmf15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a15_r0.25m.tif',
    'lpml15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a15_r0.25m.tif',
    'lpmc15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a15_r0.25m.tif',
    'lpmf30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a30_r0.25m.tif',
    'lpml30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a30_r0.25m.tif',
    'lpmc30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a30_r0.25m.tif',
    'hemi_id': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\1m_dem_point_ids.tif',
    'uf': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\uf_plot_over_dem.tiff'
}
hemi_data_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\outputs\\LAI_parsed.dat'
swe_file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\swe_.25m_canopy_19_149.csv'

merge_data_products(ddict, hemi_data_in, swe_file_out)

ddict = {
    ('er_001_mean', 'er_001_median', 'er_001_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\RSM\\19_149_expected_returns_res_.25m_0-0_t_1.tif',
    'dswe_19_045-19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dSWE\\19_045-19_050\\dswe_19_045-19_050_r.25m_q0.25.tif',
    'count_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\DEM\\19_045_dem_r.25m_count.tif',
    'dswe_19_050-19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dSWE\\19_050-19_052\\dswe_19_050-19_052_r.25m_q0.25.tif',
    'count_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\DEM\\19_050_dem_r.25m_count.tif',
    'dswe_19_052-19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dSWE\\19_052-19_107\\dswe_19_052-19_107_r.25m_q0.25.tif',
    'count_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\DEM\\19_052_dem_r.25m_count.tif',
    'dswe_19_107-19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dSWE\\19_107-19_123\\dswe_19_107-19_123_r.25m_q0.25.tif',
    'count_19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_107\\19_107_las_proc\\OUTPUT_FILES\\DEM\\19_107_dem_r.25m_count.tif',
    'count_19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_123\\19_123_las_proc\\OUTPUT_FILES\\DEM\\19_123_dem_r.25m_count.tif',
    'count_19_149': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DEM\\19_149_dem_r.25m_count.tif',
    'dnt': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DNT\\19_149_spike_free_chm_r.10m_kho_distance_.10m.tif',
    'dce': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DCE\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_DCE.tiff',
    'chm': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\CHM\\19_149_spike_free_chm_r.25m_filled.tif',
    'lpmf5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a5_r0.25m.tif',
    'lpml5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a5_r0.25m.tif',
    'lpmc5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a5_r0.25m.tif',
    'lpmf10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a10_r0.25m.tif',
    'lpml10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a10_r0.25m.tif',
    'lpmc10': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a10_r0.25m.tif',
    'lpmf15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a15_r0.25m.tif',
    'lpml15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a15_r0.25m.tif',
    'lpmc15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a15_r0.25m.tif',
    'lpmf30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a30_r0.25m.tif',
    'lpml30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a30_r0.25m.tif',
    'lpmc30': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a30_r0.25m.tif',
    'hemi_id': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\1m_dem_point_ids.tif',
    'uf': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\uf_plot_over_dem.tiff'
}
hemi_data_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\outputs\\LAI_parsed.dat'
dswe_file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\dswe_.25m_canopy_19_149.csv'
merge_data_products(ddict, hemi_data_in, dswe_file_out)