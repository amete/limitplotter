#
# this script will parse the limit results in the
# limit_results directory, build the signal points,
# and make the limit plots
#
# daniel.joseph.antrim@cern.ch
# July 2016
#

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 3001;" )

import os
import sys
sys.path.append(os.environ['LIMPLOTDIR'])

from optparse import OptionParser
import glob
import operator # itemgetter

# limitplotter
from limitplotter.utils.grid_configuration import *
from limitplotter.utils.limit_plot_tools import *

def get_configuration(grid) :
    configuration_file = ""
    if grid == "bWN" :
        configuration_file = "SRwt_sfdf.py"
    elif grid == "c1c1_slep" :
        configuration_file = "c1c1_slep.py"
    elif grid == "SlepSlep" :
        configuration_file = "SlepSlep.py"
    elif grid == "tN" :
        configuration_file = "SRall_stop2L_tN.py"
    else :
        print "get_configuration    ERROR unsupported grid. Exiting."
        sys.exit()

    print "get_configuration    grabbing configuration file (%s)"%configuration_file
    return configuration_file

def find_best_SR_per_point(conf) :
    '''
    For each signal point, loop over the regions and
    determine which is the best based on which has the
    largest expected significance.
    '''
    signals = conf.signals   # list of signal points [ Signal ]
    regions = conf.regions   # list of regions       [ Region ]
    
    for s in signals :
        exp_sig_dict = s.expectedSig
        best_region = max(exp_sig_dict.iteritems(), key=operator.itemgetter(1))[0]
        
        s.bestRegion = best_region
        # fill the best region values
        # CLs
        s.bestObservedCLs = s.observedCLs[best_region]
        s.bestExpectedCLs = s.expectedCLs[best_region]
        s.bestExpectedCLsUp1s = s.expectedCLsUp1s[best_region]
        s.bestExpectedCLsDn1s = s.expectedCLsDn1s[best_region]
        # signif.
        s.bestObservedSig = s.observedSig[best_region]
        s.bestExpectedSig = s.expectedSig[best_region]
        s.bestExpectedSigUp1s = s.expectedSigUp1s[best_region]
        s.bestExpectedSigDn1s = s.expectedSigDn1s[best_region]
        # observed CLs up/down
        if s.observedCLsUp1s : s.bestObservedCLsUp1s = s.observedCLsUp1s[best_region]
        if s.observedCLsDn1s : s.bestObservedCLsDn1s = s.observedCLsDn1s[best_region]
        # observed signif. up/down
        if s.observedSigUp1s : s.bestObservedSigUp1s = s.observedSigUp1s[best_region]
        if s.observedSigDn1s : s.bestObservedSigDn1s = s.observedSigDn1s[best_region]
        # observed upper cross section limits
        if s.observedXsecUL  : s.bestObservedXsecUL  = s.observedXsecUL[best_region]

