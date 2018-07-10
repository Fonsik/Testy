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

chainD = TChain("ntuple","")
chainD.Add("data.root/ntuple")



#chainB.Print()
#fin = ROOT.TFile.Open("ntuple.root")
#ntuple = fin.Get('ntuple')
#ntuple.Print()

noe=0
plus = std.vector('int')()
minus = std.vector('int')()
minv=ROOT.TH1F("minv", "", 300, 0, 40)
h_x=TH1F("h_x", "", 100, -1e-4, 1e-4)
lst=[chainS,chainB,chainD]
lst2=["out_sig2.root","out_bkg2.root","out_dat2.root"]
file=open("liczba.txt", "w")
for x in range(3):
	for chain in (lst[x]):
	#    print chain
		od=TFile(lst2[x], "recreate")
		entries = chain.GetEntriesFast()
		noe+=entries
		
		  


		#for jentry in xrange( entries ):
		# get the next tree in the chain
		 # ientry = chain.LoadTree(jentry)
		  #if ientry < 0:
			# break

		# verify file/tree/chain integrity
		  #nb = chain.GetEntry( jentry )
		  #if nb <= 0:
			# continue
		 
		  #find pairs
		plus.clear()
		minus.clear()


		if chain.x.size()>=2:
			for i in xrange(chain.x.size()):
				if (abs(chain.id[i])==13 or chain.mu_like[i]>0.85):
					if chain.charge[i]==1:
						plus.push_back(i)
					elif chain.charge[i]==-1:
						minus.push_back(i)

			 

				   
				for i in xrange(plus.size()):
					plusV = TLorentzVector(0,0,0,0)
					plusV.SetPxPyPzE(chain.px[plus[i]],chain.py[plus[i]],chain.pz[plus[i]],chain.e[plus[i]])
					for j in range(minus.size()):
						minusV = TLorentzVector(0,0,0,0)
						minusV.SetPxPyPzE(chain.px[minus[j]],chain.py[minus[j]],chain.pz[minus[j]],chain.e[minus[j]])
						deltaPhi=plusV.DeltaPhi(minusV)
						deltaZ=chain.z[minus[j]]-chain.z[plus[i]]
						#pT1 = plusV.Pt()
						#pT2 = minusV.Pt()
						if (abs(deltaPhi)>1 and abs(deltaZ)<0.04):
							invMass = (plusV+minusV).M()
							print j
							print invMass
							minv.Fill(invMass)
						   
	file.write(str(noe))
	file.write("\n")
	noe=0				   
	od.Write()
	od.Close()
file.close()



#TMVA::TMVAGui()
#ROOT.TMVA.TMVAGui()




