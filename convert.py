import cv2 as cv
import os
path = "E:/Professional/CovarianceTracking/Output/"

for fname in os.listdir(path):
    img = cv.imread("./Output/" + fname)
    # cv.imshow("name", img)
    # print("".join(fname.split('.')[0:-1]) + ".png")

    cv.imwrite("".join(fname.split('.')[0:-1]) + ".png", img)