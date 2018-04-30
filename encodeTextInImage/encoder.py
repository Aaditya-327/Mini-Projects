import cv2
from pprint import pprint
import binascii
import numpy
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# Converting text to binary
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Converting binary to text
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

# F1: converting [0 0 0] value to hex string
rgb_hex = lambda x: "{:02x}{:02x}{:02x}".format(tuple(x)[0], tuple(x)[1], tuple(x)[2])

# F2: converting [0 0 0] to binary (F1)
hex_bin = lambda x: bin(int(rgb_hex(x)[1:], 16))[2:]

# Add required digit onto the RGB value
def changeRGBvaluebyData(rgb, data):
    # get rgb data from matrix unit
    input_as_RGB = rgb
    # print(input_as_RGB)
    # converting rgb to hex value
    in_hex_form = rgb_hex(input_as_RGB)
    # print(in_hex_form)
    # converying hex to binary form
    in_binary_form = text_to_bits(in_hex_form)
    # print(in_binary_form)
    # add replacement data on binary
    replacement = data
    in_binary_form = in_binary_form[:-2] + replacement
    # print(in_binary_form)
    # now converting bianry back to hex
    in_hex_form = text_from_bits(in_binary_form)
    # print(in_hex_form)
    # now converting hex value to RGB value (R, G, B)
    red, green, blue = tuple(int(in_hex_form[i:i+2], 16) for i in (0, 2 ,4))
    # print(red, green, blue)
    return list((red, green, blue))

def getlasttwodigit(rgb):
    # get rgb data from matrix unit
    input_as_RGB = rgb
    # print(input_as_RGB)
    # converting rgb to hex value
    in_hex_form = rgb_hex(input_as_RGB)
    # print(in_hex_form)
    # converying hex to binary form
    in_binary_form = text_to_bits(in_hex_form)
    return in_binary_form[-2:]

def getfirst48(image_matrix):
    string, sn = '', 0
    for row in im:
        for unit in row:
            sn += 2
            if sn == 50: break
            string += getlasttwodigit(list(unit))
        break
    return string

# change = changeRGBvaluebyData((70,90,182),'01')
# print(change)
# ret = getlasttwodigit(change)
# print(ret)

def textpassword2encodedbinary(text, password):
    # encoding text to encode by pw
    in_image = encode(password, text) #1
    # print(in_image)
    # converting encoded text to binary
    binary_encoded = text_to_bits(in_image) #1
    # alt method
    # binary_encoded = text_to_bits(text)
    # encode agreko length lai binary ma save gare 48 length ko
    length_of_digits = len(in_image)
    # alt method
    # length_of_digits = len(text)

    length_of_digits_format = str(length_of_digits).zfill(6)
    first48 = text_to_bits(length_of_digits_format)
    # what to put in image
    # first 48 lai text ma ani find katiota digit
    # 8+ tetiota digit lai chai to ascii ani decrypt
    total_text = first48 + binary_encoded
    return total_text

def encodedbinary2text(binary, password):
    binary = binary[8:]
    encoded_text = text_from_bits(binary)[5:]
    # print(encoded_text)
    decoded = decode(password, encoded_text)
    # print(decoded)
    # print(encoded_text)
    return decoded

# text = 'apple is a fruit is it not?'
# password = 'password12345'
# len48txt = textpassword2encodedbinary(text, password)
# door = encodedbinary2text(len48txt, password)
# print(door)

im = cv2.imread("filename.jpg")
first48 = getfirst48(im)

rgbvalue = [[changeRGBvaluebyData(i, '11') for i in row] for row in im]
rgbvalue3dmatrix = numpy.array(rgbvalue)
print(rgbvalue3dmatrix)
