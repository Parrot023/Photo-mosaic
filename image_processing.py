import os
import cv2
import numpy as np

# Path to the directory of the build images
dir = "images"

# Getting a list of all files in dir
files = os.listdir(dir)

try:
    # Making a directory for all the files that can not be used
    os.mkdir(dir + "/wrong_file_format")
except FileExistsError:
    # If the script have been run before the folder will already exist
    print("The folder: ", dir + "/wrong_file_format", "does already exist")


def image_cropping(dir):

    """
    Funtion to crop every image in the directory. So that they are square
    """

    # Getting a new list of files as some of the other functions might have moved or changed some files
    files = os.listdir(dir)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            try:
                # Loading the image
                image = cv2.imread(dir + "/" + files[i])
                height, width, channels = image.shape

                if width > height:

                    # If the width is greater than the height the image will be landscape.
                    # Therfore we need to crop down the width but keep the height.
                    # This will give us the biggest rectangle within the image
                    cropped_image = image[0:height, 0:height]

                    cv2.imwrite(dir + "/" + files[i], cropped_image)
                    print("Cropped image:", files[i])


                elif width < height:

                    # The opposite is the case if the height is the greatest
                    cropped_image = image[0:width, 0:width]

                    cv2.imwrite(dir + "/" + files[i], cropped_image)
                    print("Cropped image:", files[i])


                else:
                    print("Image already square:", files[i])

            except:
                # If for some reason something goes wrong the file is moved to dir + "/wrong_file_format"
                print("Moved a weird image:", files[i])
                os.rename(dir + "/" + filename + type, dir + "/wrong_file_format" + "/" + filename + type)


    print("All images were cropped")

#image_cropping(dir)

def image_rescaling(width, height, dir):

    """
    Function to rescale every image.
    This makes it easier for image_mural.py to load them
    during the creation of the mosaic
    """

    # Getting a new list of files as some of the other functions might have moved or changed some files
    files = os.listdir(dir)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            # Loading the image
            image = cv2.imread(dir + "/" + files[i])
            h, w, channels = image.shape

            # If it does already have the right dimension it wont be resized
            if not height == h and not width == w:

                dim = (width, height)

                resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

                # Saving the image
                cv2.imwrite(dir + "/" + files[i], resized)

    print("All images were resized")

# image_rescaling(250,250, dir)

def brightness_to_list(dir):

    """
    Function to return a list of all the images and their average brightness
    """

    brigness_values = []

    # Getting a new list of files as some of the other functions might have moved or changed some files
    files = os.listdir(dir)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            # Turning it into a greyscale image is we only care about the brightness value
            # image = cv2.cvtColorcv2.imread(dir + "/" + files[i]), cv2.COLOR_BGR2GRAY)

            image = cv2.imread(dir + "/" + files[i])


            # Appending the filename and brigness values to the list
            # brigness_values.append([files[i], np.average(image)])
            brigness_values.append([files[i], np.average(np.average(image, axis = 0), axis = 0)])

    # Returning the final list
    return brigness_values

# b = brightness_to_list(dir)

def image_color_correction(image, pixel_color, percentage):

    shape = image.shape

    overlay = np.zeros(shape, np.uint8)

    overlay[:] = pixel_color

    return cv2.addWeighted(image, 1, overlay, percentage, 0)
