import rastools
import numpy as np
import pandas as pd
import tifffile as tif
from tqdm import tqdm
from scipy.optimize import fmin_bfgs
import scipy.odr as odr
import matplotlib
matplotlib.use('Qt5Agg')
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors


plot_out_dir = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\graphics\\thesis_graphics\\modeling snow accumulation\\"

# # ray tracing run
# batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_uf_r.25_px181_snow_off\\outputs\\'
# batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_uf_r.25_px181_snow_off_dem_offset.25\\outputs\\'
# scaling_coef = 0.1841582  # snow_off
# canopy = "snow_off"

# # batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_uf_r.25_px181_snow_on\\outputs\\'
batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_uf_r.25_px181_snow_on_dem_offset.25\\outputs\\'
scaling_coef = 0.1692154  # snow_on
canopy = "snow_on"


# if date == "045-050":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\fnsd\\interp_2x\\19_045-19_050\\masked\\dswe_fnsd_19_045-19_050_r.05m_interp2x_masked.tif'
# elif date == "050-052":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\fnsd\\interp_2x\\19_050-19_052\\masked\\dswe_fnsd_19_050-19_052_r.05m_interp2x_masked.tif'
# elif date == "19_045":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_045_r.05m_interp2x_masked.tif'
# elif date == "19_050":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_050_r.05m_interp2x_masked.tif'
# elif date == "19_052":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_052_r.05m_interp2x_masked.tif'
# elif date == "19_107":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_107\\19_107_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_107_r.05m_interp2x_masked.tif'
# elif date == "19_123":
#     var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_123\\19_123_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_123_r.05m_interp2x_masked.tif'


ddict = {'uf': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\site_library\\hemi_grid_points\\mb_65_r.25m_snow_off_offset0\\uf_plot_r.25m.tif',
         'count_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\RAS\\19_045_ground_point_density_r.25m.bil',
         'count_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\RAS\\19_050_ground_point_density_r.25m.bil',
         'count_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\RAS\\19_052_ground_point_density_r.25m.bil',
         # 'count_107': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_107\\19_107_las_proc\\OUTPUT_FILES\\RAS\\19_107_ground_point_density_r.25m.bil',
         # 'count_123': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_123\\19_123_las_proc\\OUTPUT_FILES\\RAS\\19_123_ground_point_density_r.25m.bil',
         'count_149': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_las_proc\\OUTPUT_FILES\\RAS\\19_149_ground_point_density_r.25m.bil',
         # 'swe_fcon_19_045': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_045\\19_045_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_045_r.05m_interp2x_masked.tif',
         # 'swe_fcon_19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_050\\19_050_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_050_r.05m_interp2x_masked.tif',
         # 'swe_fcon_19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_052\\19_052_las_proc\\OUTPUT_FILES\\SWE\\fcon\\interp_2x\\masked\\swe_fcon_19_052_r.05m_interp2x_masked.tif',
         'dswe_fnsd_19_045-19_050': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\fnsd\\interp_2x\\19_045-19_050\\masked\\dswe_fnsd_19_045-19_050_r.05m_interp2x_masked.tif',
         'dswe_fnsd_19_050-19_052': 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\fnsd\\interp_2x\\19_050-19_052\\masked\\dswe_fnsd_19_050-19_052_r.05m_interp2x_masked.tif'
         # 'covariant': var_in
         }
var = rastools.pd_sample_raster_gdal(ddict, include_nans=False, mode="median")


# var = var.loc[~np.isnan(var.covariant), :]  # drop nans in covariant

# if date == "045-050":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_045, var.count_050, var.count_149), axis=0) * (.25 ** 2)
# elif date == "050-052":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_050, var.count_052, var.count_149), axis=0) * (.25 ** 2)
# elif date == "19_045":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_045, var.count_149), axis=0) * (.25 ** 2)
# elif date == "19_050":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_050, var.count_149), axis=0) * (.25 ** 2)
# elif date == "19_052":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_052, var.count_149), axis=0) * (.25 ** 2)
# elif date == "19_107":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_107, var.count_149), axis=0) * (.25 ** 2)
# elif date == "19_123":
#     var.loc[:, "min_pc"] = np.nanmin((var.count_123, var.count_149), axis=0) * (.25 ** 2)
#
# # filter by min point count
# var = var.loc[var.min_pc >= 25, :]

# load img meta
hemimeta = pd.read_csv(batch_dir + 'rshmetalog.csv')
imsize = hemimeta.img_size_px[0]

# merge with image meta
hemi_var = pd.merge(hemimeta, var, left_on=('x_utm11n', 'y_utm11n'), right_on=('x_coord', 'y_coord'), how='inner')

# load image pixel angle lookup
angle_lookup = pd.read_csv(batch_dir + "phi_theta_lookup.csv")
# build phi image (in radians)
phi = np.full((imsize, imsize), np.nan)
phi[(np.array(angle_lookup.y_index), np.array(angle_lookup.x_index))] = angle_lookup.phi
# build theta image (in radians)
theta = np.full((imsize, imsize), np.nan)
theta[(np.array(angle_lookup.y_index), np.array(angle_lookup.x_index))] = angle_lookup.theta

# limit analysis by phi (in radians)
max_phi = 90 * (np.pi / 180)
# calculate radius range to avoid pixels outside of circle
imrange = np.full((imsize, imsize), False)
imrange[phi <= max_phi] = True

# # filter hemimeta to desired images
# delineate training set (set_param < param_thresh) and test set (set_param >= param thresh)
param_thresh = 0.5
set_param = np.random.random(len(hemi_var))
hemi_var.loc[:, 'training_set'] = set_param < param_thresh
# build hemiList from training_set only
hemiList = hemi_var.loc[hemi_var.training_set, :].reset_index()



# specify which time date

# date = "19_045"
# covariant = hemiList.swe_fcon_19_045

# date = "19_050"
# covariant = hemiList.swe_fcon_19_050

# date = "19_052"
# covariant = hemiList.swe_fcon_19_052

# date = "045-050"
# covariant = hemiList.loc[:, "dswe_fnsd_19_045-19_050"]
# # covariant_error = 1/np.sqrt(hemiList.loc[:, "count_045"]) + 1/np.sqrt(hemiList.loc[:, "count_050"]) + 2/np.sqrt(hemiList.loc[:, "count_149"])/4
# covariant_error = 1/np.sqrt(np.min([hemiList.loc[:, "count_045"], hemiList.loc[:, "count_050"], hemiList.loc[:, "count_149"]], axis=0) / 16)
# covariant_error = covariant_error * 0.1 * 85.1

