from libraries import raslib
import vaex
import matplotlib.pylab as plt
import numpy as np


# products to import

# snow depth .10m
hs_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.04m.tif"
dft_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\DNT\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_kho_distance_.10m.tif"
hs_10_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.10m.tif"

hs_hdf5 = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.04m.hdf5"
hs_dft_hdf5 = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.04m._dft.hdf5"

hs = raslib.raster_load(hs_in)
# dft = rastools.raster_load(dft_in)

# send hs to hdf5
raslib.raster_to_hdf5(hs_in, hs_hdf5, "hs_04m")

# sample site
# create raster of false values
site_shp_path = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\site_library\\sub_plot_library\\forest_upper.shp"
site_raster_path ="C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\site_library\\upper_forest_poly_UTM11N.tif"

template = raslib.raster_load(hs_in)
template.data = np.full([template.rows, template.cols], 0)
template.no_data = 0
raslib.raster_save(template, site_raster_path, data_format="int16")
# burn in upper forest site as true values
raslib.raster_burn(site_raster_path, site_shp_path, 1)

# sample rasters
raslib.hdf5_sample_raster(hs_hdf5, hs_dft_hdf5, [dft_in, site_raster_path, hs_10_in], sample_col_name=["dft", "uf", "hs_01m"])

##### Plotting #####
df = vaex.open(hs_dft_hdf5, 'r')
df.get_column_names()
no_data = -9999

df_uf = df[df.uf == 1]

dft = df_uf[df_uf.dft != no_data]
count_dft_all = dft.count(binby=dft.dft, limits=[0, 5], shape=100)/dft.length()
hs_samp = dft[dft.hs_04m != no_data]
count_dft_sampled = hs_samp.count(binby=hs_samp.dft, limits=[0, 5], shape=100)/hs_samp.length()

fig, ax = plt.subplots()
ax.plot(np.linspace(0, 5, 100), count_dft_all)
ax.plot(np.linspace(0, 5, 100), count_dft_sampled)
ax.set(xlabel='Relative frequency', ylabel='Distance to Nearest Tree -- DNT (m)',
       title='Normalized distributions of DNT for all points (blue) and snow-depth sampled points (orange)')
ax.grid()
plt.show()

# difference
plt.plot(np.linspace(0, 5, 100), count_dft_all - count_dft_sampled)
plt.show()

hs_samp.plot(hs_samp.dft, hs_samp.hs__04m, shape=300, vmax=0.6)
hs_samp.plot(hs_samp.hs_04m, hs_samp.hs_01m)

count_hs_sampled = hs_samp.count(binby=hs_samp.hs, limits=[0, 0.6], shape=1000)/hs_samp.length()
plt.plot(np.linspace(0, 0.6, 1000), count_hs_sampled)
count_dem_sampled = hs_samp.count(binby=hs_samp.dem, limits=[1828, 1838], shape=10000)/hs_samp.length()
plt.plot(np.linspace(1828, 1838, 10000), count_dem_sampled)

df.close()

###
hs_ras = df.hs.values.reshape([hs.rows, hs.cols])
dft_ras = df.dft.values.reshape([hs.rows, hs.cols])
dft_ras[dft_ras == -9999] = 0
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
fig1 = plt.imshow(hs_ras, interpolation='nearest')
fig2 = plt.imshow(dft_ras, interpolation='nearest')

###
# LPM plotting
import holoviews as hv
import datashader as ds
import datashader.transfer_functions as tf
import holoviews.operation.datashader as hd
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import pandas as pd

hv.extension("bokeh", "matplotlib")
hv.output(backend="matplotlib")


hs_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.25m.tif"
lpm_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LPM\\19_149_snow_off_LPM-first_30degsa_0.25m.tif"

# load images
hs = raslib.raster_load(hs_in)
lpmf = raslib.raster_load(lpm_in)

# check projections
hs.T0
lpmf.T0

# define inputs
parent = hs
child = lpmf
# create template of sample points
samples = parent.data.copy()

