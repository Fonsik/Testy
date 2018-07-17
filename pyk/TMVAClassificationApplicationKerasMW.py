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

varList = ["mu_likep","mu_likem","dist","DeltPhi","minv"]


import array

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


methodList = {'BDT','PyKeras'}
methodVars = []

for method in methodList:
    methodVars.append( array.array( 'f', [ 0 ] )  )
    t.Branch( method, methodVars[-1] ,method+'/F' )
    reader.BookMVA(method,"dataset/weights/TMVAClassification_"+method+".weights.xml")
   


BDT=ROOT.TH1F("minvBDT", "", 1000, 5, 40);
PyK=ROOT.TH1F("minvPyKeras", "", 1000, 5, 40);


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


BDT.Write();
PyKeras.Write();
fout.Write()
fout.Close()


del reader