date = "050-052"
covariant = hemiList.loc[:, "dswe_fnsd_19_050-19_052"]
# covariant_error = (1/np.sqrt(hemiList.loc[:, "count_050"]/16) + 1/np.sqrt(hemiList.loc[:, "count_052"]/16) + 2/np.sqrt(hemiList.loc[:, "count_149"]/16))/4
covariant_error = 1/np.sqrt(np.min([hemiList.loc[:, "count_050"], hemiList.loc[:, "count_052"], hemiList.loc[:, "count_149"]], axis=0) / 16)
covariant_error = covariant_error * 0.1 * 72.2

valid = ~np.isnan(covariant) & ~np.isnan(covariant_error)



# load hemiList images to imstack
imstack = np.full([imsize, imsize, len(hemiList)], np.nan)
erstack = np.full([imsize, imsize, len(hemiList)], np.nan)
for ii in tqdm(range(0, len(hemiList)), desc="loading images", ncols=100, leave=True):
    img = tif.imread(batch_dir + hemiList.file_name[ii]) * scaling_coef
    imstack[:, :, ii] = img[:, :, 0]
    erstack[:, :, ii] = img[:, :, 1]
    # print(str(ii + 1) + ' of ' + str(len(hemiList)))
#
# # preview of correlation coefficient
# # covar = np.full((imsize, imsize), np.nan)
# corcoef = np.full((imsize, imsize), np.nan)
# corcoef_e = np.full((imsize, imsize), np.nan)
# corcoef_l = np.full((imsize, imsize), np.nan)
# sprank = np.full((imsize, imsize), np.nan)
#
# for ii in range(0, imsize):
#     for jj in range(0, imsize):
#         if imrange[jj, ii]:
#             # covar[jj, ii] = np.cov(hemiList.covariant, imstack[jj, ii, :])[0, 1]
#             corcoef[jj, ii] = np.corrcoef(hemiList.covariant, imstack[jj, ii, :])[0, 1]
#             corcoef_e[jj, ii] = np.corrcoef(hemiList.covariant, np.exp(-21.613288 * imstack[jj, ii, :]))[0, 1]
#             # corcoef_l[jj, ii] = np.corrcoef(hemiList.covariant, np.log(imstack[jj, ii, :]))[0, 1]
#             # sprank[jj, ii] = spearmanr(hemiList.covariant, imstack[jj, ii, :])[0]
#
#     print(ii)
#


# reshape imstack (as imstack_long) for optimization
imstack_long = imstack
imstack_long[np.isnan(imstack_long)] = 0  # careful here..
imstack_long = np.swapaxes(np.swapaxes(imstack_long, 1, 2), 0, 1).reshape(imstack_long.shape[2], -1)
imrange_long = imrange.reshape(imrange.size)

# imstack_long = imstack_long[valid, :]
# imstack_long = imstack_long[:, imrange_long]

# # optimization function
# def gbgf(x0):
#     # unpack parameters
#     sig = x0[0]  # standard deviation of angular gaussian in radians
#     intnum = x0[1]  # interaction number
#     phi_0 = x0[2]  # central phi in radians
#     theta_0 = x0[3]  # central theta in radians
#     offset = x0[4]
#
#     # calculate angle of each pixel from (phi_0, theta_0)
#     radist = 2 * np.arcsin(np.sqrt((np.sin((phi_0 - phi) / 2) ** 2) + np.sin(phi_0) * np.sin(phi) * (np.sin((theta_0 - theta) / 2) ** 2)))
#
#     # calculate gaussian angle weights
#     weights = np.exp(- 0.5 * (radist / sig) ** 2)  # gaussian
#     weights[np.isnan(phi)] = 0
#     weights = weights / np.sum(weights)
#
#     # calculate weighted mean of contact number for each ground points
#     w_stack = np.average(imstack_long, weights=weights.ravel(), axis=1)
#     # calculate corrcoef with snowfall transmittance over all ground points
#     w_corcoef_e = np.corrcoef(hemiList.covariant + offset, np.exp(-intnum * w_stack))[0, 1]
#
#    # return negative for minimization method (we want to maximize corrcoef)
#     return -w_corcoef_e
#
#
# Nfeval = 1
# def callbackF(Xi):
#     global Nfeval
#     print('{0:4d}   {1: 3.6f}   {2: 3.6f}   {3: 3.6f}   {4: 3.6f}   {5: 3.6f}   {6: 3.6f}'.format(Nfeval, Xi[0], Xi[1], Xi[2], Xi[3], Xi[4], gbgf(Xi)))
#     Nfeval += 1
#
# print('{0:4s}   {1:9s}   {2:9s}   {3:9s}   {4:9s}   {5:9s}   {6:9s}'.format('Iter', ' X1', ' X2', 'X3', 'X4', 'X5', 'f(X)'))
# x0 = np.array([0.11, 21.6, phi[96, 85], theta[96, 85], 0], dtype=np.double)
# x0 = np.array([9.73075682e-02, 1.53251521e+01, 1.20260398e-01, 5.40964306e+00, -1.21090673e-02])  # 19_045-19_050
# [xopt, fopt, gopt, Bopt, func_calls, grad_calls, warnflg] = \
#     fmin_bfgs(gbgf, x0, callback=callbackF, maxiter=5, full_output=True, retall=False)
# # xopt = np.array([0.1296497, 21.57953188, 96.95887751, 86.24391083])  # gaussian optimization,
# # fopt = -0.4744932

# from scipy.stats import vonmises
# from scipy.special import i0
# from scipy.stats import spearmanr, pearsonr
#
# def mcor(p0):
#     # unpack parameters
#     intnum = p0[0]
#
#     tx = np.exp(-intnum * imstack_long[:, imrange_long])
#
#     pcor = np.corrcoef(tx[valid, :].swapaxes(0, 1), covariant[valid].values, rowvar=True)
#
#     pearsonr(tx[valid, 1000], covariant[valid])
#     pcor = np.corrcoef(imstack_long.swapaxes(0, 1), covariant, rowvar=True)
#
#
#     # model snow accumulation with snowfall transmittance over all ground points
#     gaus_term = mm * np.exp(-gaus_intnum * gaus_stack)
#     # unif_term = nn * np.exp(-unif_intnum * unif_stack)
#
#     # snowacc = mm * np.exp(-intnum * w_stack) + bb
#
#     dswe = covariant
#
#     # calculate sum of square residuals
#     # ssres = np.sum((dswe - gaus_term - unif_term) ** 2)
#     ssres = np.sum((dswe - gaus_term) ** 2)
#     # ssres = np.sum((dswe - unif_term) ** 2)
#
#     return ssres
#
# def rsq(p0):
#     ssres = dwst(p0)
#
#     dswe = covariant
#
#     sstot = np.sum((dswe - np.mean(dswe)) ** 2)
#     return 1 - ssres / sstot

imstack_long_valid = imstack_long[valid, :]

