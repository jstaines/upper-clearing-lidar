import rastools
import numpy as np
import pandas as pd
import tifffile as tif
from scipy.stats import spearmanr

batch_dir = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_hemi_uf_.25m_180px\\outputs\\'
# batch_dir = 'C:\\Users\\jas600\\workzone\\data\\hemigen\\mb_15_1m_pr.15_os10\\outputs\\'

batch_type = 'lin'  # 'exp', 'log', 'lin'

if batch_type == 'log':
    covar_out = batch_dir + "phi_theta_lookup_log_covar_training.csv"
    weighted_cv_out = batch_dir + "rshmetalog_log_weighted_cv.csv"
elif batch_type == 'exp':
    covar_out = batch_dir + "phi_theta_lookup_exp_covar_training.csv"
    weighted_cv_out = batch_dir + "rshmetalog_exp_weighted_cv.csv"
elif batch_type == 'lin':
    covar_out = batch_dir + "phi_theta_lookup_lin_covar_training.csv"
    weighted_cv_out = batch_dir + "rshmetalog_lin_weighted_cv.csv"


scaling_coef = 0.19546

# load img meta
hemimeta = pd.read_csv(batch_dir + 'rshmetalog.csv')

imsize = hemimeta.img_size_px[0]

# merge with covariant
# var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\19_045-19_050\\dswe_19_045-19_050_r.25m.tif'
# var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\19_050-19_052\\dswe_19_050-19_052_r.25m.tif'
var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dSWE\\19_045-19_052\\dswe_19_045-19_052_r.25m.tif'
# var_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\mb_65\\dHS\\19_045-19_050\\dhs_19_045-19_050_r.25m.tif'
var = rastools.raster_to_pd(var_in, 'covariant')
hemi_var = pd.merge(hemimeta, var, left_on=('x_utm11n', 'y_utm11n'), right_on=('x_coord', 'y_coord'), how='inner')

# load angle template
angle_lookup = pd.read_csv(batch_dir + "phi_theta_lookup.csv")
phi = np.full((imsize, imsize), np.nan)
phi[(np.array(angle_lookup.x_index), np.array(angle_lookup.y_index))] = angle_lookup.phi * 180 / np.pi
max_phi = 90
# calculate radius to avoid pixels outside of circle
imrange = np.full((imsize, imsize), False)
imrange[phi <= max_phi] = True

# filter to desired images
#hemiList = hemi_swe.loc[(hemi_swe.swe.values >= 0) & (hemi_swe.swe.values <= 150), :]
# delineate training set and test set
set_param = np.random.random(len(hemi_var))  # ommit this line if only reloading the covariant
hemi_var.loc[:, 'training_set'] = set_param < .25
hemiList = hemi_var.loc[hemi_var.training_set, :].reset_index()


imstack = np.full([imsize, imsize, len(hemiList)], np.nan)
for ii in range(0, len(hemiList)):
    imstack[:, :, ii] = tif.imread(batch_dir + hemiList.file_name[ii])[:, :, 1] * scaling_coef
    print(str(ii + 1) + ' of ' + str(len(hemiList)))

if batch_type == 'log':
    imstack = np.log(imstack)
elif batch_type == 'exp':
    imstack = np.exp(-imstack)


# covar = np.full((imsize, imsize), np.nan)
corcoef = np.full((imsize, imsize), np.nan)
corcoef_e = np.full((imsize, imsize), np.nan)
corcoef_l = np.full((imsize, imsize), np.nan)
sprank = np.full((imsize, imsize), np.nan)

for ii in range(0, imsize):
    for jj in range(0, imsize):
        if imrange[jj, ii]:
            # covar[jj, ii] = np.cov(hemiList.covariant, imstack[jj, ii, :])[0, 1]
            corcoef[jj, ii] = np.corrcoef(hemiList.covariant, imstack[jj, ii, :])[0, 1]
            # corcoef_e[jj, ii] = np.corrcoef(hemiList.covariant, np.exp(-imstack[jj, ii, :]))[0, 1]
            # corcoef_l[jj, ii] = np.corrcoef(hemiList.covariant, np.log(imstack[jj, ii, :]))[0, 1]
            sprank[jj, ii] = spearmanr(hemiList.covariant, imstack[jj, ii, :])[0]

    print(ii)

########
np.nanmax(corcoef_e)
np.nanmin(corcoef_l)
np.nanmin(corcoef)
np.nanmin(sprank)

np.where(corcoef_e == np.nanmax(corcoef_e))
np.where(corcoef_l == np.nanmin(corcoef_l))
np.where(corcoef == np.nanmin(corcoef))
np.where(sprank == np.nanmin(sprank))
########

# methods for weighting
imstack[np.isnan(imstack)] = 0  # careful here..
imstack = np.swapaxes(np.swapaxes(imstack, 1, 2), 0, 1).reshape(imstack.shape[2], -1)


