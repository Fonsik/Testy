#include <stdio.h>

void plot(){

  // opening files
  //TFile f1("out_dat2.root");
  //TFile f2("out_sig2.root");
  //TFile f3("out_bkg2.root");
  TFile ff("TMVApppy.root");


  // get histograms from the files
  //TH1F * h_n_1 = (TH1F*)f1.Get("minv");
  //TH1F * h_n_2 = (TH1F*)f2.Get("minv");
  //TH1F * h_n_3 = (TH1F*)f3.Get("minv");

  TH1F * BDT1 = (TH1F*)ff.Get("minvBDT1");
  TH1F * BDT2 = (TH1F*)ff.Get("minvBDT2");
  TH1F * BDT3 = (TH1F*)ff.Get("minvBDT3");

  TH1F * Like1 = (TH1F*)ff.Get("minvLike1");
  TH1F * Like2 = (TH1F*)ff.Get("minvLike2");
  TH1F * Like3 = (TH1F*)ff.Get("minvLike3");
  TH1F * LikeD = (TH1F*)ff.Get("minvD");
  TH1F * LikeP = (TH1F*)ff.Get("minvPCA");

  TH1F * MLP1 = (TH1F*)ff.Get("minvMLP1");
  TH1F * MLP2 = (TH1F*)ff.Get("minvMLP2");
  TH1F * MLP3 = (TH1F*)ff.Get("minvMLP3");

  // set line colors


  TCanvas c;
  c.SaveAs("plots2.pdf["); // opening pdf

  // draw all histograms

	BDT1->SetLineColor(1);
	BDT2->SetLineColor(2);
	BDT3->SetLineColor(3);
  BDT3->Rebin(20);
  BDT3->Draw("hist");
	
 if (BDT1->GetEntries()>0 && BDT2->GetEntries()>0 && BDT3->GetEntries()>0) 

  {
  BDT1->Rebin(20);
  BDT2->Rebin(20);
  
  BDT1->Draw("hist");
	BDT2->Draw("hist same");
  
  }

	c.SaveAs("plots2.pdf");

  c.Clear();

  Like1->SetLineColor(1);
  Like2->SetLineColor(2);
  Like3->SetLineColor(3);

  if (true//Like1->GetEntries()>0 && Like2->GetEntries()>0 && Like3->GetEntries()>0)
  ){
  Like1->Rebin(20);
  Like2->Rebin(20);
  Like3->Rebin(20);
  Like1->Draw("hist");
  Like2->Draw("hist same");
  Like3->Draw("hist same");
  }

  c.SaveAs("plots2.pdf");

 
  c.Clear();

  MLP1->SetLineColor(1);
  MLP2->SetLineColor(2);
  MLP3->SetLineColor(3);

  
  if (true//MLP1->GetEntries()>0 && MLP2->GetEntries()>0 && MLP3->GetEntries()>0)
  ){
  MLP1->Rebin(20);
  MLP2->Rebin(20);
  MLP3->Rebin(20);
  MLP1->Draw("hist");
  MLP2->Draw("hist same");
  MLP3->Draw("hist same");
  }

  c.SaveAs("plots2.pdf");
 c.Clear();

  BDT3->Draw("hist");
  c.SaveAs("plots2.pdf");
   c.Clear();

  LikeD->Rebin(20);
  LikeP->Rebin(20);


  LikeD->Draw("hist");
  c.SaveAs("plots2.pdf");
   c.Clear();

  LikeP->Draw("hist");

  c.SaveAs("plots2.pdf");

  c.SaveAs("plots2.pdf]"); // closing pdf


}
