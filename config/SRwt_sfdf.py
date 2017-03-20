#
# Configuration for stop2l-3body
#
# daniel.joseph.antrim@cern.ch
# July 12
#

import ROOT

import os
import sys
sys.path.append(os.environ['LIMPLOTDIR'])

from limitplotter.utils.limiters import *
conf = gridConf


###########################################
# regions to include
###########################################
conf.base_region = "SRwt"

regions = ["SRwt"]

proper_names = {}
proper_names["SRwt"] = "SRw+SRt"

conf.proper_names = proper_names


##########################################
# region colors and styles
##########################################
region_colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
# 20 : filled circle
# 21 : filled square
# 22 : filled upward triangle
region_marker_styles = [ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp]

#########################################
# location of HF results directory
#########################################
conf.results_dir = "jul28_results/results/"

########################################
# location of HF logs used for gathering
# upper limit results
########################################
conf.log_dir = "/data/uclhc/uci/user/dantrim/SuperFitter/HistFitter-00-00-49-TestExclFix/results/runlogs/" 
conf.ul_name_suffix = "_limitOnMu.log"


########################################
# axis labels
########################################
#conf.x_title = "m_{#tilde{t}} [GeV]"
conf.x_title = "m(#tilde{t}_{1}) [GeV]"
#conf.y_title = "m_{#tilde{#chi}_{1}^{ 0}} [GeV]"
conf.y_title = "m(#tilde{#chi}_{1}^{ 0}) [GeV]"

#######################################
# limit plot grid ranges
#######################################
conf.xlow   = 100       # GeV
conf.xhigh  = 475       # GeV
#conf.xhigh  = 450       # GeV
conf.ylow   = 0         # GeV 
conf.yhigh  = 460      # GeV
#conf.yhigh  = 440       # GeV


#######################################
# forbidden lines
#######################################



#######################################
# decay process
#######################################
conf.decay_process = "#scale[0.8]{#tilde{t}_{1} #rightarrow bW#tilde{#chi}_{1}^{ 0}  }"


######################################################
# which plot to plot
######################################################

## best SR per point
conf.do_best_sr_per_point = False

conf.do_limit_plot = True

## CLs/Sig per point
conf.show_exp_cls = False
conf.show_obs_cls = False 
conf.show_obs_sig = False
conf.show_exp_sig = False

## xsec upper limit
conf.do_xsec_plot = False


########################################
# 8 TeV results
########################################
conf.show_previous_8TeV_result = True
conf.previous_result_file = "/data/uclhc/uci/user/dantrim/n0225val/limitplotter/previous_contours/previous_contours_3body.root"
conf.previous_contours = {}
conf.previous_contours["wwlike"] = "obs_nominal"
conf.previous_contours["stop1l"] = "stop1lobs"
conf.previous_contours["stop2l"] = "stop2lobs"


#######################################
# file the regions
#######################################
for i, region in enumerate(regions) :
    r = Region(region)
    r.color = region_colors[i]
    r.shape = region_marker_styles[i]
    conf.regions.append(r)

