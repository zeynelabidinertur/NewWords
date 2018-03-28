#import os, PythonMagick
#from PythonMagick import Image
#import pyPdf
from ocr_effort import *

def pdf_opener(filename):
    pdf = pyPdf.PdfFileReader(open(filename, "rb"))
    return pdf

def pdf_to_image(pdf_loc):
    page_num = pdf_opener(pdf_loc).getNumPages()
    name = pdf_loc.split("\\").pop(-1).split(".")[0]
    all_directory = "images"
    if not os.path.exists(all_directory):
        os.makedirs(all_directory)
    directory = "images/" + name
    if not os.path.exists(directory):
        os.makedirs(directory)
    for page in range(page_num):
        print page
        bg_colour = "#ffffff"
        input_pdf = pdf_loc + "[%s]" %page
        img = Image()
        img.density('300')
        img.read(input_pdf)
        size = "%sx%s" % (img.columns(), img.rows())
        output_img = Image(size, bg_colour)
        output_img.type = img.type
        output_img.composite(img, 0, 0, PythonMagick.CompositeOperator.SrcOverCompositeOp)
        output_img.resize(str(img.rows()))
        output_img.magick('JPG')
        output_img.quality(75)
        folders = input_pdf.split("\\")
        folders.insert(-1,"images")
        folders.insert(-1,name)

        input_pdf = "\\".join(folders)

        output_jpg = input_pdf.replace(".pdf", "%s.jpg" %page)

        output_img.write(output_jpg)
        folder_loc = directory
    return folder_loc
#pdf_to_image("C:\Users\muhlissariyer\PycharmProjects\New Words Last Version\\Anday.pdf")

def pdf_text_extractor(pdf):
    full_text = ""
    for page in pdf.pages:
        full_text+=page.extractText()
    return full_text

def pdf_ocr_text(pdf_loc):
    folder_loc = pdf_to_image(pdf_loc)
    loc_list = pdf_loc.split("\\")[0:-1]+ folder_loc.split("/")
    folder_loc = "\\".join(loc_list)
    return ocr_from_multi_images(folder=folder_loc)
#pdf_ocr_text("C:\Users\muhlissariyer\PycharmProjects\New Words Last Version\\Anday.pdf")
