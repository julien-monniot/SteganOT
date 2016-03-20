# This module will contain the cipher / decipher algos and
from BitmapReader import BitmapReader
import copy
import math
import sys

def cipher_lsb_txt(input_file, carrier_file, output_file, n_bits):
    # Cipher lsb mode
    """
    Cipher a text into an image (LSB)
    :param input_file: file containing text to hide
    :param carrier_file: image in which the text will be hidden
    :param output_file: output image with hidden text included
    :return: True if ok, False in case of problem (eg. plain text too long...)
    """

    # Open input file and extract bytes:
    try:
        in_f = open(input_file, "rb")
        input_bytes = bytearray(in_f.read())
    except IOError as e:
        print("## ERROR : Input file couldn't be openned for reading")
        exit(1)
    in_f.close()
    input_length = len(input_bytes)

    #print("# Input text is :")
    #print(input_bytes)
    #print("# Length of text is "+str(input_length)+" bytes / "+str(input_length*8)+" bits.")

    # Check whether carrier file is big enough to store input file (assuming we are working with bitmaps)
    bitmap_reader = BitmapReader(carrier_file)
    pixels = bitmap_reader.get_pixel_array()
    if len(pixels) < (input_length * 8 + 1):    # +1 for size of message on 8 bits
        print("## ERROR : Plain text is too long ("+str(input_length*8)+" bits) for image carrier ("+str(len(pixels))+" bytes). ##\n### EXITING ###")
        return False

    # Create list of all bits (not bytes) to hide in image
    input_bits = []

    #print('Input length in byte '+format(input_length, '08b'))

    for ind in range(0, input_length):
        bits = format(input_bytes[ind], '08b')
        input_bits += bits

    print("# "+str(len(input_bits))+" bits will be written to carrier image.")
    
    # Add a stopping character
    input_bits += format(0, '08b')

    bit_mask = int(math.pow(2, n_bits) - 1)

    # Copy bits in pixels
    for ind in range(0, len(input_bits), 1):
        pixels[ind][0] = (pixels[ind][0] & ~bit_mask)
        for step in range(ind, ind + n_bits):
            i = step - ind
            if step < len(input_bits):
                pixels[ind][0] |= int(input_bits[step]) << (n_bits - 1 - i)


    #print("Copy OK")

    # Push back pixels and save bmp
    bitmap_reader.set_pixel_array(pixels)
    bitmap_reader.save_bitmap(output_file)
    print("# Cipher DONE (written to file "+output_file+")")
    return True


def decipher_lsb_txt(input_file, output_file, n_bits):
    """
    Decipher a text hidden in an image
    :param input_file: file within which is hidden the text
    :param output_file: file to which will be written deciphered text
    :return:True or False depending on success of deciphering
    """

    # Read pixel array from input image
    bitmap_reader = BitmapReader(input_file)
    pixels = bitmap_reader.get_pixel_array()

    # Decipher, from 8 first bytes to end of message
    output = open(output_file, "wb")
    text = ""
    for ind in range(0, sys.maxsize, n_bits):
        binary_pixel = format(pixels[ind][0], "08b")
        text += binary_pixel[(len(binary_pixel) -n_bits):]
        if len(text) % 8 == 0:
            if text == format(0, '08b'):    # Detect stopping character
                break
            out = int(text, 2).to_bytes(1, 'little')
            output.write(out)
            text = ""

    print("# Decipher DONE (written to file "+output_file+")")
    output.close()



