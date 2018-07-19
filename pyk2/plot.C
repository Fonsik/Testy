#include <stdio.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <iomanip>
#include <TChain.h>
#include <TTree.h>

void plot(){


  TFile ff("TMVAappKeras.root");
  
  TTree *tree = (TTree*)ff.Get("MVout");


 
  TCanvas c;
  c.SaveAs("plots2.pdf[");

  

  tree->Draw("minv", "BDTr>0.1&&minv<40");
   c.SaveAs("plots2.pdf");
   c.Clear();
  tree->Draw("minv", "Kerasr>0.5&&minv<40");
   c.SaveAs("plots2.pdf");
   c.Clear();

  c.SaveAs("plots2.pdf]");


}
