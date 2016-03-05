import numpy as np
import cv2
import sys
from numpy import binary_repr
from operator import xor

def text_from_bits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

class DeEmbed():
    def __init__(self, img):
        self.image = img
        self.size = img.size
        self.shape = img.shape
        self.rows = self.shape[0]
        self.cols = self.shape[1]

    def check4Delimiter(self, bits):
        text = ""
        delimiter = "0010111000100001"
        if len(bits) < len(delimiter):
            return False
        for i in range(len(bits)):
            text += str(bits[i])
        if delimiter in text:
            return True
        else:
            return False

    def deEmbedSecret(self):
        bits = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.check4Delimiter(bits) == True:
                    break
                pixel = self.image[i,j]
                for k in range(0, 3):
                    if pixel[k]%2 == 0:
                        bits.append(0)
                    else:
                        bits.append(1)
        result = text_from_bits(bits)
        return result[:-2]


def main(av):
    img = cv2.imread('new.png')
    steg = DeEmbed(img)
    secret = steg.deEmbedSecret()
    print secret
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=="__main__":
    from sys import argv as av
    main(av)