def dwst(p0):
    # unpack parameters
    phi_0 = p0[0]  # central phi in radians
    theta_0 = p0[1]  # central theta in radians
    sig = p0[2]  # standard deviation of angular gaussian in radians
    mm = p0[3]
    gaus_intnum = p0[4]  # interaction number
    # nn = p0[5]
    # unif_intnum = p0[6]  # interaction number

    # # old!
    # sig = p0[0]  # standard deviation of angular gaussian in radians
    # gaus_intnum = p0[1]  # interaction number
    # phi_0 = p0[2]  # central phi in radians
    # theta_0 = p0[3]  # central theta in radians
    # mm = p0[4]
    # # bb = p0[5]

    # calculate angle of each pixel from (phi_0, theta_0)
    radist = np.arccos(np.cos(phi_0) * np.cos(phi) + np.sin(phi_0) * np.sin(phi) * np.cos(theta_0 - theta))
    # calculate gaussian angle weights
    gaus_weights = np.exp(- 0.5 * (radist / sig) ** 2)  # gaussian
    gaus_weights[np.isnan(phi)] = 0
    gaus_weights = gaus_weights / np.sum(gaus_weights)
    # calculate weighted mean of contact number for each ground points
    gaus_stack = np.average(imstack_long_valid, weights=gaus_weights.ravel(), axis=1)

    # unif_weights = (phi < 75 * np.pi / 180)
    # unif_stack = np.average(imstack_long, weights=unif_weights.ravel(), axis=1)

    # model snow accumulation with snowfall transmittance over all ground points
    gaus_term = mm * np.exp(-gaus_intnum * gaus_stack)
    # unif_term = nn * np.exp(-unif_intnum * unif_stack)

    # snowacc = mm * np.exp(-intnum * w_stack) + bb

    dswe = covariant[valid]

    # calculate sum of square residuals
    # ssres = np.sum((dswe - gaus_term - unif_term) ** 2)
    ssres = np.sum((dswe - gaus_term) ** 2)
    # ssres = np.sum((dswe - unif_term) ** 2)

    return ssres

def rsq(p0):
    ssres = dwst(p0)

    dswe = covariant

    sstot = np.sum((dswe - np.mean(dswe)) ** 2)
    return 1 - ssres / sstot

Nfeval = 1
def callbackF(Xi):
    global Nfeval
    print('{0:4d}   {1: 3.6f}   {2: 3.6f}   {3: 3.6f}   {4: 3.6f}   {5: 3.6f}   {6: 3.6f}   {7: 3.6f}'.format(Nfeval, Xi[0], Xi[1], Xi[2], Xi[3], Xi[4], dwst(Xi), rsq(Xi)))
    # print('{0:4d}   {1: 3.6f}   {2: 3.6f}   {3: 3.6f}   {4: 3.6f}   {5: 3.6f}   {6: 3.6f}   {7: 3.6f}   {8: 3.6f}   {9: 3.6f}'.format(Nfeval, Xi[0], Xi[1], Xi[2], Xi[3], Xi[4], Xi[5], Xi[6], dwst(Xi), rsq(Xi)))
    Nfeval += 1

print('{0:4s}   {1:9s}   {2:9s}   {3:9s}   {4:9s}   {5:9s}   {6:9s}   {7:9s}'.format('Iter', 'phi', 'theta', 'sig', 'mm', 'intnum','f(X)', 'R2'))
# print('{0:4s}   {1:9s}   {2:9s}   {3:9s}   {4:9s}   {5:9s}   {6:9s}   {7:9s}   {8:9s}   {9:9s}'.format('Iter', 'phi', 'theta', ' sig', 'mm', 'gaus_intnum', 'nn', 'unif_intnum', 'f(X)', 'R2'))


if date == "045-050":
    # p0 = np.array([0.11534765, 0.57799291, 0.11109643, 2.4170248, 3.68344911])  # 19_045-19_050, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.094308
    # p0 = np.array([0.11481182, 0.56503876, 0.10936873, 2.44018817, 3.71200706])  # 19_045-19_050, 045-050-052, min_ct >= 10, fnsd, no bb, 25% of data, r2 = 0.119853
    # p0 = np.array([0.12120457, 0.45225687, 0.11644756, 2.46708285, 3.47311711])  # 19_045-19_050, 045-050-052, min_ct >= 25, fnsd, no bb, 50% of data, r2 = 0.130916
    # p0 = np.array([0.11644756, 2.46708285, 0.12120457, 3.47311711, 0.45225687])  # 19_045-19_050, 045-050-052, min_ct >= 25, fnsd, no bb, 50% of data, r2 = 0.130916  # new format --
    p0 = np.array([0.13138135, 2.46542192, 0.1194041, 3.35773715, 0.52777705])  # 19_045-19_050, snow_on dem.25, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.107854

elif date == "050-052":
    # p0 = np.array([0.14113609, 0.24675274, 0.21223623, 2.46673482, 6.93602817])  # 19_050-19_052, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.085339
    # p0 = np.array([0.14024832, 0.25270547, 0.19313204, 2.49243517, 7.00353594])  # 19_050-19_052, 045-050-052, min_ct >= 10, fnsd, no bb, 25% of data, r2 = 0.108983
    # p0 = np.array([0.14959617, 0.27760338, 0.20224104, 2.58846094, 7.47697446])  # 19_050-19_052, 045-050-052, min_ct >= 25, fnsd, no bb, 50% of data, r2 = 0.170783
    # p0 = np.array([0.20224104, 2.58846094, 0.14959617, 7.47697446, 0.27760338])  # 19_050-19_052, 045-050-052, min_ct >= 25, fnsd, no bb, 50% of data, r2 = 0.170783 # new format (0.08115358061317013 all points no filter)
    # p0 = np.array([ 0.19831661, 2.46775433, 0.14027416, 6.90337943, 0.25090424, 0, 0])  # 19_050-19_052, snow-on, fnsd, 25% of data, r2 = 0.089205 # no uniform term
    # p0 = np.array([ 0.19831661,  2.46775433, 0, 0, 0, 1.70155981, -0.36045782])  # 19_050-19_052, snow-on, fnsd, 25% of data, r2 = 0.074600 # no gaussian term
    # p0 = np.array([ 0.19831661,  2.46775433, 0.14027416, 6.90337943, 0.25090424, 1.70155981, -0.36045782])  # 19_050-19_052, snow-on, fnsd, 25% of data, r2 = 0.074600 # no uniform term
    p0 = np.array([0.24854724, 2.39575035, 0.17155165, 6.97084751, 0.26603563]) # 19_050-19_052, snow-on dem.25, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.111375

