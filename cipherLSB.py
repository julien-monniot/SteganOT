# This module will contain the cipher / decipher algos and
from BitmapReader import BitmapReader

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
    input_bytes[0] ^= 1
    print(input_bytes)
    print(input_length)

    # Open the carrier file :
    try:
        ca_f = open(carrier_file, "rb")
        carrier_bytes = bytearray(ca_f.read())
    except IOError as e:
        print("## ERROR : Carrier file couldn't be openned for reading")
        exit(1)

    ca_f.close()

    # Check whether carrier file is big enough to store input file (assuming we are working with bitmaps)
    bitmap_reader = BitmapReader(carrier_bytes)
    print(bitmap_reader.get_header())
    print(bitmap_reader.get_dib_header())       # Warning, still specific latest bitmap versionS
    print(bitmap_reader.has_compression())
    print(bitmap_reader.get_pixel_array())

'''
        while byte != '':
            # Do stuff with byte.
            byte = in_f.read(1)
            print(byte)
'''