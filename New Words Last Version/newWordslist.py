import Tkinter as tk
import anydbm
import pickle as pk
from tkFileDialog import askopenfilename
import re
from ScrolledText import ScrolledText
from search_for_meaning import meaning_part
# from PyDictionary import PyDictionary
# from pdf_opener_functions import *
from ttk import Progressbar
import threading
# dictionary=PyDictionary()
# Create database
database = anydbm.open("database.db", "c")

# words_en list accomodates all English dictionary words
words_en = []

# If database is empty; that means if we're using the program for the first time
if len(database) == 0:
    general_dict = {}
    general_dict["Known"] = {"All": {}}
    general_dict["Unknown"] = {}
    general_dict["Outside"] = {}
    general_dict["All"] = {}
    general_dict["Text"] = {}
    for word in open("words_en.txt"):
        words_en.append(word.strip("\n"))
    general_dict["words_en"] = words_en

# If database is not empty; that means if we used the program earlier
if len(database) != 0:
    general_dict = pk.loads(database["general_dict"])
    words_en = general_dict["words_en"]

# uw_box_selected list accommodates all selected words from the Unknown Words Box
uw_box_selected = []

# kw_box_selected list accommodates all selected words from Known Words Box
kw_box_selected = []

# texts_titles_list list accommodates all titles of the current texts (appeared in the Texts box
texts_titles_list=[]
for text in general_dict["All"]:
    texts_titles_list.append(text)

# knownWordsList = []
# generalUnknown = []
# generalKnown = []

# texts_selected_index is the index of the selected text from the Texts Box
# texts_selected_index = 0
texts_selected_index = None


# class FetchData(object):
#     def __init__(self):
#         print "Hej more!"
  

