import numpy as np

class Estimator:
    Pbias = 0.1
    Qbias = 0.1
    Rbias = 0.1
    Phibias = 0.5
    Thetabias = 0.5
    SliderPhi = 0.1
    SliderTheta = 0.1
    PhiA   = 0
    ThetaA = 0
    ThetaG = 0
    ThetaD = 0
    ThetaE = 0
    ThetaE1 = 0
    ThetaE2 = 0
    PhiG  = 0
    PhiD  = 0
    PhiE  = 0
    PhiE1 = 0
    r2d = 180 / np.pi

    def run(self, Xg, Yg, Zg, Xa, Ya, Za, dt):
        self.XgOld = Xg
        self.YgOld = Yg
        self.ZgOld = Zg
        self.XaOld = Xa
        self.YaOld = Ya
        self.ZaOld = Za
        
        self.ThetaE_old = self.ThetaE;
        self.ThetaE1_old = self.ThetaE1;
        self.ThetaE2_old = self.ThetaE2;
        self.PhiE_old = self.PhiE;
        self.PhiE1_old = self.PhiE1;

        self.PhiA = (np.arctan2(Ya,Za))*self.r2d;
        self.ThetaA = (np.arctan2(Xa,np.sqrt(Ya*Ya + Za*Za)))*self.r2d;
        self.PhiG = self.PhiE + self.PhiD*dt;
        self.ThetaG = self.ThetaE + self.ThetaD*dt;

        Pest = self.Pbias*Xg + (1-self.Pbias)*self.XgOld;
        Qest = self.Qbias*Yg + (1-self.Qbias)*self.YgOld;
        Rest = self.Rbias*Zg + (1-self.Rbias)*self.ZgOld;

        self.PhiD = Pest + Qest*np.sin(self.PhiG/self.r2d)*np.tan(self.ThetaG/self.r2d) + Rest*np.cos(self.PhiG/self.r2d)*np.tan(self.ThetaG/self.r2d);
        self.ThetaD = Qest*np.cos(self.ThetaG/self.r2d) - Rest*np.sin(self.PhiG/self.r2d);

        self.PhiEOld = self.PhiE;
        self.ThetaEOld = self.ThetaE;
        self.PhiE   = self.Phibias*self.PhiEOld + (1-self.Phibias)*(self.SliderPhi*self.PhiA+(1-self.SliderPhi)*self.PhiG);
        self.ThetaE = self.Thetabias*self.ThetaEOld + (1-self.Thetabias)*(self.SliderTheta*self.ThetaA+(1-self.SliderTheta)*self.ThetaG);

        self.ThetaE1 = 0.5*self.ThetaE+0.5*self.ThetaE_old;
        self.ThetaE2 = 0.1*self.ThetaE1+0.9*self.ThetaE1_old;
        # self.ThetaE3 = 0.1*self.ThetaE2+0.9*self.ThetaE2_old;
        
        self.PhiE1 = 0.05*self.PhiE+0.95*self.PhiE_old

        return self.ThetaE2, -self.PhiE1
