# toolkit for geographical analysis

# histograms
import laslib
import numpy as np
import pandas as pd

def pnt_sample_semivar(pts_1, vals_1, dist_inv_func, n_samples, n_iters=1, pts_2=None, vals_2=None, self_ref=False):
    if pts_2 is None:
        pts_2 = pts_1

    if vals_2 is None:
        vals_2 = vals_1

    # select a set of points at random
    samps = np.random.randint(0, high=pts_1.__len__(), size=n_samples)

    # sample target distances according to distribution
    unif_samps = np.random.random((n_samples, n_iters))
    targ_dist = dist_inv_func(unif_samps)

    # preallocate distance and difference vectors
    true_dist = np.full((n_samples, n_iters), np.nan)
    dv = np.full((n_samples, n_iters), np.nan)

    for ii in range(0, n_samples):
        # for each sample calculate distances to all points
        dd = np.sqrt(np.sum((pts_2 - pts_1[samps[ii], :]) ** 2, axis=1))
        # dd = np.sqrt((pts_2.x - pts_1.x[samps[ii]]) ** 2 + (pts_2.y - pts_1.y[samps[ii]]) ** 2)
        for jj in range(0, n_iters):
            # for each iteration, find the point with distance closest to the corresponding target distance
            idx = (np.abs(dd - targ_dist[ii, jj])).argmin()
            # record the actual distance between points
            true_dist[ii, jj] = dd[idx]
            # record value difference
            dv[ii, jj] = vals_2[idx] - vals_2[samps[ii]]
        print(ii + 1)

    df = pd.DataFrame({'dist': true_dist.reshape(n_samples * n_iters),
                       'dvals': dv.reshape(n_samples * n_iters)})
    if not self_ref:
        # remove self-referencing values
        df = df[df.dist != 0]

    unif_bounds = (np.min(unif_samps), np.max(unif_samps))  # not perfect, as target distances do not necesarily equal true distances.

    return df, unif_bounds

def bin_summarize(df, dist_inv_func, bounds, bin_count):
    dd = df.dist
    vv = df.dvals

    # calculate bins according to dist_inv_func
    bins = dist_inv_func(np.linspace(bounds[0], bounds[1], bin_count + 1))

    bin_mid = (bins[0:-1] + bins[1:]) / 2
    # bin df according to a
    v_groups = vv.groupby(np.digitize(dd, bins[0:-1]))
    d_groups = dd.groupby(np.digitize(dd, bins[0:-1]))
    stats = pd.DataFrame({'bin_low': bins[0:-1],
                          'bin_mid': bin_mid,
                          'bin_high': bins[1:],
                          'n': 0,
                          'mean_dist': np.nan,
                          'mean_bias': np.nan,
                          'stdev': np.nan})

    # report groups with counts of 0
    non_empty = np.array(v_groups.count().index) - 1
    stats.loc[non_empty, 'n'] = np.array(v_groups.count())
    stats.loc[non_empty, 'mean_dist'] = np.array(d_groups.mean())
    stats.loc[non_empty, 'mean_bias'] = np.array(v_groups.mean())
    stats.loc[non_empty, 'stdev'] = np.array(v_groups.std())

    return stats

# semivar (self referencing error with distance)

# # las example
# las_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LAS\\19_149_UF.las'
# pts_xyz = laslib.las_xyz_load(las_in, keep_class=2)
# pts = pts_xyz[:, [0, 1]]
# vals = pts_xyz[:, 2]
# # pts = pd.DataFrame(data=pts, columns=['x', 'y', 'z'])
#
# df, unif_bounds = geotk.pnt_sample_semivar(pts, vals, linear_ab, 10, 100)
# stats = geotk.bin_summarize(df, linear_ab, unif_bounds, 25)

# plot
