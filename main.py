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

        > length tuple interpretation: DEPRECATED!! GOTTA UPDATE DOCS
            (a,0,b) --> length = (2**a)-b

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
            save the extracted message to a .txt file (ask the name of file in prompt)
            read the text file and store the content of file as message.
"""
from PIL import Image
from tkinter import Tk
import PIL
import random
import img_utils
import utils

# GUI using tkinter will be created here

if __name__ == '__main__':
    op = int(input("1. Hide message in Image\n2. Extract message from Image: "))
    match op:
        case 1:
            enc_strct = (0,0,0)
            t = input("Enter text: ")
            key = [random.randint(1,200) for x in range(10)]
            print(len(t))
            kc = int(input("do you want to enter key manually? 1 for yes. 2 for no: "))
            if kc==1:
                key = list(input("Enter the key"))
                key = [ord(x) for x in key]
                enc_strct = (1,0,0)
                print(key)

            print(key)
            img = img_utils.hide_data(t, key,enc_strct)
            rname = "".join([chr(random.randint(97,120)) for x in range(5)])
            img.save(f'{rname}.png','png')
            # ----------------------------------------- #
            print("opening created image: ")
            img = Image.open(f'{rname}.png','r')
            img_len = img.size[0]
            ti_len = img_len - 1
            map_to_pixel = {
                'txtlen': (0, 0),
                'txtco-ord': (0, ti_len),
                'keylen': (ti_len, 0),
                'keyco-ord': (ti_len, ti_len),
                'encstrict': ((0, 1), (1, 0))
            }
            try:
                # etext = img_utils.extract_data(img)
                text = img_utils.extract_data(img)
                enc_strict = img.getpixel(map_to_pixel['encstrict'][0])
                if enc_strict[0] == 0:
                    print("Extracted text is:\n")
                    print(text)
                else:
                    print("Looks like you have to enter the key to get the data")
                    key = list(input("Enter the key: "))
                    key = [ord(x) for x in key]
                    print(key)
                    text = utils.deciph(text, key)
                    if enc_strict[1] == 1 and text.split(" ")[0] == "PicIt":
                        print("Extracted text is:\n")
                        print(text)
                    else:
                        pass

                    if enc_strict[1] == 0:
                        print("Extracted text is:\n")
                        print(text)

            except ValueError as e:
                print(e.args[0])
        case 2:
            i = input("Enter the name of image: ")
            img = Image.open(i,'r')
            img_len = img.size[0]
            ti_len = img_len-1
            map_to_pixel = {
                'txtlen': (0, 0),
                'txtco-ord': (0, ti_len),
                'keylen': (ti_len, 0),
                'keyco-ord': (ti_len, ti_len),
                'encstrict': ((0, 1), (1, 0))
            }
            try:
                # etext = img_utils.extract_data(img)
                text = img_utils.extract_data(img)
                enc_strict = img.getpixel(map_to_pixel['encstrict'][0])
                if enc_strict[0] == 0:
                    print("Extracted text is:\n")
                    print(text)
                else:
                    print("Looks like you have to enter the key to get the data")
                    key = list(input("Enter the key: "))
                    key = [ord(x) for x in key]
                    text = utils.deciph(text,key)
                    if enc_strict[1]==1 and text.split(" ")[0] == "PicIt":
                        print("Extracted text is:\n")
                        print(text)
                    else:
                        pass

                    if enc_strict[1]==0:
                        print("Extracted text is:\n")
                        print(text)

            except ValueError as e:
                print(e.args[0])
