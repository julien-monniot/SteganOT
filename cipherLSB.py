# This module will contain the cipher / decipher algos and


def cipher_lsb_txt(input_file, carrier_file, output_file):
    # Cipher lsb mode

    print("# In cipher lsb text wrapper with parameters :"
          "\n\t-Input file : "+input_file+"\n\t-Carrier Image : "+carrier_file+"\n\t-Output File : "+output_file)


    ### USEFUL (?) STUFFS (FOR LATER USE) ###
    # Open input and carrier file :
    in_f = open(input_file, "rb")
    ca_f = open(carrier_file, "rb")

    # Reading
    try:
        byte = in_f.read(1)
        while byte != "":
            # Do stuff with byte.
            byte = in_f.read(1)
    finally:
        in_f.close()

    pass