# elif date == "19_045":
#     p0 = None
#
# elif date == "19_050":
#     # p0 = np.array([ 0.138614188,  0.690715658,  0.0936716022, 2.3379370836, 116.016191])  # 19_050, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.601032
#     p0 = np.array([0.0936716022, 2.3379370836, 0.138614188, 116.016191, 0.690715658, 0, 1])  # 19_050, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.601032
#     p0 = np.array([ 0.0920301084,  2.34857672,  0.164146886,  152.314633, 0.309102598, -162.167554,  0.404501947])  # 19_050, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.700743
# elif date == "19_052":
#     # p0 = np.array([0.14113609, 0.24675274, 0.21223623, 2.46673482, 6.93602817])  # 19_052, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = ??
#     p0 = np.array([0.0920301084,  2.34857672,  0.164146886,  152.314633, 0.309102598, -162.167554,  0.404501947])  # 19_050, 045-050-052, min_ct >= 0, fnsd, no bb, 25% of data, r2 = 0.700743
#     p0 = np.array([0.23405479, 2.51000856, -0.15646095, 31.59489217, 0.03522606, -29.17081887, 0.05226448])

# run optimization
[popt, fopt, gopt, Bopt, func_calls, grad_calls, warnflg] = \
    fmin_bfgs(dwst, p0, callback=callbackF, maxiter=50, full_output=True, retall=False)

u_out = (180 / np.pi, 180 / np.pi, 180 / np.pi, 1, 1)

p0 * u_out
rsq(p0)
#
# sig_out = xopt[0] * 180 / np.pi
# intnum_out = 1/xopt[1]
# phi_out = np.sqrt((xopt[2] - (imsize - 1)/2) ** 2 + (xopt[3] - (imsize - 1)/2) ** 2)
# theta_out = np.arctan2(-(xopt[3] - (imsize - 1)/2), -(xopt[2] - (imsize - 1)/2)) * 180 / np.pi
#



####### Visualization

# p0 = popt.copy()

phi_0 = p0[0]  # central phi in radians
theta_0 = p0[1]  # central theta in radians
sig = p0[2]  # standard deviation of angular gaussian in radians
mm = p0[3]
gaus_intnum = p0[4]  # interaction number
# nn = p0[5]
# unif_intnum = p0[6]

# bb = p0[5]
# bb = 0

# # old
# sig = p0[0]  # standard deviation of angular gaussian in radians
# intnum = p0[1]  # interaction number
# phi_0 = p0[2]  # central phi in radians
# theta_0 = p0[3]  # central theta in radians
# mm = p0[4]
# # bb = p0[5]
bb = 0

# calculate angle of each pixel from (phi_0, theta_0)
radist = np.arccos(np.cos(phi_0) * np.cos(phi) + np.sin(phi_0) * np.sin(phi) * np.cos(theta_0 - theta))
# calculate gaussian angle weights
gaus_weights = np.exp(- 0.5 * (radist / sig) ** 2)  # gaussian
gaus_weights[np.isnan(phi)] = 0
gaus_weights = gaus_weights / np.sum(gaus_weights)
# calculate weighted mean of contact number for each ground points
gaus_stack = np.average(imstack_long, weights=gaus_weights.ravel(), axis=1)

# unif_weights = (phi < 75 * np.pi / 180)
# unif_stack = np.average(imstack_long, weights=unif_weights.ravel(), axis=1)

# model snow accumulation with snowfall transmittance over all ground points
# transmittance = np.exp(-gaus_intnum * gaus_stack)
gaus_term = np.exp(-gaus_intnum * gaus_stack)
# unif_term = np.exp(-unif_intnum * unif_stack)

fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.12, left=0.12)
ax1 = fig.add_subplot(111)
if date == "045-050":
    ax1.set_title('$\Delta$SWE vs. directionally weighted snowfall transmission $T^{*}_{(x, y)}$\n Upper Forest, 14-19 Feb. 2019, 25cm resolution')
elif date == "050-052":
    ax1.set_title('$\Delta$SWE vs. directionally weighted snowfall transmission $T^{*}_{(x, y)}$\n Upper Forest, 19-21 Feb. 2019, 25cm resolution')
ax1.set_xlabel("$\Delta$SWE [mm]")
ax1.set_ylabel("$T^{*}_{(x, y)}$ [-]")
plt.scatter(covariant, gaus_term, s=2, alpha=.05)
#
# rbins = (np.array([8, 5.7]) * 20).astype(int)
# plotrange = [[np.nanquantile(covariant, .05), np.nanquantile(covariant, .95)],
#              [0, 1]]
#
# plt.hist2d(covariant, gaus_term, range=plotrange, bins=rbins, cmap="Blues")

mm_mod = np.array([np.nanmin(gaus_term), np.nanmax(gaus_term)])
plt.plot(mm_mod * mm + bb, mm_mod, c='Black', linestyle='dashed', linewidth=1.5)
plt.ylim(0, 1)
plt.xlim(-5, 10)
if date == "045-050":
    fig.savefig(plot_out_dir + "dSWE vs DWST 045-050.png")
elif date == "050-052":
    fig.savefig(plot_out_dir + "dSWE vs DWST 050-052.png")


# ####### calculate interaction scalar across hemisphere #######
# plt.scatter(np.log(hemi_var.covariant[hemi_var.training_set.values]), -w_stack, s=2, alpha=.25)
# np.nanmean(-np.log(hemi_var.covariant[hemi_var.training_set.values]) / w_stack)
#
# from scipy.optimize import curve_fit
#
# corcoef_each = np.full((imsize, imsize), np.nan)
# is_each = np.full((imsize, imsize), np.nan)
# gg_each = np.full((imsize, imsize), np.nan)
#
# for ii in range(0, imsize):
#     for jj in range(0, imsize):
#         if imrange[jj, ii]:
#             def expfunc(p1):
#                 return -np.corrcoef(hemi_var.covariant[hemi_var.training_set.values], np.exp(-p1 * imstack[jj, ii, :]))[0, 1]
#
#
#             [popt, ffopt, ggopt, BBopt, func_calls, grad_calls, warnflg] = \
#                 fmin_bfgs(expfunc,
#                           1,
#                           maxiter=100,
#                           full_output=True,
#                           retall=False)
#
#             is_each[jj, ii] = popt[0]
#             corcoef_each[jj, ii] = -ffopt
#             gg_each[jj, ii] = ggopt
#
#     print(ii)
#
# is_each_qc = is_each.copy()
# is_each_qc[gg_each > .00001] = np.nan
# is_each_qc[is_each_qc < 0] = np.nan
# is_each_qc[is_each_qc > 1000] = np.nan
#
# plt.imshow(is_each_qc)
# plt.imshow(gg_each)
# corcoef_each_qc = corcoef_each.copy()
# corcoef_each_qc[corcoef_each_qc == 1] = np.nan
# plt.imshow(corcoef_each_qc)
# plt.colorbar()
#
#
# # Here you give the initial parameters for p0 which Python then iterates over
# # to find the best fit
# jj = 90
# ii = 90
#
# popt, pcov = curve_fit(expfunc, w_stack, hemi_var.covariant[hemi_var.training_set.values], p0=(20.0), bounds=(0, np.inf))
#
# plt.scatter(hemi_var.covariant[hemi_var.training_set.values], np.exp(-popt[0] * w_stack), s=2, alpha=.25)

