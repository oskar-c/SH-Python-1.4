# Range notes
# There are some differences when working with OpenCV and ImageJ
# For one, OpenCV will open images in BGR values, so it is necessary to convert to RGB for clarity
# Also, the Hue (H) values in HSV/HSB between OpenCV and ImageJ have different ranges (0-179 vs 0-255)

# This file will have information and code that may be useful as a reference when working between different softwares and image standards

# Code to convert Hue values between ImageJ and OpenCV
def hue_imagej_to_opencv(imagej_value):
    return imagej_value * (179 / 255)
def hue_opencv_to_imagej(opencv_value):
    return opencv_value * (255 / 179)

# For future reference, to convert between any ranges
def convert_range(value, old_range, new_range):
    old_min, old_max = old_range
    new_min, new_max = new_range
    old_value = (value - old_min) / (old_max - old_min)
    new_value = old_value * (new_max - new_min) + new_min
    return new_value

# For example to use convert_range
# old_range = (0, 255)
# new_range = (0, 179)
# value = 255
# print(convert_range(value, old_range, new_range))
# Output: 179.0


# Preliminary ranges from first hemoglobin lab notebooks

# R: 162.75 SD 3.52 
# G: 190.78 SD 3.05
# B: 189.68 SD: 2.97

# RGB: lowerBound = 152.19, 182.63, 180
# RGB: upperBound = 173.31, 199.93, 199
# HSV from ImageJ: lowerBound = 119, 29, 180
# HSV from ImageJ: upperBound = 129, 42, 203

# Hue range: OpenCV: 0-179, ImageJ: 0-255
# Saturation range (same): OpenCV: 0-255, ImageJ: 0-255
# Val/Brightness range (same): OpenCV: 0-255, ImageJ: 0-255

