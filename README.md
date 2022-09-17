# PicIt
### A GUI Tool which embeds the text in Image and extracts the text from Image. Built using Pillow (PIL), Python
***
### Project inspired by the concept of Steganography

## Core Functionality:
* This tool embeds text into images and extracts text from created images
  * Text is encrypted before it gets embed into an image. 
  * The ascii values of the text characters are distributed among the pixels as (r,g,b) values
***
* Functionalities:
    * Pixel requirement:  
        * 2 pixels for message length and starting co-ordinates  
        * 2 pixels for encryption key length and starting co-ordinates  
        * 2 pixel to store the strictness of encryption key (same data in both pixels)  
        * Total : 6  
        * Automatically calculate the amount of pixels required for the message and create it  
  
    * Pixel mapping
      * (0,0) - length of text  
      * (0,n) - Initial co-ordinates of text  
      * (n,0) - length of key  
      * (n,n) - Initial co-ordinates of key  
      * (0,2) and (2,0) - strictness of encryption  
      * where n is the length of size of image (square image)

    * If Encryption key is to be entered manually, then there should be two cases:
      * receiving user will have to enter correct key to extract the data
      * prefix and suffix "PicIt" to the plain message while hiding, if the entered key is correct then first word and last word should be decrypted to "PicIt", this is how we know that encryption key is correct.
      * message will simply decrypt using given key, if key is wrong then user will see garbage text, else readable text

    * Encryption strictness tuple interpretation:
      * (0,0,0) - Key is randomly generated, extract the key from image and send the data
      * (1,0,0) - Key is manually added, user should provide the key, regardless of key being correct or not, data will be decrypted and sent
      * (1,1,0) - Key is manually added, user should provide only the correct key, or else no data will be provided to user

    * Storing of lengths of key, text:
      * let's say `len` is the length here, convert `len` into 24-bit binary representation,
      * slice this 24-bit binary string into three 8-bit binary strings
      * convert this three 8-bit binaries into int and store in a tuple as (a,b,c)

    * length tuple interpretation:
      * (a,b,c) - convert a,b,c to binary 8-bit representation
      * concatenate all three 8-bit binary string, we get a 24-bit binary string
      * convert this 24-bit binary string to int, now we have the length.

    * Co-ordinate tuple interpretation:
      * (a,n,b) interpreted as (a,b)
    * Text co-ordinate tuple will hold random number 'n' in middle element.

    * Key co-ordinate tuple will hold Orientation of traversal in middle element:
        * 0 - vertical
        * 1 - horizontal

* Features:
    * Manually enter encryption key?
        * Yes : only encrypted text will be stored, receiving user will have to enter key manually to extract message.
        * No : encryption key will be randomly generated and will be stored in picture with metadata
    * File for messages:
        * Save the extracted message to a .txt file 
        * Read the text file and store the content of file as message.