def make_best_sr_plot(conf) :
    '''
    Make a plot showing a region marker for the best
    region at each point
    '''
    c = conf.best_sr_canvas
    c.cd()
    
    # draw the frame/axes
    frame = make_frame(conf)
    frame.Draw("axis")
    frame.GetXaxis().SetTitle(conf.x_title)
    frame.GetYaxis().SetTitle(conf.y_title)
 #   frame.GetXaxis().CenterTitle()
 #   frame.GetYaxis().CenterTitle()
    c.Update()

    ## draw forbidden line
    #line = draw_forbidden_line(conf)
    #draw_text( (0.0 + 1.5*ROOT.gPad.GetLeftMargin()), (1.0-8.6*ROOT.gPad.GetTopMargin()), ROOT.kGray+2, conf.forbidden_line_text, size=0.03, angle=32.8)
    #line.Draw()
    #c.Update()

    # make legend
    leg = make_default_legend(0.65,0.68,0.90,0.90)
    # for the best-sr-per-point plot the legend entries
    # can be ambiguous if the plotted markers overlap it
    # so make this legend solid fill
    leg.SetFillColor(ROOT.kWhite)
    leg.SetFillStyle(1001)
    leg.SetHeader("Best Selection")
    leg.Draw()

    # gather the shapes/colors/markers by region
    shapes = {}
    colors = {}
    markers = {}
    for r in conf.regions :
        m = ROOT.TMarker()
        m.SetX(-999)
        m.SetY(-999)
        m.SetMarkerStyle(r.shape)
        m.SetMarkerColor(r.color)
        colors[r.name] = r.color
        shapes[r.name] = r.shape
        m.SetMarkerSize(2.0 * m.GetMarkerSize())
        markers[r.name] = m
        m.Draw()
    # now add the legend entries (ROOT is stupid and doesn't
    # let me do this in the previous loop 
    for reg in sorted(markers) :
        leg.AddEntry(markers[reg], conf.proper_names[reg], 'p')
    c.Update() 

    # now draw the points
    ms = []
    for s in conf.signals :
        x = s.mX
        y = s.mY
        sr = s.bestRegion
        marker = ROOT.TMarker()
        marker.SetX(float(x))
        marker.SetY(float(y))
        marker.SetMarkerStyle(shapes[str(sr)])
       # marker = ROOT.TMarker(float(x), float(y), shapes[sr] )
        marker.SetMarkerSize(2.0 * marker.GetMarkerSize())
        marker.SetMarkerColor(colors[sr])
        ms.append(marker)
    for marker in ms :
        marker.Draw('same')

    # draw legend again to make sure it is not hidden 
    # by plotted grid points
    leg.Draw()
    c.Update()

    ## draw "official" and process labels
    #draw_top_left_label(get_atlas_label(),  (0.0 + 1.2*ROOT.gPad.GetLeftMargin()), (1.0-1.5*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(get_lumi_label(),   (0.0 + 1.2*ROOT.gPad.GetLeftMargin()), (1.0-2.4*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(conf.decay_process, (0.0 + 1.25*ROOT.gPad.GetLeftMargin()), (1.0-3.2*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(conf.mass_info,     (0.0 + 1.2*ROOT.gPad.GetLeftMargin()), (1.0-4.0*ROOT.gPad.GetTopMargin()))

    save_name = get_bestSR_output_name(conf)
    print " >>> Savig best-sr-per-point plot to %s"%save_name
    c.SaveAs(save_name)

def get_bestSR_output_name(conf) :
    outname = ""
    outname += "bestSRplot_"
    outname += conf.base_region
    outname += "_"
    outname += conf.grid
    outname += "_"
    if conf.channel != "" :
        outname += conf.channel
    outname += ".pdf"
    return outname

