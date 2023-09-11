import cv2 as cv
import os

"""
Simple script to convert the output images from .pgm to .png
"""

path = "E:/Professional/CovarianceTracking/Output/"

for fname in os.listdir(path):
    img = cv.imread("./Output/" + fname)
    cv.imwrite("".join(fname.split('.')[0:-1]) + ".png", img)