## plot optimization topography

# sigma

# sample optimization topography for sigma
v_list = np.linspace(0.0001, 25*np.pi/180, 100)  # sig
w_data = pd.DataFrame(columns={"sig", "r2"})
ii = 0
px = p0.copy()
for vv in v_list:

    px[2] = vv
    r2 = rsq(px)

    new_row = {"sig": vv,
               "r2": r2}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)

    ii += 1
    print(ii)

fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.15, left=0.15)
ax1 = fig.add_subplot(111)
if date == "045-050":
    ax1.set_title('Optimization of Gaussian weight function width $\sigma$\nUpper Forest, 14-19 Feb. 2019, 25cm resolution')
elif date == "050-052":
    ax1.set_title('Optimization of Gaussian weight function width $\sigma$\nUpper Forest, 19-21 Feb. 2019, 25cm resolution')
ax1.set_ylabel("$R^2$ for $\Delta$SWE vs. $T^{*}$")
ax1.set_xlabel("Standard deviation of Gausian weight function $\sigma$ [$^{\circ}$]")
plt.plot(w_data.sig * 180 / np.pi, w_data.r2)
plt.xlim(0, 25)
plt.ylim(0, .10)
fig.savefig(plot_out_dir + "optimization_gaussian_width_sigma_" + date + "_" + canopy + ".png")

#####
# interaction scalar
# sample optimization topography for mu*
v_list = np.linspace(0, 1, 100)  # mu*
w_data = pd.DataFrame(columns={"mu", "r2"})
ii = 0
px = p0.copy()
for vv in v_list:

    px[4] = vv
    r2 = rsq(px)

    new_row = {"mu": vv,
               "r2": r2}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)

    ii += 1
    print(ii)

fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.15, left=0.15)
ax1 = fig.add_subplot(111)
if date == "045-050":
    ax1.set_title('Optimization of snowfall absorbtion coefficient $\mu^*$\nUpper Forest, 14-19 Feb. 2019, 25cm resolution')
elif date == "050-052":
    ax1.set_title('Optimization of snowfall absorbtion coefficient $\mu^*$\nUpper Forest, 19-21 Feb. 2019, 25cm resolution')
ax1.set_ylabel("$R^2$ for $\Delta$SWE vs. modeled snow accumulation")
ax1.set_xlabel("snowfall absorbtion coefficient $\mu^*$ [-]")
plt.plot(w_data.mu, w_data.r2)
plt.xlim(0, 1)
plt.ylim(0, .10)
fig.savefig(plot_out_dir + "optimization_snow_absorption_mu_star_" + date + "_" + canopy + ".png")


################################################
## plot transmittance over hemisphere

## plot hemispherical footprint

# intnum = p0[4]
intnum = 1

# rerun corcoef_e with optimized transmission scalar
corcoef_e = np.full((imsize, imsize), np.nan)
for ii in range(0, imsize):
    for jj in range(0, imsize):
        if imrange[jj, ii]:
            corcoef_e[jj, ii] = np.corrcoef(covariant[valid], np.exp(-intnum * imstack[jj, ii, valid]))[0, 1]

    print(ii)

# prep divergent colormap
import matplotlib.colors as colors
# set the colormap and centre the colorbar

class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)
    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...

        # maintain equal intensity scaling on either side of midpoint
        dmid = (self.midpoint - self.vmin, self.vmax - self.midpoint)
        maxmid = np.max(dmid)
        r_min = self.midpoint - maxmid
        r_max = self.midpoint + maxmid
        c_low = (self.vmin - r_min) / (2 * maxmid)
        c_high = 1 + (r_max - self.vmax) / (2 * maxmid)
        x, y = [self.vmin, self.midpoint, self.vmax], [c_low, 0.5, c_high]

        # use vmin and vmax as extreme ends of colormap
        # x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]

        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))



# colormap parameters
set = corcoef_e  # this is what we are plotting
# val_min = np.nanmin(set)
scale = .25
val_min = -scale
val_mid = 0
# val_max = np.nanmax(set)
val_max = scale
# abs_max = np.max(np.abs([val_min, val_max]))
abs_max = scale
cmap = matplotlib.cm.RdBu

if date == "045-050":
    date_name = "14-19 Feb 2019"
elif date == "050-052":
    date_name = "19-21 Feb 2019"

if intnum == 1:
    trans_name = "light transmittance"
else:
    trans_name = "snowfall transmittance"

if canopy == "snow_off":
    canopy_name = "snow-off canopy"
elif canopy == "snow_on":
    canopy_name = "snow-on canopy"


# plot with axes
fig = plt.figure(figsize=(7, 7))
fig.suptitle(r"Correlation of $\Delta$SWE with " + trans_name + " over upper hemisphere\nUpper Forest, " + date_name + ", " + canopy_name)
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(set, cmap=cmap, clim=(val_min, val_max), norm=MidpointNormalize(vmin=-abs_max, midpoint=val_mid, vmax=abs_max))
ax0.axis("off")

# create polar axes and labels
ax = fig.add_subplot(111, polar=True, label="polar")
ax.set_facecolor("None")
ax.set_rmax(90)
ax.set_rgrids(np.linspace(0, 90, 7), labels=['', '15$^\circ$', '30$^\circ$', '45$^\circ$', '60$^\circ$', '75$^\circ$', '90$^\circ$'], angle=315)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_thetagrids(np.linspace(0, 360, 4, endpoint=False), labels=['N\n  0$^\circ$', 'W\n  270$^\circ$', 'S\n  180$^\circ$', 'E\n  90$^\circ$'])

# add colorbar
fig.subplots_adjust(top=0.95, left=0.1, right=0.75, bottom=0.05)
cbar_ax = fig.add_axes([0.85, 0.20, 0.03, 0.6])
fig.colorbar(im, cax=cbar_ax)
cbar_ax.set_ylabel("Pearson's correlation coefficient")

fig.savefig(plot_out_dir + "footprint_corcoef_" + date + "_" + canopy + "_mu_" + str(intnum) + ".png")


# plot with contours
# plot with axes
fig = plt.figure(figsize=(7, 7))
fig.suptitle("Correlation of $\Delta$SWE with " + trans_name + " over upper hemisphere\nUpper Forest, " + date_name + ", " + canopy_name)
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(set, cmap=cmap, clim=(val_min, val_max), norm=MidpointNormalize(vmin=-abs_max, midpoint=val_mid, vmax=abs_max))
ax0.axis("off")