# create affine transform
x, y = np.ogrid[0:parent.rows, 0:parent.cols]
parentindex = np.where(np.full_like(parent.data, True))
geocoords = parent.T1 * (parentindex[0], parentindex[1])
childindex = np.rint(~child.T1 * (geocoords[0], geocoords[1])).astype(int)
in_bounds = (childindex[0] >= 0) & (childindex[0] < child.rows) & (childindex[1] >= 0) & (childindex[1] < child.cols)
child_in_bounds = (childindex[0][in_bounds], childindex[1][in_bounds])
sample_values = child.data[child_in_bounds]

reshape_values = np.full_like(parentindex[0], parent.no_data)
reshape_values[in_bounds] = sample_values
child_reshaped = np.reshape(reshape_values, parent.data.shape)

plot_data = pd.DataFrame({"hs": parent.data.reshape(parent.rows*parent.cols),
                          "lpmf": child_reshaped.reshape(parent.rows*parent.cols)})

plot_data[plot_data == parent.no_data] = np.nan
plot_data = plot_data[~np.any(np.isnan(plot_data), axis=1)]

cvs = ds.Canvas(plot_width=400, plot_height=400)
agg = cvs.points(plot_data, "hs", "lpmf", ds.count())
hd.datashade(plot_data)
hd.shade(hv.Image(agg))
hv.RGB(np.array(tf.shade(agg).to_pil()))

tf.Image(tf.shade(agg))

import holoviews as hv
hv.extension('bokeh')
from bokeh.plotting import figure, output_file, show

output_file('test_bokeh.html')
p = figure(plot_width=400, plot_height=400)
p.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.6], color='red')
plot = plot_data.hvplot(kind='scatter', x='hs', y='lpmf', datashade=True)
show(hv.render(plot))
show(p)

# test bokeh
import numpy as np
import pandas as pd
import holoviews as hv
hv.extension("bokeh")
from bokeh.plotting import show

data = np.random.normal(size=[50, 2])
df = pd.DataFrame(data=data, columns=['col1', 'col2'])

plot = df.hvplot(kind="scatter", x="col1", y="col2")
show(hv.render(plot))


# basic datashader
import datashader as ds
import pandas as pd
import numpy as np
import datashader.transfer_functions as tf
from datashader.utils import export_image

hs_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_052\\hs_19_052_res_.10m.tif"
dnt_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\DNT\\19_149_snow_off_627975_5646450_spike_free_chm_.10m_kho_distance_.10m.tif"
img_out = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\graphics\\ds_test_hs_vs_dnt.png"

# load parent
parent = raslib.raster_to_pd(hs_in, 'hs')
merged = raslib.pd_sample_raster(parent, dnt_in, 'dnt')

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.scatter(merged.hs, merged.dnt)

cvs = ds.Canvas(plot_width=400, plot_height=400)
agg = cvs.points(data, 'hs', 'dnt', agg=ds.count('dnt'))
img = tf.shade(agg, cmap=['lightblue', 'darkblue'], how='log')
export_image(img, img_out)
#####

# datashader + holoviews + matplotlib
import matplotlib
matplotlib.use('TkAgg')
import holoviews as hv
import holoviews.operation.datashader as hd
hd.shade.cmap=["lightblue", "darkblue"]
hv.extension("matplotlib")
hv.output(backend='matplotlib')
#agg = ds.Canvas().points(df,'x','y')
agg = ds.Canvas().points(data, 'hs', 'dnt')

# fig = plt.imshow(agg.data, interpolation='nearest', cmap='binary_r')
# plt.colorbar()
# plt.title('hs vs. dnt')
# plt.show()

tt = hd.shade(hv.Image(agg))
hv.RGB(np.array(tf.shade(agg).to_pil()))
#####

points = hv.Points(data.loc[:, ['hs', 'dnt']])
hd.datashade(points)

# datashader + holoviews + bokeh
hv.extension("bokeh")
hv.output(backend="bokeh")
hd.datashade(data)

dnt = raslib.raster_load(dnt_in)
dnt_pts = np.where(dnt.data != dnt.no_data)
dnt_coords = dnt.T1 * dnt_pts




