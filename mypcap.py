import numpy as np
import pcap
from conf import Conf
iunit = np.sqrt(-1+0j)

class Pcap:
    def __init__(self):
        self.info = Conf().get_conf()
    def get_real_imag(self,data):
        if len(data) == 32:
            d1 = np.array([1,2,3,4], dtype=complex)
            d2 = np.array([1,2,3,4], dtype=complex)
            for y in np.arange(8):
                real = ord(data[4*y+3])*16*16+ord(data[4*y+2])
                imag = ord(data[4*y+1])*16*16+ord(data[4*y])
                if real >= 32768:
                    real = -(real-32768)/32767.0
                else:
                    real = real/32767.0
                if imag >= 32768:
                    imag = -(imag-32768)/32767.0*iunit
                else:
                    imag = imag/32767.0*iunit
                if y < 4:
                    d1[y] = real + imag
                if y >= 4:
                    d2[y-4] = real + imag
            return d1,d2
        if len(data) == 64:
            d1 = np.array([1,2,3,4], dtype=complex)
            d2 = np.array([1,2,3,4], dtype=complex)
            d3 = np.array([1,2,3,4], dtype=complex)
            d4 = np.array([1,2,3,4], dtype=complex)
            for y in np.arange(16):
                real = ord(data[4*y+3])*16*16+ord(data[4*y+2])
                imag = ord(data[4*y+1])*16*16+ord(data[4*y])
                if real >= 32768:
                    real = -(real-32768)/32767.0
                else:
                    real = real/32767.0
                if imag >= 32768:
                    imag = -(imag-32768)/32767.0*iunit
                else:
                    imag = imag/32767.0*iunit
                if y < 4:
                    d1[y] = real + imag
                if 4 <= y < 8:
                    d2[y-4] = real + imag
                if 8 <= y < 12:
                    d3[y-8] = real + imag
                if 12 <= y < 16:
                    d4[y-12] = real + imag
            return d1,d2,d3,d4
    def get_vector(self):
        CRNTI0,CRNTI1 = None,None
        only_polar = self.info[0][:4]
        yield only_polar,()
        pc = pcap.pcap()
        for ptime,buf in pc:
            if len(buf) !=574 and len(buf) != 578 : continue
            if ord(buf[42]) != 0x1e and ord(buf[46]) != 0x1e : continue
            x = len(buf)
            if CRNTI0 != None and CRNTI1 != None:
                if CRNTI0 != ord(buf[x-71]) and CRNTI1 != ord(buf[x-70]):continue
            if CRNTI0 == None and CRNTI1 == None:
                CRNTI0,CRNTI1 = ord(buf[x-71]),ord(buf[x-70])
            if (ord(buf[x-551]) == 0x11):  #UDP
                flag = str(bin(ord(buf[x-69])))[-1]
                if flag == '0':
                    WeightVector = self.get_real_imag(buf[x-67:x-35])
                    yield only_polar,WeightVector
                else:
                    WeightVector = self.get_real_imag(buf[x-67:x-3])
                    yield only_polar,WeightVector

# if __name__ == "__main__":
#     Pcap().get_vector()