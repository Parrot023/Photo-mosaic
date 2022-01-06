# Image mural
This project is a tool to create on massive image out of thousands of smaller images. To create whats called an image mural.

## Usage
To use the tool you will at first need quite a lot of build images. Depending on your size of mural i would recommend at least a couple of thousands to not reuse the images to often.

I you want to test out the tool but you don't have any build images. Use the script image_downloader.py to download a range of images from Bing

When you have your build images place them in the directory called images

Now would be a good time to find the base image to your mural. First crop the image to match the dimensions of the mural you would like to create. If you do not do this the tool will re-scale your image to match the dimensions you specify. This might make your image look stretched. When you have cropped your image name it main.jpeg or change the parameter BASE_IMAGE_PATH in image_mural.py and put it in the main project directory

Now change the parameters in image_mural.py to match the mural you would like to create

To create the mural run image_mural.py after changing the parameters

You will find the output of the tool in the directory named output

**If you for some cool reason use this tool it would be really cool if you would let me know :-)**

***A better documentation of how to use this tool will hopefully follow (but who knows)***


## To do:
- [ ] Make user friendly
- [ ] Improve efficiency
- [X] Add comments
- [X] Add feature to not reuse images
- [x] Create a script to make a smaller mural out of a tiny batch of images
- [x] Create a script to process the images (Making all of them the same dimensions)
- [x] Upgrade the first script to take a folder of pictures as an input and output one massive mural picture