# phi threshhold
t_list = np.arange(0, 90, 5)
w_data = pd.DataFrame(columns={"threshold", "corcoef", "sprank"})

for tt in t_list:
    weights = np.full((imsize, imsize), 0)
    weights[phi <= tt] = 1
    weights = weights / np.sum(weights)

    w_stack = np.average(imstack, weights=weights.ravel(), axis=1)

    w_corcoef = np.corrcoef(hemiList.covariant, w_stack)[0, 1]
    w_sprank = spearmanr(hemiList.covariant, w_stack)[0]

    new_row = {"threshold": tt,
               "corcoef": w_corcoef,
               "sprank": w_sprank}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)

# phi dist from max
max_coord = np.where(corcoef == np.nanmin(corcoef))

yid, xid = np.indices((imsize, imsize))
radist = np.sqrt((yid - max_coord[0][0]) ** 2 + (xid - max_coord[1][0]) ** 2) * np.pi / 180

p_list = np.linspace(0, 20, 101)
w_data = pd.DataFrame(columns={"power", "corcoef", "sprank"})

for pp in p_list:
    # # cos power
    # weights = np.cos(radist)
    # weights[weights < 0] = 0
    # weights[np.isnan(phi)] = 0
    # weights = weights ** pp

    # normal distribution
    weights = np.exp(- 0.5 * (pp * radist) ** 2)
    weights[np.isnan(phi)] = 0
    weights = weights ** pp

    weights = weights / np.sum(weights)

    w_stack = np.average(imstack, weights=weights.ravel(), axis=1)

    w_corcoef = np.corrcoef(hemiList.covariant, w_stack)[0, 1]
    w_sprank = spearmanr(hemiList.covariant, w_stack)[0]

    new_row = {"power": pp,
               "corcoef": w_corcoef,
               "sprank": w_sprank}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)


# coef threshhold
t_list = np.linspace(np.nanmin(corcoef), 0, 20)
w_data = pd.DataFrame(columns={"threshold", "corcoef", "sprank", "count"})

for tt in t_list:
    weights = np.full((imsize, imsize), 0)
    weights[corcoef <= tt] = 1
    count = np.sum(weights)
    weights = weights / np.sum(weights)

    w_stack = np.average(imstack, weights=weights.ravel(), axis=1)

    w_corcoef = np.corrcoef(hemiList.covariant, w_stack)[0, 1]
    w_sprank = spearmanr(hemiList.covariant, w_stack)[0]

    new_row = {"threshold": tt,
               "corcoef": w_corcoef,
               "sprank": w_sprank,
               "count": count}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)

# weighted coef threshhold
t_list = np.linspace(np.nanmin(corcoef), 0, 20)
w_data = pd.DataFrame(columns={"threshold", "corcoef", "sprank", "count"})

for tt in t_list:
    weights = np.full((imsize, imsize), 0.0)
    weights[corcoef <= tt] = -corcoef[corcoef <= tt]
    # weights[corcoef <= tt] = corcoef[corcoef <= tt] ** 2
    count = np.sum(corcoef <= tt)
    weights = weights / np.sum(weights)

    w_stack = np.average(imstack, weights=weights.ravel(), axis=1)

    w_corcoef = np.corrcoef(hemiList.covariant, w_stack)[0, 1]
    w_sprank = spearmanr(hemiList.covariant, w_stack)[0]

    new_row = {"threshold": tt,
               "corcoef": w_corcoef,
               "sprank": w_sprank,
               "count": count}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)

# weighted sprank threshhold
t_list = np.linspace(np.nanmin(sprank), 0, 20)
w_data = pd.DataFrame(columns={"threshold", "corcoef", "sprank", "count"})

for tt in t_list:
    weights = np.full((imsize, imsize), 0.0)
    weights[sprank <= tt] = -sprank[sprank <= tt]
    count = np.sum(sprank <= tt)
    weights = weights / np.sum(weights)

    w_stack = np.average(imstack, weights=weights.ravel(), axis=1)

    w_corcoef = np.corrcoef(hemiList.covariant, w_stack)[0, 1]
    w_sprank = spearmanr(hemiList.covariant, w_stack)[0]

    new_row = {"threshold": tt,
               "corcoef": w_corcoef,
               "sprank": w_sprank,
               "count": count}
    w_data = w_data.append(new_row, ignore_index=True, verify_integrity=True)



# calculate weights by sqr or abs method
angle_lookup_covar = angle_lookup.copy()

angle_lookup_covar.loc[:, 'covar'] = localCovar[angle_lookup_covar.y_index.values, angle_lookup_covar.x_index.values]
angle_lookup_covar.loc[:, "abs_covar"] = np.abs(angle_lookup_covar.covar)
angle_lookup_covar.loc[:, "abs_covar_weight"] = angle_lookup_covar.covar / np.sum(angle_lookup_covar.loc[:, "abs_covar"])
angle_lookup_covar.loc[:, "sqr_covar"] = angle_lookup_covar.covar ** 2
angle_lookup_covar.loc[:, "sqr_covar_weight"] = angle_lookup_covar.covar / np.sum(angle_lookup_covar.loc[:, "sqr_covar"])

