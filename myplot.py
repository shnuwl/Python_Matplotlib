import wx
import string
import numpy as np
import matplotlib.pyplot as plt

from mypcap import GetPcap

tp, AntNum, a_sita, nlA, a_beam = None, 4, None, None, None
theta, powAnt, Fc, Mf1Value, AntDistance = None, None, None, None, None
switch, drawing, polar, WV, rate = True, 1, True, None, 0.3
userText0, userText1, userText2, userText3 = None, None, None, None
IUNIT = np.sqrt(-1+0j)

class TopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        userLabel = wx.StaticText(self, -1, "Input WeightVector:", pos=(10, 35))
        userLabel1 = wx.StaticText(self, -1, "+", pos=(105, 65))
        userLabel2 = wx.StaticText(self, -1, "+", pos=(105, 95))
        userLabel3 = wx.StaticText(self, -1, "+", pos=(105, 125))
        userLabel4 = wx.StaticText(self, -1, "+", pos=(105, 155))
        userLabel5 = wx.StaticText(self, -1, "j", pos=(225, 65))
        userLabel6 = wx.StaticText(self, -1, "j", pos=(225, 95))
        userLabel7 = wx.StaticText(self, -1, "j", pos=(225, 125))
        userLabel8 = wx.StaticText(self, -1, "j", pos=(225, 155))
        rateLabel = wx.StaticText(self, -1, "s", pos=(340, 115))
        self.userText00 = wx.TextCtrl(self, -1, "", pos=(10, 65), size=(90, 25))
        self.userText10 = wx.TextCtrl(self, -1, "", pos=(125, 65), size=(90, 25))
        self.userText20 = wx.TextCtrl(self, -1, "", pos=(10, 95), size=(90, 25))
        self.userText30 = wx.TextCtrl(self, -1, "", pos=(125, 95), size=(90, 25))
        self.userText40 = wx.TextCtrl(self, -1, "", pos=(10, 125), size=(90, 25))
        self.userText50 = wx.TextCtrl(self, -1, "", pos=(125, 125), size=(90, 25))
        self.userText60 = wx.TextCtrl(self, -1, "", pos=(10, 155), size=(90, 25))
        self.userText70 = wx.TextCtrl(self, -1, "", pos=(125, 155), size=(90, 25))
        self.rateText = wx.TextCtrl(self, -1, "0.3", pos=(270, 115), size=(60, 25))
        self.toggleBtn = wx.Button(self, wx.ID_ANY, "Stop", pos=(50, -1))
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.OnToggle)
        self.bStart = True
        self.toggleBtn0 = wx.Button(self, wx.ID_ANY,"Rect_polar", pos=(220, -1))
        self.toggleBtn0.Bind(wx.EVT_BUTTON, self.OnToggle0)
        self.polar = False
        self.toggleBtn1 = wx.Button(self, wx.ID_ANY, "Draw", pos=(250, 60))
        self.toggleBtn1.Bind(wx.EVT_BUTTON, self.OnToggle1)
        self.toggleBtn2 = wx.Button(self, wx.ID_ANY, "Refresh Rate", pos=(250, 150))
        self.toggleBtn2.Bind(wx.EVT_BUTTON, self.OnToggle2)

    def StartTimer(self):
        global switch
        switch, self.bStart = False, False
        self.toggleBtn.SetLabel("Start")

    def StopTimer(self):
        global switch, drawing
        switch, self.bStart, drawing = True, True, 1
        self.toggleBtn.SetLabel("Stop")

    def Only_polar(self):
        global polar
        polar = True
        self.toggleBtn0.SetLabel("Rect_polar")

    def Rect_polar(self):
        global polar
        polar = False
        self.toggleBtn0.SetLabel("Only_polar")

    def OnToggle(self, event):
        if self.bStart:
            self.StartTimer()
        else:
            self.StopTimer()

    def OnToggle0(self, event):
        if polar:
            self.Rect_polar()
        else:
            self.Only_polar()

    def OnToggle1(self, event):
        global userText0, userText1, userText2, userText3, drawing
        userText00, userText10 = string.atof(self.userText00.GetValue()), string.atof(self.userText10.GetValue())
        userText20, userText30 = string.atof(self.userText20.GetValue()), string.atof(self.userText30.GetValue())
        userText40, userText50 = string.atof(self.userText40.GetValue()), string.atof(self.userText50.GetValue())
        userText60, userText70 = string.atof(self.userText60.GetValue()), string.atof(self.userText70.GetValue())
        userText0 = userText00 + userText10 * IUNIT
        userText1 = userText20 + userText30 * IUNIT
        userText2 = userText40 + userText50 * IUNIT
        userText3 = userText60 + userText70 * IUNIT
        drawing = 0

    def OnToggle2(self, event):
        global rate
        rate = string.atof(self.rateText.GetValue())
              
class TopFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Control Panel", size = (400,240))
        TopPanel(self) 
          
