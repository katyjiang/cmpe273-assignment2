from PIL import Image # PIL is short for Python Image Library
import sys
import pytesseract

"""
The function going to use pytesseract to do OCR.
There are many things we can help to make OCR more accurate, such as crop image
to interesrting part, or use OpenCV to pre-process the image to increase
text-background contrast.
"""
def process(filePath):

    croppedImg = cropImage(filePath)
    
    # You can un-comment following line to save the cropped image
    # croppedImg.save(getCroppedImageName(filePath))

    return pytesseract.image_to_string(croppedImg)

""" Given a filePath, return cropped image.
This function highly rely on the size of the image given by the teacher
"""
def cropImage(filePath):
    
    # Open file. Alternatively we can use OpenCV to open it
    img = Image.open(filePath)

    # Get width and height in pixels of the image
    width, height = img.size

    # Now do crop, only save part of the image we are intereseted in.
    # Alternatively we can use OpenCV to do the cropption.
    # Why do we want to do cropption? because we want to get rid of
    # anything we don't interest, thus make the result more accurate.
    
    # Be careful, I manually measure the scantron-100.jpg provided by the
    # teacher to get the ratio of the interesting part.
    # What I measured (the numbers below are depends on my machine
    # so, later we will use ratio):
    # Width of the image is 71mm
    # Height of the image is 170mm
    # Width of the interesting part is 24mm
    # Height of the interesting part is 124mm
    # The top-left corner of the interesting part is [19, 25]
    # The bottom-right corner of the interesting part is [44, 148]
    top_left_x_ratio = float(19)/71
    top_left_y_ratio = float(25)/170
    bottom_right_x_ratio = float(44)/71
    bottom_right_y_ratio = float(148)/170

    # Since we know the ratio, lets get the top-left and bottom-right value
    top_left_x = top_left_x_ratio * width
    top_left_y = top_left_y_ratio * height
    bottom_right_x = bottom_right_x_ratio * width
    bottom_right_y = bottom_right_y_ratio * height

    # Do the cropption
    croppedImg = img.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    return croppedImg
    
# Given a filePath, add "_cropped" to the file name
def getCroppedImageName(filePath):
    lastDotIndex = filePath.rfind(".")
    extension = filePath[lastDotIndex:]
    return filePath.replace(extension, "_cropped"+extension)
    

# For testing purpose only
# To use this, download the scantron-100.jpg given by teacher
# into the same folder as this file, then open terminal, run
# ===================================
# python3.8 ocr.py scantron-100.jpg
# ===================================
if __name__ == "__main__":
    text = process(sys.argv[1])
    lines = text.splitlines() # will split text into multiple lines
    index = 0
    for line in lines:
        print(index, end =" ")
        print(line)
        index = index + 1
        
    
