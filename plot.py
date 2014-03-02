import numpy as np
import matplotlib.pyplot as plt
from mypcap import Pcap
tp,AntNum,a_sita,nlA,a_beam = None,4,None,None,None
theta,powAnt,Fc,Mf1Value,AntDistance = None,None,None,None,None
class Plot:
    def __init__(self):
        self.only_polar = True
        self.error_power = np.array([0,0,0,0])
        self.error_phase = np.array([0,0,0,0])

    def main(self):
        p = Pcap().get_vector()
        fig = plt.figure(figsize=(16,9))
        while 1:
            only_polar,WeightVector = p.next()
            if only_polar == "True":
                fig_list = range(4)
                fig_list[0] = fig.add_subplot(221, projection='polar')
                fig_list[1] = fig.add_subplot(222, projection='polar')
                fig_list[2] = fig.add_subplot(223, projection='polar')
                fig_list[3] = fig.add_subplot(224, projection='polar')
                i = 0
                for W in WeightVector:
                    self.deal_data(W,len(fig_list),fig_list[i])
                    i += 1
                plt.draw()
                plt.pause(0.1)
                fig.clf()
            else:
                fig_list = range(8)
                fig_list[0] = fig.add_subplot(241)
                fig_list[1] = fig.add_subplot(242, projection='polar')
                fig_list[2] = fig.add_subplot(243)
                fig_list[3] = fig.add_subplot(244, projection='polar')
                fig_list[4] = fig.add_subplot(245)
                fig_list[5] = fig.add_subplot(246, projection='polar')
                fig_list[6] = fig.add_subplot(247)
                fig_list[7] = fig.add_subplot(248, projection='polar')
                i = 0
                for W in WeightVector:
                    self.deal_data(W,len(fig_list),fig_list[i],fig_list[i+1])
                    i += 2
                plt.draw()
                plt.pause(0.1)
                fig.clf()

    def deal_data(self,WeightVector,len_f,*fig_l):
        global tp,AntNum,a_sita,nlA,a_beam,theta,powAnt,Fc,Mf1Value,AntDistance
        HBW,c,Fc,pi = 90,3e8,2.6 * 1e9,np.pi
        iunit = np.sqrt(-1+0j)
        error_power = self.error_power
        error_phase = self.error_phase
        lamb = c/Fc
        AntDistance = lamb * 0.5
        calibration_error = np.power(10,(error_power/20.0))*np.exp(iunit*pi*error_phase/180.0)
        w = calibration_error*WeightVector
        N=361
        theta = np.linspace(-180,180,N)/180*pi
        if len_f == 8:
            tp = theta/pi*180
            nlA = 10*np.log10(AntNum)
        a_sita = np.ones(N)
        alpha = np.ones((AntNum,N),dtype=np.complex)
        for index in np.arange(1,AntNum+1):
            alpha[index-1] = np.exp(iunit*(index-1)*2*pi/lamb*AntDistance*np.sin(theta))
        a_beam = np.power(np.abs(np.dot(w,alpha)),2)* np.power(10,(a_sita/10))
        powAnt = np.power(10,(a_sita/10))*AntNum
        Mf1Value = np.max([np.max(a_beam),np.max(powAnt/AntNum),np.max(powAnt)])
        self.draw(len_f,fig_l)

    def draw(self,len_f,fig_l):
        if len_f == 4:
            f =fig_l[0]
            f.plot(0,Mf1Value,'w')
            f.plot(theta,powAnt/AntNum,'r')
            f.plot(theta,powAnt,'b')
            f.plot(theta,a_beam,'m')
        elif len_f == 8:
            f1,f2 = fig_l[0],fig_l[1]
            f1.set_xlabel('degree')
            f1.set_ylabel('Gain (dB)')
            f1.plot(tp,a_sita,'r',label='Omni antenna 5W')
            f1.plot(tp,a_sita+nlA,'b',label='Omni antenna '+str(5*AntNum)+'W')
            f1.plot(tp,10*np.log10(a_beam),'m',label='beam pattern,d='+str(AntDistance*1e3)+'mm,fc='+str(Fc/1e9)+'GHz')
            handles, labels = f1.get_legend_handles_labels()
            f1.legend(handles, labels,loc=3,fontsize=10)
            f1.grid(True)
            f2.plot(0,Mf1Value,'w')
            f2.plot(theta,powAnt/AntNum,'r')
            f2.plot(theta,powAnt,'b')
            f2.plot(theta,a_beam,'m')

if __name__ == "__main__":
    Plot().main()