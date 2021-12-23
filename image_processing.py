import os
import cv2
import numpy as np

dir = "images"

files = os.listdir(dir)

try:
    os.mkdir(dir + "/wrong_file_format")
except FileExistsError:
    print("the folder: ", dir + "/wrong_file_format", "does already exist")

def image_renaming(dir):

    files = os.listdir(dir)

    try:
        os.mkdir(dir + "/wrong_file_format")
    except FileExistsError:
        print("the folder: ", dir + "/wrong_file_format", "does already exist")

    #renames every file and moves those that aren't jpeg or jpg
    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        print(type)

        if type == ".jpeg" or type == ".jpg" or type == ".png":
            os.rename(dir + "/" + filename + type, dir + "/" + str(i) + type)

        elif not os.path.isdir(dir + "/" + filename + type):
            os.rename(dir + "/" + filename + type, dir + "/wrong_file_format" + "/" + filename + type)

    print("All filenames were changed to match future functions")

#image_renaming(dir)

def image_cropping(dir):

    files = os.listdir(dir)

    print(files)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            try:
                print(files[i])
                image = cv2.imread(dir + "/" + files[i])
                height, width, channels = image.shape

                if width > height:

                    # If the width is greater than the height the image will be landscape.
                    # Therfore we need to crop down the width but keep the height.
                    # This will give us the biggest rectangle within the image
                    cropped_image = image[0:height, 0:height]

                    cv2.imwrite(dir + "/" + files[i], cropped_image)
                    print("Saving image", files[i])


                elif width < height:

                    # The opposite is the case if the height is the greatest
                    cropped_image = image[0:width, 0:width]

                    cv2.imwrite(dir + "/" + files[i], cropped_image)
                    print("Saving image", files[i])


                else:
                    print("Image already square:", files[i])

            except:
                print("Moved one weird image")
                os.rename(dir + "/" + filename + type, dir + "/wrong_file_format" + "/" + filename + type)


    print("All images were cropped")

#image_cropping(dir)

def image_rescaling(width, height, dir):

    files = os.listdir(dir)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            image = cv2.imread(dir + "/" + files[i])
            h, w, channels = image.shape

            if not height == h and not width == w:

                dim = (width, height)

                resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

                cv2.imwrite(dir + "/" + files[i], resized)

    print("All images were resized")

# image_rescaling(250,250, dir)

def brightness_to_list(dir):

    brigness_values = []

    files = os.listdir(dir)

    for i in range(len(files)):

        filename, type = os.path.splitext(files[i])

        if type == ".jpeg" or type == ".jpg" or type == ".png":

            image = cv2.cvtColor(cv2.imread(dir + "/" + files[i]), cv2.COLOR_BGR2GRAY)
            # print(int(filename))
            brigness_values.append([files[i], np.average(image)])

            # print(np.average(image), filename)

    return brigness_values

# b = brightness_to_list(dir)