class Plot:
    def __init__(self):
        self.only_polar = True
        self.error_power = np.array([0, 0, 0, 0])
        self.error_phase = np.array([0, 0, 0, 0])

    def main(self):
        p = GetPcap().get_vector()
        fig = plt.figure(figsize=(16, 9))
        while 1:
            global drawing, WV, rate
            if drawing == 0:
                drawing = 1
            while not switch:
                if drawing == 0:
                    drawing = 2
                    break
                plt.pause(0.02)#0.2
            if drawing == 2:
                WeightVector = list()
                temp = [userText0, userText1, userText2, userText3]
                for i in range(4):
                    WeightVector.append(temp)
                WV = WeightVector
                self.trans_weight(fig, WV, 0)
            elif WV is None:
                fig.clf()
                self.trans_weight(fig, p.next())
                plt.draw()
                plt.pause(rate)
            else:
                fig.clf()
                self.trans_weight(fig, WV, 0)
                self.trans_weight(fig, p.next())
                plt.draw()
                plt.pause(rate)

    def trans_weight(self, fig, WeightVector, title=1):
        if polar:
            fig_list = range(4)
            fig_list[0] = fig.add_subplot(221, projection='polar')
            fig_list[1] = fig.add_subplot(222, projection='polar')
            fig_list[2] = fig.add_subplot(223, projection='polar')
            fig_list[3] = fig.add_subplot(224, projection='polar')
            i = 0
            for W in WeightVector:
                fig_list[i].set_xticklabels(('270', '315', '0', '45', '90', '135', '180', '225'))
                self.deal_data(W, len(fig_list), fig_list[i])
                if title == 1:
                    fig_list[i].set_title(W, fontsize=12)
                i += 1
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
                fig_list[i+1].set_xticklabels(('270', '315', '0', '45', '90', '135', '180', '225'))
                self.deal_data(W,len(fig_list), fig_list[i], fig_list[i+1])
                if title == 1:
                    fig_list[i].set_title(W, fontsize=12)
                i += 2

    def deal_data(self, WeightVector, len_f, *fig_l):
        global tp, AntNum, a_sita, nlA, a_beam, theta, powAnt, Fc, Mf1Value, AntDistance
        HBW, c, Fc, pi = 90, 3e8, 2.6 * 1e9, np.pi
        IUNIT = np.sqrt(-1 + 0j)
        error_power = self.error_power
        error_phase = self.error_phase
        lamb = c / Fc
        AntDistance = lamb * 0.5
        calibration_error = np.power(10, (error_power / 20.0)) * np.exp(IUNIT * pi * error_phase / 180.0)
        w = calibration_error * WeightVector
        N = 361
        theta = np.linspace(-180, 180, N) / 180 * pi
        if len_f == 8:
            tp = theta / pi * 180
            nlA = 10 * np.log10(AntNum)
        a_sita = np.ones(N)
        alpha = np.ones((AntNum, N), dtype=np.complex)
        for index in np.arange(1, AntNum + 1):
            alpha[index - 1] = np.exp(IUNIT * (index - 1) * 2 * pi / lamb * AntDistance * np.sin(theta - pi / 2))
        a_beam = np.power(np.abs(np.dot(w, alpha)), 2) * np.power(10, (a_sita / 10))
        powAnt = np.power(10, (a_sita / 10)) * AntNum
        Mf1Value = np.max([np.max(a_beam), np.max(powAnt / AntNum), np.max(powAnt)])
        self.draw(len_f, fig_l)

    def draw(self,len_f,fig_l):
        if len_f == 4:
            f = fig_l[0]
            f.plot(0, Mf1Value, 'w')
            f.plot(theta, powAnt / AntNum, 'r')
            f.plot(theta, powAnt, 'b')
            f.plot(theta, a_beam, 'm')
        elif len_f == 8:
            f1, f2 = fig_l[0], fig_l[1]
            f1.set_xlabel('degree')
            f1.set_ylabel('Gain (dB)')
            f1.plot(tp, a_sita, 'r', label='Omni antenna 5W')
            f1.plot(tp, a_sita + nlA, 'b', label='Omni antenna ' + str(5 * AntNum) + 'W')
            f1.plot(tp, 10*np.log10(a_beam), 'm', 
                    label='beam pattern,d=' + str(AntDistance * 1e3) + 'mm,fc=' + str(Fc / 1e9) + 'GHz')
            handles, labels = f1.get_legend_handles_labels()
            f1.legend(handles, labels, loc=3, fontsize=10)
            f1.grid(True)
            f2.plot(0, Mf1Value, 'w')
            f2.plot(theta, powAnt / AntNum, 'r')
            f2.plot(theta, powAnt, 'b')
            f2.plot(theta, a_beam, 'm')

if __name__ == "__main__":
    app = wx.App()
    frame = TopFrame()
    frame.Show()
    Plot().main()
    app.MainLoop()