def draw_sig_or_cls(conf, reg_="", pwc=False) :

    print "draw_sig_or_cls    NEED TO HANDLE PWC CASE"
    c = conf.limit_canvas
    c.cd()

    tex = ROOT.TLatex(0.0,0.0,"")
    tex.SetTextFont(42)
    tex.SetTextSize(0.35 * tex.GetTextSize())
    tex.SetTextAngle(50)
    #tex.SetTextSize(0.5 * tex.GetTextSize())
    markers = []
    for s in conf.signals :
        val, x, y = 0.0, 0.0, 0.0
        x = float(s.mX)
        #if x>400: continue
        y = float(s.mY)
        if x > 810 : continue
        if y > 400 : continue
        if (x-y) > 19. and (x-y)<21: continue
        if (x-y) > 49. and (x-y)<51: continue
        if (x-y) > 89. and (x-y)<91: continue
        ##### SERHAN
        ##### SERHAN
        ##### SERHAN
        # Hack...
        if "2body" in reg_ and (x-y<172): continue
        #elif "3body" in reg_ and (x-y>172 or (x-y)%10!=0 or x%25!=0 or (x-y)<25 or ((x-y) <= 80. and x>= 500.)): continue
        ##elif "3body" in reg_ and (x-y<85. or x-y>172): continue
        #elif "4body" in reg_ and (x-y>80.): continue
        elif "34body" in reg_ and (x-y>172.): continue
        ##### SERHAN
        ##### SERHAN
        ##### SERHAN
        if conf.show_exp_cls :
            val = float(s.expectedCLs[reg_])
        elif conf.show_obs_cls :
            val = float(s.observedCLs[reg_])
        elif conf.show_obs_sig :
            val = float(s.observedSig[reg_])
        elif conf.show_exp_sig :
            val = float(s.expectedSig[reg_])
        elif conf.do_xsec_plot:
            val = float(s.observedXsecUL[reg_])

        #if "SRwt" in reg_ and y > 300 : continue

        tex.DrawLatex(x, y, "%.2f"%float(val))

    z_title = ""
    if   conf.show_exp_cls : z_title = "Numbers give the expected CL_{s} values"
    elif conf.show_obs_cls : z_title = "Numbers give the observed CL_{s} values"
    elif conf.show_obs_sig : z_title = "Numbers give the observed Significance"
    elif conf.show_exp_sig : z_title = "Numbers give the expected Significance"
    elif conf.show_exp_sig : z_title = "Numbers give the expected Significance"
    elif conf.do_xsec_plot : z_title = "Numbers give the observed Excluded Model Cross-sections [pb]"

    if not conf.do_xsec_plot:
        draw_text(0.96,0.38,ROOT.kBlack,z_title,angle=90.0, size=0.03)
    else:
        draw_text(0.96,0.13,ROOT.kBlack,z_title,angle=90.0, size=0.03)
    c.Update()

def save_hepdata_root_file(conf, reg_="", pwc = False):

    print "save_hepdata_root_file    NEED TO HANDLE PWC CASE"

    hist_name = ""
    if conf.show_exp_cls :
        hist_name = "exp_cls_TH2" 
    elif conf.show_obs_cls :
        hist_name = "obs_cls_TH2" 
    elif conf.do_xsec_plot:
        hist_name = "obs_xs_TH2" 

    out_file = ROOT.TFile("ExclusionHEPData.root","UPDATE")
    if out_file.GetListOfKeys().Contains(hist_name):
        hist = out_file.Get(hist_name)
    else:
        hist = ROOT.TH2F(hist_name, hist_name, 750, 100, 850, 600, 0, 600)

    for s in conf.signals :
        val, x, y = 0.0, 0.0, 0.0
        x = float(s.mX)
        y = float(s.mY)
        ##### SERHAN
        ##### SERHAN
        ##### SERHAN
        if "2body" in reg_ and (x-y<172): continue
        elif "34body" in reg_ and (x-y>172.): continue
        ##### SERHAN
        ##### SERHAN
        ##### SERHAN
        if conf.show_exp_cls :
            hist.Fill(x,y,float(s.expectedCLs[reg_]))
        elif conf.show_obs_cls :
            hist.Fill(x,y,float(s.observedCLs[reg_]))
        elif conf.do_xsec_plot:
            hist.Fill(x,y,float(s.observedXsecUL[reg_]))

    graph = ROOT.TGraph2D(hist)    
    graph.SetName(hist_name.replace("TH2","TGraph2"))
    graph.SetTitle(hist_name.replace("TH2","TGraph2"))

    out_file.cd()
    hist.Write()
    graph.Write()
    out_file.Close()

def draw_upperlimit_xsec(conf) :
    print "draw_upperlimit_xsec    THIS METHOD IS NOT IMPLEMENTED"

def get_limit_output_name(conf) :
    outname = ""
    outname += "limplot_"
    outname += conf.base_region
    outname += "_"
    outname += conf.grid
    outname += "_"
    if conf.channel != "" :
        outname += conf.channel
        outname += "_"
    if conf.do_xsec_plot : outname += "exclXS"
    elif conf.show_exp_cls : outname += "expCLs"
    elif conf.show_obs_cls : outname += "obsCLs"
    elif conf.show_exp_sig : outname += "expSig"
    elif conf.show_obs_sig : outname += "obsSig" 
    outname += ".pdf"
    return outname

