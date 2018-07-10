#include <stdio.h>

void plot(){

  // opening files
  TFile f1("out_dat2.root");
  TFile f2("out_sig2.root");
  TFile f3("out_bkg2.root");

  // get histograms from the files
  TH1F * h_n_1 = (TH1F*)f1.Get("minv");
  TH1F * h_n_2 = (TH1F*)f2.Get("minv");
  TH1F * h_n_3 = (TH1F*)f3.Get("minv");

  // set line colors


  TCanvas c;
  c.SaveAs("plots2.pdf["); // opening pdf

  // draw all histograms

   float s3=500;
   float s2=5;
   float n1, n2, n3, nc1, nc2, nc3;
   FILE *f=fopen("liczba.txt", "r");
   
   fscan(f,"%1d%",nc1);
   fscan(f,"%1d%",nc2);
   fscan(f,"%1d%",nc3);
   
   n1=h_n_1->GetEntries();
   n2=h_n_2->GetEntries();
   n3=h_n_3->GetEntries();

   h_n_2->Scale(s2/nc2);
   h_n_3->Scale(s3/nc3);
  // h_n_3->Scale(s3);



 h_n_2->Add(h_n_3,1);
  h_n_2->Scale(100);
    n2=h_n_2->GetEntries();
     h_n_1->Scale(1/n1);
   h_n_2->Scale(1/n2);
h_n_1->SetLineColor(1);
h_n_2->SetLineColor(2);
h_n_3->SetLineColor(3);

 h_n_1->DrawNormalized("e");
  h_n_2->DrawNormalized("same");
 //h_n_3->Draw("same");

 c.SaveAs("plots2.pdf");
 c.Clear();
  c.SaveAs("plots2.pdf]"); // closing pdf


}
