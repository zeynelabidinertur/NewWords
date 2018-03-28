from Tkinter import *
#from PyDictionary import PyDictionary
#dictionary=PyDictionary()

def meaning_part(event, T, unknown_words_list, popup):
    cursor_loc = T.index(CURRENT)
    x, y = cursor_loc.split('.')
    text_loc_begin = x + "." + str(int(y) - 15)
    text_loc_end = x + "." + str(int(y) + 15)
    prev = T.get(text_loc_begin, cursor_loc).split(" ")
    next = T.get(cursor_loc, text_loc_end).split(" ")
    hovered_word = prev[-1] + next[0]
    if hovered_word in unknown_words_list:
        #word_meaning = dictionary.meaning(hovered_word).values()[0][0]#this return all the meanings of the word and we select just the first one
        word_meaning = "denem bir ki"
        popup.add_command(label=word_meaning)
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            popup.delete(0)
            popup.grab_release()