class NewWords:
    def __init__(self, root):
        # super(NewWords,self).__init__()
        root.title("New Words")
        self.root=root
        global general_dict

        # define our frames
        upper_canvas = tk.Canvas(root, width=800, height=50)
        upper_canvas.create_text(350, 15, text="new Words", font=("Calibri", 14, "bold"), anchor="w")
        upper_canvas.create_text(135, 40, text="Texts" + " "*70 + "Known Words" + " "*24 + "Unknown Words",
                                 font=("Calibri", 12), anchor="w", )
        upper_frame = tk.Frame(root, relief="groove", borderwidth=3)
        lower_canvas = tk.Canvas(root, width=800, height=50)
        lower_canvas.create_text(245, 40, text="All Words" + " "*18 + "Outside Words",
                                 font = ("Calibri", 12), anchor="w", )
        lower_frame = tk.Frame(root, relief="groove", borderwidth=3)

        upper_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        upper_frame.pack(side=tk.TOP, fill=tk.BOTH)
        lower_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        lower_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # upper Frame
        add_book_bt = tk.Button(upper_frame, text="Add a\ntext!", command=self.add_text)
        ocr_pdf_bt = tk.Button(upper_frame, text="OCR PDF!", command=self.ocr_pdf)
        texts_box_sb = tk.Scrollbar(upper_frame)
        self.texts_lb = tk.Listbox(upper_frame, yscrollcommand=texts_box_sb.set, width=40)
        for book in general_dict["All"]:
            self.texts_lb.insert(tk.END, book)

        self.texts_lb.bind('<<ListboxSelect>>', self.texts_selection)
        texts_box_sb.config(command=self.texts_lb.yview)
        open_bt = tk.Button(upper_frame, text="Open", command=self.open_text)
        largo = tk.Button(upper_frame, text="Delete the\nbook!", command=self.delete_text)
        kw_box_sb = tk.Scrollbar(upper_frame)
        self.kw_lb = tk.Listbox(upper_frame, yscrollcommand=kw_box_sb.set, selectmode="multiple", )
        self.kw_lb.bind('<<ListboxSelect>>', self.kw_box_selection)
        kw_box_sb.config(command=self.kw_lb.yview)

        shift_left_bt = tk.Button(upper_frame, text="<=", command=self.shift_left)
        shift_right_bt = tk.Button(upper_frame, text="=>", command=self.shift_right)
        uw_box_sb = tk.Scrollbar(upper_frame)
        self.uw_lb = tk.Listbox(upper_frame, yscrollcommand=uw_box_sb.set, selectmode="multiple")
        self.uw_lb.bind('<<ListboxSelect>>', self.uw_selection)
        uw_box_sb.config(command=self.uw_lb.yview)

        add_book_bt.grid(row=0, column=0, rowspan=2, padx=(10, 10))
        ocr_pdf_bt.grid(row=1, column=0, rowspan=2, padx=(10, 10))
        self.texts_lb.grid(row=0, column=1, rowspan=2, padx=(10, 0))
        texts_box_sb.grid(row=0, column=2, rowspan=2, sticky=tk.N + tk.S, padx=(0, 10))
        open_bt.grid(row=0, column=3, padx=(10, 10), pady=(30, 10))
        largo.grid(row=1, column=3, rowspan=1, padx=(10, 10), pady = (10, 30))
        self.kw_lb.grid(row=0, column=4, rowspan=2, padx=(20, 0))
        kw_box_sb.grid(row=0, column=5, rowspan=2, sticky=tk.N+tk.S, padx=(0, 10))
        shift_left_bt.grid(row=0, column=6, rowspan=1, padx=(10, 10), pady=(30,0))
        shift_right_bt.grid(row=1, column=6, padx=(10, 10), pady=(0, 30))
        self.uw_lb.grid(row=0, column=7, rowspan=2, padx=(10, 0))
        uw_box_sb.grid(row=0, column=8, rowspan=2, sticky=tk.N+tk.S, padx=(0, 10))

        # lower Frame
        all_words_sb = tk.Scrollbar(lower_frame)
        self.all_words_box = tk.Listbox(lower_frame, yscrollcommand=all_words_sb.set)
        self.all_words_box.bind('<<ListboxSelect>>', self.all_words_selection)
        all_words_sb.config(command=self.all_words_box.yview)
        for i in range(19):
            self.all_words_box.insert(i)

        ow_box_sb = tk.Scrollbar(lower_frame)
        self.ow_box = tk.Listbox(lower_frame, yscrollcommand=ow_box_sb.set, height=10)
        self.ow_box.bind('<<ListboxSelect>>', self.outside_words_selection)
        ow_box_sb.config(command=self.ow_box.yview)

        self.all_words_box.grid(row=0, column=0, padx= (230, 0))
        all_words_sb.grid(row=0, column=1,  padx= (0, 30), sticky=tk.N+tk.S)

        self.ow_box.grid(row=0, column=2, padx= (10, 0))
        ow_box_sb.grid(row=0, column=3, sticky=tk.N+tk.S)

        # self.empty_spaces = []
        # for i in range(20):
        #     self.empty_spaces.append(""*i)
        self.selected_text_title = "[]"

    # "add_text" method is activated when "Add a text!" button is clicked. It gives the opportunity to choose
    # a file (currently working only with txt files)
    def progressbar(self):
        root2 = tk.Tk()
        pb = Progressbar(root2, orient="horizontal", length=200, mode="determinate")
        pb.pack()
        pb.start()
        root2.mainloop()
    def ocr_pdf(self):
        filename = askopenfilename(filetypes=[("PDF Files", ('.pdf'))])
        filename2 = filename.replace("/","\\")
        #t = threading.Thread(target=self.progressbar)
        #t.start()
        #t.
        full_text = "hebele bhsaldkjk"#pdf_ocr_text(str(filename2))
        filename = filename.replace(".pdf", ".txt")
        doc_file = open(filename,"w")
        doc_file.write(full_text.encode('utf-8'))
        doc_file.close()
        self.add_text(filename)

    def add_text(self, *ocr_filename):
        global texts_titles_list
        if ocr_filename == ():
            filename = askopenfilename(filetypes=[("Word Files", ('.docx', '.txt', '.pdf'))])
        else:
            filename = ocr_filename[0]
        """ PDF OPENER --if else can be made better for differentiating pdf from others"""
        if filename.split(".")[-1] == "pdf":
                    pdf = pdf_opener(filename)
            #print pdf_text_extractor(pdf)
            file_title = filename.split("/")[-1].split(".")[0]
            self.extract_words(file_title, filename, pdf_text_extractor(pdf))
            texts_titles_list.append(file_title)
            self.texts_lb.insert(tk.END, file_title)
            return
        """ PDF OPENER """
        if filename == "":
            return
        file_title = re.split("/", filename)[-1].split(".")[0]
        file_title_ = ""

        for word in file_title.split():
            # any Non-alphanumeric character is removed from the title
            file_title_ += re.sub("\W", "", word)
            file_title_ += " "

        file_title = file_title_
        # If there is another text with the same title, we add underline (_) to the end of the title
        while file_title in texts_titles_list:
            file_title += "_"
        texts_titles_list.append(file_title)

        self.texts_lb.insert(tk.END, file_title)
        self.extract_words(file_title, filename)

    # "extract_wors" function extracts all words from the text and accommodates each word to the appropriate
    # place (Known, Unknown, Outside ect.)
    def extract_words(self, file_title, filename, *pdf_content):
        global general_dict
        file_title = str(file_title)

        # "words_list" is a list with tuples as its items. Each tuple's first it number of repetitions
        # and second item is the word corresponding to number of repetitions
        words_list = []

        # "words_number" is a dictionary with words as keys and their repetitions as values
        words_number = {}
        file1 = open(filename)
        text_content = ""
        for line in file1:
            text_content += line
            line = line.lower()
            # extract each word from the line
            for word in re.split("[^A-Za-z]", line):
                word = word.strip()
                if word == "":
                    continue
                else:
                    if word in words_number:
                        # if word is already in the dictionary, add 1 to its value
                        words_number[word] += 1
                    else:
                        # if word is not in the dictionary add the word to the dictionary with its value 1
                        words_number[word] = 1
        """"PDF PART"""
        if filename.split("/")[-1].split(".")[-1] == "pdf":
            text_content = pdf_content
        """"PDF PART"""
        general_dict["Text"][file_title] = text_content

        for word in words_number:
            words_list.append((words_number[word], word))

        words_list.sort()
        words_list.reverse()
        general_dict["Known"][file_title] = {}
        general_dict["Unknown"][file_title] = {}
        general_dict["Outside"][file_title] = {}
        general_dict["All"][file_title] = words_list

        for repeat, word in words_list:
            if word not in words_en:
                # if word not in english dictionary:
                general_dict["Outside"][file_title][word] = repeat
                continue
            if word in general_dict["Known"]["All"]:
                # if word is known (based on the previous texts):
                general_dict["Known"][file_title][word] = repeat
            else:
                general_dict["Unknown"][file_title][word] = repeat

    # based on the selected value inside "Texts" box, "texts_selection" method accomodates words to the
    # appropriate boxes (Known, Unknown, Outside, All)
    def texts_selection(self, event):
        global uw_box_selected
        global texts_selected_index
        uw_box_selected = []
        self.uw_lb.delete(0, tk.END)
        self.kw_lb.delete(0, tk.END)
        self.ow_box.delete(0, tk.END)
        self.all_words_box.delete(0, tk.END)
        listbox = event.widget
        if listbox.get(0) == "":
            return
        texts_selected_index = listbox.curselection()[0]
        self.selected_text_title = listbox.get(texts_selected_index)
        self.uw_lb.insert(tk.END, self.selected_text_title)
        self.uw_lb.insert(tk.END, "")
        uw_list = []
        for word in general_dict["Unknown"][self.selected_text_title]:
            uw_list.append(word)
        uw_list.sort()
        for word in uw_list:
            self.uw_lb.insert(tk.END, word)
        self.kw_lb.insert(tk.END, self.selected_text_title)
        self.kw_lb.insert(tk.END, "")

        kw_list = []
        for word in general_dict["Known"][self.selected_text_title]:
            kw_list.append(word)
            kw_list.sort()
        for word in kw_list:
            self.kw_lb.insert(tk.END, word)
        self.ow_box.insert(tk.END, self.selected_text_title)
        self.ow_box.insert(tk.END, "")

        ow_list = []
        for word in general_dict["Outside"][self.selected_text_title]:
            ow_list.append(word)
            ow_list.sort()
        for word in ow_list:
            self.ow_box.insert(tk.END, word)

        for count1, word in general_dict["All"][self.selected_text_title]:
            self.all_words_box.insert(tk.END, str(count1) + "  " + word)

    # "delete_text" method deletes the selected text. It makes sure that everything belonging to the text
    # is cleaned up from the database except known words extracted from the text that now are part of
    # all known words set
    def delete_text(self):
        global general_dict
        global uw_box_selected
        global texts_titles_list
        if texts_selected_index == None:
            return
        self.texts_lb.delete(texts_selected_index)
        general_dict["Unknown"].pop(self.selected_text_title)
        general_dict["Known"].pop(self.selected_text_title)
        general_dict["Outside"].pop(self.selected_text_title)
        general_dict["All"].pop(self.selected_text_title)
        texts_titles_list.remove(self.selected_text_title)
        self.uw_lb.delete(0, tk.END)
        self.kw_lb.delete(0, tk.END)
        self.ow_box.delete(0, tk.END)
        self.all_words_box.delete(0, tk.END)
        uw_box_selected = []


    def open_text(self):
        #in the usage of tags there were 3 problems faced, 1-the markings such as dot, comma but it is solved
        # 2-Uppercases are not matching, this is not solved
        # 3-Words that are shorter than 4 letters take the next words first letter
        if self.selected_text_title != "[]":

            text_root = tk.Tk()
            text_root.title(self.selected_text_title)
            popup = tk.Menu(text_root, tearoff=0)
            textWindow = ScrolledText(text_root, wrap = "word")
            uw_list = self.uw_lb.get(0,tk.END)
            text_root.bind("<Button-1>", lambda eff:meaning_part(eff, T=textWindow, unknown_words_list=uw_list, popup=popup))
            textWindow.insert(1.0, general_dict["Text"][self.selected_text_title])
            textWindow.tag_config("A", foreground="red", background="white")
            textWindow.pack(expand = True, fill = tk.BOTH)
            for pre_word in uw_list:#general_dict["Unknown"][self.selected_text_title]:
                word =  " " + pre_word + " "
                start = 1.0
                search_pos = textWindow.search(word, start, stopindex=tk.END)
                if not search_pos:
                    for x in '"^+%&/()=?_-*,;:.!>#${{[]}\'':
                        word = " " + pre_word + x
                        search_pos = textWindow.search(word, start, stopindex=tk.END)
                        if search_pos: break
                    if not search_pos:
                        for x in '"^+%&/()=?_-*,;:.!>#${{[]}\'':
                            word = x + pre_word + " "
                            search_pos = textWindow.search(word, start, stopindex=tk.END)
                            if search_pos: break
                #print word, search_pos

                while search_pos:
                    length = len(word)
                    row, col = search_pos.split('.')
                    end = int(col) + length
                    #if str(end)[-1]=="0":
                    #    end += 1

                    print end, col
                    end = row + '.' + str(end)

                    print search_pos, end, word
                    textWindow.tag_add("A", search_pos, float(end))
                    start = end
                    search_pos = textWindow.search(word, start, stopindex=tk.END)


    def shift_left(self):
        global uw_box_selected
        global general_dict
        if len(uw_box_selected)==0:
            return
        for index, word in uw_box_selected:
            if index ==0 or index==1:
                continue
            self.uw_lb.delete(index)
            self.kw_lb.insert(tk.END, word)
            general_dict["Known"]["All"][word] = general_dict["Unknown"][self.uw_lb.get(0)][word]
            for book in general_dict["All"]:
                try:
                    general_dict["Unknown"][book][word]
                    general_dict["Known"][book][word] = general_dict["Unknown"][book][word]
                except:
                    continue
                general_dict["Unknown"][book].pop(word)

        uw_box_selected = []

    def shift_right(self):
        global kw_box_selected
        global general_dict
        if len(kw_box_selected) == 0:
            return

        for index, word in kw_box_selected:
            if index == 0 or index == 1:
                continue
            self.kw_lb.delete(index)
            self.uw_lb.insert(tk.END, word)
            general_dict["Known"]["All"].pop(word)
            for book in general_dict["All"]:
                try:
                    general_dict["Known"][book][word]
                    general_dict["Unknown"][book][word] = general_dict["Known"][book][word]
                except:
                    continue
                general_dict["Known"][book].pop(word)

        kw_box_selected = []
        

    def kw_box_selection(self, event):
        global kw_box_selected
        global texts_selected_index
        texts_selected_index = None
        kw_box_selected = []
        listbox = event.widget
        list_indexes = listbox.curselection()

        for index in list_indexes:
            value = listbox.get(index)
            kw_box_selected.append((index, value))
        kw_box_selected.reverse()

    def uw_selection(self, event):
        global texts_selected_index
        global uw_box_selected
        texts_selected_index = None
        uw_box_selected = []
        listbox = event.widget
        list_indexes = listbox.curselection()

        for index in list_indexes:
            value = listbox.get(index)
            uw_box_selected.append((index, value))
        uw_box_selected.reverse()

    def all_words_selection(self, event):
        global texts_selected_index
        global uw_box_selected
        texts_selected_index = None
        uw_box_selected = []

    def outside_words_selection(self, event):
        global texts_selected_index
        global uw_box_selected
        texts_selected_index = None
        uw_box_selected = []


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(1,1)
    root.geometry("800x450+300+100")
    NewWords(root)
    root.mainloop()

s = pk.dumps(general_dict)
database["general_dict"] = s

database.close()
