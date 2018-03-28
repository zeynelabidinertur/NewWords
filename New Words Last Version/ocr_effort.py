import pytesseract
from PIL import Image as ima#, ImageEnhance, ImageFilter
import os
lang = "tur"
tesseract_location = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
#image = "Moran.jpg"
def ocr_from_image(image, lang):
    pytesseract.pytesseract.tesseract_cmd = tesseract_location
    im = ima.open(image) # the second one
    """This part is for enhancing the image"""
    #im = im.filter(ImageFilter.MedianFilter())
    #enhancer = ImageEnhance.Contrast(im)
    #im = enhancer.enhance(2)
    #im = im.convert('1')
    #im.save('temp.jpg')
    #file = Image.open('temp.jpg')
    """But it slows the process a lot and i'm not sure about its overall performance """
    text = pytesseract.image_to_string(im, lang=lang)
    #print text
    text_b = text.replace("-\n", "")
    text_c = text_b.replace("\n", " ")
    return text_c

def ocr_from_multi_images(folder):
    print os.listdir(folder)
    full_text = ""
    for jpg in [pdf_file for pdf_file in os.listdir(folder) if pdf_file.endswith(".jpg")]:
        input_jpg = folder + "\\" + jpg
        full_text+= ocr_from_image(input_jpg, lang)
    return full_text

#fold = "C:\Users\muhlissariyer\PycharmProjects\New Words Last Version\images\Anday"
#ocr_from_multi_images(fold)

#in order to make this work you have to install tesseract-ocr to your computer
# and on top of that you have to use the 3rd line to determine the location that tesseract is built