# import pandas as pd
# import numpy as np
# import laslib
# import time
#
# poisson_list = [0, .05, .15]
# os_list = [1.5, 2, 15]
# # define metadata object
# hemimeta = laslib.HemiMetaObj()
#
# # source las file
# hemimeta.src_las_file = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LAS\\19_149_snow_off_classified_merged.las"
# hemimeta.src_keep_class = [1, 5]  # range of classes or single class ([1, 5] passes all classes within 1-5)
# hemimeta.poisson_sampling_radius = poisson_list[ii]  # meters (for no poisson sampling, specify 0)
#
# # output file dir
# hemimeta.file_dir = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\opt\\poisson_r.15m\\"
#
# # max distance of points considered in image
# hemimeta.max_distance = 50  # meters
#
# # image size
# hemimeta.img_size = 10  # in inches
# hemimeta.img_resolution = 100  # pixels/inch
#
#
# poisson_sampling_radius = .15
#
# # poisson sample point cloud (src_las_in)
# if (hemimeta.poisson_sampling_radius is None) or (hemimeta.poisson_sampling_radius == 0):
#     # skip poisson sampling
#     las_poisson_path = hemimeta.src_las_file
#     print("no Poisson sampling conducted")
# else:
#     if hemimeta.poisson_sampling_radius > 0:
#         # poisson sampling
#         las_poisson_path = hemimeta.src_las_file.replace('.las', '_poisson_' + str(hemimeta.poisson_sampling_radius) + '.las')
#         # laslib.las_poisson_sample(hemimeta.src_las_file, hemimeta.poisson_sampling_radius, classification=hemimeta.src_keep_class, las_out=las_poisson_path)  # takes 10 minutes
#     else:
#         raise Exception('hemimeta.poisson_sampling_radius should be a numeric >= 0 or None.')
#
# # export las to hdf5
# print("-------- Exporting to HDF5 --------")
# hdf5_path = las_poisson_path.replace('.las', '.hdf5')
# # laslib.las_xyz_to_hdf5(las_poisson_path, hdf5_path, keep_class=hemimeta.src_keep_class)
#
# # import hemi-photo lookup
# lookup_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\hemispheres\\hemi_lookup_cleaned.csv"
# max_quality = 4
# las_day = "19_149"
# # import hemi_lookup
# lookup = pd.read_csv(lookup_in)
# # filter lookup by quality
# lookup = lookup[lookup.quality_code <= max_quality]
# # filter lookup by las_day
# lookup = lookup[lookup.folder == las_day]
#
# hemimeta.id = lookup.index
# hemimeta.origin = np.array([lookup.xcoordUTM1,
#                             lookup.ycoordUTM1,
#                             lookup.elevation + lookup.height_m]).swapaxes(0, 1)
#
#
# # point size
# hemimeta.optimization_scalar = 10
# footprint = 0.15  # in m
# c = 2834.64  # meters to points
# hemimeta.point_size_scalar = footprint**2 * c * hemimeta.optimization_scalar
# hemimeta.file_name = ["las_" + las_day + "_img_" + fn[0:-4] + "_pr_" + str(hemimeta.poisson_sampling_radius) +
#                       "_os_" + str(hemimeta.optimization_scalar) + ".png" for fn in lookup.filename]
# hm = laslib.hemigen(hdf5_path, hemimeta, initial_index=0)

### ### ### ### ###

import pandas as pd
import numpy as np
import laslib
import os


batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\synthetic_hemis\\batches\\pp_hemi_optimization_pr.15_os10\\'
las_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LAS\\19_149_las_proc_classified_merged.las"


# batch_dir = 'C:\\Users\\jas600\\workzone\\data\\hemigen\\mb_15_1m_pr.15_os10\\'
# las_in = "C:\\Users\\jas600\\workzone\\data\\hemigen\\hemi_lookups\\19_149_las_proc_classified_merged.las"

# create batch dir if does not exist
if not os.path.exists(batch_dir):
    os.makedirs(batch_dir)

# hemi run
# define metadata object
hemimeta = laslib.HemiMetaObj()

# source las file
las_day = 19_149
hemimeta.src_las_file = las_in
hemimeta.src_keep_class = [1, 5]  # range of classes or single class ([1, 5] passes all classes within 1-5)
hemimeta.poisson_sampling_radius = 0.15  # meters (for no poisson sampling, specify 0)

# output file dir
hemimeta.file_dir = batch_dir + "outputs\\"
if not os.path.exists(hemimeta.file_dir):
    os.makedirs(hemimeta.file_dir)

# max distance of points considered in image
hemimeta.max_distance = 50  # meters
hemimeta.min_distance = .5  # meters
hemi_m_above_ground = 0  # meters

# image size
hemimeta.img_size = 10  # in inches
hemimeta.img_resolution = 100  # pixels/inch


# poisson sample point cloud (src_las_in)
if (hemimeta.poisson_sampling_radius is None) or (hemimeta.poisson_sampling_radius == 0):
    # skip poisson sampling
    las_poisson_path = hemimeta.src_las_file
    print("no Poisson sampling conducted")
else:
    if hemimeta.poisson_sampling_radius > 0:
        # poisson sampling
        las_poisson_path = hemimeta.src_las_file.replace('.las', '_poisson_' + str(hemimeta.poisson_sampling_radius) + '.las')
        laslib.las_poisson_sample(hemimeta.src_las_file, hemimeta.poisson_sampling_radius, classification=hemimeta.src_keep_class, las_out=las_poisson_path)  # takes 10 minutes
    else:
        raise Exception('hemimeta.poisson_sampling_radius should be a numeric >= 0 or None.')

# export las to hdf5
print("-------- Exporting to HDF5 --------")
hdf5_path = las_poisson_path.replace('.las', '.hdf5')
laslib.las_xyz_to_hdf5(las_poisson_path, hdf5_path, keep_class=hemimeta.src_keep_class)

# import hemi-photo lookup
lookup_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\hemispheres\\hemi_lookup_cleaned.csv"
max_quality = 4
las_day = "19_149"
# import hemi_lookup
lookup = pd.read_csv(lookup_in)
# filter lookup by quality
lookup = lookup[lookup.quality_code <= max_quality]
# filter lookup by las_day
lookup = lookup[lookup.folder == las_day]

hemimeta.id = lookup.index
hemimeta.origin = np.array([lookup.xcoordUTM1,
                            lookup.ycoordUTM1,
                            lookup.elevation + lookup.height_m]).swapaxes(0, 1)

# point size
hemimeta.optimization_scalar = 10
footprint = 0.15  # in m
c = 2834.64  # meters to points
hemimeta.point_size_scalar = footprint**2 * c * hemimeta.optimization_scalar
hemimeta.file_name = ["las_" + las_day + "_img_" + fn[0:-4] + "_pr_" + str(hemimeta.poisson_sampling_radius) +
                       "_os_" + str(hemimeta.optimization_scalar) + ".png" for fn in lookup.filename]
hm = laslib.hemigen(hdf5_path, hemimeta, initial_index=0)