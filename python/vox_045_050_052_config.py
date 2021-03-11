import numpy as np
import las_ray_sampling as lrs
config_id = "045_050_052_r0.25"

# vox = lrs.VoxelObj()
# # vox.las_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\LAS\\19_149_las_proc_classified_merged.las'
# vox.las_in = 'C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\19_045_all_WGS84_utm11N.las'
# # vox.traj_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_all_traj.txt'
# vox.traj_in = 'C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\19_045_all_trajectories_WGS84_utm11N.txt'
# vox.return_set = 'first'
# vox.drop_class = 7
# vox.las_traj_hdf5 = vox.las_in.replace('.las', '_ray_sampling_' + vox.return_set + '_returns_drop_' + str(vox.drop_class) + '_las_traj.h5')
# vox.sample_dtype = np.uint32
# vox.return_dtype = np.uint32
# vox.las_traj_chunksize = 5000000
# vox.cw_rotation = -34 * np.pi / 180
# voxel_length = .25
# vox.step = np.full(3, voxel_length)
# vox.sample_length = voxel_length / np.pi
# vox.vox_hdf5 = vox.las_in.replace('.las', "_" + config_id + '_vox.h5')
#
# # specify origin and max for alignment with other sets (pulled from 19_149 vox)
# vox.origin = np.array([-2.63693299e+06,  5.03236474e+06,  1.80983250e+03])
# vox.max = np.array([-2.63665114e+06,  5.03262022e+06,  1.87498250e+03])

voxList = ['C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\19_045_all_WGS84_utm11N_19_045_r0.25_vox.h5',
           'C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\19_050_all_WGS84_utm11N_19_050_r0.25_vox.h5',
           'C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\19_052_all_WGS84_utm11N_19_052_r0.25_vox.h5']

vox_out = 'C:\\Users\\jas600\\workzone\\data\\ray_sampling\\sources\\045_050_052_combined_WGS84_utm11N_r0.25_vox.h5'
z_slices = 8

# BUILD VOX
# combine voxel spaces
vox = lrs.load_vox_meta(vox_out, load_data=False, load_post=True)
# calculate prior
# lrs.beta_lookup_prior_calc(vox, z_slices, agg_sample_length=None)