# create polar axes and labels
ax = fig.add_subplot(111, polar=True, label="polar")
ax.set_facecolor("None")
ax.set_rmax(90)
ax.set_rgrids(np.linspace(0, 90, 7), labels=['', '15$^\circ$', '30$^\circ$', '45$^\circ$', '60$^\circ$', '75$^\circ$', '90$^\circ$'], angle=315)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_thetagrids(np.linspace(0, 360, 4, endpoint=False), labels=['N\n  0$^\circ$', 'W\n  270$^\circ$', 'S\n  180$^\circ$', 'E\n  90$^\circ$'])

# add colorbar
fig.subplots_adjust(top=0.95, left=0.1, right=0.75, bottom=0.05)
cbar_ax = fig.add_axes([0.85, 0.20, 0.03, 0.6])
fig.colorbar(im, cax=cbar_ax)
cbar_ax.set_ylabel("Pearson's correlation coefficient")

# contours
# ax.set_rgrids([])  # no rgrids
# ax.grid(False)  # no grid
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
matplotlib.rcParams["lines.linewidth"] = 1
CS = ax0.contour(set, np.linspace(-.4, .4, 9), colors="k")
plt.clabel(CS, inline=1, fontsize=8)

fig.savefig(plot_out_dir + "footprint_corcoef_" + date + "_" + canopy + "_mu_" + str(intnum) + "_contours.png")

## do it again, just plot transmittance (no dswe shenanigans)!

# intnum = p0[4]
intnum = 1

# rerun corcoef_e with optimized transmission scalar
hemi_mean_tx = np.full((imsize, imsize), np.nan)
hemi_sd_tx = np.full((imsize, imsize), np.nan)
corcoef_e = np.full((imsize, imsize), np.nan)
for ii in range(0, imsize):
    for jj in range(0, imsize):
        if imrange[jj, ii]:
            tx = np.exp(-intnum * imstack[jj, ii, valid])
            hemi_mean_tx[jj, ii] = np.mean(tx)
            hemi_sd_tx[jj, ii] = np.std(tx)
            # corcoef_e[jj, ii] = np.corrcoef(covariant[valid], tx)[0, 1]

    print(ii)

def add_polar_axes(r_label_color="black"):
    # create polar axes and labels
    ax = fig.add_subplot(111, polar=True, label="polar")
    ax.set_facecolor("None")
    ax.set_rmax(90)
    ax.set_rgrids(np.linspace(0, 90, 7), labels=['', '15$^\circ$', '30$^\circ$', '45$^\circ$', '60$^\circ$', '75$^\circ$', '90$^\circ$'], angle=315)
    [t.set_color(r_label_color) for t in ax.yaxis.get_ticklabels()]
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.linspace(0, 360, 4, endpoint=False), labels=['N\n  0$^\circ$', 'W\n  270$^\circ$', 'S\n  180$^\circ$', 'E\n  90$^\circ$'])


## plot mean tx
fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(hemi_mean_tx, cmap='Greys_r', clim=(0, 1))
ax0.axis("off")

add_polar_axes(r_label_color="white")

# add colorbar
fig.subplots_adjust(top=0.95, left=0.1, right=0.75, bottom=0.05)
cbar_ax = fig.add_axes([0.85, 0.20, 0.03, 0.6])
fig.colorbar(im, cax=cbar_ax)

## plot sd tx
fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(hemi_sd_tx, cmap='Greys_r')
ax0.axis("off")

add_polar_axes()

# add colorbar
fig.subplots_adjust(top=0.95, left=0.1, right=0.75, bottom=0.05)
cbar_ax = fig.add_axes([0.85, 0.20, 0.03, 0.6])
fig.colorbar(im, cax=cbar_ax)

# summarize by angle band
phi_step = 1  # in degrees
phi_bin = np.floor(phi * 180 / (np.pi * phi_step)) * phi_step  # similar to ceil, except for int values
bins = np.unique(phi_bin)
bins = bins[~np.isnan(bins)]
bin_count = len(bins)

theta_step = 90
theta_bin = (theta * 180 / np.pi + 45)
theta_bin[theta_bin >= 360] -= 360
theta_bin = np.floor(theta_bin / theta_step) * theta_step
t_bins = np.unique(theta_bin)  # N, E, S, W
t_bins = t_bins[~np.isnan(t_bins)]
t_bin_count = len(t_bins)


# tx_bin_mean = np.full(bin_count, np.nan)
# tx_bin_sd = np.full(bin_count, np.nan)
# for ii in range(0, bin_count):
#     bb = bins[ii]
#     mask = (phi_bin == bb)
#     tx_bin_mean[ii] = np.mean(hemi_mean_tx[mask])
#     tx_bin_sd[ii] = np.mean(hemi_sd_tx[mask])
#     # tx_std_bin_means[:, ii] = np.mean(tx_std_stack_long[:, mask], axis=1)
#
# plt.plot(bins, tx_bin_mean)
# lower_bound = tx_bin_mean - tx_bin_sd
# upper_bound = tx_bin_mean + tx_bin_sd
# plt.fill_between(bins, lower_bound, upper_bound, alpha=0.5)
# # plt.plot(bins, tx_bin_sd)

# by direction
tx_bin_mean = np.full([bin_count, t_bin_count], np.nan)
tx_bin_sd = np.full([bin_count, t_bin_count], np.nan)
for jj in range(0, t_bin_count):
    tt = t_bins[jj]
    for ii in range(0, bin_count):
        bb = bins[ii]
        mask = (phi_bin == bb) & (theta_bin == tt)
        tx_bin_mean[ii, jj] = np.mean(hemi_mean_tx[mask])
        tx_bin_sd[ii, jj] = np.mean(hemi_sd_tx[mask])
        # tx_std_bin_means[:, ii] = np.mean(tx_std_stack_long[:, mask], axis=1)


fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.15, left=0.15)
ax1 = fig.add_subplot(111)
plt.plot(bins, tx_bin_mean[:, 0], label="North")
plt.plot(bins, tx_bin_mean[:, 1], label="East")
plt.plot(bins, tx_bin_mean[:, 2], label="South")
plt.plot(bins, tx_bin_mean[:, 3], label="West")
plt.legend(loc="upper right")

lower_bound = tx_bin_mean - tx_bin_sd
upper_bound = tx_bin_mean + tx_bin_sd

plt.fill_between(bins, lower_bound[:, 0], upper_bound[:, 0], alpha=0.25)
plt.fill_between(bins, lower_bound[:, 1], upper_bound[:, 1], alpha=0.25)
plt.fill_between(bins, lower_bound[:, 2], upper_bound[:, 2], alpha=0.25)
plt.fill_between(bins, lower_bound[:, 3], upper_bound[:, 3], alpha=0.25)

