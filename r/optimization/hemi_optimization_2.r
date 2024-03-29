library('dplyr')
library('tidyr')
library('ggplot2')

plot_out_dir = "C:/Users/Cob/index/educational/usask/research/masters/graphics/thesis_graphics/validation/hemiphoto_validation/"
p_width = 8  # inches
p_height = 5.7  # inches
dpi = 100

photos_lai_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_manual_parsed.dat"
photos_lai = read.csv(photos_lai_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_lai$original_file = gsub("_r.JPG", ".JPG", photos_lai$picture)
photos_meta_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/hemi_lookup_cleaned.csv"
photos_meta = read.csv(photos_meta_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_meta$id <- as.numeric(rownames(photos_meta)) - 1

photos = merge(photos_lai, photos_meta, by.x='original_file', by.y='filename', all.x=TRUE)

synth_lai_in = "C:/Users/Cob/index/educational/usask/research/masters/data/lidar/synthetic_hemis/opt/poisson/LAI_parsed.dat"
synth_lai = read.csv(synth_lai_in, header=TRUE, na.strings = c("NA",""), sep=",")
synth_meta_in = "C:/Users/Cob/index/educational/usask/research/masters/data/lidar/synthetic_hemis/opt/poisson/hemimetalog.csv"
synth_meta = read.csv(synth_meta_in, header=TRUE, na.strings = c("NA",""), sep=",")
synth_meta$footprint = sqrt(synth_meta$point_size_scalar / (synth_meta$optimization_scalar * 2834.64))

comp times = synth_meta %>%
  group_by(poisson_radius_m) %>%
  summarise(ct_mean = mean(computation_time_s))

synth = merge(synth_lai, synth_meta, by.x='picture', by.y='file_name', all.x=TRUE)

all = merge(synth, photos, by='id', all.x=TRUE, suffixes=c("_synth", "_photo"))

# calculate errors
all = all %>%
  mutate(lai_no_cor_error = lai_no_cor_synth - lai_no_cor_photo) %>%
  mutate(lai_s_cc_error = lai_s_cc_synth - lai_s_cc_photo) %>%
  mutate(co_error = openness_synth - openness_photo) %>%
  mutate(co_error_1 = transmission_s_1_synth - transmission_s_1_photo) %>%
  mutate(co_error_2 = transmission_s_2_synth - transmission_s_2_photo) %>%
  mutate(co_error_3 = transmission_s_3_synth - transmission_s_3_photo) %>%
  mutate(co_error_4 = transmission_s_4_synth - transmission_s_4_photo) %>%
  mutate(co_error_5 = transmission_s_5_synth - transmission_s_5_photo)

rmse = function(difdata){
  sqrt(sum(difdata^2, na.rm = TRUE))/sqrt(length(na.omit(difdata)))
}
# define rmse
mae = function(difdata){
  sum(abs(difdata), na.rm = TRUE)/length(na.omit(difdata))
}

# plots

# optimized LAI
all_agg = all %>%
  group_by(poisson_radius_m, optimization_scalar) %>%
  summarise(rmse_lai_s_cc = rmse(lai_s_cc_error), mae_lai_s_cc = mae(lai_s_cc_error), mean_bias_lai_s_cc = mean(lai_s_cc_error, na.rm = TRUE),
            rmse_co = rmse(co_error), mae_co = mae(co_error), mean_bias_co = mean(co_error, na.rm = TRUE))
all_agg$poisson_radius_m = as.factor(all_agg$poisson_radius_m)

# mean bias lai
ggplot(all_agg, aes(x=optimization_scalar, y=mean_bias_lai_s_cc, color=poisson_radius_m)) +
  geom_point() +
  geom_line() +
  # labs(x='point size scalar [-]', y='LAI mean bias [-]', color='Poisson r [m]', title='Mean bias of LAI from sythetic hemispheres vs. photography (n=15)')
  labs(x='point size scalar [-]', y='LAI mean bias [-]', color='Poisson r [m]')
ggsave(paste0(plot_out_dir, "point_size_optimization_mean_bian.png"), width=p_width, height=p_height, dpi=dpi)


# rmse lai
ggplot(all_agg, aes(x=optimization_scalar, y=rmse_lai_s_cc, color=poisson_radius_m)) +
  geom_point() +
  geom_line()  +
  # labs(x='point size scalar [-]', y='LAI RMSE [-]', color='Poisson r [m]', title='RMSE of LAI from sythetic hemispheres vs. photography (n=15)') +
  labs(x='point size scalar [-]', y='LAI RMSE [-]', color='Poisson r [m]') +
  ylim(0, 1.1)
ggsave(paste0(plot_out_dir, "point_size_optimization_rmse.png"), width=p_width, height=p_height, dpi=dpi)


# mean bias co
ggplot(all_agg, aes(x=optimization_scalar, y=mean_bias_co, color=poisson_radius_m)) +
  geom_point() +
  geom_line()

# rmse co
ggplot(all_agg, aes(x=optimization_scalar, y=rmse_co, color=poisson_radius_m)) +
  geom_point() +
  geom_line()


# plot mean bias of canopy openness over all rings
all_agg = all %>%
  group_by(poisson_radius_m, optimization_scalar) %>%
  summarise(rmse_lai_s_cc = rmse(lai_s_cc_error), mae_lai_s_cc = mae(lai_s_cc_error), mean_bias_lai_s_cc = mean(lai_s_cc_error, na.rm = TRUE),
            rmse_co = rmse(co_error), mae_co = mae(co_error), mean_bias_co = mean(co_error, na.rm = TRUE),
            rmse_co_1 = rmse(co_error_1), mae_co_1 = mae(co_error_1), mean_bias_co_1 = mean(co_error_1, na.rm = TRUE),
            rmse_co_2 = rmse(co_error_2), mae_co_2 = mae(co_error_2), mean_bias_co_2 = mean(co_error_2, na.rm = TRUE),
            rmse_co_3 = rmse(co_error_3), mae_co_3 = mae(co_error_3), mean_bias_co_3 = mean(co_error_3, na.rm = TRUE),
            rmse_co_4 = rmse(co_error_4), mae_co_4 = mae(co_error_4), mean_bias_co_4 = mean(co_error_4, na.rm = TRUE),
            rmse_co_5 = rmse(co_error_5), mae_co_5 = mae(co_error_5), mean_bias_co_5 = mean(co_error_5, na.rm = TRUE),
            n = length(na.omit(lai_s_cc_error))) %>%
  gather("mb_group", "mean_bias", mean_bias_co, mean_bias_co_1, mean_bias_co_2, mean_bias_co_3, mean_bias_co_4, mean_bias_co_5)
all_agg$poisson_radius_m = as.factor(all_agg$poisson_radius_m)

ggplot(all_agg, aes(x=optimization_scalar, y=mean_bias, color=mb_group)) +
  facet_grid(. ~ poisson_radius_m) +
  geom_point() +
  geom_line()

# plot rmse of canopy openness over all rings
all_agg = all %>%
  group_by(poisson_radius_m, optimization_scalar) %>%
  summarise(rmse_lai_s_cc = rmse(lai_s_cc_error), mae_lai_s_cc = mae(lai_s_cc_error), mean_bias_lai_s_cc = mean(lai_s_cc_error, na.rm = TRUE),
            rmse_co = rmse(co_error), mae_co = mae(co_error), mean_bias_co = mean(co_error, na.rm = TRUE),
            rmse_co_1 = rmse(co_error_1), mae_co_1 = mae(co_error_1), mean_bias_co_1 = mean(co_error_1, na.rm = TRUE),
            rmse_co_2 = rmse(co_error_2), mae_co_2 = mae(co_error_2), mean_bias_co_2 = mean(co_error_2, na.rm = TRUE),
            rmse_co_3 = rmse(co_error_3), mae_co_3 = mae(co_error_3), mean_bias_co_3 = mean(co_error_3, na.rm = TRUE),
            rmse_co_4 = rmse(co_error_4), mae_co_4 = mae(co_error_4), mean_bias_co_4 = mean(co_error_4, na.rm = TRUE),
            rmse_co_5 = rmse(co_error_5), mae_co_5 = mae(co_error_5), mean_bias_co_5 = mean(co_error_5, na.rm = TRUE),
            n = length(na.omit(lai_s_cc_error))) %>%
  gather("rmse_group", "rmse", rmse_co, rmse_co_1, rmse_co_2, rmse_co_3, rmse_co_4, rmse_co_5)
all_agg$poisson_radius_m = as.factor(all_agg$poisson_radius_m)

ggplot(all_agg, aes(x=optimization_scalar, y=rmse, color=rmse_group)) +
  facet_grid(. ~ poisson_radius_m) +
  geom_point() +
  geom_line()

# calculation time
all$poisson_radius_m = as.factor(all$poisson_radius_m)
ggplot(all, aes(x=point_count, y=computation_time_s, color=poisson_radius_m)) +
  geom_point() +
  ylim(0, 200) +
  xlim(0, 1.4*10^7)

ggplot(all, aes(x=optimization_scalar, y=computation_time_s, color=poisson_radius_m)) +
  geom_point() +
  ylim(0, 200)


# subset to look at spread
selection_1 <- all %>%
  filter(poisson_radius_m==0.15, optimization_scalar==8)
selection_2 <- all %>%
  filter(poisson_radius_m==0.05, optimization_scalar==.7)
selection_3 <- all %>%
  filter(poisson_radius_m==0, optimization_scalar==.45)
selection = rbind(selection_1, selection_2, selection_3)

selection$poisson_radius_m = as.factor(selection$poisson_radius_m)

ggplot(selection, aes(x=lai_s_cc_photo, y=lai_s_cc_synth, color=poisson_radius_m)) + 
  geom_point() +
  geom_abline(slope=1, intercept=0)

# Threshold method comparison
photos_meta_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/hemi_lookup_cleaned.csv"
photos_meta = read.csv(photos_meta_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_meta$id <- as.numeric(rownames(photos_meta)) - 1
photos_meta = photos_meta %>% select('id', 'filename')


photos_manual_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_manual_parsed.dat"
photos_manual = read.csv(photos_manual_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_manual$original_file = gsub("_r.JPG", ".JPG", photos_manual$picture)
photos_manual = photos_manual %>% select('original_file', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')
photos_manual = merge(photos_meta, photos_manual, by.x='filename', by.y='original_file', all.y=TRUE)
lai_manual = photos_manual %>%
  gather('lai_method', 'manual', 3:6) %>%
  select(-'filename', -'openness', -'transmission')
trans_manual = photos_manual %>%
  gather('transmission_method', 'manual', c('transmission', 'openness')) %>%
  select(-'filename', -'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

photos_rc_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_rc_parsed.dat"
photos_rc = read.csv(photos_rc_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_rc$original_file = gsub("_r.JPG", ".JPG", photos_rc$picture)
photos_rc = photos_rc %>% select('original_file', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')
photos_rc = merge(photos_meta, photos_rc, by.x='filename', by.y='original_file', all.y=TRUE)
lai_rc = photos_rc %>%
  gather('lai_method', 'rc', 3:6) %>%
  select(-'filename', -'openness', -'transmission')
trans_rc = photos_rc %>%
  gather('transmission_method', 'rc', c('transmission', 'openness')) %>%
  select(-'filename', -'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

photos_rc_rings_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_rc_rings_parsed.dat"
photos_rc_rings = read.csv(photos_rc_rings_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_rc_rings$original_file = gsub("_r.JPG", ".JPG", photos_rc_rings$picture)
photos_rc_rings = photos_rc_rings %>% select('original_file', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')
photos_rc_rings = merge(photos_meta, photos_rc_rings, by.x='filename', by.y='original_file', all.y=TRUE)
lai_rc_rings = photos_rc_rings %>%
  gather('lai_method', 'rc_rings', 3:6) %>%
  select(-'filename', -'openness', -'transmission')
trans_rc_rings = photos_rc_rings %>%
  gather('transmission_method', 'rc_rings', c('transmission', 'openness')) %>%
  select(-'filename', -'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

photos_nh_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_nh_parsed.dat"
photos_nh = read.csv(photos_nh_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_nh$original_file = gsub("_r.JPG", ".JPG", photos_nh$picture)
photos_nh = photos_nh %>% select('original_file', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')
photos_nh = merge(photos_meta, photos_nh, by.x='filename', by.y='original_file', all.y=TRUE)
lai_nh = photos_nh %>%
  gather('lai_method', 'nh', 3:6) %>%
  select(-'filename', -'openness', -'transmission')
trans_nh = photos_nh %>%
  gather('transmission_method', 'nh', c('transmission', 'openness')) %>%
  select(-'filename', -'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

photos_nh_rings_in = "C:/Users/Cob/index/educational/usask/research/masters/data/hemispheres/19_149/clean/sized/LAI_nh_rings_parsed.dat"
photos_nh_rings = read.csv(photos_nh_rings_in, header=TRUE, na.strings = c("NA",""), sep=",")
photos_nh_rings$original_file = gsub("_r.JPG", ".JPG", photos_nh_rings$picture)
photos_nh_rings = photos_nh_rings %>% select('original_file', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')
photos_nh_rings = merge(photos_meta, photos_nh_rings, by.x='filename', by.y='original_file', all.y=TRUE)
lai_nh_rings = photos_nh_rings %>%
  gather('lai_method', 'nh_rings', 3:6) %>%
  select(-'filename', -'openness', -'transmission')
trans_nh_rings = photos_nh_rings %>%
  gather('transmission_method', 'nh_rings', c('transmission', 'openness')) %>%
  select(-'filename', -'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

synth_data_in = "C:/Users/Cob/index/educational/usask/research/masters/data/lidar/synthetic_hemis/opt/poisson/LAI_parsed.dat"
synth_data = read.csv(synth_data_in, header=TRUE, na.strings = c("NA",""), sep=",")
synth_data = synth_data %>% select('picture', 'lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc', 'openness', 'transmission')

synth_meta_in = "C:/Users/Cob/index/educational/usask/research/masters/data/lidar/synthetic_hemis/opt/poisson/hemimetalog.csv"
synth_meta = read.csv(synth_meta_in, header=TRUE, na.strings = c("NA",""), sep=",")
synth_meta = synth_meta %>% select('id', 'file_name', 'poisson_radius_m', 'optimization_scalar')

synth = merge(synth_meta, synth_data, by.x='file_name', by.y='picture', all.x=TRUE)
lai_synth = synth %>%
  gather('lai_method', 'lai_synth', 5:8) %>%
  select(-'openness', -'transmission')
trans_synth = synth %>%
  gather('transmission_method', 'trans_synth', c('transmission', 'openness')) %>%
  select(-'lai_no_cor', -'lai_s', -'lai_cc', -'lai_s_cc')

rmse = function(difdata){
  sqrt(sum(difdata^2, na.rm = TRUE))/sqrt(length(na.omit(difdata)))
}
# define rmse
mae = function(difdata){
  sum(abs(difdata), na.rm = TRUE)/length(na.omit(difdata))
}

# LAI
lai = merge(lai_synth, lai_manual, by=c('id', 'lai_method'), all.x=TRUE)
lai = merge(lai, lai_rc, by=c('id', 'lai_method'), all.x=TRUE)
lai = merge(lai, lai_rc_rings, by=c('id', 'lai_method'), all.x=TRUE)
lai = merge(lai, lai_nh, by=c('id', 'lai_method'), all.x=TRUE)
lai = merge(lai, lai_nh_rings, by=c('id', 'lai_method'), all.x=TRUE)

lai = lai %>%
  gather('threshold_method', 'lai_photo', 7:11) %>%
  mutate(lai_error = lai_synth - lai_photo)

lai_summary = lai %>%
  group_by(poisson_radius_m, optimization_scalar, threshold_method, lai_method) %>%
  summarise(lai_rmse = rmse(lai_error), lai_mae = mae(lai_error), lai_mean_bias = mean(lai_error, na.rm = TRUE), n = n())

lai_summary$poisson_radius_m = as.factor(lai_summary$poisson_radius_m)
lai_summary$threshold_method = as.factor(lai_summary$threshold_method)
lai_summary$lai_method = as.factor(lai_summary$lai_method)

levels(lai_summary$lai_method)
levels(lai_summary$threshold_method) = c('Manual', 'Nobis-Hunziker', 'Nobis-Hunziker rings', 'Ridler-Calvard', 'Ridler-Calvard rings')

lai_summary$lai_method_order = factor(lai_summary$lai_method, levels=c('lai_no_cor', 'lai_s', 'lai_cc', 'lai_s_cc'))
levels(lai_summary$lai_method_order) = c('No correction', 'Schleppi', 'Chen-Cihlar', 'Schleppi + Chen-Cihlar')

# plots
# lai rmse
ggplot(lai_summary, aes(x=optimization_scalar, y=lai_rmse, color=poisson_radius_m)) +
  facet_grid(lai_method_order ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  ylim(0, 1.75) +
  labs(title='LAI RMSE between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal) and LAI corrections (vertical)',
       x='Point size optimization scalar',
       y='RMSE of LAI',
       color='Poisson sampling radius (m)')

# lai mae
ggplot(lai_summary, aes(x=optimization_scalar, y=lai_mae, color=poisson_radius_m)) +
  facet_grid(lai_method_order ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  ylim(0, 1.65) +
  labs(title='LAI MAE between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal) and LAI corrections (vertical)',
       x='Point size optimization scalar',
       y='MAE of LAI',
       color='Poisson sampling radius (m)')

# lai mean bias
ggplot(lai_summary, aes(x=optimization_scalar, y=lai_mean_bias, color=poisson_radius_m)) +
  facet_grid(lai_method_order ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  geom_abline(slope=0, intercept=0) +
  labs(title='LAI mean bias between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal) and LAI corrections (vertical)',
       x='Point size optimization scalar',
       y='Mean bias of LAI',
       color='Poisson sampling radius (m)')

# subsetting
lai_subset = lai_summary %>%
  filter(threshold_method == 'manual', lai_method == 'lai_s')


# transmission
trans = merge(trans_synth, trans_manual, by=c('id', 'transmission_method'), all.x=TRUE)
trans = merge(trans, trans_rc, by=c('id', 'transmission_method'), all.x=TRUE)
trans = merge(trans, trans_rc_rings, by=c('id', 'transmission_method'), all.x=TRUE)
trans = merge(trans, trans_nh, by=c('id', 'transmission_method'), all.x=TRUE)
trans = merge(trans, trans_nh_rings, by=c('id', 'transmission_method'), all.x=TRUE)

trans = trans %>%
  gather('threshold_method', 'trans_photo', 7:11) %>%
  mutate(trans_error = trans_synth - trans_photo)

trans_summary = trans %>%
  group_by(poisson_radius_m, optimization_scalar, threshold_method, transmission_method) %>%
  summarise(trans_rmse = rmse(trans_error), trans_mae = mae(trans_error), trans_mean_bias = mean(trans_error, na.rm = TRUE), n = n())

trans_summary$poisson_radius_m = as.factor(trans_summary$poisson_radius_m)
trans_summary$threshold_method = as.factor(trans_summary$threshold_method)
trans_summary$transmission_method = as.factor(trans_summary$transmission_method)

levels(trans_summary$threshold_method) = c('Manual', 'Nobis-Hunziker', 'Nobis-Hunziker rings', 'Ridler-Calvard', 'Ridler-Calvard rings')

trans_summary$trans_method_order = factor(trans_summary$transmission_method, levels=c('transmission', 'openness'))
levels(trans_summary$trans_method_order) = c('Transmission', 'Openness')


# openness rmse
openness_summary = trans_summary %>%
  filter(transmission_method == 'openness')

ggplot(openness_summary, aes(x=optimization_scalar, y=trans_rmse, color=poisson_radius_m)) +
  facet_grid(. ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  ylim(0, .25) +
  labs(title='RMSE of canopy openness between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal)',
       x='Point size optimization scalar',
       y='RMSE of Canopy Openness',
       color='Poisson sampling radius (m)')

# openness mae
ggplot(openness_summary, aes(x=optimization_scalar, y=trans_mae, color=poisson_radius_m)) +
  facet_grid(. ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10()+
  ylim(0, .25) +
  labs(title='MAE of canopy openness between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal)',
       x='Point size optimization scalar',
       y='MAE of Canopy Openness',
       color='Poisson sampling radius (m)')

# openness mean bias
ggplot(openness_summary, aes(x=optimization_scalar, y=trans_mean_bias, color=poisson_radius_m)) +
  facet_grid(. ~ threshold_method) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  geom_abline(slope=0, intercept=0) +
  labs(title='Mean bias of canopy openness between synthetic hemispheres and hemispherical photos (n = 15)',
       subtitle='for different photo threshold methods (horizontal)',
       x='Point size optimization scalar',
       y='Mean bias of canopy openness',
       color='Poisson sampling radius (m)')


# BOOKMAKR -- everything below this is old hat...

# plot
# RMSE
ggplot(synth_photos_da, aes(x=th_hold_las, y=rmse_lai, color=os, shape = group)) +
  geom_point() +
  geom_line() +
  labs(title="RMSE of LAI across point size, threshold, and methods", x="Synthetic threshold (1-255)", y="RMSE of LAI (LiDAR vs. Photo)", color="Synthetic point size", shape="LAI method")

# mean_bias
ggplot(synth_photos_da, aes(x=th_hold_las, y=mean_bias_lai, color=os, shape=group)) +
  geom_point() +
  geom_line() +
  labs(title="Mean Bias of LAI across point size, threshold, and methods", x="Synthetic threshold (1-255)", y="Mean Bias of LAI (LiDAR - Photo)", color="Synthetic point size", shape="LAI method")
  


synth_photos_da$th_hold_las = as.factor(synth_photos_da$th_hold_las)
synth_photos_da$os = as.numeric(as.character(synth_photos_da$os))

ggplot(synth_photos_da, aes(x=os, y=mean_bias_lai, color=th_hold_las, shape=group)) +
  geom_point() +
  geom_line()


# what kind of spread do we see amonth the primary contenders?

synth_photos$th_hold_las = as.factor(synth_photos$th_hold_las)
synth_photos$os = as.factor(synth_photos$os)

selection_1 <- synth_photos %>%
  filter(os==0.05, th_hold_las==128, group=="Miller_")
selection_2 <- synth_photos %>%
  filter(os==0.1, th_hold_las==80, group=="Miller_")
selection_3 <- synth_photos %>%
  filter(os==0.25, th_hold_las==32, group=="Miller_")

selection = rbind(selection_1, selection_2, selection_3)

ggplot(selection, aes(x=lai_photo, y=lai_las, color=os, label=loc)) + 
  geom_point() +
  geom_abline(slope=1, intercept=0) +
  labs(title="Photo-LAI vs. LiDAR-LAI for 3 best cases", x="Photo LAI", y="LiDAR LAI", color="Synthetic point size")

ggplot(synth_photos, aes(x=lai_photo, y=lai_las, color=th_hold_las)) + 
  facet_grid(os ~ group) +
  geom_point() +
  geom_abline(slope=1, intercept=0)
  
  