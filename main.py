"""
    Project inspired by the concept of Steganography
    Project Name : PicIt

    Functionalities:
        > Pixel requirement:
            2 pixels for message length and starting co-ordinates
            2 pixels for encryption key length and starting co-ordinates
            2 pixel to store the strictness of encryption key (same data in both pixels)
            Total : 6
            Automatically calculate the amount of pixels required for the message and create it
            n -> length of image (square image)

            (0,0) --> length of text
            (0,n) --> Initial co-ordinates of text
            (n,0) --> length of key
            (n,n) --> Initial co-ordinates of key
            (0,2) and (2,0) --> strictness of encryption

        > If Encryption key is to be entered manually, then there should be two cases:
            1. receiving user will have to enter correct key to extract the data
                prefix "PicIt" to the plain message while hiding, if the entered key is correct then first word should be decrypted to "PicIt", this is how we know that encryption key is correct.
            2. message will simply decrypt using given key, if key is wrong then user will see garbage text, else readable text

        > Encryption strictness tuple interpretation:
            (0,0,0) --> Key is randomly generated, extract the key from image and send the data
            (1,0,0) --> Key is manually added, user should provide the key, regardless of key being correct or not, data will be decrypted and sent
            (1,1,0) --> Key is manually added, user should provide only the correct key, or else no data will be provided to user

        > Storing of lengths of key, text:
            let's say `len` is the length here, convert `len` into 24-bit binary representation,
            slice this 24-bit binary string into three 8-bit binary strings
            convert this three 8-bit binaries into int and store in a tuple as (a,b,c)

        > length tuple interpretation:
            (a,b,c) --> convert a,b,c to binary 8-bit representation
            concatenate all three 8-bit binary string, we get a 24-bit binary string
            convert this 24-bit binary string to int, now we have the length.

        > Co-ordinate tuple interpretation:
            (a,n,b) --> (x,y) = (a,b)
            > Text co-ordinate tuple will hold random number 'n' in middle element.

            > Key co-ordinate tuple will hold Orientation of traversal in middle element:
                0 --> vertical
                1 --> horizontal

    Features:
        > Manually enter encryption key?
            Yes : only encrypted text will be stored, receiving user will have to enter key manually to extract message.
            No : encryption key will be randomly generated and will be stored in picture with metadata
        > file for messages:
            save the extracted message to a .txt file
            read the text file and store the content of file as message.
"""
from PIL import Image
from tkinter import *
from tkinter import filedialog as fd
import commands
import random
import img_utils
import utils
import os

# CONSTANTS
green_Tcolor = '#10AD14'
BACKGROUND = '#2F3136'
darker_BG = '#222222'
lighter_BG = '#55585E'
xs_padding = 3
s_padding = 5
m_padding = 10
header_font_tuple = ('consolas',20,'bold')
header_font_tuple2 = ('consolas',18,'bold')
txt_font_tuple = ('consolas',12)
label_font_tuple = ('Segoe UI Symbol',12,'bold')
btn_font_tuple = ('Segoe UI Symbol', 10)
lable_text_color = 'white'

# root window configurations
root = Tk()
root.geometry("1250x900")
root.resizable(width=False,height=False)
root.config(background=BACKGROUND)
root.title("PicIt - Application by Syed Usama")

# Variables
enc_strictness = IntVar()
key = StringVar()
ext_key = StringVar()

# ---- creating and packing GUI elements ---- #

# Title Label
t_label = Label(text="PicIt - Turn Your Text Into a Picture",font=header_font_tuple,background=BACKGROUND,foreground=lable_text_color)
t_label.pack(side=TOP,pady=m_padding,padx=m_padding,ipady=s_padding,ipadx=s_padding)

# Input Frame
inpFrame = Frame(master=root,background=BACKGROUND)
inpFrame.pack(side=TOP,pady=s_padding,padx=s_padding,expand=True,anchor=N)

# Input text area
inp_label = Label(master=inpFrame,text="Enter the text :",font=label_font_tuple,background=BACKGROUND,foreground=lable_text_color)
inp_label.grid(row=0,column=0,pady=s_padding,padx=s_padding,sticky=N)
inp_field = Text(master=inpFrame,insertbackground=green_Tcolor,font=txt_font_tuple, foreground=green_Tcolor, background=darker_BG, height=17, width=120)
inp_field.grid(row=0,column=1,padx=s_padding,pady=s_padding)

# Key Label Entry
key_label = Label(master=inpFrame,text="Enter the key :",font=label_font_tuple,background=BACKGROUND,foreground=lable_text_color)
key_label.grid(row=1,column=0,pady=s_padding,padx=s_padding)
key_entry =Entry(master=inpFrame,textvariable=key,width=120,background=darker_BG,font=txt_font_tuple,foreground=green_Tcolor,insertbackground=green_Tcolor,readonlybackground=BACKGROUND)
key_entry.grid(row=1,column=1,padx=s_padding,pady=s_padding,ipady=xs_padding)


