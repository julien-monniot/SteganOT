#!/usr/bin/python3

# Image Steganography test application #

import sys
import argparse
from cipherLSB import cipher_lsb_txt, decipher_lsb_txt

# Naughty, dirty globals :

ERR_STR = "## ERROR : "
modes = ['cip', 'decip']
algos = ['lsb-txt', 'lsb-img', 'lsb-dct-img']
bits = ['1', '2', '4', '8']
default_output = "steganOUT"

def arg_parser(argv):

    parser = argparse.ArgumentParser(description='This program is a steganography tool. \nIt can be used to hide a '
                                                 'text or an image into an image carrier.',
                                     epilog='Authors : L.A-L. and J.M.')

    parser.add_argument('-m',
                        help='[Mandatory] Sets program for ciphering or deciphering.',
                        choices=modes,
                        required=True)
    parser.add_argument('-i',
                        metavar='<input file>',
                        help='[Mandatory] Input data to be hidden in carrier (Default should be '
                        '\na text file, and can be a image if mode (-m) set to "lsb-img"), '
                        '\nor image from which you wish to retrieve data',
                        required=True)
    parser.add_argument('-c',
                        metavar='<carrier image>',
                        help='[Optional] Image that will be used as carrier to hide input data (cipher mode only).')
    parser.add_argument('-o',
                        metavar='<output file>',
                        default=default_output,
                        help='[Optional] Name of the output file (default = "steganOUT"')
    parser.add_argument('-a',
                        default=algos[0],
                        help="Algo used to hide information.",
                        choices=algos
                        )
    parser.add_argument('-b',
                        default=bits[0],
                        help="[Optional] Number of bits used to store information per byte",
                        choices=bits
                        )

    return vars(parser.parse_args(argv))


if __name__ == "__main__":

    # Parse program arguments.
    parsedArguments = arg_parser(sys.argv[1:])

    if parsedArguments['m'] == 'cip':

        # For cipher operation, we'll need an input image (mandatory in program options), a carrier image, and
        # optionally an output file name (-o) and an algo (default is lsb-txt)

        if parsedArguments['c'] is None:
            print(ERR_STR+"No carrier image provided. Exiting now.")
            exit(1)

        # Call appropriate module
        if parsedArguments['a'] == algos[0]:
            cipher_lsb_txt(parsedArguments['i'], parsedArguments['c'], parsedArguments['o'], int(parsedArguments['b']))
        elif parsedArguments['a'] == algos[1]:
            # Will make a call to a cipher wrapper called cipherLSB_img
            pass
        elif parsedArguments['a'] == algos[2]:
            # Will make a call to a cipher wrapper called cipherLSB_DCT
            pass

    elif parsedArguments['m'] == 'decip':

        # Call appropriate module
        if parsedArguments['a'] == algos[0]:
            decipher_lsb_txt(parsedArguments['i'], parsedArguments['o'], int(parsedArguments['b']))
        elif parsedArguments['a'] == algos[1]:
            # Will make a call to a cipher wrapper called cipherLSB_img
            pass
        elif parsedArguments['a'] == algos[2]:
            # Will make a call to a cipher wrapper called cipherLSB_DCT
            pass