plt.xlim(0, 90)
plt.ylim(0, 1)
ax1.set_ylabel("Light transmittance [-]")
ax1.set_xlabel("Angle from zenith [$^{\circ}$]")

# plt.plot(bins, tx_bin_sd[:, 0])
# plt.plot(bins, tx_bin_sd[:, 1])
# plt.plot(bins, tx_bin_sd[:, 2])
# plt.plot(bins, tx_bin_sd[:, 3])

#
# ###
# # plot radial distribution of corcoef_e
# sig = xopt[0]
# cpy = xopt[2]
# cpx = xopt[3]
# yid, xid = np.indices((imsize, imsize))
# radist = np.sqrt((yid - cpy) ** 2 + (xid - cpx) ** 2) * np.pi / 180
#
# radcor = pd.DataFrame({"phi": np.rint(np.ravel(radist) * 180 / np.pi).astype(int),
#                        "corcoef_e": np.ravel(corcoef_e)})
#
# radmean = radcor.groupby('phi').mean().reset_index(drop=False)
# radmean = radmean.assign(gaus=np.exp(- 0.5 * (radmean.phi * np.pi / (sig * 180)) ** 2))
#
# plt.plot(radmean.phi, radmean.corcoef_e)
# plt.plot(radmean.phi, radmean.gaus * np.nanmax(radmean.corcoef_e))
# plt.plot(radmean.phi, radmean.corcoef_e - radmean.gaus * np.nanmax(radmean.corcoef_e))
#
# ###
#
# maxcoords = np.where(corcoef_e == np.nanmax(corcoef_e))
# jj = maxcoords[0][0]
# ii = maxcoords[1][0]
#
# plt.scatter(hemiList.covariant, np.exp(-xopt[1] * imstack[jj, ii, :]), alpha=0.1, s=5)
#
# immid = ((imsize - 1)/2).astype(int)
# jj = immid
# ii = immid
# plt.scatter(hemiList.covariant, np.exp(-xopt[1] * imstack[jj, ii, :]), alpha=0.1, s=5)
# # cumulative weights... this is all messed
#
# plt.imshow(sprank, cmap=plt.get_cmap('Purples_r'))
# plt.colorbar()
#

# angle_lookup_covar.sqr_covar_weighted
# angle_lookup_covar.sort_values(phi)
# peace = angle_lookup_covar.loc[~np.isnan(angle_lookup_covar.covar), :]
# peace.loc[:, 'sqr_covar_weight_cumsum'] = np.cumsum(peace.sort_values('phi').sqr_covar_weight.values).copy()
#
# plt.scatter(peace.phi, peace.sqr_covar_weight_cumsum)

# plot scatter at coords


# p0 = popt.copy()

intnum = 1
ii = 85
jj = 97

ii = 80
jj = 13

ii = 90
jj = 90

# trans = np.exp(-intnum * imstack[jj, ii, :])
# cn = imstack[jj, ii, :]


fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.12, left=0.12)
ax1 = fig.add_subplot(111)
plt.scatter(cn, covariant, s=2, alpha=.05)
plt.scatter(cn[jj, ii, valid], func(cn, ma[jj, ii], mb[jj, ii], mc[jj, ii]), s=2, alpha=.25)
plt.scatter(cn, func(cn, ma[jj, ii], mb[jj, ii], mc[jj, ii]), s=2, alpha=.25)
plt.scatter(cn, func(cn, ma[jj, ii], -0.5, mc[jj, ii]), s=2, alpha=.25)
plt.scatter(cn, func(cn, ma[jj, ii], mb[jj, ii], 10), s=2, alpha=.25)
plt.scatter(cn, func(cn, 1, mb[jj, ii], mc[jj, ii]), s=2, alpha=.25)

## new curve fitting yikes!!!

from scipy.optimize import curve_fit

def func(x, a, b, c):
    return a * np.exp(-b * x) + c
## ma -- y intercept is ma + mc
## mb -- absorption coeficient, or how rapidly values converge to mc with increasing contact number
## mc -- asymptopic SWE at infinite contact number


coord_list = []
popt_list = []
pcov_list = []

p_start = (1, 0.5, 0)
p_bounds = ((-np.inf, 0, -np.inf), (np.inf, 10, np.inf))

for ii in range(0, imsize):
    for jj in range(0, imsize):
        if imrange[jj, ii]:
            if phi[jj, ii] * 180 / np.pi <= 75:
                coord_list.append((jj, ii))
                try:
                    popt, pcov = curve_fit(func, imstack[jj, ii, valid], covariant[valid], p0=p_start, bounds=p_bounds)
                except RuntimeError:
                    popt = np.nan
                    pcov = np.nan

                popt_list.append(popt)
                pcov_list.append(pcov)

                print((jj, ii))


# rerun corcoef_e with optimized transmission scalar
ma = np.full((imsize, imsize), np.nan)
mb = np.full((imsize, imsize), np.nan)
mc = np.full((imsize, imsize), np.nan)
for kk in range(0, len(coord_list)):
    jj, ii = coord_list[kk]
    if popt_list[kk] is not np.nan:
        ma[jj, ii], mb[jj, ii], mc[jj, ii] = popt_list[kk]
    print(kk)

fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(ma, cmap='RdBu', clim=(-1, 1))
ax0.axis("off")

fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(mb, cmap='Greys_r', clim=(0, 10))
ax0.axis("off")

fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
im = ax0.imshow(mc, cmap='Greys', clim=(4, 5))
ax0.axis("off")

# orthogonal distance regression


# nonlinear function to optimize
# def f(p, x):
#     return p[0] * np.exp(-p[1] * x) + p[2]

# lets restructure data to drop unused data

max_phi = 90

valid_angles = (phi * 180 / np.pi) <= max_phi
phi_valid = phi[valid_angles]
theta_valid = theta[valid_angles]
angles_valid = pd.DataFrame({"phi": phi_valid,
                             "theta": theta_valid})
angles_valid = pd.merge(angles_valid, angle_lookup, on=("phi", "theta"), how="left")

imstack_valid = imstack[valid_angles][:, valid]
erstack_valid = erstack[valid_angles][:, valid]
covariant_valid = covariant[valid]
covariant_error_valid = covariant_error[valid]

n_angle, n_xvar = np.shape(imstack_valid)