def get_forbiddenlines(conf) :

    out_lines = []

    if grid == "bWN" or grid == "tN":

        x_low = conf.xlow
        y_low = conf.ylow

        # mW line
        y_high_w = 400 #320
        slope = 1.0
        y_w = slope * x_low - 84.8
        beginx = x_low
        endx_w = 500 #400
        #endx_w = 1.2*320

        line_w = ROOT.TLine(beginx, y_w, endx_w, endx_w * slope - 84.8)
        line_w.SetLineStyle(2)
        line_w.SetLineWidth(2)
        line_w.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_w)

        # mTop line
        beginx = 172.5
        y_t = 0.0
        endx_t = 550 #450

        line_t = ROOT.TLine(beginx, y_t, endx_t, endx_t * slope - 172.5)
        line_t.SetLineStyle(2)
        line_t.SetLineWidth(2)
        line_t.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_t)

        # mchi line
        beginx = x_low
        y_chi = 100
        endx_chi = 450 #317
        line_chi = ROOT.TLine(beginx, y_chi, endx_chi, endx_chi * slope) 
        line_chi.SetLineStyle(2)
        line_chi.SetLineWidth(2)
        line_chi.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_chi)

    else :
        print "get_forbiddenlines    ERROR unhandled grid. Will not draw kinematic boundary lines."
    return out_lines


