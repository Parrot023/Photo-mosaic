import cv2
import image_processing
import numpy as np

MURAL_WIDTH = 120#120 #CM
MURAL_HEIGHT = 80#80 # CM
PPI = 300 #PIXELS PER INCH
IMAGE_SIZE_CM = 2.5 #CM

PPCM = int(PPI / 2.54) #PIXEL PER CM
N_IMAGES_WIDTH = int(MURAL_WIDTH / IMAGE_SIZE_CM)
N_IMAGES_HEIGHT = int(MURAL_HEIGHT / IMAGE_SIZE_CM)

IMAGE_SIZE_PX = int(IMAGE_SIZE_CM * PPCM) # IMAGE HEIGHT IN (PX)
MURAL_WIDTH_PX = MURAL_WIDTH * PPCM
MURAL_HEIGHT_PX = MURAL_HEIGHT * PPCM


print("PPCM", PPCM)
print("IMAGE SIZE", IMAGE_SIZE_PX)
print("MURAL WIDTH (PX)", MURAL_WIDTH_PX)
print("MURAL HEIGHT (PX)", MURAL_HEIGHT_PX)
print("NUMBER OF IMAGES WIDE", N_IMAGES_WIDTH)
print("NUMBER OF IMAGES HIGH", N_IMAGES_HEIGHT)
print("TOTAL NUMBER OF IMAGES NEEDED", N_IMAGES_WIDTH * N_IMAGES_HEIGHT)


image = cv2.imread("main.jpeg")
img_height, img_width, img_channels = image.shape
new_height = int((img_height / MURAL_HEIGHT)) * MURAL_HEIGHT
new_width = int((img_width / MURAL_WIDTH)) * MURAL_WIDTH

# if not img_height == new_height and not img_width == new_height:
#
#     exit()

# image_processing.image_cropping("images")
# image_processing.image_rescaling(IMAGE_SIZE_PX, IMAGE_SIZE_PX, "images")

image = cv2.resize(image, (N_IMAGES_WIDTH, N_IMAGES_HEIGHT))
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blank_image = np.zeros((MURAL_HEIGHT_PX, MURAL_WIDTH_PX, 3), np.uint8)

def best_image(pixel_color, b_list):

    smallest_difference = 256
    best_image = None

    for index, i in enumerate(b_list):

        if abs(pixel_color - i[1]) < smallest_difference:

            smallest_difference = abs(pixel_color - i[1])

            best_image = i[0]

            best_image_index = index

    image = cv2.imread("images/" + best_image)

    return image, best_image, smallest_difference

print("Creating mural")

for y in range(N_IMAGES_HEIGHT):
    for x in range(N_IMAGES_WIDTH):

        pixel_color = image[y][x]

        b_list = image_processing.brightness_to_list("images")

        pixel_image, pixel_image_name, difference = best_image(pixel_color, b_list)

        pos_x = x * IMAGE_SIZE_PX
        pos_y = y * IMAGE_SIZE_PX

        try:

            # blank_image[pos_x : pos_x + IMAGE_SIZE_PX, pos_y : pos_y + IMAGE_SIZE_PX] = pixel_image
            blank_image[pos_y : pos_y + IMAGE_SIZE_PX, pos_x : pos_x + IMAGE_SIZE_PX] = pixel_image

            # print("worked:", x,y)
        except Exception as e:
            print(e)
            print("didnt work:", x,y)
            print(x * IMAGE_SIZE_PX, x * IMAGE_SIZE_PX + IMAGE_SIZE_PX)
            print(y * IMAGE_SIZE_PX, y * IMAGE_SIZE_PX + IMAGE_SIZE_PX)

    print("Finished row number", y, "out of", N_IMAGES_HEIGHT)


cv2.imwrite("mural.jpg", blank_image)