# write weights to file
angle_lookup_covar.to_csv(covar_out, index=False)

# Calculate weighted value for all images
abs_weight = np.full([imsize, imsize], np.nan)
abs_weight[(angle_lookup_covar.y_index.values, angle_lookup_covar.x_index.values)] = angle_lookup_covar.abs_covar_weight.values

sqr_weight = np.full([imsize, imsize], np.nan)
sqr_weight[(angle_lookup_covar.y_index.values, angle_lookup_covar.x_index.values)] = angle_lookup_covar.sqr_covar_weight.values

hemi_var.loc[:, "cv_abs_weighted"] = np.nan
hemi_var.loc[:, "cv_sqr_weighted"] = np.nan

for ii in range(0, len(hemi_var)):
    temp_im = tif.imread(batch_dir + hemi_var.file_name[ii])[:, :, 1] * scaling_coef
    if batch_type == 'log':
        temp_im = np.log(temp_im)
    elif batch_type == 'exp':
        temp_im = np.exp(-temp_im)
    hemi_var.cv_abs_weighted[ii] = np.nansum(-1 * temp_im * abs_weight)
    hemi_var.cv_sqr_weighted[ii] = np.nansum(-1 * temp_im * sqr_weight)
    print(str(ii + 1) + ' of ' + str(len(hemi_var)))

hemi_var.to_csv(weighted_cv_out, index=False)


import matplotlib
matplotlib.use('Qt5Agg')
# matplotlib.use('TkAgg')
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


figout = batch_dir + 'covar_plot.png'


fig = plt.figure()
a = fig.subplots()
# imgplot = plt.imshow(localCovar, cmap=plt.get_cmap('cividis_r'))
imgplot = plt.imshow(localCovar, cmap=plt.get_cmap('Purples_r'))
plt.axis('off')
plt.colorbar()


## visualize weights
plt.imshow(abs_weight, cmap=plt.get_cmap('Purples_r'))
plt.imshow(sqr_weight, cmap=plt.get_cmap('Purples_r'))


# load data
data_in ='C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\ray_sampling\\batches\\lrs_hemi_uf_.25m_180px\\outputs\\rshmetalog_weighted_cv.csv'
hemi_var = pd.read_csv(data_in)


# all points
plt.scatter(hemi_var.covariant, hemi_var.log_cn_weighted)
# training set
plt.scatter(hemi_var.covariant[hemi_var.training_set.values], -hemi_var.log_cn_abs_weighted[hemi_var.training_set.values], s=1, alpha=.25)
# test set
plt.scatter(hemi_var.covariant[~hemi_var.training_set.values], -hemi_var.log_cn_abs_weighted[~hemi_var.training_set.values], s=1, alpha=.25)

plt.scatter(hemi_var.covariant[~hemi_var.training_set.values], -hemi_var.cv_sqr_weighted[~hemi_var.training_set.values], s=1, alpha=.25)

plt.scatter(hemi_var.covariant[hemi_var.training_set.values], w_stack, s=1, alpha=.25)

## plot of sd with angle
fig = plt.figure()
# fig.subplots_adjust(top=0.8)
ax1 = fig.add_subplot(111)
ax1.set_ylabel("Pearson's Correlation Coeficient\nfor Canopy Contact Number and dSWE")
ax1.set_xlabel("Standard deviation of Gausian Contact Number field of view [degrees]\nCentered at hemisspherical maximum")
ax1.set_title('Optimization of Canopy field of view')

plt.plot(180 / (np.pi * w_data.power), w_data.corcoef)
# plt.plot(180 / (np.pi * w_data.power), w_data.sprank)
plt.xlim(0, 180)


plt.imshow(sprank, cmap=plt.get_cmap('Purples_r'))
plt.colorbar()

# divergent colormap

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
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

val_min = np.nanmin(sprank)
val_max = np.nanmax(sprank)
val_mid = 0
cmap = matplotlib.cm.RdBu_r

plt.imshow(corcoef, cmap=cmap, clim=(val_min, val_max), norm=MidpointNormalize(midpoint=val_mid, vmin=val_min, vmax=val_max))
plt.colorbar()
plt.show()

ii = 95
jj = 86
plt.scatter(hemiList.covariant, np.exp(-imstack[jj, ii, :] * 50), alpha=0.05, s=5)
# cumulative weights... this is all messed

# angle_lookup_covar.sqr_covar_weighted
# angle_lookup_covar.sort_values(phi)
# peace = angle_lookup_covar.loc[~np.isnan(angle_lookup_covar.covar), :]
# peace.loc[:, 'sqr_covar_weight_cumsum'] = np.cumsum(peace.sort_values('phi').sqr_covar_weight.values).copy()
#
# plt.scatter(peace.phi, peace.sqr_covar_weight_cumsum)