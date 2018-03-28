#from PyDictionary import PyDictionary
#dictionary=PyDictionary()
#print dictionary.meaning("done")
#print (dictionary.synonym("Life"))
#print (dictionary.antonym("Life"))
#print (dictionary.translate("Range",'tr'))


# dictionary=PyDictionary("hotel","ambush","nonchalant","perceptive")
# #'There can be any number of words in the Instance'
#
# print dictionary.printMeanings() #'''This print the meanings of all the words'''
# print dictionary.getMeanings() #"""This will return meanings as dictionaries"""
# print dictionary.getSynonyms()
#
# print dictionary.translateTo("hi") #'''This will translate all words to Hindi'''


#from pdf2image import *

#images = convert_from_path("test_pf.pdf")

#import pyPdf
#filename = "test_pf.pdf"
#pdf = pyPdf.PdfFileReader(open(filename, "rb"))
#for page in pdf.pages:
#    print page.extractText()
from ttk import *
from Tkinter import *

from Tkinter import *
import threading, time
def doit(stop_event, arg):
    while not stop_event.wait(1):
        print ("working on %s" % arg)
    print("Stopping as you wish.")


def main():
    pill2kill = threading.Event()
    t = threading.Thread(target=doit, args=(pill2kill, "task"))
    t.start()
    time.sleep(5)
    pill2kill.set()
    t.join()

main()