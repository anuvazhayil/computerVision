import numpy as np
import cv2
import sys
from numpy import binary_repr
from operator import xor

def text_to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

class Embed():
    def __init__(self, img):
        self.image = img
        self.shape = img.shape
        self.rows = self.shape[0]
        self.cols = self.shape[1]

    def checkTextSize(self, text):
        delimiter = "0010111000100001"
        if 8 * len(text) + len(delimiter) >= self.rows * self.cols * 3:
            print "Text size too big to embed"

    def embedSecret(self, text):
        bits = []
        bits = text_to_bits(text)
        delimiter = [0,0,1,0,1,1,1,0,0,0,1,0,0,0,0,1] #text= ".!"
        b = 0
        d = 0
        for i in range(self.rows):
            for j in range(self.cols):
                pixel = self.image[i,j]
                for k in range(0, 3):
                    if len(bits) + len(delimiter) == b + d:
                        break
                    if b == len(bits) and d < len(delimiter):
                        if pixel[k]%2 != 0 and delimiter[d] == 0:
                            self.image[i,j][k] = self.image[i,j][k] - 1
                        if pixel[k]%2 == 0:
                            self.image[i,j][k] = xor(self.image[i,j][k], delimiter[d])
                        d += 1
                    else:
                        if pixel[k]%2 != 0 and bits[b] == 0:
                            self.image[i,j][k] = self.image[i,j][k] - 1
                        if pixel[k]%2 == 0:
                            self.image[i,j][k] = xor(self.image[i,j][k], bits[b])
                        b += 1
        return self.image


def main(av):

    img = cv2.imread('image.png')
    steg = Embed(img)
    user_input = raw_input('Enter the text: ')
    #user_input = 'hello' * 1000
    steg.checkTextSize(user_input)
    result = steg.embedSecret(user_input)
    cv2.imwrite("new.png", result)
    cv2.imshow("new.png",result)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__=="__main__":
    from sys import argv as av
    main(av)
