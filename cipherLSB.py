# This module will contain the cipher / decipher algos and
from BitmapReader import BitmapReader
import copy


def cipher_lsb_txt(input_file, carrier_file, output_file):
    # Cipher lsb mode

    print("# In cipher lsb text wrapper with parameters :"
          "\n\t-Input file : " + input_file + "\n\t-Carrier Image : " + carrier_file + "\n\t-Output File : " + output_file)

    # Open input file :
    try:
        in_f = open(input_file, "rb")
        input_bytes = bytearray(in_f.read())
    except IOError as e:
        print("## ERROR : Input file couldn't be openned for reading")
        exit(1)

    in_f.close()

    input_length = len(input_bytes)

    # Now we have a byte array of our input file, elegantly named "input_bytes".
    print("Input text is :")
    print(input_bytes)
    print("The lenght (in bytes) is : "+str(input_length))

    # Check whether carrier file is big enough to store input file (assuming we are working with bitmaps)
    bitmap_reader = BitmapReader(carrier_file)
    pixels = bitmap_reader.get_pixel_array()
    old_pixels = copy.deepcopy(pixels)

    print("Lenght of pixel array = "+str(len(pixels)))
    if len(pixels) < (input_length * 8 + 1):    # +1 for size of message on 8 bits
        return False                         # Not enough space in pixel array to store data

    # Create list of all bits to hide in image
    input_bits = []
    # first add number of bytes in message
    input_bits += format(input_length, '08b')

    for ind in range(0, input_length):
        bits = format(input_bytes[ind], '08b')
        input_bits += bits

    print("Lenght of input bits array : "+str(len(input_bits)))

    # Copy bits in pixels
    for ind in range(0, len(input_bits)):
        pixels[ind][0] = (pixels[ind][0] & ~1) | int(input_bits[ind])

    print("Copy OK")

    # Push back pixels and save bmp
    bitmap_reader.set_pixel_array(pixels)
    bitmap_reader.save_bitmap(output_file)
    return True


def decipher_lsb_txt(input_file, output_file):
    """
    Decipher a text hidden in an image
    :param input_file: file within which is hidden the text
    :param output_file: file to which will be written deciphered text
    :return:True or False depending on success of deciphering
    """

    bitmap_reader = BitmapReader(input_file)
    pixels = bitmap_reader.get_pixel_array()
    size_bits = []
    for i in range(0, 8):
        print("Byte = "+hex(pixels[i][0]))
        binary_pixel = format(pixels[i][0], "08b")
        size_bits += binary_pixel[len(binary_pixel)-1]

    size = 0
    for bit in size_bits:
        size = (size << 1) | int(bit)

    print("The message to decipher is "+str(size)+" bytes long.")

    # Decipher, from 8 first bytes to end of message
    output = open(output_file, "wb")
    text = ""
    for ind in range(8, 8+(size*8)):
        binary_pixel = format(pixels[ind][0], "08b")
        text += binary_pixel[len(binary_pixel)-1]
        if len(text) % 8 == 0:
            print(text)
            out = int(text, 2).to_bytes(1, 'little')
            output.write(out)
            text = ""

    print("Deciphering OK")
    output.close()