def make_limit_plot(conf) :
    print "make_limit_plot..."

    c = conf.limit_canvas
    c.cd()

    ################################
    # draw the frame/axes
    ################################
    frame = make_frame(conf)
    frame.Draw("axis")
    frame.GetXaxis().SetTitle(conf.x_title)
    frame.GetYaxis().SetTitle(conf.y_title)
    c.Update()

    ################################# 
    # make a legend
    ################################# 
    leg = make_default_legend(0.55,0.72,0.89,0.91)

    ########################################
    ### draw previous results
    ########################################
    ##if conf.show_previous_8TeV_result :
    ##    rfile = ROOT.TFile(conf.previous_result_file)
    ##    for key, value in conf.previous_contours.iteritems():
    ##        exclusion_8TeV = rfile.Get(value)
    ##        exclusion_8TeV.SetLineColor((ROOT.kAzure+6))
    ##        exclusion_8TeV.SetFillColor((ROOT.kAzure+6))
    ##        exclusion_8TeV.Draw("same F")

    ##    ##prev_wwlike = rfile.Get(conf.previous_contours["wwlike"])
    ##    ##prev_stop1l = rfile.Get(conf.previous_contours["stop1l"])
    ##    ##prev_stop2l = rfile.Get(conf.previous_contours["stop2l"])

    ##    ###prev_wwlike.SetLineColor(ROOT.TColor.GetColor("#FF4444"))
    ##    ###prev_stop1l.SetLineColor(ROOT.TColor.GetColor("#F685E4"))
    ##    ###prev_stop2l.SetLineColor(ROOT.TColor.GetColor("#B93B8F"))

    ##    ##prev_wwlike.SetLineColor((ROOT.kAzure+6)+1)
    ##    ##prev_stop1l.SetLineColor((ROOT.kSpring-5)-1)
    ##    ##prev_stop2l.SetLineColor((ROOT.kOrange-3)-2)

    ##    ##prev_wwlike.SetFillColorAlpha(ROOT.kAzure+6, 0.65)
    ##    ##prev_stop1l.SetFillColorAlpha(ROOT.kSpring-5, 1.00)
    ##    ##prev_stop2l.SetFillColorAlpha(ROOT.kOrange-3,0.65)

    ##    ##prev_wwlike.SetLineWidth(3)
    ##    ##prev_stop1l.SetLineWidth(3)
    ##    ##prev_stop2l.SetLineWidth(3)

    ##    ###prev_wwlike.SetFillStyle( 1001 )
    ##    ###prev_wwlike.SetFillStyle( 3005 )
    ##    ###prev_wwlike.SetFillColorAlpha(ROOT.TColor.GetColor("#FF4444"), 0.1)

    ##    ##prev_stop1l.Draw("same F")
    ##    ##prev_stop2l.Draw("same F")
    ##    ##prev_wwlike.Draw("same F")

    ##    ##prev_stop1l.Draw("same")
    ##    ##prev_stop2l.Draw("same")
    ##    ##prev_wwlike.Draw("same")



    ################################
    # grab the 95% CL contours
    ################################

    g_obs = []
    g_obsUp = []
    g_obsDn = []
    g_exp = []
    g_expUp = []
    g_expDn = []
  
    # obs
    if grid == "bWN":
        g_obs       = make_contour(conf, reg_=region, type="obs", pwc=False)
        print "make_limit_plot   NOT GRABBING UP/DOWN OBSERVED CONTOURS"
        g_obsUp = None
        g_obsDn = None
        #g_obsUp     = make_contour(conf, reg_=region, type="obsUp", pwc=False)
        #g_obsDn     = make_contour(conf, reg_=region, type="obsDn", pwc=False)

        # exp
        g_exp       = make_contour(conf, reg_=region, type="exp", pwc=False)
        g_expUp     = make_contour(conf, reg_=region, type="expUp", pwc=False)
        g_expDn     = make_contour(conf, reg_=region, type="expDn", pwc=False)
    elif grid == "c1c1_slep":
        g_obs       = make_contour(conf, reg_=region, type="obs", pwc=True)
        print "make_limit_plot   NOT GRABBING UP/DOWN OBSERVED CONTOURS"
        g_obsUp = None
        g_obsDn = None
        #g_obsUp     = make_contour(conf, reg_=region, type="obsUp", pwc=True)
        #g_obsDn     = make_contour(conf, reg_=region, type="obsDn", pwc=True)

        # exp
        g_exp       = make_contour(conf, reg_=region, type="exp", pwc=True)
        g_expUp     = make_contour(conf, reg_=region, type="expUp", pwc=True)
        g_expDn     = make_contour(conf, reg_=region, type="expDn", pwc=True)
    elif grid == "SlepSlep":
        g_obs       = make_contour(conf, reg_=region, type="obs", pwc=True)
        print "make_limit_plot   NOT GRABBING UP/DOWN OBSERVED CONTOURS"
        g_obsUp = None
        g_obsDn = None
        #g_obsUp     = make_contour(conf, reg_=region, type="obsUp", pwc=True)
        #g_obsDn     = make_contour(conf, reg_=region, type="obsDn", pwc=True)

        # exp
        g_exp       = make_contour(conf, reg_=region, type="exp", pwc=True)
        g_expUp     = make_contour(conf, reg_=region, type="expUp", pwc=True)
        g_expDn     = make_contour(conf, reg_=region, type="expDn", pwc=True)
    elif grid == "tN":
        for r in conf.regions:
            if True: ###"4body" in r.name:
                if "34body" in r.name:
                    directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_May2/SR34body_stop2L_tN/"
                elif "2body" in r.name:
                    directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_May2/SR2body_stop2L_tN/"
                else: continue
                inputfile    = ROOT.TFile(directory+"Graphs.root","READ")
                inputfile_Up = ROOT.TFile(directory+"Graphs_Up.root","READ")
                inputfile_Dn = ROOT.TFile(directory+"Graphs_Down.root","READ")
                g_obs.append(inputfile.Get("obs_nominal").Clone())
                g_obsUp.append(inputfile_Up.Get("obs_nominal").Clone())
                g_obsDn.append(inputfile_Dn.Get("obs_nominal").Clone())
                g_exp.append(inputfile.Get("exp_nominal").Clone())
                g_expUp.append(inputfile.Get("exp_up").Clone())
                g_expDn.append(inputfile.Get("exp_dn").Clone())
                inputfile.Close()
            else: 
                # obs
                g_obs.append(make_contour(conf, reg_=r.name, type="obs", pwc=False))
                g_obsUp.append(None)
                g_obsDn.append(None)
                # exp
                g_exp.append(make_contour(conf, reg_=r.name, type="exp", pwc=False))
                g_expUp.append(make_contour(conf, reg_=r.name, type="expUp", pwc=False))
                g_expDn.append(make_contour(conf, reg_=r.name, type="expDn", pwc=False))

   # g_obs.SetName("stop2l_3body_observed")
   # g_obs.SaveAs("observed_contour.root")

   # g_exp.SetName("stop2l_3body_expected")
   # g_exp.SaveAs("expected_contour.root")

   # g_expUp.SetName("stop2l_3body_expected_u1s")
   # g_expUp.SaveAs("expected_contour_u1s.root")

   # g_expDn.SetName("stop2l_3body_expected_d1s")
   # g_expDn.SaveAs("expected_contour_d1s.root")

    if grid != "tN":
        #################################
        # draw the band around the
        # expected contours
        #################################
        make_exclusion_band(conf, g_exp, g_expUp, g_expDn)
        c.Update()

        ################################
        # draw the observed contours
        ################################
        g_obs.SetLineColor(ROOT.TColor.GetColor( c_Observed ))
        g_obs.SetLineStyle(1)
        g_obs.SetLineWidth(3)
        g_obs.Draw("C same")
        c.Update()

        for g in [g_obsUp, g_obsDn] :
            if not g : continue
            g.SetLineColor(ROOT.TColor.GetColor( c_Observed ))
            g.SetLineStyle(3)
            g.SetLineWidth(2)
            g.Draw("C same")
        c.Update()
    else:
        for index,r in enumerate(conf.regions):
            make_exclusion_band(conf, g_exp[index], g_expUp[index], g_expDn[index])
            c.Update()
        
            ################################
            # draw the observed contours
            ################################
            g_obs[index].SetLineColor(ROOT.TColor.GetColor( c_Observed ))
            g_obs[index].SetLineStyle(1)
            g_obs[index].SetLineWidth(3)
            g_obs[index].Draw("C same")
            c.Update()

            for g in [g_obsUp[index], g_obsDn[index]] :
                if not g : continue
                g.SetLineColor(ROOT.TColor.GetColor( c_Observed ))
                g.SetLineStyle(3)
                g.SetLineWidth(2)
                g.Draw("C same")
            c.Update()


    ######################################
    # draw previous results
    ######################################
    if conf.show_previous_8TeV_result :
        rfile = ROOT.TFile(conf.previous_result_file)
        for key, value in conf.previous_contours.iteritems():
            exclusion_8TeV = rfile.Get(value)
            exclusion_8TeV.SetLineColor((ROOT.kAzure+6))
            exclusion_8TeV.SetFillColor((ROOT.kAzure+6))
            exclusion_8TeV.Draw("same F")
        rfile.Close()
        # Top polarization
        #spinline_obs = ROOT.TLine(198, 0, 198, 198-172.5)
        #spinline_obs.SetLineWidth(1)
        #spinline_obs.SetLineColor((ROOT.kAzure+6))
        #spinline_obs.Draw("same F")
        from array import array
        x_spin = array('f',[ 172.5, 198.0,     198.0, 172.5 ])
        y_spin = array('f',[   0.0,   0.0, 198-172.5,   0.0 ])
        spinline_obs = ROOT.TPolyLine(4,x_spin, y_spin)
        spinline_obs.SetLineWidth(1)
        spinline_obs.SetLineColor((ROOT.kAzure+6))
        spinline_obs.SetFillColor((ROOT.kAzure+6))
        spinline_obs.Draw("f")

    #####################################
    # draw official and process labels
    #####################################
    draw_top_left_label(get_atlas_label(),  (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-1.6*ROOT.gPad.GetTopMargin()), font=72)
    #draw_top_left_label("Internal",         (0.125 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-1.6*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label("Internal",         (0.165 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-1.6*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label("Preliminary",         (0.165 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-1.6*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(get_lumi_label(),   (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-2.7*ROOT.gPad.GetTopMargin()))
    draw_top_left_label(get_lumi_label(),   (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-2.35*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(conf.decay_process, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-3.65*ROOT.gPad.GetTopMargin()))
    #draw_top_left_label(conf.decay_process, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-3.8*ROOT.gPad.GetTopMargin()))
    draw_top_left_label("#scale[0.75]{#tilde{t}_{1}#tilde{t}_{1} production, #tilde{t}_{1} #rightarrow t^{#scale[0.5]{(}}*^{#scale[0.2]{ }#scale[0.5]{)}} + #tilde{#chi}_{1}^{0}}", (0.0 + 1.*ROOT.gPad.GetLeftMargin()),   (0.915+ROOT.gPad.GetTopMargin()))
    draw_top_left_label("#scale[0.7]{All limits at 95% CL}",   (0.0 + 1.3*ROOT.gPad.GetLeftMargin()),   (1.0-3.2*ROOT.gPad.GetTopMargin()))
    if grid=="bWN" and region=="SRwt" :
        region_label = "SR_{W}^{3-body} + SR_{t}^{3-body}" 
        draw_top_left_label(region_label, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-4.7*ROOT.gPad.GetTopMargin()))  
    elif grid=="tN": # and region=="SRall" :
        region_label = "SR^{2/3/4-body}" 
        #draw_top_left_label(region_label, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-4.7*ROOT.gPad.GetTopMargin()))  
        #draw_top_left_label(region_label, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-5.4*ROOT.gPad.GetTopMargin()))  
    c.Update()

    ######################################
    # draw the legend
    ######################################
    #leg = make_default_legend(0.55,0.72,0.89,0.91)
    #leg = make_default_legend(0.55,0.77,0.88,0.92)
    if grid != "tN":
        leg.AddEntry(g_obs, "Observed limit (#pm1 #sigma_{theory}^{SUSY})","l")
    else:
        leg.AddEntry(g_obs[0], "Observed limit (#pm1 #sigma_{theory}^{SUSY})","l")

    #lines for the +/1 1 sigma theory
    #y_obs_up = 0.895 * 1.0075
    #y_obs_dn = 0.8699 * 1.013
    y_obs_up = 0.8825 * 1.0075
    y_obs_dn = 0.8575 * 1.013
    draw_line(0.5625, y_obs_up, 0.62115, y_obs_up, ROOT.TColor.GetColor(c_Observed), line_style=3, line_width=2)
    draw_line(0.5625, y_obs_dn, 0.62115, y_obs_dn, ROOT.TColor.GetColor(c_Observed), line_style=3, line_width=2)

    legend_band_entry(leg, "Expected limit (#pm1 #sigma_{exp})", ROOT.TColor.GetColor(c_BandYellow), 1001, ROOT.TColor.GetColor(c_Expected), 7, 2)



    ##leg.AddEntry(prev_wwlike, "ATLAS 8 TeV (WW-like)","f")
    ##leg.AddEntry(prev_stop2l, "ATLAS 8 TeV (Stop-2L)","f")
    ##leg.AddEntry(prev_stop1l, "ATLAS 8 TeV (Stop-1L)","f")
    leg.AddEntry(exclusion_8TeV,"ATLAS 8 TeV, 20 fb^{-1}","f")


    # now that we have all the contours, draw the legend
    leg.Draw()
    c.Update()

    #####################################
    # draw the forbidden lines
    #####################################
    kin_lines = get_forbiddenlines(conf)
    for line_ in kin_lines :
        line_.Draw()

    if "bWN" in grid or "tN" in grid:
        mwline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < m_{b} + m_{W}"
        mtline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < m_{t}"
        mxline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < 0"

        draw_text( 0.16, 0.33, ROOT.kGray+2, mxline_text, size=0.025, angle=50)
        draw_text( 0.17, 0.23, ROOT.kGray+2, mwline_text, size=0.025, angle=50)
        draw_text( 0.19, 0.14, ROOT.kGray+2, mtline_text, size=0.025, angle=50)
        #draw_text( 0.54, 0.51, ROOT.kGray+2, mwline_text, size=0.025, angle=39)
        #draw_text( 0.74, 0.51, ROOT.kGray+2, mtline_text, size=0.025, angle=41)
        #draw_text( 0.35, 0.51, ROOT.kGray+2, mxline_text, size=0.025, angle=41)

        Twobody_text = "2-body"
        Threebody_text = "3-body"
        Fourbody_text = "4-body"

        #draw_text( 0.50, 0.66, ROOT.kGray+2, Fourbody_text,  size=0.03, angle=50)
        #draw_text( 0.545, 0.605, ROOT.kGray+2, Threebody_text, size=0.03, angle=50)
        ##draw_text( 0.59, 0.56, ROOT.kGray+2, Twobody_text,   size=0.03, angle=50)
        #draw_text( 0.55, 0.2, ROOT.kGray+2, Twobody_text,   size=0.03, angle=0)
    c.Update()
        

    ######################################
    # draw CLs on plot
    ######################################
    if(conf.show_exp_cls or conf.show_obs_cls or conf.show_exp_sig or conf.show_obs_sig or conf.do_xsec_plot): #and not conf.do_xsec_plot :
        #draw_sig_or_cls(conf, reg_=region)
        for r in conf.regions:
            draw_sig_or_cls(conf, reg_=r.name)
            #save_hepdata_root_file(conf, reg_=r.name)

    
    #######################################
    ## draw upper limit on production xsec
    ## for each point
    #######################################
    #if conf.do_xsec_plot :
    #    draw_upperlimit_xsec(conf)


    ########################################
    # save
    ########################################
    save_name = get_limit_output_name(conf)
    print " >>> Saving limit plot to %s"%save_name
    ROOT.gPad.RedrawAxis()
    c.SaveAs(save_name)


