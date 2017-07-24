import ROOT as r

def mirror_borders(hist):
    numx = hist.GetNbinsX()
    numy = hist.GetNbinsY()
    
    # corner points
    hist.SetBinContent(0,0,hist.GetBinContent(1,1))
    hist.SetBinContent(numx+1,numy+1,hist.GetBinContent(numx,numy))
    hist.SetBinContent(numx+1,0,hist.GetBinContent(numx,1))
    hist.SetBinContent(0,numy+1,hist.GetBinContent(1,numy))
    
    for i in range(1,numx+1):
      hist.SetBinContent(i,0,	   hist.GetBinContent(i,1))
      hist.SetBinContent(i,numy+1, hist.GetBinContent(i,numy))
    for i in range(1,numy+1):
      hist.SetBinContent(0,i,      hist.GetBinContent(1,i))
      hist.SetBinContent(numx+1,i, hist.GetBinContent(numx,i))

def set_borders(hist,val=0):
  numx = hist.GetNbinsX()
  numy = hist.GetNbinsY()
  
  for i in range(1,numx+1):
    hist.SetBinContent(i,0,val)
    hist.SetBinContent(i,numy+1,val)
  for i in range(1,numx+1):
    hist.SetBinContent(0,i,val)
    hist.SetBinContent(numx+1,i,val)

def add_borders(hist,name="",title=""):
  nbinsx = hist.GetNbinsX()
  nbinsy = hist.GetNbinsY()
  
  xbinwidth = float( hist.GetXaxis().GetBinCenter(nbinsx) - hist.GetXaxis().GetBinCenter(1) ) / float(nbinsx-1)
  ybinwidth = float( hist.GetYaxis().GetBinCenter(nbinsy) - hist.GetYaxis().GetBinCenter(1) ) / float(nbinsy-1)
  
  xmin = hist.GetXaxis().GetBinCenter(0) - xbinwidth/2. 
  xmax = hist.GetXaxis().GetBinCenter(nbinsx+1) + xbinwidth/2. 
  ymin = hist.GetYaxis().GetBinCenter(0) - ybinwidth/2. 
  ymax = hist.GetYaxis().GetBinCenter(nbinsy+1) + ybinwidth/2. 
  
  histX = r.TH2F(name, title, nbinsx+2, xmin, xmax, nbinsy+2, ymin, ymax)
 
  for ibin1 in range(0,hist.GetNbinsX()+2): 
    for ibin2 in range(0,hist.GetNbinsY()+2): 
      histX.SetBinContent( ibin1+1, ibin2+1, hist.GetBinContent(ibin1,ibin2) )
  
  return histX

def extract_graph_from_histo(org_histo):
    result      = r.TGraph2D(1)
    pvalue      = 0.05
    level       = r.TMath.NormQuantile(1.0-pvalue)
    copy_histo  = org_histo.Clone()
    copy_histo.SetDirectory(0)
    mirror_borders(copy_histo)
    histo1 = add_borders(copy_histo,"histo1","histo1")
    set_borders(histo1,0)
    histo2 = add_borders(histo1,"histo2","histo2")
    histo3 = histo2.Clone()
    histo3.SetName("histo3")
    histo3.SetTitle("histo3")
    gbc, nx, ny = histo3.GetBinContent, histo3.GetNbinsX(), histo3.GetNbinsY()
    histo3.SetContour(1)
    histo3.SetContourLevel(0,level)
    canvas      = r.TCanvas("tmp_can","tmp_can")
    canvas.cd()
    histo3.Draw("CONT LIST")
    canvas.Update()
    contours    = r.gROOT.GetListOfSpecials().FindObject('contours')
    if contours.GetEntries() : 
        result = contours.At(0).First()
        contours.Delete()
        histo3.Delete()
    return result