# Radio Frame for storing radio buttons
radFrame = Frame(master=inpFrame,background=BACKGROUND)
radFrame.grid(row=2,column=1)

radio_label = Label(master=radFrame,text="Select Encryption method: ",font=label_font_tuple,background=BACKGROUND,foreground=lable_text_color)
radio_label.grid(row=0,column=0,pady=s_padding,padx=s_padding,sticky='W')

# Radio buttons for encryption strictness levels
r0 = Radiobutton(master=radFrame, text="Auto Generate Key", variable=enc_strictness,font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=0, command=lambda : commands.radio_command(enc_strictness, key_entry,key))
r0.grid(row=0,column=1,padx=s_padding,pady=s_padding,sticky='W')

r1 = Radiobutton(master=radFrame, text="Security Level 1", variable=enc_strictness,font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=1, command=lambda : commands.radio_command(enc_strictness, key_entry,key))
r1.grid(row=0,column=2,padx=s_padding,pady=s_padding,sticky='W')

r2 = Radiobutton(master=radFrame, text="Security Level 2", variable=enc_strictness,font=label_font_tuple, background=BACKGROUND, activebackground=lighter_BG, value=2, command=lambda : commands.radio_command(enc_strictness, key_entry,key))
r2.grid(row=0,column=3,padx=s_padding,pady=s_padding,sticky='W')
# calling this command externally to initialize default condition
commands.radio_command(enc_strictness, key_entry,key)
# help button which shows information about different encryption methods.
help_btn = Button(master=radFrame, text="Show info about encryption methods", activebackground=lighter_BG,font=btn_font_tuple,relief=RAISED,foreground=lable_text_color,background=darker_BG,command=lambda: commands.show_enc_help())
help_btn.grid(row=0,column=4,padx=s_padding,pady=s_padding,sticky='W')
# -- End of Radio Frame -- #

# Buttons
opntxt_btn = Button(master=inpFrame, text="Open a file to load text", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=lable_text_color, background=darker_BG, command=lambda: commands.get_file_data(inp_field))
opntxt_btn.grid(row=3, column=1, pady=s_padding, padx=s_padding,sticky=NW)

embedtxt_btn = Button(master=inpFrame, text="Embed text into image", activebackground=lighter_BG, font=btn_font_tuple, relief=RAISED, foreground=lable_text_color, background=darker_BG, command=lambda: commands.create_image(inp_field,key,enc_strictness))
embedtxt_btn.grid(row=3, column=1, pady=s_padding, padx=s_padding,sticky=NE)

# ---- End of Input Frame ---- #

# Frame for extracting operations
extFrame = Frame(master=root,background=BACKGROUND)
extFrame.pack(side=TOP,anchor=N)

ext_title_label = Label(master=extFrame,text="Extract text from image :",font=header_font_tuple2,background=BACKGROUND,foreground=lable_text_color)
ext_title_label.grid(row=0,column=1,pady=xs_padding,padx=xs_padding,sticky=N)

ext_label = Label(master=extFrame,text="Extracted text :",font=label_font_tuple,background=BACKGROUND,foreground=lable_text_color)
ext_label.grid(row=1,column=0,pady=s_padding,padx=s_padding,sticky=N,ipady=m_padding)
ext_field = Text(master=extFrame,state=DISABLED,insertbackground=green_Tcolor,font=txt_font_tuple, foreground=green_Tcolor, background=darker_BG, height=12, width=115)
ext_field.grid(row=1,column=1,padx=s_padding,pady=s_padding,sticky='N')

opnimg_btn = Button(master=extFrame, text="Open image file to extract text", font=btn_font_tuple, foreground=lable_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.open_image(ext_field))
opnimg_btn.grid(row=2, column=1, pady=s_padding, padx=s_padding, sticky=N)

savetxt_btn = Button(master=extFrame, text="Save extracted text to a file", font=btn_font_tuple, foreground=lable_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.save_txt_file(ext_field))
savetxt_btn.grid(row=2, column=1, pady=s_padding, padx=s_padding, sticky=NW)

copyext_btn = Button(master=extFrame, text="Copy extracted text to clipboard", font=btn_font_tuple, foreground=lable_text_color, background=darker_BG, relief=RAISED, command=lambda : commands.copy_ext(ext_field,root))
copyext_btn.grid(row=2, column=1, pady=s_padding, padx=s_padding, sticky=NE)
# ---- End of Extracting frame ---- #

root.mainloop()