#######################################################
if __name__ == "__main__" :

    global grid, channel

    parser = OptionParser()
    parser.add_option("-c", "--channel", default="")
    parser.add_option("-g", "--grid", default="")
    (options, args) = parser.parse_args()

    channel     = options.channel
    grid        = options.grid

    if channel=="" or grid=="" :
        print "ERROR input options are empty (channel: %s, grid: %s)"%(channel, grid)
        sys.exit()

    conf_file = get_configuration(grid)
    #execute the grid configuration
    gridConf = GridConfiguration(grid)
    gridConf.name = gridConf
    gridConf.channel = channel
    execfile("./config/%s"%conf_file)

    # have now loaded everything
    print "=================================="
    print "  limitplotter summary            "
    print "----------------------------------"
    print " configuration file:  %s          "%conf_file
    print " grid:                %s          "%gridConf.grid
    print " channel:             %s          "%gridConf.channel
    print " base region:         %s          "%gridConf.base_region
    print " do limit plot:       %s          "%gridConf.do_limit_plot
    print " show obs CLs:        %s          "%gridConf.show_obs_cls
    print " show exp CLs:        %s          "%gridConf.show_exp_cls
    print " show obs signif.:    %s          "%gridConf.show_obs_sig
    print " show exp signif.:    %s          "%gridConf.show_exp_sig
    print " do best SR plot:     %s          "%gridConf.do_best_sr_per_point
    print " do xsec plot:        %s          "%gridConf.do_xsec_plot
    print " show previous limit: %s          "%gridConf.show_previous_8TeV_result
    print "=================================="


    # collect limit result files
    gridConf.collect_limit_result_files()

    # build the grid
    gridConf.assign_grid()

    # fill the 'raw' limit results
    gridConf.fill_raw_results()

    for s in gridConf.signals :
        print "(%.1f,%.1f)"%(float(s.mX), float(s.mY))


    # find the best SR per point (if doing PWC)
    find_best_SR_per_point(gridConf)

    if gridConf.do_best_sr_per_point :
        make_best_sr_plot(gridConf)

    # make the limit plot
    if gridConf.do_limit_plot or gridConf.do_xsec_plot :
        make_limit_plot(gridConf)


