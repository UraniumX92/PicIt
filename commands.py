from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox as msgbox
from tkinter import filedialog as fd
import json
from PIL import Image
import img_utils
import os
import utils


def show_enc_help():
    """
    Shows the information about encryption strictness levels

    :return: None
    """
    msg = ("Security Level 0 : \nThe encryption key will be included in image, any user having this tool can extract from such images.\n\n"
           "Security Level 1 : \nKey will not be included in image. While extracting from image, user will be prompted to enter the key, this key will be used to decrypt the text even if the key is incorrect. \n"
           "Needless to state: if the key is incorrect, the extracted text will look like garbage text\n\n"
           "Security Level 2 : \nKey will not be included in image, but in this case encryption key should be entered correctly while extracting, otherwise user will not be provided any extracted text.\n\n"
           "Note : \nWhile manually entering key, you need not enter numbers separated by commas (like in auto generated key), you are supposed to use the key like a \"password\" for the image,"
           " you can just enter the text in that area.")
    msgbox.showinfo(title="Security Levels",message=msg)


def create_image(txtarea:Text,keyvar:StringVar,enc_strc:IntVar):
    """
    Takes the text from txtarea, key from keyvar, encryption strictness level from enc_strc
    and embeds the data in image and saves it

    :param txtarea:
    :param keyvar:
    :param enc_strc:
    :return: None
    """
    MIN_LENGTH = 10
    text = txtarea.get(1.0,END)
    text = text[:-1] if text[-1]=='\n' else text
    key = []
    key_val = keyvar.get()
    enc_val = enc_strc.get()
    encst_tup = tuple()

    if text == '' or key_val == '':
        return msgbox.showerror(title="Fields empty",message="Please fill all the required fields")
    elif len(text)<MIN_LENGTH:
        return msgbox.showerror(title="Text too small",message=f"Text should have atleast {MIN_LENGTH} characters.")

    match enc_val:
        case 0:
            encst_tup = (0,0,0)
        case 1:
            encst_tup = (1,0,0)
        case 2:
            encst_tup = (1,1,0)

    key = utils.get_key(key_val)

    confirm = msgbox.askyesno(title="Confirmation",message=f"are you sure you want to proceed with Security Level {enc_val} ?")
    if confirm:
        try:
            img = img_utils.hide_data(message=text,key=key,enc_strictnes=encst_tup)
        except OverflowError as err: # if image to be created requires too many pixels (img_utils.LIMIT)
            return msgbox.showerror(title="Text is too long",message=err.args[0])

        file = fd.asksaveasfilename(title="Save the created image as",initialdir=os.getcwd())
        if file!='':
            sf = file.split(".")
            if len(sf)==1:
                sf.append('')
            sf[-1] = 'png'
            file = f"{''.join(sf[:-1])}.{sf[-1]}"
            img.save(file,'png')
            msgbox.showinfo(title="Image created and saved",message=f"Successfully created and saved image at : {file}")
    else:
        return

def open_image(textarea:Text):
    """
    Opens image and extracts the image's data and writes it in textarea

    :param textarea:
    :return: None
    """
    data = textarea.get(1.0,END)
    textarea.config(state=NORMAL)
    file = fd.askopenfile(title="Open image",initialdir=os.getcwd())
    if file:
        try:
            img = Image.open(file.name,'r')
            enctup = img_utils.get_enc_tup(img)
            inpkey = ''
            if enctup == (0,0,0):
                text = img_utils.extract_data(img)
                text = ' '.join(text.split(" ")[1:-1])
                textarea.delete(1.0,END)
                textarea.insert(END,text)
            elif enctup == (1,0,0):
                inpkey = askstring(title="Key required",prompt="Enter the encryption key :\t\t\t")
                if inpkey=='' or (not inpkey):
                    return msgbox.showerror(title="Error",message="cannot extract text without key")
                rawtext = img_utils.extract_data(img)
                inpkey = utils.get_key(inpkey)
                text = utils.deciph(text=rawtext,key=inpkey)
                tlist = text.split(' ')
                if tlist[0] in img_utils.sgt_list and (tlist[0] == tlist[-1]):
                    text = ' '.join(text.split(" ")[1:-1])
                else:
                    pass
                textarea.delete(1.0,END)
                textarea.insert(END,text)
            elif enctup == (1,1,0):
                inpkey = askstring(title="Key required", prompt="Enter the encryption key :\t\t\t")
                if inpkey=='' or (not inpkey):
                    return msgbox.showerror(title="Error",message="cannot extract text without key")
                rawtext = img_utils.extract_data(img)
                inpkey = utils.get_key(inpkey)
                text = utils.deciph(text=rawtext, key=inpkey)
                tlist = text.split(' ')
                if tlist[0] in img_utils.sgt_list and (tlist[0] == tlist[-1]):
                    text = ' '.join(text.split(" ")[1:-1])
                else:
                    return msgbox.showerror(title="Incorrect key",message="Provided key is incorrect, cannot extract data from image")
                textarea.delete(1.0,END)
                textarea.insert(END,text)
            textarea.config(state=DISABLED)
            return msgbox.showinfo(title="Success",message="Succesfully extracted text from image!")
        except Exception as err:
            if isinstance(err,PIL.UnidentifiedImageError):
                return msgbox.showerror(title="Invalid file type for image",message="Selected file is not an image file.")
            elif isinstance(err,TypeError):
                return msgbox.showerror(title="Error",message=err.args[0])

def get_file_data(textarea:Text):
    """
    reads the data from selected file and sets the value of stringvar as the data

    :param textarea:
    :return: None
    """
    try:
        file = fd.askopenfile(title="Open file",initialdir=os.getcwd())
        if file:
            data = file.read()
            file.close()
            textarea.delete(1.0,END)
            textarea.insert(1.0,data)
    except UnicodeDecodeError:
        msgbox.showerror(title="Invalid data format",message="Selected file does not contain text data.")


def copy_ext(txtarea:Text,root:Tk):
    """
    copies the text from txtarea to clipboard

    :param txtarea: Text
    :param root: Tk
    :return: None
    """
    root.clipboard_clear()
    t = txtarea.get(1.0,END)
    t = t[:-1] if t[-1]=='\n' else t
    root.clipboard_append(t)
    root.update()

def save_txt_file(txtarea:Text):
    """
    takes text from txtarea and writes it into a file and saves it

    :param txtarea:
    :return: None
    """
    text = txtarea.get(1.0,END)
    text = text[:-1] if text[-1] == '\n' else text
    if text == '':
        return msgbox.showerror(title="Error",message="Text area is empty")
    else:
        file = fd.asksaveasfilename(title="Save the created image as", initialdir=os.getcwd())
        if file != '':
            sf = file.split('.')
            if len(sf)==1:
                sf.append('')
            sf[-1] = 'txt'
            file = f"{''.join(sf[:-1])}.{sf[-1]}"
            with open(file,'w') as f:
                f.write(text)
            msgbox.showinfo(title="Success",message=f"Text file successfully saved at: {file}")

def copy_key(s_var:StringVar,root:Tk):
    """
    copies the text from StringVar variable and appends to clipboard

    :param val:
    :param root:
    :return: None
    """
    root.clipboard_clear()
    root.clipboard_append(s_var.get())
    root.update()

def get_random_key(entry_var:StringVar):
    entry_var.set(f"{utils.random_KeyGen(20)}")
