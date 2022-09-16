def binary_to_decimal(bin_str:str) -> int:
	"""
		takes a binary value as a string, converts binary to int and returns int.

		:return: int converted from given binary
	"""
	bin_str = str(bin_str)
	temp = bin_str[::-1]
	if all(x in "01" for x in bin_str):
		n=0
		for i in range(len(temp)):
			n += int(temp[i])*(2**i)
		return n
	else:
		raise TypeError(f"Invalid value for binary string \"{bin_str}\"")

def decimal_to_binary(num:int) -> str:
	"""
		:return:  8-bit binary as string if num is in range of 2^8 else the length of string might be higher depending on value.
	"""
	if num == 0:
		return "0"
	else:
		bstr = ""
		while num!=0:
			if num%2==0:
				bstr = f"0{bstr}"
			else:
				bstr = f"1{bstr}"
			num = int(num/2)
		if len(bstr)<8:
			bstr = f"{'0'*(8-len(bstr))}{bstr}"
		return bstr

def binary_to_text(bin_str:str):
	blist = bin_str.split(" ")
	text = ""
	for bnum in blist:
		text += chr(binary_to_decimal(bnum))
	return text


def text_to_binary(txt:str):
	bstr = ""
	for char in txt:
		bstr += f"{decimal_to_binary(ord(char))} "
	return bstr

if __name__ == '__main__':
    pass
