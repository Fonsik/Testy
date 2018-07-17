#!/usr/bin/env python
 
import ROOT
from ROOT import TMVA, TFile, TString, TTree, TLorentzVector
from array import array
from subprocess import call
from os.path import isfile
from ROOT import std

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader("Color:!Silent")




# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.

#plus = std.vector('int')()
#minus = std.vector('int')()

chain = ROOT.TChain("ntuple","")
# Muon data
chain.Add("~/Test/Testy/out_dat.root/ntuple")
# Electron data
#chain.Add("data12/Egamma.PhysCont.grp14.root/tau")







'''varList = ["x1","y1","z1","px1","py1","pz1","x2","y2","z2","px2","py2","pz2","mu_like_1","mu_like_2",
"deltaZ","deltaPhi","pT_1","pT_2",
"invMass"]'''

varList = ["mu_likep","mu_likem","dist","DeltPhi","minv"]


import array
#The use of arrays is needed, because the pointer to the address of the object that is used for filling must be given to the TTree::Branch() call, even though the formal argument is declared a void*.

'''v_x1 = array.array('f',[0]) ; reader.AddVariable(varList[0],v_x1)
v_y1 = array.array('f',[0]) ; reader.AddVariable(varList[1],v_y1)
v_z1 = array.array('f',[0]) ; reader.AddVariable(varList[2],v_z1)
v_px1 = array.array('f',[0]) ; reader.AddVariable(varList[3],v_px1)
v_py1 = array.array('f',[0]) ; reader.AddVariable(varList[4],v_py1)
v_pz1 = array.array('f',[0]) ; reader.AddVariable(varList[5],v_pz1)

v_x2 = array.array('f',[0]) ; reader.AddVariable(varList[6],v_x2)
v_y2 = array.array('f',[0]) ; reader.AddVariable(varList[7],v_y2)
v_z2 = array.array('f',[0]) ; reader.AddVariable(varList[8],v_z2)
v_px2 = array.array('f',[0]) ; reader.AddVariable(varList[9],v_px2)
v_py2 = array.array('f',[0]) ; reader.AddVariable(varList[10],v_py2)
v_pz2 = array.array('f',[0]) ; reader.AddVariable(varList[11],v_pz2)
v_deltaZ = array.array('f',[0]) ; reader.AddVariable(varList[2],v_deltaZ)
v_deltaPhi = array.array('f',[0]) ; reader.AddVariable(varList[3],v_deltaPhi)
v_mu_like_1 = array.array('f',[0]) ; reader.AddVariable(varList[0],v_mu_like_1)
v_mu_like_2 = array.array('f',[0]) ; reader.AddVariable(varList[1],v_mu_like_2)
v_invMass = array.array('f',[0]) ; reader.AddSpectator(varList[4],v_invMass)

v_pT_1 = array.array('f',[0]) ; reader.AddVariable(varList[4],v_pT_1)
v_pT_2 = array.array('f',[0]) ; reader.AddVariable(varList[5],v_pT_2)'''
dist=array.array('f', [0])
DeltPhi=array.array('f', [0])
mu_likep=array.array('f', [0])
mu_likem=array.array('f', [0])
minv=array.array('f', [0])

reader.AddVariable( "dist", dist)
reader.AddVariable( "DeltPhi",DeltPhi)
reader.AddVariable( "mu_likep", mu_likep)
reader.AddVariable( "mu_likem", mu_likem)
reader.AddSpectator( "minv", minv )


fout = ROOT.TFile("TMVAappKeras.root","RECREATE")
t = TTree( 'MVout', 'MVA outputs' )
 
#maxn = 10
#n = array( 'i', [ 0 ] )
#d = array( 'f', maxn*[ 0. ] )
'''t.Branch( varList[0],v_x1 ,varList[0]+'/F' )
t.Branch( varList[1],v_y1 ,varList[1]+'/F' )
t.Branch( varList[2],v_z1 ,varList[2]+'/F' )
t.Branch( varList[3],v_px1 ,varList[3]+'/F' )
t.Branch( varList[4],v_py1 ,varList[4]+'/F' )
t.Branch( varList[5],v_pz1 ,varList[5]+'/F' )
t.Branch( varList[6],v_x2 ,varList[6]+'/F' )
t.Branch( varList[7],v_y2 ,varList[7]+'/F' )
t.Branch( varList[8],v_z2 ,varList[8]+'/F' )
t.Branch( varList[9],v_px2 ,varList[9]+'/F' )
t.Branch( varList[10],v_py2 ,varList[10]+'/F' )
t.Branch( varList[11],v_pz2 ,varList[11]+'/F' )
t.Branch( varList[2],v_deltaZ ,varList[2]+'/F' )
t.Branch( varList[3],v_deltaPhi ,varList[3]+'/F' )
t.Branch( varList[0],v_mu_like_1 ,varList[0]+'/F' )
t.Branch( varList[1],v_mu_like_2 ,varList[1]+'/F' )
t.Branch( varList[4],v_invMass ,varList[4]+'/F' )'''