def w_opt(w0):

    # model to fix on per-angle basis
    def f_exp(p, x):
        return p[0] * np.exp(-w0[0] * x) + p[1]

    # null hypothesis function
    def f_h0(p, x):
        return p[0] + x * 0

    # define odr model
    nlm = odr.Model(f_exp)
    h0m = odr.Model(f_h0)

    # preallocate
    coord_list = []
    beta_list = []
    sd_beta_list = []
    res_var_list = []
    h0_res_var_list = []
    sum_square_list = []
    sum_square_eps_list = []
    stopreason_list = []

    for kk in range(n_angle):
        nlm_data = odr.RealData(imstack_valid[kk, :], covariant_valid, sx=np.sqrt(erstack_valid[kk, :]), sy=covariant_error_valid)  # errors as standard deviation
        # nlm_data = odr.Data(imstack_valid[kk, :], covariant_valid, wd=1. / (erstack_valid[kk, :]), we=1. / (covariant_error_valid ** 2))  # errors as weights
        nlm_odr = odr.ODR(nlm_data, nlm, beta0=[0., 4.])
        nlm_odr.set_job(fit_type=0)
        nlm_output = nlm_odr.run()

        h0_odr = odr.ODR(nlm_data, h0m, beta0=[4.])
        h0_odr.set_job(fit_type=0)
        h0_output = h0_odr.run()

        beta_list.append(nlm_output.beta)
        sd_beta_list.append(nlm_output.sd_beta)
        res_var_list.append(nlm_output.res_var)
        h0_res_var_list.append(h0_output.res_var)
        sum_square_list.append(nlm_output.sum_square)
        sum_square_eps_list.append(nlm_output.sum_square_eps)
        stopreason_list.append(nlm_output.stopreason)
        print(kk)


    # unpack outputs
    beta = np.full((imsize, imsize, 2), np.nan)
    beta_sd = np.full((imsize, imsize, 2), np.nan)
    convergence = np.full((imsize, imsize), False)
    res_var = np.full((imsize, imsize), np.nan)
    sum_square = np.full((imsize, imsize), np.nan)
    sum_square_eps = np.full((imsize, imsize), np.nan)
    r2 = np.full((imsize, imsize), np.nan)

    for kk in range(n_angle):
        jj = angles_valid.y_index[kk]
        ii = angles_valid.x_index[kk]
        beta[jj, ii, :] = beta_list[kk]
        beta_sd[jj, ii, :] = sd_beta_list[kk]
        convergence[jj, ii] = (stopreason_list[kk] == ['Sum of squares convergence'])
        res_var[jj, ii] = res_var_list[kk]
        sum_square[jj, ii] = sum_square_list[kk]
        sum_square_eps[jj, ii] = sum_square_eps_list[kk]
        r2[jj, ii] = 1 - res_var_list[kk] / h0_res_var_list[kk]
        # print(kk)

    # # aic = sum(valid) * np.log(res_var) + 2 * 2
    # aic = sum(valid) * np.log(np.array(res_var_list)) + 2
    # # aic = sum(valid) * np.log(np.array(sum_square_list) / sum(valid)) + 2
    #
    # delta = aic - np.nanmin(aic)
    # weights = np.exp(-delta / 2)
    # weights = weights / np.nansum(weights)

    res_var_sum = np.sum(res_var_list)
    global res_var_sum_global
    res_var_sum_global = res_var_sum

    return res_var_sum

Nfeval = 1
def callbackF(xi):
    global Nfeval
    print('{0:4d}   {1: 3.6f}   {2: 3.6f}'.format(Nfeval, xi[0], res_var_sum_global))
    Nfeval += 1

print('{0:4s}   {1:9s}   {2:9s}'.format('Iter', 'w0', 'rvs'))

# w0 = np.array([0.5])
# w0 = np.array([0.35988068])  # storm 2, 25% of data, phi <= 75, Bopt = np.array([[0.00092937]]), fopt = 117817.82946957053
w0 = np.array([0.370131])  # storm 2, 25% of data, phi <= 75, Bopt = np.array([[0.00092937]]), resvar = 23678.128482


[popt, fopt, gopt, Bopt, func_calls, grad_calls, warnflg] = \
    fmin_bfgs(w_opt, w0, callback=callbackF, maxiter=50, full_output=True, retall=False)


# now modeling dswe
bb = np.nanmean(beta[:, :, 1])
mm = np.nanmean(np.exp(-w0[0] * imstack[:, :, valid]) * beta[:, :, 0][:, :, np.newaxis], axis=(0, 1))
dswe = bb + mm

plt.scatter(dswe, covariant[valid], alpha=.25)

pt = (np.min(covariant[valid]), np.max(covariant[valid]))
plt.plot(pt, pt)

def weighted_avg_and_sstot(values, weights):
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    sstot = values.size * np.average((values-average)**2, weights=weights)
    return (average, sstot)

values = covariant_valid
weights = covariant_error_valid
inv_weights = 1 / covariant_error_valid ** 2
inv_weights = inv_weights / np.sum(inv_weights)
av, sstot = weighted_avg_and_sstot(covariant_valid, inv_weights)
np.mean(covariant_valid)
np.var(covariant_valid) * np.sum(valid)

# fig = plt.figure(figsize=(7, 7))
# #create axes in the background to show cartesian image
# ax0 = fig.add_subplot(111)
# im = ax0.imshow(convergence, cmap='Greys')
# ax0.axis("off")
#
# np.nansum(beta[:, :, 0])
#
fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
poof = np.nan
im = ax0.imshow(beta[:, :, 0], cmap='RdBu', clim=(-4, 4))
ax0.axis("off")

fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
poof = np.nan
im = ax0.imshow(beta[:, :, 1], cmap='Greys')
ax0.axis("off")
#
fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
poof = np.nan
im = ax0.imshow(beta[:, :, 0] + beta[:, :, 1], cmap='Greys', clim=(0, 10))
ax0.axis("off")
#
fig = plt.figure(figsize=(7, 7))
#create axes in the background to show cartesian image
ax0 = fig.add_subplot(111)
poof = np.nan
im = ax0.imshow(r2, cmap='Greys')
ax0.axis("off")


# nlm_output.pprint()

jj = 62
ii = 159

jj = 159
ii = 62

ii = 87
jj = 94

x = imstack[jj, ii, valid]
y = covariant[valid]
fig = plt.figure()
fig.subplots_adjust(top=0.90, bottom=0.12, left=0.12)
ax1 = fig.add_subplot(111)
plt.scatter(x, y, s=2, alpha=.05)
# plt.errorbar(x, y, xerr=erstack[jj, ii, valid], yerr=covariant_error[valid]**2, fmt='o', alpha=0.25)
# plt.errorbar(x, y, yerr=covariant_error[valid]**2, fmt='o', alpha=0.05)
plt.scatter(x, f_exp(beta[jj, ii, :], x), s=2, alpha=.25, c='g')
# plt.scatter(np.exp(-nlm_output.beta[1]*x), y, s=2, alpha=.05)
# plt.scatter(np.exp(-nlm_output.beta[1]*x), f(nlm_output.beta, x), s=2, alpha=.25)

plt.scatter(covariant_valid, covariant_error_valid,  alpha=.05)