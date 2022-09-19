import binary_conversion
import random
import math
import json
import os

bullet_char = "\u2022"

def generate_ascii_values():
    return [chr(num) for num in range(1, 256)]

# ----------------------------------- #
ascii_values = generate_ascii_values()
# ----------------------------------- #

def randint(a,b):
    return random.randint(a,b)

def random_KeyGen(keylen:int):
    return [random.randint(1, 250) for x in range(keylen)]

def ciph(text: str, key: list) -> str:
    """
    Takes text and key, encrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : encrypted text
    """
    ciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) + key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - ((ascii_index * -1)%len(ascii_values))
        ciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return ciphered_text


def deciph(text: str, key: list) -> str:
    """
    Takes text and key, decrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : decrypted text
    """
    deciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) - key[i]
        if ascii_index >= len(ascii_values):
            ascii_index = ascii_index % len(ascii_values)
        elif ascii_index < 0:
            ascii_index = len(ascii_values) - ((ascii_index * -1)%len(ascii_values))
        deciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return deciphered_text

def dump_json(object, filename):
    with open(filename, "w") as dump:
        json.dump(object, dump, indent=4)

def load_json(filename):
    with open(filename, "r") as load:
        return json.load(load)

def oneD_to_2DList(list1D:list,size:int,func=None) -> list:
    """
    Takes a 1-D list and converts it into 2-D list where `size` is the size of each list in 2nd dimension

    :param list1D: One dimenstional list
    :param size: size of each list in 2nd dimension
    :param func: (Optional) Function to execute on each list in 2nd dimension
    :return: 2-D List
    """
    if not func :
        def f(a):
            return a
        func = f

    return [func(list1D[i:i+size]) for i in range(0,len(list1D),size)]

def get_dimension(num):
    """
    This is to use to get the dimension for image size, suppose if `num` pixels are required to store the metadata + data
    then this function gives the minimum dimension required for a square image.

    :param num: number of pixels required
    :return: int: minimum dimension required for a square image. which on squaring is just greater than given `num`

    """
    return math.ceil(num**(1/2))

def get_exponent(num,base=2):
    """
    takes a number and base
    returns a smallest int x , such that base ** x > num

    :param num: integer number
    :param base: base for the exponent (default value is 2)
    :return: smallest int x, such that base ** x > num
    """
    return math.ceil(math.log(num,base))

def get_tuple_from_size(num:int) -> tuple:
    """
    takes a number `num` and creates it's 24-bit binary, then slices the 24-bit into three 8-bit binaries
    converts these 3 binaries to int and returns the tuple of size 3

    :param num: integer number
    :return: tuple which represents the `num` in binary when all 3 elements of tuple are concatenated
    """
    bnum = binary_conversion.decimal_to_binary(num)
    bnum = f"{'0'*(24-len(bnum))}{bnum}"
    btup = [bnum[i:8+i] for i in range(0,len(bnum),8)]
    return tuple([binary_conversion.binary_to_decimal(x) for x in btup])

def get_size_from_tuple(tup:tuple) -> int:
    """
    takes the tuple of size 3 and converts each int element of tuple to 8-bit binaries, concatenates these three binaries to get 24-bit binary
    converts this 24-bit binary to integer and returns it

    :param tup: tuple of size 3, containing integers
    :return: int : which is represented by the tuple when all elements are converted to 8-bit binaries and concatenated to get 24-bit binary and then converted to an integer
    """
    btup = [binary_conversion.decimal_to_binary(x) for x in tup]
    b24bit = "".join(btup)
    return binary_conversion.binary_to_decimal(b24bit)

def get_key(strval:str):
    """
    takes string, tries to decode using json, converts to list
    checks if all the elements in the list are integers or not, if not, then tries to convert the characters to integer using ord().
    if it fails to so.. then entire string will be taken as string key, and each character of this string will be converted to integer and returns as list

    :param strval:
    :return: list
    """
    k = []
    try:
        k = json.loads(strval)
        if type(k) != type(list()):
            raise json.decoder.JSONDecodeError("not int")
        elif any(type(x) != type(int()) for x in k):
            raise json.decoder.JSONDecodeError("not int")
    except json.decoder.JSONDecodeError:
        k = [ord(x) for x in strval]
    return k
