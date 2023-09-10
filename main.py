from __future__ import annotations
import cv2 as cv
import numpy as np
import os
from typing import overload

"""
http://www.scholarpedia.org/article/Eigenfaces

"the Exteded Yale Face Database B" and reference Athinodoros Georghiades, Peter Belhumeur, and David Kriegman's paper, 
"From Few to Many: Illumination Cone Models for Face Recognition under Variable Lighting and Pose", PAMI, 2001
"""

class EigenFaces():
    def __init__(self):
        self.original_images = []
        self.U = None
        self.S = None
        self.eigen_faces = None
        self.original_shape = None
        self.avg_face = None

    # TODO - make this overload work so you can just put in a list of images if thats how you want to load
    # @overload
    # def loadData(self, img_list: list[np.ndarray]):
    #     print("eigen load given list of images")

    def loadData(self, str_list: list[str]):
        """
        
        """
        # Glasses seem to be throwing off the algorithm the most, even just looking at the centerlight data we get bad reconstruction but it is relatively good with no glasses
        self.original_images = [cv.cvtColor(cv.imread("./Samples/YaleFaces/" + fname), cv.COLOR_RGB2GRAY) for fname in str_list if "noglasses" in fname]
        # self.original_images = [cv.cvtColor(cv.imread("./Samples/YaleFaces/" + fname), cv.COLOR_RGB2GRAY) for fname in str_list if "noglasses" in fname or "normal" in fname]
        # self.original_images = [cv.cvtColor(cv.imread("./Samples/YaleFaces/" + fname), cv.COLOR_RGB2GRAY) for fname in str_list]
        self.original_shape = self.original_images[0].shape


    def train(self):
        """
        
        """
        X = None

        for img in self.original_images:
            imM, imN = img.shape
            reshaped = img.reshape((imM * imN, 1))

            if X is None:
                X = reshaped.copy()
                self.original_shape = (imM, imN)
            else:
                X = np.append(X, reshaped, 1)

        self.avg_face = np.matrix(np.average(X, axis=1)).T

        #Subtract the mean face from all the faces to get mean centered data
        X = X - self.avg_face

        self.U, S, Vt = np.linalg.svd(X, full_matrices=False)
        self.S = np.diag(S)


    def generateAlpha(self, img, r):
        return self.U[:, :r].T @ img
    
    def approximate(self, img, r):
        return self.avg_face + self.U[:, :r] @ self.generateAlpha(img, r)


    """
    Below are some functions that may never really be useful in a real application but can help to understand how EigenFaces work.
    """

    def getEigenFaceImage(self, idx):
        """
        Returns the basis vector at the specified index in the shape of the original image.
        """


        # return cv.convertScaleAbs((((self.U[:, idx] + 1) / 2) * 255).reshape(self.original_shape))
        img = self.U[:, idx]
        return cv.convertScaleAbs((((img - np.min(img)) / (np.max(img) - np.min(img)))*255).reshape(self.original_shape))


    def generateProfileTileImages(self, show_images=False, save_images=False):
        """
        This function is dataset dependant - will only work on the ./YaleFaces folder in this directory
        """
        # TODO generalize and parameterize this function better so it can be used on more data sets

        M, N = self.original_shape
        num_subjects = 15
        #num_photos - number of photos taken of each person
        num_photos = 11

        for i in range(num_subjects):
            image_subset = self.original_images[i*num_photos:(i+1)*num_photos]
            # all_poses - the image array that stores all pose images for one person
            all_poses = np.zeros((M*3, N*4))
            row = 0

            for j, img in enumerate(image_subset):
                all_poses[row*M:(row+1)*M, (j%4)*N:((j%4)+1)*N] = img

                if j%4 == 3:
                    row += 1

            if show_images:
                cv.imshow(str(i), cv.convertScaleAbs(all_poses))
            if save_images:
                cv.imwrite(f"./Output/tiled.subject{i + 1}.pgm", cv.convertScaleAbs(all_poses))


class FisherFaces:
    def __init__(self):
        self.class_dict = {}
        self.avg_face = None


    def loadData(self, fname_list):
        """
        This function assumes the data is in the format filename.classname.filetype
        """
        for f in fname_list:
            img = cv.imread("./Samples/YaleFaces/" + f)
            img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

            class_name = f.split('.')[1]
            if class_name not in self.class_dict:
                self.class_dict[class_name] = [img]
            else:
                self.class_dict[class_name].append(img)


    def train(self):
        fa = np.matrix(list(self.class_dict.values()))
        print(np.ndarray.flatten(fa).shape)


if __name__ == "__main__":
    SAMPLES_PATH = "E:/Professional/CovarianceTracking/Samples/YaleFaces/"
    REDUCTION = 1600

    eface = EigenFaces()
    eface.loadData(os.listdir(SAMPLES_PATH)[11:])
    eface.train()

    # Snippet here to show the basis images
    # for i in range(3):
    #     basis_vec_image = eface.getEigenFaceImage(i)
    #     cv.imshow("test" + str(i), basis_vec_image)
    #     cv.imwrite(f"./Output/basis_vec_{i + 1}_image.pgm", basis_vec_image)

    # Snippet here to show original image we are using as a test for visual comparison
    original = cv.imread(SAMPLES_PATH + os.listdir(SAMPLES_PATH)[0])
    original = cv.cvtColor(original, cv.COLOR_RGB2GRAY)
    cv.imshow("Test: True Image", original)

    # Snippet here to show the approximated image
    approx = eface.approximate(original.reshape((original.shape[0] * original.shape[1], 1)), REDUCTION).reshape(original.shape)
    approx = cv.convertScaleAbs(((approx - np.min(approx)) / (np.max(approx) - np.min(approx))) * 255)
    cv.imshow("Test: approx", approx)
    cv.imwrite(f"./Output/approximation_noglasses_r_nop1={REDUCTION}.pgm", approx)

    for i in range(1000):
        approx = eface.approximate(original.reshape((original.shape[0] * original.shape[1], 1)), i).reshape(original.shape)
        approx = cv.convertScaleAbs(((approx - np.min(approx)) / (np.max(approx) - np.min(approx))) * 255)

        error = np.sum(np.square(original - approx))

        cv.imshow("grow", approx)
        cv.waitKey(100)


    # eface.generateProfileTileImages()

    cv.waitKey(0)


    # fishface = FisherFaces()
    # fishface.loadData(os.listdir(SAMPLES_PATH))
    # fishface.train()
