import cv2 as cv
# This file will read an input image, filter for the desired color splotch, 
# and output a csv file with RGB values and relavent statistics, as well as displaying input and output

# Note that to exit image display and have the file save, press any key

# Input image and check if it was properly loaded
inputImg = cv.imread("images/sample1.15.jpg")
if inputImg is None:
    print("Image is empty!")

cv.imshow("Input", inputImg)

# By default OpenCV will load images as BGR, so we convert to RGB here for clarity
imgRGB = cv.cvtColor(inputImg, cv.COLOR_BGR2RGB)
blur = cv.GaussianBlur(imgRGB,(5,5),0)

# Using RGB ~3 standard deviations from mean RGB Values for desired color range. Preliminary ranges from first labs
lowerBound =  152.19, 182.63,180
upperBound = 173.31, 199.93, 199

# Filter image to isolate colors within our range
mask = cv.inRange(blur, lowerBound, upperBound)
# Create a kernel for morphological operations, larger size closes more small holes
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (12,12))
# Apply morphological opening and closing operations to further isolate colored splotch
open = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
closed = cv.morphologyEx(open, cv.MORPH_CLOSE, kernel)
# Create output image using our original image and our desired isolated area
outputImg = cv.bitwise_and(blur, blur, mask=closed)

# To display output image using cv.imshow, we must convert back to BGR
cv.imshow('Output', cv.cvtColor(outputImg, cv.COLOR_RGB2BGR))
cv.waitKey(0)


# Next part of this script will create a file to store our HSV values and statistics

# Making data to store RGB values
x_r = []
y_g = []
z_b = []
height = outputImg.shape[0]
width = outputImg.shape[1]
channels = outputImg.shape[2]
for row in range(0,height):
     for col in range(0, width):
        if outputImg[row,col].all() != 0:
            x_r.append(outputImg[row, col, 0])
            y_g.append(outputImg[row,col, 1])
            z_b.append(outputImg[row, col, 2])

# Import necessary libraries for statistics and filemaking
import io
import numpy as np
from datetime import datetime

# Calculate statistics on our RGB values
mean_r, mean_g, mean_b = np.mean(x_r), np.mean(y_g), np.mean(z_b)
sdev_r, sdev_g, sdev_b = np.std(x_r), np.std(y_g), np.std(z_b)
median_r, median_g, median_b = np.median(x_r), np.median(y_g), np.median(z_b)


# Make unique filename
now = datetime.now()
file_name = "rgb_values_" + now.strftime("%Y-%m-%d %H-%M-%S") + ".csv"

# Create new csv file to store RGB values and statistics
with io.open(file_name, "w") as file_obj:
    # write the header row
    file_obj.write("Mean R, Mean G, Mean B\n")
    file_obj.write("{},{},{}\n".format(mean_r, mean_g, mean_b))
    file_obj.write("Stdev R, Stdev G, Stdev B\n")
    file_obj.write("{},{},{}\n".format(sdev_r, sdev_g, sdev_b))
    file_obj.write("Median R, Median G, Median B\n")
    file_obj.write("{},{},{}\n".format(median_r, median_g, median_b))
    file_obj.write("\n")
    file_obj.write("R, G, B\n")
    # write RGB files to file
    for i in range(len(x_r)):
        # write the values to the file
        file_obj.write("{},{},{}\n".format(x_r[i], y_g[i], z_b[i]))
