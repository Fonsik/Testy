# TMVA linear discriminators

import ROOT
#from ROOT import TChain, TSelector, TTree
from ROOT import *
#from ROOT import std
import math


chainS = ROOT.TChain("ntuple","")
chainS.Add("MC_resonance_search_signal.root/ntuple")

chainB = TChain("ntuple","")
chainB.Add("MC_resonance_search_background_small.root/ntuple")

#chainB.Print()
#fin = ROOT.TFile.Open("ntuple.root")
#ntuple = fin.Get('ntuple')
#ntuple.Print()


plus = std.vector('int')()
minus = std.vector('int')()
minv=ROOT.TH1F("minv", "", 300, 0, 40)
h_x=TH1F("h_x", "", 100, -1e-4, 1e-4)

for chain in {chainS, chainB}:
#    print chain

    entries = chain.GetEntriesFast()



    for jentry in xrange( entries ):
    # get the next tree in the chain
      ientry = chain.LoadTree(jentry)
      if ientry < 0:
         break

    # verify file/tree/chain integrity
      nb = chain.GetEntry( jentry )
      if nb <= 0:
         continue
     
      #find pairs
      plus.clear()
      minus.clear()


      if chain.x.size()>=2:
	for i in xrange(chain.x.size()):
         h_x.Fill(chain.x[i])
         # some cut-like selection
         if chain.mu_like[i]>0.85:
          if ( chain == chainS and abs(chain.id[i])==13) or (chain == chainB ):
           if chain.charge[i]==1:
            plus.push_back(i)
	   elif chain.charge[i]==-1:
            minus.push_back(i)

     

           
      for i in xrange(plus.size()):
          plusV = TLorentzVector(0,0,0,0)
          plusV.SetPxPyPzE(chain.px[plus[i]],chain.py[plus[i]],chain.pz[plus[i]],chain.e[plus[i]])
          for j in xrange(minus.size()):
              minusV = TLorentzVector(0,0,0,0)
              minusV.SetPxPyPzE(chain.px[minus[j]],chain.py[minus[j]],chain.pz[minus[j]],chain.e[minus[j]])
              deltaPhi=plusV.DeltaPhi(minusV)
              deltaZ=chain.z[minus[j]]-chain.z[plus[i]]
              pT1 = plusV.Pt()
              pT2 = minusV.Pt()
              mu_like_1=chain.mu_like[plus[i]]
              mu_like_2=chain.mu_like[minus[j]]
              if abs(deltaPhi)>1 and abs(deltaZ)<0.04
               invMass = (plusV+minusV).M()
               minv.Fill(invMass)

#TMVA::TMVAGui()
#ROOT.TMVA.TMVAGui()




