import cv2 as cv
# This file will read an input image, filter for the desired color splotch, 
# and output a csv file with HSV values and relavent statistics, as well as displaying input and output

# Note that to exit image display and have the file save, press any key

# Input image and check if it was properly loaded
inputImg = cv.imread("images/sample1.15.jpg")
if inputImg is None:
    print("Image is empty!")

cv.imshow("Input", inputImg)

# By default OpenCV will load images as BGR, so we convert to HSV here
imgHSV = cv.cvtColor(inputImg, cv.COLOR_BGR2HSV)
blur = cv.GaussianBlur(imgHSV,(5,5),0)

# Please note these ranges are within OpenCV standard ranges for HSV values. Different software will use different ranges

# Preliminary ranges from first labs
lowerBound =  82, 29, 180
upperBound = 95, 42, 203

# Filter image to isolate colors within our range
mask = cv.inRange(blur, lowerBound, upperBound)
# Create a kernel for morphological operations, larger size closes more small holes
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (12,12))
# Apply morphological opening and closing operations to further isolate colored splotch
open = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
closed = cv.morphologyEx(open, cv.MORPH_CLOSE, kernel)
# Create output image using our original image and our desired isolated area
outputImg = cv.bitwise_and(blur, blur, mask=closed)

# To display output image using cv.imshow, we convert back to BGR
cv.imshow('Output in HSV', outputImg)
cv.waitKey(0)


# Next part of this script will create a file to store our HSV values and statistics

# Making data to store RGB values
x_h = []
y_s = []
z_v = []
height = outputImg.shape[0]
width = outputImg.shape[1]
channels = outputImg.shape[2]
for row in range(0,height):
     for col in range(0, width):
        if outputImg[row,col].all() != 0:
            x_h.append(outputImg[row, col, 0])
            y_s.append(outputImg[row,col, 1])
            z_v.append(outputImg[row, col, 2])

# Import necessary libraries for statistics and filemaking
import io
import numpy as np
from datetime import datetime

# Calculate statistics on our RGB values
mean_h, mean_s, mean_v = np.mean(x_h), np.mean(y_s), np.mean(z_v)
sdev_h, sdev_s, sdev_v = np.std(x_h), np.std(y_s), np.std(z_v)
median_h, median_s, median_v = np.median(x_h), np.median(y_s), np.median(z_v)

# Make unique filename
now = datetime.now()
file_name = "hsv_values_" + now.strftime("%Y-%m-%d %H-%M-%S") + ".csv"

# Create new csv file to store RGB values and statistics
with io.open(file_name, "w") as file_obj:
    # write the header row
    file_obj.write("Please note these are with OpenCV standard ranges\n")
    file_obj.write("Mean H, Mean S, Mean V\n")
    file_obj.write("{},{},{}\n".format(mean_h, mean_s, mean_v))
    file_obj.write("Stdev H, Stdev S, Stdev V\n")
    file_obj.write("{},{},{}\n".format(sdev_h, sdev_s, sdev_v))
    file_obj.write("Median H, Median S, Median V\n")
    file_obj.write("{},{},{}\n".format(median_h, median_s, median_v))
    file_obj.write("\n")
    file_obj.write("H, S, V\n")
    # write RGB files to file
    for i in range(len(x_h)):
        # write the values to the file
        file_obj.write("{},{},{}\n".format(x_h[i], y_s[i], z_v[i]))
