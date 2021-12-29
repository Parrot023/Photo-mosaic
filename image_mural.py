import cv2
import image_processing
import numpy as np


# MURAL DIMENSION ------------------------------------------------
MURAL_WIDTH = 20 # CM
MURAL_HEIGHT = 20 # CM
PPI = 300 # PIXELS PER INCH
IMAGE_SIZE_CM = 2.5 # CM

PPCM = int(PPI / 2.54) #PIXEL PER CM
N_IMAGES_WIDE = int(MURAL_WIDTH / IMAGE_SIZE_CM) # NUMBER OF IMAGES WIDE
N_IMAGES_HIGH = int(MURAL_HEIGHT / IMAGE_SIZE_CM) # NUMBER OF IMAGES HIGH

IMAGE_SIZE_PX = int(IMAGE_SIZE_CM * PPCM) # IMAGE HEIGHT AND WIDTH IN (PX)
MURAL_WIDTH_PX = MURAL_WIDTH * PPCM # MURAL WIDTH IN PIXELS
MURAL_HEIGHT_PX = MURAL_HEIGHT * PPCM # MURAL HEIGHT IN PIXELS
# -------------------------------------------------------------------

# Determines whether or not to use the same image multiple times in a row
REUSE_IMAGES = False
# Determines how many images are left before allowing previously used images
REUSE_IMAGES_MIN_IMAGES = 100

# MURAL INFO ---------------------------------------------------------
print("PPCM", PPCM)
print("IMAGE SIZE", IMAGE_SIZE_PX)
print("MURAL WIDTH (PX)", MURAL_WIDTH_PX)
print("MURAL HEIGHT (PX)", MURAL_HEIGHT_PX)
print("NUMBER OF IMAGES WIDE", N_IMAGES_WIDE)
print("NUMBER OF IMAGES HIGH", N_IMAGES_HIGH)
print("TOTAL NUMBER OF IMAGES NEEDED", N_IMAGES_WIDE * N_IMAGES_HIGH)
# ---------------------------------------------------------------------

# Letting the user exit after seing the mural dimensions
if input("Do you want to continue (y/n): ") != "y":
    print("Aborting mural creation")
    exit()

# Loading mural base image
image = cv2.imread("Main2.jpg")
img_height, img_width, img_channels = image.shape

# Letting the user exit before resizing their base image
if not img_height/img_width == N_IMAGES_HIGH/N_IMAGES_WIDE:

    message = """You mural base image does not have the same aspect ratio as your mural
    your images will be resized to match your mural. This may result in the image looking stretched. Continue? (y/n)"""

    if input(message) != "y":
        exit()

# image_processing.image_cropping("images")
# image_processing.image_rescaling(IMAGE_SIZE_PX, IMAGE_SIZE_PX, "images")

# Resizing and converting base image to Grayscale
image = cv2.resize(image, (N_IMAGES_WIDE, N_IMAGES_HIGH))
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Blank image for the mural
mural_image = np.zeros((MURAL_HEIGHT_PX, MURAL_WIDTH_PX, 3), np.uint8)

def best_image(pixel_color, image_list):

    smallest_difference = 256
    best_image_name = None

    for index, i in enumerate(image_list):

            # If the differance between this image average color and the pixel
            # is lower than the smallest difference this is the new best image
            if abs(pixel_color - i[1]) < smallest_difference:

                # Index 1 is the average color of the image
                smallest_difference = abs(pixel_color - i[1])

                # Index 0 is the filename
                best_image_name = i[0]

                best_image_index = index

    image = cv2.imread("images/" + best_image_name)
    return image, best_image_name, smallest_difference, best_image_index

print("Creating mural")

original_image_list = image_processing.brightness_to_list("images")
image_list = image_processing.brightness_to_list("images")

# Looping through every pixel in the base_image
for y in range(N_IMAGES_HIGH):
    for x in range(N_IMAGES_WIDE):

        pixel_color = image[y][x]

        pixel_image, pixel_image_name, difference, index = best_image(pixel_color, image_list)

        # The mural is IMAGE_SIZE_PX bigger than the base image
        # As the base image have been resized to N_IMAGES_WIDE x N_IMAGES_HIGH
        pos_x = x * IMAGE_SIZE_PX
        pos_y = y * IMAGE_SIZE_PX

        try:
            # Index 0 of the image is the y position
            # Index 1 is the x
            mural_image[pos_y : pos_y + IMAGE_SIZE_PX, pos_x : pos_x + IMAGE_SIZE_PX] = pixel_image

        except Exception as e:
            print(e)
            print("Insertion of image at x:", x, "y:", y, "was not possible")
            print("You images might not have been resized correctly")

        # If REUSE_IMAGES have been set to false the used image will be removed
        # if less than REUSE_IMAGES_MIN_IMAGES are available the list will be refilled
        if REUSE_IMAGES == False:
            image_list.pop(index)

            if len(image_list) < REUSE_IMAGES_MIN_IMAGES:

                image_list = [i for i in original_image_list]
                print("Refilled image list")

    print("Finished row number", y, "out of", N_IMAGES_HIGH - 1)


# cv2.imwrite("mural.jpg", mural_image)

#TOP LEFT
cv2.imwrite("TOP_LEFT.jpg", mural_image[0:int(MURAL_HEIGHT_PX/2), 0 : int(MURAL_WIDTH_PX/2)])
#TOP RIGHT
cv2.imwrite("TOP_RIGHT.jpg", mural_image[0:int(MURAL_HEIGHT_PX/2), int(MURAL_WIDTH_PX/2) : MURAL_WIDTH_PX])
#BOTTOM LEFT
cv2.imwrite("BOTTOM_LEFT.jpg", mural_image[int(MURAL_HEIGHT_PX/2) : MURAL_HEIGHT_PX, 0:int(MURAL_WIDTH_PX/2)])
#BOTTOM RIGHT
cv2.imwrite("BOTTOM_RIGHT.jpg", mural_image[int(MURAL_HEIGHT_PX/2) : MURAL_HEIGHT_PX, int(MURAL_WIDTH_PX/2):MURAL_WIDTH_PX])
