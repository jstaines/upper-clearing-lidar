def merge_data_products(ddict, hemi_data_in, file_out, mode='nearest'):
    import pandas as pd
    import rastools
    import numpy as np

    data = rastools.pd_sample_raster_gdal(ddict, mode)

    if 'dce' in ddict.keys():
        data.dce = np.rint(data.dce * 10)/10

    if hemi_data_in is not None:
        # merge with hemisfer outputs
        print('Merging with hemi_data... ', end='')
        hemi_data = pd.read_csv(hemi_data_in)
        merged = data.merge(hemi_data, how='left', left_on='hemi_id', right_on='id')
        merged = merged.drop(columns='id')
        print('done')
    else:
        merged = data



    # save to file
    print('saving to file... ', end='')
    merged.to_csv(file_out, index=False)
    print('done')


# first item in ddict is parent by default
# subsequent items are sampled at non-null parent cell centers
ddict = {
    'mb_15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\mb_15_plot_r.25m.tif',
    'plots': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_r.25m\\site_plots_r.25m.tif',
    ('er_p0_mean', 'er_p0_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_mb_15_dem_.25m_61px_mp15.25\\outputs\\las_19_149_rs_mb_15_r.25_p0.0000_t3.1416.tif',
    'hemi_id': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\1m_dem_point_ids.tif'
}
hemi_data_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\batches\\mb_15_1m_pr.15_os10\\outputs\\LAI_parsed.dat'
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\mb_15_merged_.25m_native_canopy_19_149.csv'

merge_data_products(ddict, hemi_data_in, file_out)




ddict = {
    'mb_15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\mb_15_plot_r.25m.tif',
    'plots': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_r.25m\\site_plots_r.25m.tif',
    'swe_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_045_r.05m_interp2x_masked.tif',
    'swe_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_050_r.05m_interp2x_masked.tif',
    'swe_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_052_r.05m_interp2x_masked.tif',
    'dswe_19_045-19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_045-19_050\\masked\\dswe_ahpl_19_045-19_050_r.05m_interp2x_masked.tif',
    'dswe_19_050-19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_050-19_052\\masked\\dswe_ahpl_19_050-19_052_r.05m_interp2x_masked.tif',
    ('er_p0_mean', 'er_p0_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_mb_15_dem_.25m_61px_mp15.25\\outputs\\las_19_149_rs_mb_15_r.25_p0.0000_t3.1416.tif',
    'hemi_id': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\1m_dem_point_ids.tif'
}

hemi_data_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\batches\\mb_15_1m_pr.15_os10\\outputs\\LAI_parsed.dat'
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\mb_15_merged_.25m_ahpl_median_canopy_19_149.csv'
merge_data_products(ddict, hemi_data_in, file_out, mode='median')


ddict = {
    'mb_15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\mb_15_plot_r.10m.tif',
    'plots': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_r.25m\\site_plots_r.10m.tif',
    'dnt': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DNT\\19_149_spike_free_dsm_can_r.10m_kho_distance_.10m.tif',
    'dce': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DCE\\19_149_spike_free_chm_r.10m_dce.tif',
    'chm': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\CHM\\19_149_spike_free_chm_r.10m.tif',
    # 'lpmf5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a5_r0.10m.tif',
    # 'lpml5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a5_r0.10m.tif',
    # 'lpmc5': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a5_r0.10m.tif',
    'lpmf15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a15_r0.10m.tif',
    'lpml15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a15_r0.10m.tif',
    'lpmc15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a15_r0.10m.tif',
}
hemi_data_in = None
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\mb_15_merged_.10m_native_canopy_19_149.csv'

merge_data_products(ddict, hemi_data_in, file_out)


ddict = {
    'plots': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_r.25m\\site_plots_r.10m.tif',
    'swe_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_045_r.05m_interp2x_masked.tif',
    'swe_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_050_r.05m_interp2x_masked.tif',
    'swe_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_052_r.05m_interp2x_masked.tif',
    'dswe_19_045-19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_045-19_050\\masked\\dswe_ahpl_19_045-19_050_r.05m_interp2x_masked.tif',
    'dswe_19_050-19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_050-19_052\\masked\\dswe_ahpl_19_050-19_052_r.05m_interp2x_masked.tif',
    'dnt': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DNT\\19_149_spike_free_dsm_can_r.10m_kho_distance_.10m.tif',
    'dce': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DCE\\19_149_spike_free_chm_r.10m_dce.tif',
    'chm': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\CHM\\19_149_spike_free_chm_r.10m.tif',
    'lpmf15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-first_a15_r0.10m.tif',
    'lpml15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a15_r0.10m.tif',
    'lpmc15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-canopy_a15_r0.10m.tif',
}
hemi_data_in = None
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\uf_merged_.10m_ahpl_median_canopy_19_149.csv'

merge_data_products(ddict, hemi_data_in, file_out, mode='median')


ddict = {
    # 'mb_15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_1m\\mb_15_plot_r.05m.tif',
    'plots': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\hemi_grid_points\\mb_65_r.25m\\site_plots_r.05m.tif',
    'swe_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_045_r.05m_interp2x_masked.tif',
    'swe_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_050_r.05m_interp2x_masked.tif',
    'swe_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\SWE\\ahpl\\interp_2x\\masked\\swe_ahpl_19_052_r.05m_interp2x_masked.tif',
    'dswe_19_045-19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_045-19_050\\masked\\dswe_ahpl_19_045-19_050_r.05m_interp2x_masked.tif',
    'dswe_19_050-19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\ahpl\\interp_2x\\19_050-19_052\\masked\\dswe_ahpl_19_050-19_052_r.05m_interp2x_masked.tif',
    'lpml15': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LPM\\19_149_LPM-last_a15_r0.10m.tif',
    ('er_p0_mean', 'er_p0_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_mb_15_dem_.25m_61px_mp15.25\\outputs\\las_19_149_rs_mb_15_r.25_p0.0000_t3.1416.tif',
}
hemi_data_in = None
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\uf_merged_.05m_ahpl_native.csv'

merge_data_products(ddict, hemi_data_in, file_out, mode='nearest')
