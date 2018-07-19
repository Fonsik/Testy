#!/usr/bin/env python
 
import ROOT
from ROOT import TMVA, TFile, TString, TTree, TLorentzVector, TChain
from array import array
from subprocess import call
from os.path import isfile
from ROOT import std
from decimal import Decimal

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader("Color:!Silent")

import array

#dist=array.array('f', [0])
#DeltPhi=array.array('f', [0])
mu_likep=array.array('f', [0])
mu_likem=array.array('f', [0])
minv=array.array('f', [0])
xp=array.array('f', [0])
yp=array.array('f', [0])
zp=array.array('f', [0])
xm=array.array('f', [0])
ym=array.array('f', [0])
zm=array.array('f', [0])
pxp=array.array('f', [0])
pyp=array.array('f', [0])
pzp=array.array('f', [0])
pxm=array.array('f', [0])
pym=array.array('f', [0])
pzm=array.array('f', [0])
varBDT=array.array('f', [0])
varKer=array.array('f', [0])

reader.AddVariable( "xp", xp)
reader.AddVariable( "yp", yp)
reader.AddVariable( "zp", zp)
reader.AddVariable( "pxp", pxp)
reader.AddVariable( "pyp", pyp)
reader.AddVariable( "pzp", pzp)
reader.AddVariable( "xm", xm)
reader.AddVariable( "ym", ym)
reader.AddVariable( "zm" , zm)
reader.AddVariable( "pxm", pxp)
reader.AddVariable( "pym", pym)
reader.AddVariable( "pzm", pzm)
'''reader.AddVariable( "dist")
reader.AddVariable( "DeltPhi")'''
reader.AddVariable( "mu_likep", mu_likep)
reader.AddVariable( "mu_likem", mu_likem)
reader.AddSpectator( "minv", minv )


fout = ROOT.TFile("TMVAappKeras.root","RECREATE")
t = TTree( 'MVout', 'MVA outputs' )


methodList = {'BDT','PyKeras'}
methodVars = []

for method in methodList:
    methodVars.append( array.array( 'f', [ 0 ] )  )
    t.Branch( method, methodVars[-1] ,method+'/F' )
    reader.BookMVA(method,"dataset/weights/TMVAClassification_"+method+".weights.xml")
   

#input = TFile.Open( "out_dat.root" )
#data = input.Get("ntuple" )
data = ROOT.TChain("ntuple","")
data.Add("~/Test/Testy/out_dat.root/ntuple")


t.Branch("xp",xp, "xp/F");
t.Branch("yp",yp, "yp/F");
t.Branch("zp",zp, "zp/F");
t.Branch("xm",pxp, "zm/F");
t.Branch("ym",pyp, "ym/F");
t.Branch("zm",pzp, "zm/F");
t.Branch("pxp",xm, "pxp/F");
t.Branch("pyp",ym, "pyp/F");
t.Branch("pzp",zm, "pzp/F");
t.Branch("pxm",pxp, "pxm/F");
t.Branch("pym",pym, "pym/F");
t.Branch("pzm",pzm, "pzm/F");
t.Branch("mu_likep",mu_likep, "mu_likep/F");
t.Branch("mu_likem",mu_likem, "mu_likem/F");
t.Branch("minv",minv, "minv/F");
t.Branch("BDTr",varBDT, "varBDT/F");
t.Branch("Kerasr",varKer, "varKer/F");



#for ievt in range (data.GetEntries()):
a = data.GetEntries()
for ievt in range(a):

  data.GetEntry(ievt)
  xp[0]= data.xp
  yp[0]= data.yp
  zp[0]= data.zp
  pxp[0]= data.pxp
  pyp[0]= data.pyp
  pzp[0]= data.pzp
  xm[0]= data.xm
  ym[0]= data.ym
  zm[0]= data.zm
  pxm[0]= data.pxm
  pym[0]= data.pym
  pzm[0]= data.pzm
  minv[0]= data.minv
  mu_likep[0]= data.mu_likep
  mu_likem[0]= data.mu_likem
  varBDT[0]= reader.EvaluateMVA("BDT")
  varKer[0]= reader.EvaluateMVA("PyKeras")
  t.Fill()
 
  if (ievt%1000 == 0):
    print "--- ... Processing event: ", ievt, "  ", round(100.0*((ievt+1)/float(a)),2), "%" 
     #print "BDT = ",varBDT,", PyKeras = ",varKer
 

t.Write()
fout.Write()
fout.Close()


del reader




