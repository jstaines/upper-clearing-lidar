library('dplyr')
library('tidyr')
library('ggplot2')
library('grid')
library('gridExtra')
library('latex2exp')

plot_out_dir = "C:/Users/Cob/index/educational/usask/research/masters/graphics/thesis_graphics/frequency distributions/swe_distribution_fitting/"
p_width = 8  # inches
p_height = 5.7  # inches
dpi = 100

# upper forest plot
uf_045_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_045_uf_fcon_r.05m_interp2x_by_lpml15.csv'
uf_045 = read.csv(uf_045_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_fcon_19_045)

uf_050_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_050_uf_fcon_r.05m_interp2x_by_lpml15.csv'
uf_050 = read.csv(uf_050_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_fcon_19_050)

uf_052_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_052_uf_fcon_r.05m_interp2x_by_lpml15.csv'
uf_052 = read.csv(uf_052_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_fcon_19_052)

uf_045_050_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_dswe_19_045-19_050_uf_ucgo_r.05m_interp2x_by_lpml15.csv'
uf_045_050 = read.csv(uf_045_050_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(dswe = "dswe_ucgo_19_045.19_050")

uf_050_052_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_dswe_19_050-19_052_uf_ucgo_r.05m_interp2x_by_lpml15.csv'
uf_050_052 = read.csv(uf_050_052_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(dswe = "dswe_ucgo_19_050.19_052")


# upper clearing plot
uc_045_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_045_uc_clin_r.05m_interp2x_by_lpml15.csv'
uc_045 = read.csv(uc_045_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_clin_19_045)

uc_050_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_050_uc_clin_r.05m_interp2x_by_lpml15.csv'
uc_050 = read.csv(uc_050_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_clin_19_050)

uc_052_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_swe_19_052_uc_clin_r.05m_interp2x_by_lpml15.csv'
uc_052 = read.csv(uc_052_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(swe = swe_clin_19_052)

uc_045_050_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_dswe_19_045-19_050_uc_ucgo_r.05m_interp2x_by_lpml15.csv'
uc_045_050 = read.csv(uc_045_050_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(dswe = "dswe_ucgo_19_045.19_050")

uc_050_052_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_dswe_19_050-19_052_uc_ucgo_r.05m_interp2x_by_lpml15.csv'
uc_050_052 = read.csv(uc_050_052_in, header=TRUE, na.strings = c("NA",""), sep=",") %>%
  rename(dswe = "dswe_ucgo_19_050.19_052")


# Check normality of dswe distributions
# qqnorm(uf_045_050$dswe)
# qqnorm(uf_050_052$dswe)
# qqnorm(uc_045_050$dswe)
# qqnorm(uc_050_052$dswe)

# coefficient of variation
cv_uf_045 = sd(uf_045$swe)/mean(uf_045$swe)
cv_uf_050 = sd(uf_050$swe)/mean(uf_050$swe)
cv_uf_052 = sd(uf_052$swe)/mean(uf_052$swe)

cv_uc_045 = sd(uc_045$swe)/mean(uc_045$swe)
cv_uc_050 = sd(uc_050$swe)/mean(uc_050$swe)
cv_uc_052 = sd(uc_052$swe)/mean(uc_052$swe)

# forest descriptive stats
mean(uf_045$swe)
mean(uf_050$swe)
mean(uf_052$swe)

sd(uf_045$swe)
sd(uf_050$swe)
sd(uf_052$swe)

# clearing descriptive stats
mean(uc_045$swe)
mean(uc_050$swe)
mean(uc_052$swe)

sd(uc_045$swe)
sd(uc_050$swe)
sd(uc_052$swe)

# dswe parameters
mean(uf_045_050$dswe)
sd(uf_045_050$dswe)
sd(uf_045_050$dswe)/mean(uf_045_050$dswe)

mean(uc_045_050$dswe)
sd(uc_045_050$dswe)
sd(uc_045_050$dswe)/mean(uc_045_050$dswe)

mean(uf_050_052$dswe)
sd(uf_050_052$dswe)
sd(uf_050_052$dswe)/mean(uf_050_052$dswe)

mean(uc_050_052$dswe)
sd(uc_050_052$dswe)
sd(uc_050_052$dswe)/mean(uc_050_052$dswe)

# shook 1995
qq_func = function(data){
  swe = data$swe
  
  # calculate mean and standard deviation in transformed distribution
  s_y = sqrt(log(1 + (sd(swe)/mean(swe))^2))
  y_bar = log(mean(swe)) - s_y^2/2
  
  # rank by decreasing quantile
  p_ = rank(-1 * swe)/(nrow(data) + 1)
  f_ = 1 - p_
  
  # calculate k_value frequency factor
  k_y = qnorm(f_, mean=0, sd=1)
  k_ = (exp(s_y * k_y - (s_y^2)/2) - 1)/sqrt(exp(s_y^2) - 1)
  
  data$k_vals = k_
  
  data
}


k_045 = qq_func(uf_045)
k_050 = qq_func(uf_050)
k_052 = qq_func(uf_052)

# linear fitting
lm_045 = lm(swe ~ k_vals, data=k_045)
lm_050 = lm(swe ~ k_vals, data=k_050)
lm_052 = lm(swe ~ k_vals, data=k_052)

summary(lm_045)
summary(lm_050)
summary(lm_052)

# 045
fo = TeX(paste0("\\hat{y} = ", sprintf("%.2f",lm_045$coefficients[2]), "x+", sprintf("%.2f",lm_045$coefficients[1])), output="character")
r2 = TeX(paste0("R^2 = ", sprintf("%.4f",summary(lm_045)$adj.r.squared)), output="character")

ggplot(k_045, aes(x=k_vals, y=swe)) +
  geom_point(size=.75) +
  labs(x='K', y='SWE (mm)', title=paste0('SWE - lognormal Q-Q plot for 14 Feb. 2019 (n=', as.character(nrow(k_045)), ')\nUpper Forest, 5cm resolution, bias corrected with LPM-Last')) + 
  theme_minimal() +
  geom_smooth(method='lm', se=FALSE, alpha=.15, color='turquoise4', linetype='dashed') +
  annotate("text", x=2, y=195, label=fo, parse=TRUE) +
  annotate("text", x=2, y=185, label=r2, parse=TRUE)
ggsave(paste0(plot_out_dir, "swe_19_045_fcon_lognormal_qq_lpml15.png"), width=p_width, height=p_height, dpi=dpi)

# 050
fo = TeX(paste0("\\hat{y} = ", sprintf("%.2f",lm_050$coefficients[2]), "x+", sprintf("%.2f",lm_050$coefficients[1])), output="character")
r2 = TeX(paste0("R^2 = ", sprintf("%.4f",summary(lm_050)$adj.r.squared)), output="character")

ggplot(k_050, aes(x=k_vals, y=swe)) +
  geom_point(size=.75) +
  labs(x='K', y='SWE (mm)', title=paste0('SWE - lognormal Q-Q plot for 19 Feb. 2019 (n=', as.character(nrow(k_050)), ')\nUpper Forest, 5cm resolution, bias corrected with LPM-Last')) +
  theme_minimal() +
  geom_smooth(method='lm', se=FALSE, alpha=.15, color='turquoise4', linetype='dashed')  +
  annotate("text", x=2, y=195, label=fo, parse=TRUE) +
  annotate("text", x=2, y=185, label=r2, parse=TRUE)
ggsave(paste0(plot_out_dir, "swe_19_050_fcon_lognormal_qq_lpml15.png"), width=p_width, height=p_height, dpi=dpi)

# 052
fo = TeX(paste0("\\hat{y} = ", sprintf("%.2f",lm_052$coefficients[2]), "x+", sprintf("%.2f",lm_052$coefficients[1])), output="character")
r2 = TeX(paste0("R^2 = ", sprintf("%.4f",summary(lm_052)$adj.r.squared)), output="character")

ggplot(k_052, aes(x=k_vals, y=swe)) +
  geom_point(size=.75) +
  labs(x='K', y='SWE (mm)', title=paste0('SWE - lognormal Q-Q plot for 21 Feb. 2019 (n=', as.character(nrow(k_052)), ')\nUpper Forest, 5cm resolution, bias corrected with LPM-Last')) +
  theme_minimal() +
  geom_smooth(method='lm', se=FALSE, alpha=.15, color='turquoise4', linetype='dashed') +
  annotate("text", x=2, y=195, label=fo, parse=TRUE) +
  annotate("text", x=2, y=185, label=r2, parse=TRUE)
ggsave(paste0(plot_out_dir, "swe_19_052_fcon_lognormal_qq_lpml15.png"), width=p_width, height=p_height, dpi=dpi)



lognorm_model = function(k_data, lm){
  x_vals = seq(min(k_data$swe), max(k_data$swe), by = 0.1)

  mu = summary(lm)$coefficients[1]
  sig = summary(lm)$coefficients[2]
  
  lmu = log(mu^2/sqrt(mu^2 + sig^2))
  lsig = sqrt(log(1 + sig^2/mu^2))
  
  y_vals = dlnorm(x_vals, meanlog=lmu, sdlog=lsig)
  m_data = data.frame(x_vals, y_vals)
}

m_045 = lognorm_model(k_045, lm_045)
ggplot(k_045, aes(x=swe)) +
  geom_histogram(aes(y=..density..), fill='cornflowerblue', alpha=1, binwidth = 1) +
  geom_line(data=m_045, aes(x=x_vals, y=y_vals), size=1) +
  labs(x='SWE [mm]', y='Density [-]', title='SWE observed and lognormal modeled distributions for\n14 Feb. 2019 Upper Forest, 5cm res., rejection sampled')
ggsave(paste0(plot_out_dir, "swe_19_045_fcon_lognormal_model_lpml15.png"), width=p_width, height=p_height, dpi=dpi)

m_050 = lognorm_model(k_050, lm_050)
ggplot(k_050, aes(x=swe)) +
  geom_histogram(aes(y=..density..), fill='cornflowerblue', alpha=1, binwidth = 1) +
  geom_line(data=m_050, aes(x=x_vals, y=y_vals), size=1) +
  labs(x='SWE [mm]', y='Density [-]', title='SWE observed and lognormal modeled distributions for\n19 Feb. 2019 Upper Forest, 5cm res., rejection sampled')
ggsave(paste0(plot_out_dir, "swe_19_050_fcon_lognormal_model_lpml15.png"), width=p_width, height=p_height, dpi=dpi)

m_052 = lognorm_model(k_052, lm_052)
ggplot(k_052, aes(x=swe)) +
  geom_histogram(aes(y=..density..), fill='cornflowerblue', alpha=1, binwidth = 1) +
  geom_line(data=m_052, aes(x=x_vals, y=y_vals), size=1) +
  labs(x='SWE [mm]', y='Density [-]', title='SWE observed and lognormal modeled distributions for\n21 Feb. 2019 Upper Forest, 5cm res., rejection sampled')
ggsave(paste0(plot_out_dir, "swe_19_052_fcon_lognormal_model_lpml15.png"), width=p_width, height=p_height, dpi=dpi)
# 
# # compute correlation of snow depth with point count
# pc_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/merged_data_products/merged_uf_r.10m_point_density_median_snow_depth.csv'
# pc = read.csv(pc_in, header=TRUE, na.strings = c("NA",""), sep=",")
# 
# # calculate pearsons r
# cor.test(pc$X19_045_pdens, pc$X19_045_hs, method="pearson")
# cor.test(pc$X19_050_pdens, pc$X19_050_hs, method="pearson")
# cor.test(pc$X19_052_pdens, pc$X19_052_hs, method="pearson")
# 
# cor.test(pc$X19_149_pdens, pc$X19_045_hs, method="pearson")
# cor.test(pc$X19_149_pdens, pc$X19_050_hs, method="pearson")
# cor.test(pc$X19_149_pdens, pc$X19_052_hs, method="pearson")
# 
# # load rejection sampled
# 
# # upper forest plot
# hs_045_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_hs_19_045_uf_r.10m_interp2x_by_lpml15.csv'
# hs_045 = read.csv(hs_045_in, header=TRUE, na.strings = c("NA",""), sep=",")
# 
# hs_050_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_hs_19_050_uf_r.10m_interp2x_by_lpml15.csv'
# hs_050 = read.csv(hs_050_in, header=TRUE, na.strings = c("NA",""), sep=",")
# 
# hs_052_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/products/rejection_sampled/resampled_hs_19_052_uf_r.10m_interp2x_by_lpml15.csv'
# hs_052 = read.csv(hs_052_in, header=TRUE, na.strings = c("NA",""), sep=",")
# 
# # calculate pearsons r
# cor.test(hs_045$X19_045_pdens, hs_045$X19_045_hs, method="pearson")
# cor.test(hs_050$X19_050_pdens, hs_050$X19_050_hs, method="pearson")
# cor.test(hs_052$X19_052_pdens, hs_052$X19_052_hs, method="pearson")
# 
# cor.test(hs_045$X19_149_pdens, hs_045$X19_045_hs, method="pearson")
# cor.test(hs_050$X19_149_pdens, hs_050$X19_050_hs, method="pearson")
# cor.test(hs_052$X19_149_pdens, hs_052$X19_052_hs, method="pearson")
# 
# 
# mean(pc$X19_045_hs, na.rm=TRUE) / mean(hs_045$X19_045_hs, na.rm=TRUE)
# 
# 
# mean(pc$X19_050_hs, na.rm=TRUE) / mean(hs_050$X19_050_hs, na.rm=TRUE)
# 
# 
# mean(pc$X19_052_hs, na.rm=TRUE) / mean(hs_052$X19_052_hs, na.rm=TRUE)



# 
# ### old hat below
# 
# data_in = 'C:/Users/Cob/index/educational/usask/research/masters/data/lidar/analysis/swe_uf_.25m_canopy_19_149.csv'
# data = read.csv(data_in, header=TRUE, na.strings = c("NA",""), sep=",")
# 
# # filter to upper forest
# data = data[data$uf == 1, ]
# 
# 
# gd = 'C:/Users/Cob/index/educational/usask/research/masters/graphics/automated/'
# plot_h = 21  # cm
# plot_w = 29.7  # cm
# 
# # gather snow depths  
# data_swe = data %>%
#   gather("date", "swe", c(8, 10, 12, 14, 16))
# data_swe$date = as.factor(data_swe$date)
# levels(data_swe$date) = c("19_045", "19_050", "19_052", "19_107", "19_123")
# 
# 
# 
# # calculate K
# datelist = levels(data_swe$date)
# data_swe$k_vals = NA
# date = datelist[3]
# for (date in levels(data_swe$date)){
#   # pull out non-negative and non-NA swe values for the corresponding date
#   valid_samps = (data_swe$date == date) & (data_swe$swe > 0) & !is.na(data_swe$swe)
#   swe = data_swe$swe[valid_samps]
#   
#   # calculate mean and standard deviation in transformed distribution
#   s_y = sqrt(log(1 + (sd(swe)/mean(swe))^2))
#   y_bar = log(mean(swe)) - s_y^2/2
#   
#   # rank by decreasing quantile
#   p_ = rank(-1 * swe)/(sum(valid_samps) + 1)
#   f_ = 1 - p_
#   
#   # calculate k_value frequency factor
#   k_y = qnorm(f_, mean=0, sd=1)
#   k_ = (exp(s_y * k_y - (s_y^2)/2) - 1)/sqrt(exp(s_y^2) - 1)
#   
#   data_swe$k_vals[valid_samps] = k_
# }
# 
# # plots
# 
# p_hist = ggplot(data_swe, aes(x=swe)) +
#   facet_grid(. ~ date) +
#   geom_histogram(aes(y=..density..), fill='blue', alpha=0.5, binwidth = 1) +
#   labs(x='SWE (mm)', y='frequency', title='SWE distributions within the Upper Forest for different survey dates') +
#   theme_minimal()
# 
# p_swek = ggplot(data_swe, aes(x=k_vals, y=swe)) +
#   facet_grid(. ~ date) +
#   geom_line(size=.75) +
#   labs(x='K', y='SWE (mm)', title='SWE vs. lognormal frequency factor K over the Upper Forest\nslope = sd, intercept = mean of lognormal distribution (Shook 1995)') +
#   ylim(0, 255)
# 
# 
# 
# p_sk = grid.arrange(p_hist, p_swek, nrow=3)
# ggsave(paste0(gd, "swe_dist.pdf"), p_sk, width = plot_w, height = plot_h, units = "cm")
# 
# 
# 
# ##### Everything below is old, OLD hat #####
# 
# datelist = levels(data_hs$date)
# mu <- numeric(length = length(datelist))
# sig <- numeric(length = length(datelist))
# data_swe$lnsamps = 0
# for (ii in 1:length(datelist)){
#   date = datelist[ii]
#   samples = data_swe$swe[data_swe$date == date]
#   mu_x = mean(samples, na.rm=TRUE)
#   sig_x = sd(samples, na.rm=TRUE)
#   
#   mu[ii] = log(mu_x^2/sqrt(mu_x^2 + sig_x^2))
#   sig[ii] = sqrt(log(1 + sig_x^2/mu_x^2))
#   
#   n = length(samples)
#   data_swe$lnsamps[data_swe$date == date] = rlnorm(n, meanlog=mu[ii], sdlog=sig[ii])
# }
# 
# 
# p_045 = ggplot(data_hs, aes(sample=hs)) +
#   stat_qq(distribution=stats::qlnorm, na.rm=TRUE, dparams=c(mu[1], sig[1])) +
#   geom_abline(intercept=0, slope=1) +
#   xlim(0, 1) + 
#   labs(title=datelist[1],  x=sprintf(mu[1], sig[1], fmt='theoretical log normal\n(mu=%#.3f, sig=%#.3f)'), y = 'snow depth distribution') +
#   theme_minimal()
# 
# p_050 = ggplot(data_hs, aes(sample=hs)) +
#   stat_qq(distribution=stats::qlnorm, na.rm=TRUE, dparams=c(mu[2], sig[2])) +
#   geom_abline(intercept=0, slope=1) +
#   xlim(0, 1) + 
#   labs(title=datelist[2],  x=sprintf(mu[2], sig[2], fmt='theoretical log normal\n(mu=%#.3f, sig=%#.3f)'), y = 'snow depth distribution') +
#   theme_minimal()
# 
# p_052 = ggplot(data_hs, aes(sample=hs)) +
#   stat_qq(distribution=stats::qlnorm, na.rm=TRUE, dparams=c(mu[3], sig[3])) +
#   geom_abline(intercept=0, slope=1) +
#   xlim(0, 1) + 
#   labs(title=datelist[3],  x=sprintf(mu[3], sig[3], fmt='theoretical log normal\n(mu=%#.3f, sig=%#.3f)'), y = 'snow depth distribution') +
#   theme_minimal()
# 
# p_107 = ggplot(data_hs, aes(sample=hs)) +
#   stat_qq(distribution=stats::qlnorm, na.rm=TRUE, dparams=c(mu[4], sig[4])) +
#   geom_abline(intercept=0, slope=1) +
#   xlim(0, 1) + 
#   labs(title=datelist[4],  x=sprintf(mu[4], sig[4], fmt='theoretical log normal\n(mu=%#.3f, sig=%#.3f)'), y = 'snow depth distribution') +
#   theme_minimal()
# 
# p_123 = ggplot(data_hs, aes(sample=hs)) +
#   stat_qq(distribution=stats::qlnorm, na.rm=TRUE, dparams=c(mu[5], sig[5])) +
#   geom_abline(intercept=0, slope=1) +
#   xlim(0, 1) + 
#   labs(title=datelist[5],  x=sprintf(mu[5], sig[5], fmt='theoretical log normal\n(mu=%#.3f, sig=%#.3f)'), y = 'snow depth distribution') +
#   theme_minimal()
# 
# p_qq = grid.arrange(p_045, p_050, p_052, p_107, p_123, nrow=1, top = textGrob('Quantile-Quantile plots of snow depth distributions vs. parameter-fit log-normal'))
# 
# p_hist = ggplot(data_hs, aes(x=hs)) +
#   facet_grid(. ~ date) +
#   geom_histogram(aes(y=..density..), fill='blue', alpha=0.5, binwidth = .01) +
#   geom_density(size=1) +
#   xlim(-.2, .8) +
#   labs(x='Snow depth (m)', y='frequency', title='Snow depth distributions for different survey dates') +
#   theme_minimal()
# 
# p_theo = ggplot(data_hs) +
#   facet_grid(. ~ date) +
#   geom_histogram(aes(x=hs, y=..density..), fill='blue', alpha=0.5, binwidth = .01) +
#   geom_density(aes(x=lnsamps), color='black', size=1) +
#   xlim(-.2, .8) +
#   labs(x='Snow depth (m)', y='frequency', title='Comparison of snow depth distribution with samples from theoretical log-normal') +
#   theme_minimal()
# 
# 
# p_sdd = grid.arrange(p_hist, p_theo, p_qq, nrow=3)
# ggsave(paste0(gd, "snow_depth_log_normal_fitting.png"), p_sdd, width = plot_w, height = plot_h, units = "cm")
# 
# 
# # ,gp=gpar(fontsize=20,font=3)