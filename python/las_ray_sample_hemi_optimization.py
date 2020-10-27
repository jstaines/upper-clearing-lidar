import las_ray_sampling as lrs
import numpy as np
import pandas as pd
import os

# config for batch rs_hemi

vox = lrs.VoxelObj()
vox.las_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LAS\\19_149_las_proc_classified_merged.las'
# vox.las_in = 'C:\\Users\\jas600\\workzone\\data\\las\\19_149_las_proc_classified_merged.las'
vox.traj_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_all_traj.txt'
# vox.traj_in = 'C:\\Users\\jas600\\workzone\\data\\las\\19_149_all_traj.txt'
vox.return_set = 'first'
vox.drop_class = 7
hdf5_path = vox.las_in.replace('.las', '_ray_sampling_' + vox.return_set + '_returns_drop_' + str(vox.drop_class) + '.h5')
vox.hdf5_path = hdf5_path
vox.chunksize = 10000000
voxel_length = .25
vox.step = np.full(3, voxel_length)
vox.sample_length = voxel_length/np.pi
vox_id = 'rs_vl' + str(voxel_length)
vox.id = vox_id

# vox = lrs.ray_sample_las(vox, create_new_hdf5=True)

# LOAD VOX
vox = lrs.vox_load(hdf5_path, vox_id)





batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\batches\\lrs_hemi_optimization_r.25_px361\\'

img_lookup_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\hemispheres\\hemi_lookup_cleaned.csv"
# img_lookup_in = 'C:\\Users\\jas600\\workzone\\data\\las\\hemi_lookup_cleaned.csv'
max_quality = 4
las_day = "19_149"
# import hemi_lookup
img_lookup = pd.read_csv(img_lookup_in)
# filter lookup by quality
img_lookup = img_lookup[img_lookup.quality_code <= max_quality]
# filter lookup by las_day
img_lookup = img_lookup[img_lookup.folder == las_day]

[file.replace('.JPG', '') for file in img_lookup.filename]


pts = pd.DataFrame({'id': img_lookup.filename,
                    'x_utm11n': img_lookup.xcoordUTM1,
                    'y_utm11n': img_lookup.ycoordUTM1,
                    'z_m': img_lookup.elevation})

# batch_dir = 'C:\\Users\\jas600\\workzone\\data\\hemigen\\mb_15_1m_pr.15_os10\\'
# las_in = "C:\\Users\\jas600\\workzone\\data\\hemigen\\hemi_lookups\\19_149_las_proc_classified_merged.las"
# pts_in = 'C:\\Users\\jas600\\workzone\\data\\hemigen\\hemi_lookups\\1m_dem_points_mb_15.csv'

# # load points
# pts = pd.read_csv(pts_in)

# configure hemisphere outputs
rshmeta = lrs.RaySampleHemiMetaObj()

# ray resampling parameters
# ratio = .05  # ratio of voxel area weight of prior
# F = .16 * 0.05  # expected footprint area
# V = np.prod(vox.step)  # volume of each voxel
mean_path_length = 2 * np.pi / (6 + np.pi) * voxel_length  # mean path length through a voxel cube across angles (m)
prior_weight = 5  # in units of scans (1 <=> equivalent weight to 1 expected voxel scan)
# prior_b = ratio * V / F  # path length required to scan "ratio" of one voxel volume
prior_b = mean_path_length * prior_weight
prior_a = prior_b * 0.001
rshmeta.prior = [prior_a, prior_b]
rshmeta.ray_sample_length = vox.sample_length
rshmeta.ray_iterations = 361  # model runs for each ray, from which median and std of returns is calculated

# image dimensions
rshmeta.img_size = 100  # square, in pixels/ray samples
rshmeta.max_phi_rad = np.pi/2

# image geometry
hemi_m_above_ground = img_lookup.height_m  # meters
rshmeta.max_distance = 50  # meters
rshmeta.min_distance = voxel_length * np.sqrt(3)  # meters


# output file dir
rshmeta.file_dir = batch_dir + "outputs\\"
if not os.path.exists(rshmeta.file_dir):
    os.makedirs(rshmeta.file_dir)





rshmeta.id = pts.id
rshmeta.origin = np.array([pts.x_utm11n,
                           pts.y_utm11n,
                           pts.z_m + hemi_m_above_ground]).swapaxes(0, 1)

rshmeta.file_name = ["las_19_149_id_" + str(id) + ".tif" for id in pts.id]

rshm = lrs.rs_hemigen(rshmeta, vox, initial_index=0)


# parse results
import tifffile as tif

# contact number log
cnlog = rshm.copy()

angle_lookup = pd.read_csv(cnlog.file_dir[0] + "phi_theta_lookup.csv")
phi = np.full((cnlog.img_size_px[0], cnlog.img_size_px[0]), np.nan)
phi[(np.array(angle_lookup.x_index), np.array(angle_lookup.y_index))] = angle_lookup.phi * 180 / np.pi

phi_bands = [0, 15, 30, 45, 60, 75]

cnlog.loc[:, ["rsm_med_1", "rsm_med_2", "rsm_med_3", "rsm_med_4", "rsm_med_5"]] = np.nan
cnlog.loc[:, ["rsm_cv_1", "rsm_cv_2", "rsm_cv_3", "rsm_cv_4", "rsm_cv_5"]] = np.nan
for ii in range(0, len(cnlog)):
    img = tif.imread(cnlog.file_dir[ii] + cnlog.file_name[ii])
    med = img[:, :, 0]
    cv = img[:, :, 1]
    med_temp = []
    cv_temp = []
    for jj in range(0, 5):
        mask = (phi >= phi_bands[jj]) & (phi < phi_bands[jj + 1])
        med_temp.append(np.nanmean(med[mask]))
        cv_temp.append(np.nanmean(cv[mask]))
    cnlog.loc[ii, ["rsm_med_1", "rsm_med_2", "rsm_med_3", "rsm_med_4", "rsm_med_5"]] = med_temp
    cnlog.loc[ii, ["rsm_cv_1", "rsm_cv_2", "rsm_cv_3", "rsm_cv_4", "rsm_cv_5"]] = cv_temp

cnlog.to_csv(cnlog.file_dir[0] + "contact_number_optimization.csv")

###

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tifffile as tif
ii = 0
peace = tif.imread(rshm.file_dir[ii] + rshm.file_name[ii])[:, :, 0]
peace[phi > 75] = np.nan
plt.imshow(peace, interpolation='nearest')