#t.Branch( varList[4],v_pT_1 ,varList[4]+'/F' )
#t.Branch( varList[5],v_pT_2 ,varList[5]+'/F' )



methodList = {'BDT','PyKeras'}
methodVars = []

for method in methodList:
    methodVars.append( array.array( 'f', [ 0 ] )  )
    t.Branch( method, methodVars[-1] ,method+'/F' )
    reader.BookMVA(method,"dataset/weights/TMVAClassification_"+method+".weights.xml")
   


BDT=ROOT.TH1F("minvBDT", "", 1000, 5, 40);
PyK=ROOT.TH1F("minvPyKeras", "", 1000, 5, 40);

entries = chain.GetEntries()
input = TFile.Open( "~/Test/Testy/out_dat.root" )
data = input.Get("ntuple" )

data.SetBranchAddress( "mu_likep", mu_likem);
data.SetBranchAddress( "mu_likem", mu_likep);
data.SetBranchAddress( "dist", dist);
data.SetBranchAddress( "minv", minv);
data.SetBranchAddress( "DeltPhi", DeltPhi);

for ievt in range (data.GetEntries()):
  if ievt%1000 == 0: 
    print "--- ... Processing event: ", ievt 
  data.GetEntry(ievt);
  varBDT = reader.EvaluateMVA("BDT");
  varMLP = reader.EvaluateMVA("PyKeras");
  if (varBDT>0.2): 
    BDT.Fill(minv[0])
  if varMLP>0.9: 
    PyK.Fill(minv[0])

"""
#for jentry in xrange( 100 ):
for jentry in xrange( entries ):
    # get the next tree in the chain
    ientry = chain.LoadTree(jentry)
    if ientry % 1000:
        print "Entry: ",ientry
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
         # some cut-like selection
         if chain.mu_like[i]>0.5:
          ###if ( chain == chainS and abs(chain.id[i])==13 and abs(chain.id[i])==13 ) or (chain == chainB ):
           if chain.charge[i]==1:
            plus.push_back(i)
	   elif chain.charge[i]==-1:
            minus.push_back(i)

    print chain.x.size(),plus.size(),minus.size()

           
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
              invMass = (plusV+minusV).M()

              v_x1[0] = chain.x[plus[i]]
              v_y1[0] = chain.y[plus[i]]
              v_z1[0] = chain.z[plus[i]]
              v_px1[0] = chain.px[plus[i]]
              v_py1[0] = chain.py[plus[i]]
              v_pz1[0] = chain.pz[plus[i]]
              v_x2[0] = chain.x[minus[j]]
              v_y2[0] = chain.y[minus[j]]
              v_z2[0] = chain.z[minus[j]]
              v_px2[0] = chain.px[minus[j]]
              v_py2[0] = chain.py[minus[j]]
              v_pz2[0] = chain.pz[minus[j]]
              v_mu_like_1[0] = mu_like_1
              v_mu_like_2[0] = mu_like_2
              #v_deltaZ[0] = deltaZ
              #v_deltaPhi[0] = deltaPhi
              #v_pT_1[0] = pT1
              #v_pT_2[0] = pT2
              v_invMass[0] = invMass



              #Evaluate all methods
              ii=0
              for method in methodList:
                #print ientry, method, vevtsel_tau_et, reader.EvaluateMVA(method)
                methodVars[ii][0]=reader.EvaluateMVA(method)


                ii=ii+1

         
              t.Fill()"""
 



h_minvBDT2.Write();
h_minvBDT3.Write();
fout.Write()
fout.Close()





del reader

#TMVA::TMVAGui()
#ROOT.TMVA.TMVAGui()




