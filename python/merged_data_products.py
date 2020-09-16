import pandas as pd
import rastools

# first item in ddict is parent by default
# subsequent items are sampled at non-null parent cell centers
ddict = {
    ('er_001_mean', 'er_001_median', 'er_001_sd'): 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\RSM\\19_149_expected_returns_res_.25m_0-0_t_1.tif',
    'hs_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\19_045-19_149\\19_045-19_149_dhs_r.25.tif',
    'count_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\DEM\\19_045_dem_r.25m_count.tif',
    'hs_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\19_050-19_149\\19_050-19_149_dhs_r.25.tif',
    'count_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\DEM\\19_050_dem_r.25m_count.tif',
    'hs_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\19_052-19_149\\19_052-19_149_dhs_r.25.tif',
    'count_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\DEM\\19_052_dem_r.25m_count.tif',
    'hs_19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\19_107-19_149\\19_107-19_149_dhs_r.25.tif',
    'count_19_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_107\\19_107_las_proc\\OUTPUT_FILES\\DEM\\19_107_dem_r.25m_count.tif',
    'hs_19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\dhs\\19_123-19_149\\19_123-19_149_dhs_r.25.tif',
    'count_19_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_123\\19_123_las_proc\\OUTPUT_FILES\\DEM\\19_123_dem_r.25m_count.tif',
    'count_19_149': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\DEM\\19_149_dem_r.25m_count.tif',
    'dnt': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\DNT\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_kho_distance_.10m.tif',
    'dce': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\DCE\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_DCE.tiff',
    'chm': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\CHM\\19_149_snow_off_627975_5646450_spike_free_chm_.10m.bil',
    'lpmf': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LPM\\19_149_snow_off_LPM-first_30degsa_0.25m.tif',
    'lpml': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LPM\\19_149_snow_off_LPM-last_30degsa_0.25m.tif',
    'lpmc': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LPM\\19_149_snow_off_LPM-canopy_30degsa_0.25m.tif',
    'hemi_id': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\1m_dem_point_ids.tif',
    'uf': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\uf_plot_over_dem.tiff'
}
keys = list(ddict.keys())
hemi_data_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\outputs\\LAI_parsed.dat'
file_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\analysis\\hs_uf_.25m_canopy_19_149.csv'

data = None
for kk in keys:
    data = rastools.pd_sample_raster(data, ddict[kk], kk)

    # print update
    if isinstance(kk, tuple):
        print('loaded ' + ", ".join(kk))
    else:
        print('loaded ' + kk)

# filter to uf
data = data[data.uf == 1]
data = data.drop(columns='uf')

# merge with hemisfer outputs
hemi_data = pd.read_csv(hemi_data_in)
merged = data.merge(hemi_data, how='left', left_on='hemi_id', right_on='id')
merged = merged.drop(columns='id')
print('merged with hemi_data')

# save to file
merged.to_csv(file_out, index=False)