df = pd.read_csv(traj_in)

cvs = ds.Canvas(plot_width=400, plot_height=400)
agg = cvs.points(df, 'Easting[m]', 'Northing[m]', agg=ds.mean('Height[m]'))
img = tf.shade(agg, cmap=['lightblue', 'darkblue'], how='log')
export_image(img, img_out)

### simple scatter plot

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


hs_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\products\\hs\\19_045\\hs_19_045_res_.25m.tif"
lpm_in = "C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\LPM\\19_149_snow_off_LPM-canopy_30degsa_0.25m.tif"

# load images
hs = raslib.raster_load(hs_in)
lpmc = raslib.raster_load(lpm_in)

# check projections
hs.T0
lpmc.T0

# define inputs
parent = hs
child = lpmc
# create template of sample points
samples = parent.data.copy()

# create affine transform
x, y = np.ogrid[0:parent.rows, 0:parent.cols]
parentindex = np.where(np.full_like(parent.data, True))
geocoords = parent.T1 * (parentindex[0], parentindex[1])
childindex = np.rint(~child.T1 * (geocoords[0], geocoords[1])).astype(int)
in_bounds = (childindex[0] >= 0) & (childindex[0] < child.rows) & (childindex[1] >= 0) & (childindex[1] < child.cols)
child_in_bounds = (childindex[0][in_bounds], childindex[1][in_bounds])
sample_values = child.data[child_in_bounds]

reshape_values = np.full_like(parentindex[0], np.nan)
reshape_values[in_bounds] = sample_values
child_reshaped = np.reshape(reshape_values, parent.data.shape)

plot_data = pd.DataFrame({"hs": parent.data.reshape(parent.rows*parent.cols),
                          "lpmc": child_reshaped.reshape(parent.rows*parent.cols)})

plot_data[plot_data == parent.no_data] = np.nan
plot_data = plot_data[~np.any(np.isnan(plot_data), axis=1)]


fig = plt.figure(figsize=(10, 10), dpi=100)
ax = plt.axes([0., 0., 1., 1.])
sp1 = ax.scatter(plot_data.hs, plot_data.lpmc, s=1, c="black")
fig.add_axes(ax)
# fig.savefig(hemimeta.file_dir + hemimeta.file_name[ii])
# raster of LAI
lai_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\outputs\\LAI_parsed.dat'
pts_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\1m_dem_points.csv'
template_in = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\DEM\\19_149_dem_res_1.00m.bil'


lai = pd.read_csv(lai_in)
pts = pd.read_csv(pts_in)
lai = lai.merge(pts, how='left', on='id')
lai = lai.loc[:, ['id', 'x_utm11n', 'y_utm11n', 'x_index', 'y_index', 'lai_s_cc', 'openness']]

ras = raslib.raster_load(template_in)

idx = (lai.x_index.values.astype(int), lai.y_index.values.astype(int))
ras.data[idx] = lai.lai_s_cc
ras_out = 'C:\\Users\\Cob\\index\\educational\\usask\\research\\masters\\data\\lidar\\19_149\\19_149_snow_off\\OUTPUT_FILES\\synthetic_hemis\\uf_1m_pr_.15_os_10\\lai_test.tif'
raslib.raster_save(ras, ras_out)

lai_data = np.full([ras.rows, ras.cols], np.nan)
lai_data[(lai.x_index.values, lai.y_index.values)] = lai.lai_s
fig = plt.imshow(lai_data, interpolation='nearest', cmap='binary_r')
plt.colorbar()
plt.title('Simulated LAI over Upper Forest \n LAI-2000 with Schleppi et al. 2007 correction')

open_data = np.full([ras.rows, ras.cols], np.nan)
open_data[(lai.x_index.values, lai.y_index.values)] = 1 - lai.openness
fig = plt.imshow(open_data, interpolation='nearest', cmap='binary_r')
plt.colorbar()
plt.title('Canopy closure over Upper Forest \n from LAI-2000 rings')

