import cv2
import image_processing
import numpy as np
import os


# MOSAIC PARAMETERS ------------------------------------------------
MOSAIC_WIDTH = 180 # CM
MOSAIC_HEIGHT = 180 # CM
PPI = 300 # PIXELS PER INCH
IMAGE_SIZE_CM = 2 # CM

PPCM = int(PPI / 2.54) #PIXEL PER CM
TILE_WIDTH = 90 # CM
TILE_HEIGHT = 90 # CM

BASE_IMAGE_PATH = "main.jpeg"
BUILD_IMAGES_DIR_PATH = "images"
OUTPUT_DIR = "output"

# Determines whether or not to use the same image multiple times in a row
REUSE_IMAGES = False
# Determines how many images are left before allowing previously used images
REUSE_IMAGES_MIN_IMAGES = 200

# Determines whether or not the best image shoud be tinted towards the original pixel color
# This can give the mosaic a better look
CORRECT_COLORS = True
# Determines how much the image will be tinted
# More than 0.05 will tint the image quite a lot
CORRECTION_PECENTAGE = 0.05

N_IMAGES_WIDE = int(MOSAIC_WIDTH / IMAGE_SIZE_CM) # NUMBER OF IMAGES WIDE
N_IMAGES_HIGH = int(MOSAIC_HEIGHT / IMAGE_SIZE_CM) # NUMBER OF IMAGES HIGH

IMAGE_SIZE_PX = int(IMAGE_SIZE_CM * PPCM) # IMAGE HEIGHT AND WIDTH IN (PX)
MOSAIC_WIDTH_PX = MOSAIC_WIDTH * PPCM # mosaic WIDTH IN PIXELS
MOSAIC_HEIGHT_PX = MOSAIC_HEIGHT * PPCM # mosaic HEIGHT IN PIXELS

TILE_WIDTH_PX = TILE_WIDTH * PPCM
TILE_HEIGHT_PX = TILE_HEIGHT * PPCM
# -------------------------------------------------------------------


if MOSAIC_WIDTH % TILE_WIDTH != 0 or MOSAIC_HEIGHT % TILE_HEIGHT != 0:

    print("""You mosaic width does not divide into your tile width
    or you mosaic height does not divide into you tile height""")
    print("TILE_WIDTH:", TILE_WIDTH)
    print("TILE_HEIGHT:", TILE_HEIGHT )

    exit()

# mosaic INFO ---------------------------------------------------------
print("MOSAIC DIMENSIONS")
print("Pixels per cm", PPCM)
print("Building images height and width in pixels", IMAGE_SIZE_PX)
print("mosaic width in pixels", MOSAIC_WIDTH_PX)
print("mosaic height in pixels", MOSAIC_WIDTH_PX)
print("Number of images wide", N_IMAGES_WIDE)
print("Number of images high", N_IMAGES_HIGH)
print("Total numer of images needed", N_IMAGES_WIDE * N_IMAGES_HIGH)
print("NOTICE!!: All your base images will be cropped and resized to match the size mentioned above. This cannot be undone. Please backup all off your build images!")
# ---------------------------------------------------------------------

# Letting the user exit after seing the mosaic dimensions
if input("Do you want to continue (y/n): ") != "y":
    print("Aborting mosaic creation")
    exit()

# Loading mosaic base image
image = cv2.imread(BASE_IMAGE_PATH)
img_height, img_width, img_channels = image.shape

# Letting the user exit before resizing their base image
if not img_height/img_width == N_IMAGES_HIGH/N_IMAGES_WIDE:

    message = "You mosaic base image does not have the same aspect ratio as your mosaic your images will be resized to match your mosaic. This may result in the image looking stretched. Continue? (y/n)"

    if input(message) != "y":
        exit()

# Using the function image_cropping from image_processing.py to make every image square
image_processing.image_cropping("images")
# Using the function image_rescaling from image_processing.py to make every image the size that was just defined
image_processing.image_rescaling(IMAGE_SIZE_PX, IMAGE_SIZE_PX, "images")

# Resizing and converting base image to Grayscale
image = cv2.resize(image, (N_IMAGES_WIDE, N_IMAGES_HIGH))
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Blank image for the mosaic
mural_image = np.zeros((MOSAIC_HEIGHT_PX, MOSAIC_WIDTH_PX, 3), np.uint8)

def best_image(pixel_color, image_list):

    smallest_difference = 256**256
    best_image_name = None

    for index, i in enumerate(image_list):

            # If the differance between this image average color and the pixel
            # is lower than the smallest difference this is the new best image

            total_diff = 0

            B_diff = abs(pixel_color[0] - i[1][0])**2
            G_diff = abs(pixel_color[1] - i[1][1])**2
            R_diff = abs(pixel_color[2] - i[1][2])**2

            total_diff = B_diff + G_diff + R_diff

            # if abs(pixel_color - i[1]) < smallest_difference:
            if total_diff < smallest_difference:

                # Index 1 is the average color of the image
                # smallest_difference = abs(pixel_color - i[1])
                smallest_difference = total_diff

                # Index 0 is the filename
                best_image_name = i[0]

                best_image_index = index

    image = cv2.imread("images/" + best_image_name)
    return image, best_image_name, smallest_difference, best_image_index

print("Creating mosaic")

original_image_list = image_processing.brightness_to_list(BUILD_IMAGES_DIR_PATH)
image_list = image_processing.brightness_to_list(BUILD_IMAGES_DIR_PATH)

# Looping through every pixel in the base_image
for y in range(N_IMAGES_HIGH):
    for x in range(N_IMAGES_WIDE):

        pixel_color = image[y][x]

        pixel_image, pixel_image_name, difference, index = best_image(pixel_color, image_list)

        # Corrects the color of the image by overlaying the pixel color
        if CORRECT_COLORS:
            pixel_image = image_processing.image_color_correction(pixel_image, pixel_color, CORRECTION_PECENTAGE)

        # The mosaic is IMAGE_SIZE_PX bigger than the base image
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

try:
    os.mkdir(OUTPUT_DIR)
except FileExistsError:
    print("Output directory does already exist :-)")

# Saving the image in smaller parts as the full image is way to big
for i in range(int(MOSAIC_HEIGHT / TILE_HEIGHT)):
    for j in range(int(MOSAIC_WIDTH / TILE_WIDTH)):
        # Each part of th image is saved with a name in the format XY.jpg
        cv2.imwrite(OUTPUT_DIR + "/{}{}.jpg".format(j,i), mural_image[i * TILE_HEIGHT_PX: i * TILE_HEIGHT_PX + TILE_HEIGHT_PX, j * TILE_WIDTH_PX : j * TILE_WIDTH_PX + TILE_WIDTH_PX])
