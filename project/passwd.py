#!/usr/bin/python
import base64
import sys
import random
import string

def id_generator(size=6, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))

def pass_generator(rand_string):
		tmpStr = base64.b64encode(rand_string)
		passStr = ""
		for c in tmpStr:
				passStr += chr(ord(c) + 1)
		return passStr


if __name__ == "__main__":
		password = id_generator()
		print password
		print pass_generator(password)