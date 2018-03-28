def key(event):
    print "pressed", repr(event.char)
    cursor_loc = T.index(CURRENT)
    x, y =cursor_loc.split('.')
    text_loc_begin = x+"."+str(int(y)-15)
    text_loc_end = x +"."+ str(int(y) + 15)
    prev = T.get(text_loc_begin, cursor_loc).split(" ")
    next = T.get(cursor_loc, text_loc_end).split(" ")
    print prev, "y"
    print next, "x"
    print prev[-1]+next[0], "yoo"

def do_popup():
    # display the popup menu
    try:
        print "yoo"
        popup.tk_popup(root.winfo_pointerx(), root.winfo_pointery(), 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()

        # root = Tk()
        # frame = Frame(root, width=100, height=100)
        # Te = Text(root, height=5, width=30)
        # popup = Menu(frame, tearoff=0)

        unknown_words_list = ["here", "shall", "done", "should", "widget"]
        from threads import RepeatedTimer











        #popup.delete(1)

            #print dictionary.meaning(hovered_word)

##root.bind("<Button-1>", meaning_part)
##T.pack()
##T.configure(font=("Times New Roman", 12, "bold"))
##T.insert(END, "Just a text Widget\nin two lines\n Shall we try something new here\n I think we shall do this\n How Should this be done\n It should be done based on science",)
##frame.pack()
###rt = RepeatedTimer(0.5, meaning_part, "World")
##mainloop()
#rt.stop()




import os, PythonMagick
from PythonMagick import Image
import pyPdf


# from datetime import datetime

# start_time = datetime.now()

def pdf_opener(filename):
    # filename = "test_pf.pdf"
    pdf = pyPdf.PdfFileReader(open(filename, "rb"))
    return pdf

    for page in pdf.pages:
        print page.extractText()


pdf_dir = r"C:\Users\muhlissariyer\Desktop\pdfs"
bg_colour = "#ffffff"


def pdf_to_image():
    for pdf in [pdf_file for pdf_file in os.listdir(pdf_dir) if pdf_file.endswith(".pdf")]:
        input_pdf = pdf_dir + "\\" + pdf + "[1]"
        img = Image()
        img.density('300')
        print input_pdf
        img.read(input_pdf)

        size = "%sx%s" % (img.columns(), img.rows())

        output_img = Image(size, bg_colour)
        output_img.type = img.type
        output_img.composite(img, 0, 0, PythonMagick.CompositeOperator.SrcOverCompositeOp)
        output_img.resize(str(img.rows()))
        output_img.magick('JPG')
        output_img.quality(75)

        output_jpg = input_pdf.replace(".pdf", ".jpg")
        output_img.write(output_jpg)

# print datetime.now() - start_time














from wand.image import Image
from PIL import Image as PI
import sys
import os
from pyocr import pyocr
from pyocr import  builders
import io
#TESSERACT_CMD = os.environ["TESSDATA_PREFIX"] + os.sep + 'tesseract.exe' if os.name == 'nt' else 'tesseract'

tool = pyocr.get_available_tools()[0]
print tool
lang = tool.get_available_languages()
print lang
req_image = []
final_text = []

image_pdf = Image(file="test_pf.pdf", resolution=300)
image_jpeg = image_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))


for img in req_image:
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    final_text.append(txt)