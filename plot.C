#include <stdio.h>

void plot(){

  // opening files
  TFile f1("out_dat2.root");
  TFile f2("out_sig2.root");
  TFile f3("out_bkg2.root");
  TFile f4("out_dat.root");
  TFile f5("out_sig.root");
  TFile f6("out_bkg.root");

  // get histograms from the files
  TH1F * h_n_1 = (TH1F*)f1.Get("minv");
  TH1F * h_n_2 = (TH1F*)f2.Get("minv");
  TH1F * h_n_3 = (TH1F*)f3.Get("minv");
  
  TH1F * h_n_4 = (TH1F*)f4.Get("minv");
  TH1F * h_n_5 = (TH1F*)f5.Get("minv");
  TH1F * h_n_6 = (TH1F*)f6.Get("minv");

  // set line colors


  TCanvas c;
  c.SaveAs("plots2.pdf["); // opening pdf

  // draw all histograms

   float s3=500;
   float s2=5;
   float n1, n2, n3, nc1, nc2, nc3, n4,n5,n6;
   //FILE *f=fopen("liczba.txt", "r");
   
	nc2=10000;
	nc3=29900;
	nc1=45450;

   
   n1=h_n_1->GetEntries();
   n2=h_n_2->GetEntries();
   n3=h_n_3->GetEntries();
    
   n4=h_n_4->GetEntries();
   n5=h_n_5->GetEntries();
   n6=h_n_6->GetEntries();

   h_n_2->Scale(s2/nc2);
   h_n_3->Scale(s3/nc3);
   
   h_n_5->Scale(s2/nc2);
   h_n_6->Scale(s3/nc3);
  // h_n_3->Scale(s3);



	h_n_2->Add(h_n_3,1);
	h_n_2->Scale(100);
	n2=h_n_2->GetEntries();
    h_n_1->Scale(1/n1);
    h_n_2->Scale(1/n2);
    
h_n_1->SetLineColor(1);
h_n_2->SetLineColor(2);
h_n_3->SetLineColor(3);

	h_n_1->Rebin(3);
	h_n_2->Rebin(3);
	h_n_1->DrawNormalized("e");
	h_n_2->DrawNormalized("same");
 //h_n_3->Draw("same");

 c.SaveAs("plots2.pdf");
 c.Clear();
 
 	h_n_5->Add(h_n_6,1);
	h_n_5->Scale(100);
	n5=h_n_5->GetEntries();
    h_n_4->Scale(1/n4);
    h_n_5->Scale(1/n5);
    
	h_n_4->SetLineColor(1);
	h_n_5->SetLineColor(2);
	h_n_6->SetLineColor(3);

	h_n_4->Rebin(3);
	h_n_5->Rebin(3);
	h_n_4->DrawNormalized("e");
	h_n_5->DrawNormalized("same");
	c.SaveAs("plots2.pdf");
  
  c.SaveAs("plots2.pdf]"); // closing pdf


}
