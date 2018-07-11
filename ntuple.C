#define ntuple_cxx
#include "ntuple.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <iomanip>
#include <TChain.h>
#include <vector>
#include <TLorentzVector.h>


float skal (TLorentzVector v1,TLorentzVector v2)
{
return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2];
}


void ntuple::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   TFile output(this->outputFileName.data(), "recreate");
   TH1F h_nparticles("h_nparticles", "", 100, 0, 1000);
   TH1F h_x("h_x", "", 100, -1e-4, 1e-4);
   TH1F h_mu_like("h_mu_like", "", 100, 0, 1);
   TH1F h_mu("h_mu", "", 100, 0, 1);
   TH1F h_minv("minv", "", 300, 0, 40);
float sa, sb, sab;
   vector <TLorentzVector> VGp, VGpd;
   vector <TLorentzVector> VGm, VGmd;
   TLorentzVector xyze;
   int kk=0;
   TH2F h_x_y("h_x_y", "", 100, -1e-4, 1e-4, 100, -1e-4, 1e-4);

   Long64_t nbytes = 0, nb = 0;

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      int nparticles = id->size();
      h_nparticles.Fill(nparticles);
      for(int particle=0; particle < nparticles; particle++){
	h_x.Fill(x->at(particle));
	h_x_y.Fill(x->at(particle), y->at(particle));
	h_mu_like.Fill(mu_like->at(particle));

	if (id->at(particle)==13||id->at(particle)==-13) {h_mu.Fill(mu_like->at(particle));}

        if (mu_like->at(particle)>0.85)
		 {
		if(charge->at(particle)>0)
		{
		xyze.SetPxPyPzE(px->at(particle),py->at(particle),pz->at(particle),e->at(particle)); VGp.push_back(xyze);
		xyze.SetXYZM(x->at(particle),y->at(particle),z->at(particle),e->at(particle)); VGpd.push_back(xyze);
		}

		if(charge->at(particle)<0)
		{
		xyze.SetPxPyPzE(px->at(particle),py->at(particle),pz->at(particle),e->at(particle)); VGm.push_back(xyze);
		xyze.SetXYZM(x->at(particle),y->at(particle),z->at(particle),e->at(particle)); VGmd.push_back(xyze);
		}

		 }

		                                          }
        float angl=0, dis=0;
        for (int i=0; i<VGp.size(); i++)
   {
        for (int j=0; j<VGm.size(); j++)
        {
        angl=VGp[i].DeltaPhi(VGm[j]);
        dis=VGpd[i][2]-VGmd[j][2];
        if (abs(angl)>2&&abs(dis)<0.04)
      {h_minv.Fill((VGp[i]+VGm[j]).M());}
        }

   }
   VGp.resize(0);
   VGm.resize(0);
   VGpd.resize(0);
   VGmd.resize(0);


   }


   output.Write();
   output.Close();
}

int main(int argc, char** argv){

  if(argc < 3){
    std::cout << "Usage:\n\t" << argv[0] << " output.root input1.root [input2.root input3.root ...]\n\n";
    return 1;
  }

  std::cout << "Output: " << argv[1] << "\n";
  // TChain is like a TTree, but can work across several root files
  TChain * chain = new TChain("ntuple");
  std::cout << "Inputs:\n";
  for(int i=2; i<argc; i++){
    std::cout << "\t" << argv[i] << "\n";
    chain->Add(argv[i]);
  }

  ntuple t(chain);
  t.outputFileName = argv[1];
  t.Loop();

  std::cout << "[ DONE ]\n\n";

}
