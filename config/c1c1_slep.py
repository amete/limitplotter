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
conf.base_region = "SR"

regions = ["SRA","SRB","SRC"]

proper_names = {}
proper_names["SRA"] = "SR-mT2,90"
proper_names["SRB"] = "SR-mT2,120"
proper_names["SRC"] = "SR-mT2,150"

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
#conf.results_dir = "/data/uclhc/uci/user/dantrim/SuperFitter/HistFitter-00-00-49-TestExclFix/results/" 

########################################
# location of HF logs used for gathering
# upper limit results
########################################
#conf.log_dir = "/data/uclhc/uci/user/dantrim/SuperFitter/HistFitter-00-00-49-TestExclFix/results/runlogs/" 
conf.ul_name_suffix = "_limitOnMu.log"


########################################
# axis labels
########################################
conf.x_title = "m_{#tilde{#chi}_{1}^{#pm}} [GeV]"
conf.y_title = "m_{#tilde{#chi}_{1}^{ 0}} [GeV]"

#######################################
# limit plot grid ranges
#######################################
conf.xlow   = 100       # GeV
conf.xhigh  = 750       # GeV
conf.ylow   = 0         # GeV 
conf.yhigh  = 450       # GeV


#######################################
# forbidden lines
#######################################



#######################################
# decay process
#######################################
conf.decay_process = "#scale[0.8]{C1C1 via slepton}"
#conf.decay_process = "#scale[0.8]{#tilde{t} #rightarrow bW#tilde{#chi}_{1}^{ 0}  }"


######################################################
# which plot to plot
######################################################

## best SR per point
conf.do_best_sr_per_point = True

conf.do_limit_plot = True

## CLs/Sig per point
conf.show_exp_cls = False
conf.show_obs_cls = True
conf.show_obs_sig = False
conf.show_exp_sig = False

## xsec upper limit
conf.do_xsec_plot = False


########################################
# 8 TeV results
########################################
conf.show_previous_8TeV_result = True
conf.previous_result_file = "/data/uclhc/uci/user/amete/limits_twolepton/8tev_2lewk_limits/combined_obs.root"
conf.previous_contours = {}
conf.previous_contours["mt2"] = "contour_obs"
conf.previous_contours["superrazor"] = "Graph"


#######################################
# file the regions
#######################################
for i, region in enumerate(regions) :
    r = Region(region)
    r.color = region_colors[i]
    r.shape = region_marker_styles[i]
    conf.regions.append(r)