def process_fourbody_countours():
    # Open output
    #directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results/SR4body_stop2L_tN/"
    #directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_Apr6/SR34body_stop2L_tN/"
    #directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_Apr6/SR2body_stop2L_tN/"
    directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_May2/SR34body_stop2L_tN/"
    #directory = "/data/uclhc/uci/user/amete/limits_twolepton/limitplotter/limit_results_May2/SR2body_stop2L_tN/"
    outputfile = r.TFile(directory+"Graphs.root","RECREATE")

    # Open input
    #inputfile  = r.TFile(directory+"SmoothedFourBody.root","READ")
    inputfile  = r.TFile(directory+"SR34body_stop2L_tN_Nominal_MassPlane.root","READ")
    #inputfile  = r.TFile(directory+"SR34body_stop2L_tN_Up_MassPlane.root","READ")
    #inputfile  = r.TFile(directory+"SR2body_stop2L_tN_Nominal_MassPlane.root","READ")
    #inputfile  = r.TFile(directory+"SR2body_stop2L_tN_Up_MassPlane.root","READ")

    # Obs, Exp w/ +/-1sigma 
    histo = inputfile.Get("sigp1clsf").Clone() # Obs
    result = extract_graph_from_histo(histo)
    result.SetName("obs_nominal")
    result.SetTitle("obs_nominal")
    outputfile.cd()
    result.Write()

    histo = inputfile.Get("sigp1expclsf").Clone() # Exp
    result = extract_graph_from_histo(histo)
    result.SetName("exp_nominal")
    result.SetTitle("exp_nominal")
    outputfile.cd()
    result.Write()

    histo = inputfile.Get("sigclsu1s").Clone() # Exp + 1 sigma
    result = extract_graph_from_histo(histo)
    result.SetName("exp_up")
    result.SetTitle("exp_up")
    outputfile.cd()
    result.Write()

    histo = inputfile.Get("sigclsd1s").Clone() # Exp - 1 sigma
    result = extract_graph_from_histo(histo)
    result.SetName("exp_dn")
    result.SetTitle("exp_dn")
    outputfile.cd()
    result.Write()
    
    # Close the files
    inputfile.Close()
    outputfile.Close()

if "__main__" in __name__:
    process_fourbody_countours()

    ## Open the output
    #outputfile = r.TFile("Graphs_of_8TeV_ATLAS_results.root","UPDATE")

    ## Get the graphs
    ##
    #r.gROOT.LoadMacro("graphs_Limits_FourBody_ICHEP14.C")
    #result = r.graph_Observed.Clone() 
    #result.SetName("FourBody_ICHEP14_Obs")
    #result.SetTitle("FourBody_ICHEP14_Obs")
    #outputfile.cd()
    #result.Write()

    ##
    #inputfile = r.TFile("contours_WW.root","READ")
    #result = inputfile.Get("obs_nominal").Clone() 
    #result.SetName("WWlike_Obs")
    #result.SetTitle("WWlike_Obs")
    #outputfile.cd()
    #result.Write()
    #inputfile.Close()

    ##
    #inputfile = r.TFile("Charm_Stop_Comb_V30_Nominal_hypotest__1_harvest_list.root","READ")
    #histo  = inputfile.Get("sigp1clsf").Clone() 
    #result = extract_graph_from_histo(histo) 
    #result.SetName("Charm_Stop_Comb_Obs")
    #result.SetTitle("Charm_Stop_Comb_Obs")
    #outputfile.cd()
    #result.Write()
    #inputfile.Close()

    ##
    #r.gROOT.LoadMacro("OneLepton_limit_SoftLepton_Paper2013_v12_AllSRs_Stop4body_Nominal_result__1_harvest_list_EXP_1006.C")
    #histo  = r.firstObsH.Clone() 
    #result = extract_graph_from_histo(histo) 
    #result.SetName("OneLepton_SoftLepton_Obs")
    #result.SetTitle("OneLepton_SoftLepton_Obs")
    #outputfile.cd()
    #result.Write()

    ##
    #r.gROOT.LoadMacro("Charm_graphs_Limits_Stop_ICHEP14.C")
    #result = r.graph_Observed.Clone() 
    #result.SetName("Charm_Stop_ICHEP14_Obs")
    #result.SetTitle("Charm_Stop_ICHEP14_Obs")
    #outputfile.cd()
    #result.Write()

    ##
    #r.gROOT.LoadMacro("Combined_Zero_1Lepton_tN1_BR100.C")
    #histo  = r.hg2.Clone()
    #result = extract_graph_from_histo(histo) 
    #result.SetName("Combined_Zero_1Lepton_Obs")
    #result.SetTitle("Combined_Zero_1Lepton_Obs")
    #outputfile.cd()
    #result.Write()

    ##
    #r.gROOT.LoadMacro("OneLepton_3body_2014.C")
    #histo  = r.thb_obs.Clone()
    #result = extract_graph_from_histo(histo) 
    #result.SetName("OneLepton_3body_Obs")
    #result.SetTitle("OneLepton_3body_Obs")
    #outputfile.cd()
    #result.Write()

    ##
    #r.gROOT.LoadMacro("TwoLepton_contour_obs_nom_2l_21_3b.C")
    #histo  = r.l2_3b_obs.Clone()
    #result = extract_graph_from_histo(histo) 
    #result.SetName("TwoLepton_2l_21_3b_Obs")
    #result.SetTitle("TwoLepton_2l_21_3b_Obs")
    #outputfile.cd()
    #result.Write()

    ## Close the output
    #outputfile.Close()
