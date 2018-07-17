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

using namespace std;
void ntuple::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntries();

   TFile output(this->outputFileName.data(), "recreate");
  // TH1F h_nparticles("h_nparticles", "", 100, 0, 1000);
  // TH1F h_x("h_x", "", 100, -1e-4, 1e-4);
  // TH1F h_mu_like("h_mu_like", "", 100, 0, 1);
   //TH1F h_mu("h_mu", "", 100, 0, 1);
   //TH1F h_minv("minv", "", 300, 0, 40);
   TTree *out = new TTree("ntuple","ntuple");


    float sa, sb, sab, minv;
    float angl=0, dis=0;
    float xp,yp,zp,pxp,pyp,pzp,xm,ym,zm,pxm,pym,pzm,mu_likep,mu_likem, dist;


   TLorentzVector xyze;
   
   vector <TLorentzVector> vGp, vGpd;
   vector <TLorentzVector> vGm, vGmd;
   vector <float> vmu_likem, vmu_likep;
   
   

      out->Branch("xp", &xp, "xp/F");
      out->Branch("yp", &yp, "yp/F");
	    out->Branch("zp", &zp, "zp/F");
      out->Branch("xm", &pxp, "zm/F");
      out->Branch("ym", &pyp, "ym/F");
      out->Branch("zm", &pzp, "zm/F");
      out->Branch("pxp", &xm, "pxp/F");
      out->Branch("pyp", &ym, "pyp/F");
      out->Branch("pzp", &zm, "pzp/F");
      out->Branch("pxm", &pxm, "pxm/F");
      out->Branch("pym", &pym, "pym/F");
      out->Branch("pzm", &pzm, "pzm/F");
      //out->Branch("dist", &dist, "dist/F");
      out->Branch("mu_likep", &mu_likep, "mu_likep/F");
      out->Branch("mu_likem", &mu_likem, "mu_likem/F");
      
      out->Branch("minv", &minv, "MINV/F");
      //out->Branch("DeltPhi", &angl, "DP/F");
      
    bool isSignal = ( ((std::string)(this->outputFileName.data())).find("sig")  )< 100;
    cout<<" isSignal = "<<isSignal<<endl;
    

   int kk=0;
  

   Long64_t nbytes = 0, nb = 0;

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      int nparticles = id->size();
     // h_nparticles.Fill(nparticles);
      for(int particle=0; particle < nparticles; particle++){
//	h_x.Fill(x->at(particle));
	//h_x_y.Fill(x->at(particle), y->at(particle));
	//h_mu_like.Fill(mu_like->at(particle));


	if ( mu_like->at(particle)>0.5 &&  ( (isSignal && (id->at(particle)==13||id->at(particle)==-13))   || !isSignal ))
	 {
		if(charge->at(particle)>0)
		{
		xyze.SetPxPyPzE(px->at(particle),py->at(particle),pz->at(particle),e->at(particle)); vGp.push_back(xyze);
		xyze.SetXYZM(x->at(particle),y->at(particle),z->at(particle),e->at(particle)); vGpd.push_back(xyze);
		vmu_likep.push_back(mu_like->at(particle));
		}

		if(charge->at(particle)<0)
		{
		xyze.SetPxPyPzE(px->at(particle),py->at(particle),pz->at(particle),e->at(particle)); vGm.push_back(xyze);
		xyze.SetXYZM(x->at(particle),y->at(particle),z->at(particle),e->at(particle)); vGmd.push_back(xyze);
		vmu_likem.push_back(mu_like->at(particle));
		}
	}




                                                }

        int proc=100.0*(jentry+1)/nentries;
        cout<<"Wejscie: "<<jentry+1<<". Wykonano: "<<proc<<"%."<< "\r"<<flush;

//cout<<endl;
//cout<<vGp.size()<<endl;
     for (int i=0; i<vGp.size(); i++)
   {
        for (int j=0; j<vGm.size(); j++)
        {    
		    minv=(vGp[i]+vGm[j]).M();
	        //angl=vGp[i].DeltaPhi(vGm[j]);
	        xp=vGpd[i][0];
	        yp=vGpd[i][1];
	        zp=vGpd[i][2];
	        pxp=vGp[i][0];
	        pyp=vGp[i][1];
	        pzp=vGp[i][2];
	        xm=vGmd[j][0];
	        ym=vGmd[j][1];
	        zm=vGmd[j][2];
	        pxm=vGm[j][0];
	        pym=vGm[j][1];
	        pzm=vGm[j][2];
          //dist=abs(zp-zm);
	        mu_likep=vmu_likep[i];
	        mu_likem=vmu_likem[j];
	        
	        out->Fill();
	        

 


     


        }

   }


   
   vGp.resize(0);
   vGm.resize(0);
   vGpd.resize(0);
   vGmd.resize(0);
   vmu_likep.resize(0);
   vmu_likem.resize(0);
   }

   out->Write();

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
