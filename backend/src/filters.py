# Import the necessary libraries
import cv2
import csv
import os
import matplotlib.pyplot as plt
from skimage.exposure import is_low_contrast
import numpy as np

# create an array of all the input images
fileNames = []
modifyOrigImages = []
openedImages = []
imageFlags = []
imagesPath = "../src/captures/"
threshold = 100
fileNames = os.listdir(imagesPath)
print(fileNames)


def variance_of_laplacian(img2):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    gray = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def BGR2RGB(BGR_img):
    # turning BGR pixel color to RGB
    rgb_image = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2RGB)
    return rgb_image


# read the input images into input array
def readImages(index):
    for file in fileNames:
        openedImages.append(cv2.imread(file))


def evaluateImages(length):
    with open("imagesInfo.txt", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        # criteria: blur, contrast, sharpness, and color balance
        for i in range(length):
            fileName = fileNames[i]
            currentImgFlags = []
            img = cv2.imread(imagesPath + fileName)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # populate image flags
            # array format: [ image file name, [flags], corrected file name], where the indices of flags are:
            # index 0 : contrast, 1 for too high, 0 for too low
            # index 1 : blurriness, 1 for too blurry, 0 for clear

            # file gets corrected if the contrast is too low/high
            if is_low_contrast(gray, 0.35):
                currentImgFlags.append(1)
            else:
                currentImgFlags.append(0)
            # file gets corrected if the blur is too much / adds sharpenning
            # if the file has a variance less than threshold, it is blurry. fix sharpness or blurriness accordingly
            if variance_of_laplacian(img) < threshold:
                currentImgFlags.append(1)
            else:
                currentImgFlags.append(0)

            # Implement fixes:
            if currentImgFlags[0] == 1:
                # image is high contrast, balance it out
                contrast = 2.3
                image2 = cv2.addWeighted(
                    img, contrast, np.zeros(img.shape, img.dtype), 0, 40
                )
            else:
                contrast = 1.0
                image2 = cv2.addWeighted(
                    img, contrast, np.zeros(img.shape, img.dtype), 0, 20
                )

            if currentImgFlags[1] == 1:
                # image is too blurry, apply sharpness
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                image2 = cv2.filter2D(img, ddepth=-1, kernel=kernel)
            else:
                # image is too sharp, apply blur
                image2 = cv2.GaussianBlur(img, (3, 3), 0)

            # always apply color correction to balance colors:
            alpha = 1.5  # Contrast control (1.0 means no change)
            beta = 30  # Brightness control (0 means no change)
            image2 = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            saturation_factor = 1.5  # Adjust this value to change saturation
            hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
            image2 = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            # Define a matrix for color correction (can be a custom matrix)
            color_correction_matrix = np.array(
                [[1.2, 0.1, 0.1], [0.0, 1.3, 0.2], [0.1, 0.2, 1.4]]
            )

            image2 = cv2.transform(img, color_correction_matrix)
            correctedFile = imagesPath + "corrected/" + fileName + "_enhanced.jpeg"
            cv2.imwrite(correctedFile, image2)
            imageFlags.append([fileName, correctedFile])
            cv2.waitKey(0)
            currentImgFlags = []
            # closing all open windows
            cv2.destroyAllWindows()
        csvwriter.writerows(imageFlags)
