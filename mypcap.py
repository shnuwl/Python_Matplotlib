import numpy as np
import pcap
iunit = np.sqrt(-1+0j)

class Pcap:
    def __init__(self):
        pass
    def get_real_imag(self,data):
        if len(data) == 32:
            d1 = np.array([1,2,3,4], dtype=complex)
            d2 = np.array([1,2,3,4], dtype=complex)
            for y in np.arange(8):
                real = ord(data[4*y])*16*16+ord(data[4*y+1])
                imag = ord(data[4*y+2])*16*16+ord(data[4*y+3])
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
                real = ord(data[4*y])*16*16+ord(data[4*y+1])
                imag = ord(data[4*y+2])*16*16+ord(data[4*y+3])
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
        yield ()
        pc = pcap.pcap()
        for ptime,buf in pc:
            if len(buf) !=574 and len(buf) != 578 : continue
            if ord(buf[42]) != 0x1e and ord(buf[46]) != 0x1e : continue
            x = len(buf)
            if CRNTI0 != None and CRNTI1 != None:
                if CRNTI0 != ord(buf[x-66]) and CRNTI1 != ord(buf[x-65]):continue
            if CRNTI0 == None and CRNTI1 == None:
                CRNTI0,CRNTI1 = ord(buf[x-66]),ord(buf[x-65])
            if (ord(buf[x-551]) == 0x11):  #UDP
                flag = str(bin(ord(buf[x-67])))[-1]
                if flag == '0':
                    WeightVector = self.get_real_imag(buf[x-64:x-32])
                    yield WeightVector
                else:
                    WeightVector = self.get_real_imag(buf[x-64:x])
                    yield WeightVector

# if __name__ == "__main__":
#     Pcap().get_vector()