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

    if len(pixels) < (input_length * 8 + 1):    # +1 for size of message on 8 bits
        return False                         # Not enough space in pixel array to store data

    # Create list of all bits to hide in image
    input_bits = []
    # first add number of bytes in message
    input_bits += format(input_length, '08b')

    for ind in range(0, input_length):
        bits = format(input_bytes[ind], '08b')
        input_bits += bits

    print("Input bits : ")
    print(input_bits)

    # Copy bits in pixels
    print(len(input_bits))
    for ind in range(0, len(input_bits)):
        #print("Before : "+str(pixels[ind]))
        pixels[ind][0] ^= int(input_bits[ind])
        #print("After : "+str(pixels[ind]))

    print("New pixels : ")
    print(pixels[:12])
    print("Old pixels : ")
    print(old_pixels[:12])

    # Push backp pixels and save bmp
    bitmap_reader.set_pixel_array(pixels)
    bitmap_reader.save_bitmap(output_file)
    return True
