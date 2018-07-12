# TMVA linear discriminators

import ROOT
from ROOT import TChain, TSelector, TTree, TFile, TLorentzVector, std
#from ROOT import *
#from ROOT import std
import math

chainS = ROOT.TChain("ntuple","")
chainS.Add("MC_resonance_search_signal.root/ntuple")

chainB = TChain("ntuple","")
chainB.Add("MC_resonance_search_background_small.root/ntuple")

chainD = TChain("ntuple","")
chainD.Add("data.root/ntuple")



#chainB.Print()
#fin = ROOT.TFile.Open("ntuple.root")
#ntuple = fin.Get('ntuple')
#ntuple.Print()

noe=0
Vp=TLorentzVector(0,0,0,0)
Vm=TLorentzVector(0,0,0,0)
plus = std.vector('int')()
minus = std.vector('int')()
lst=[chainS,chainB,chainD]
lst2=["out_sig2.root","out_bkg2.root","out_dat2.root"]
file=open("liczba.txt", "w")
for xr in range(3):
	a=lst2[xr]
	chain=lst[xr]
	od=TFile(a, "recreate")
	minv=ROOT.TH1F("minv", "", 300, 0, 40)
	entries = chain.GetEntries()
	noe+=entries
	print "entries ",entries
	print chain  


	for jentry in xrange( entries ):
		#get the next tree in the chain
		ientry = chain.LoadTree(jentry)
		if ientry < 0:
			break

		#verify file/tree/chain integrity
		nb = chain.GetEntry( jentry )
		if nb <= 0:
			continue
		 
		  #find pairs
		plus.clear()
		minus.clear()
	
		if chain.x.size()>=2: 
			for i in xrange(chain.x.size()):
				if chain.mu_like[i]>0.85:
					if ( chain == chainS and abs(chain.id[i])==13) or (chain == chainB or chain==chainD ):
						if chain.charge[i]==1:
							plus.push_back(i)
						elif chain.charge[i]==-1:
							minus.push_back(i)
						
			 

		r1=plus.size()
		r2=minus.size()  
		for i in xrange(r1):
			Vp.SetPxPyPzE(chain.px[plus[i]],chain.py[plus[i]],chain.pz[plus[i]],chain.e[plus[i]])
			for j in xrange(r2):
				Vm.SetPxPyPzE(chain.px[minus[j]],chain.py[minus[j]],chain.pz[minus[j]],chain.e[minus[j]])
				deltaPhi=Vp.DeltaPhi(Vm)
				deltaZ=chain.z[plus[i]]-chain.z[minus[j]]
				#pT1 = plusV.Pt()
				#pT2 = minusV.Pt()
				if (abs(deltaPhi)>3 and abs(deltaZ)<0.04):
					invMass = (Vp+Vm).M()
					minv.Fill(invMass)
			   
	file.write(str(noe))
	file.write("\n")
	noe=0				   
	od.Write()
	od.Close()
file.close()



#TMVA::TMVAGui()
#ROOT.TMVA.TMVAGui()
