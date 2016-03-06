import dpkt
import numpy as np

IUNIT = np.sqrt(-1+0j)

class GetPcap:
    def __init__(self):
        pass

    def get_real_imag(self, data):
        if len(data) == 32:
            d1 = np.array([1, 2, 3, 4], dtype=complex)
            d2 = np.array([1, 2, 3, 4], dtype=complex)
            for y in np.arange(8):
                real = ord(data[4*y])*16*16 + ord(data[4*y + 1])
                imag = ord(data[4*y + 2])*16*16 + ord(data[4*y + 3])
                if real >= 32768:
                    real = -(real-32768) / 32767.0
                else:
                    real = real / 32767.0
                if imag >= 32768:
                    imag = -(imag-32768) / 32767.0 * IUNIT
                else:
                    imag = imag / 32767.0 * IUNIT
                if y < 4:
                    d1[y] = real + imag
                if y >= 4:
                    d2[y-4] = real + imag
            return d1,d2
        if len(data) == 64:
            d1 = np.array([1, 2, 3, 4], dtype=complex)
            d2 = np.array([1, 2, 3, 4], dtype=complex)
            d3 = np.array([1, 2, 3, 4], dtype=complex)
            d4 = np.array([1, 2, 3, 4], dtype=complex)
            for y in np.arange(16):
                real = ord(data[4*y])*16*16 + ord(data[4*y + 1])
                imag = ord(data[4*y + 2])*16*16 + ord(data[4*y + 3])
                if real >= 32768:
                    real = -(real-32768) / 32767.0
                else:
                    real = real / 32767.0
                if imag >= 32768:
                    imag = -(imag-32768) / 32767.0 * IUNIT
                else:
                    imag = imag / 32767.0 * IUNIT
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
        x = 510
        f = file("..\TM8_eth.pcap", "rb")
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            if len(buf) != 574 or ord(buf[42]) != 0x1e : continue
            if (CRNTI0 is not None) and (CRNTI1 is not None):
                if CRNTI0 != ord(buf[506]) and CRNTI1 != ord(buf[507]):continue
            if (CRNTI0 is None) and (CRNTI1 is None):
                CRNTI0, CRNTI1 = ord(buf[506]), ord(buf[507])
            if (ord(buf[23]) == 0x11):  #UDP
                flag = str(bin(ord(buf[508])))[-1]
                if flag == '0':
                    WeightVector = self.get_real_imag(buf[x:x+32])
                    yield WeightVector
                else:
                    WeightVector = self.get_real_imag(buf[x:x+64])
                    yield WeightVector
