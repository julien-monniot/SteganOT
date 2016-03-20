#!/bin/python3.5

from subprocess import run, Popen

if __name__ == "__main__":

    print("# DEMO #")

    stegano = "./Steganogra.py"
    eog = "eog"
    cat = "cat"

    number_of_bits = "1"

    # Cipher
    input_text = "clear_text_short.txt"
    carrier_img = "lena.bmp"
    output_img = "lena_cipher_short.bmp"

    # Decipher
    input_img = output_img
    output_text = "decipher_text_short.txt"

    cmd1_c = ["./Steganogra.py", "-m", "cip", "-i", input_text, "-c", carrier_img, "-o", output_img, "-b", number_of_bits]
    cmd2_dc = ["./Steganogra.py", "-m", "decip", "-i", input_img, "-o", output_text,"-b", number_of_bits]

    #### Cipher short text in LSB of pixels (lena.bmp) ####
    print("## Task 1 : Cipher short text - 1 bit/byte")
    print("## Cipher operation : ")
    print("## Command : ", end="")
    print(cmd1_c)

    run(["cat", input_text])
    proc = Popen(["eog", carrier_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to run cipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd1_c)
    print(result.stdout)

    input("\n\t--- Press Enter to display output_img. ---\n")

    proc = Popen(["eog", output_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to continue. ---\n")

    print("## Decipher operation : ")
    print("## Command : ", end="")
    print(cmd2_dc)

    input("\n\t--- Press Enter to run decipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd2_dc)
    print(result.stdout)

    print("# Deciphered text : ")
    run(["cat", output_text])

    input("\n\t--- Press Enter to start next task ---\n")

    #### Cipher long text in LSB of pixels (lena.bmp) ####

    input_text = "clear_text_long.txt"
    output_img = "lena_cipher_long.bmp"

    # Decipher
    input_img = output_img
    output_text = "decipher_text_long.txt"

    cmd1_c = ["./Steganogra.py", "-m", "cip", "-i", input_text, "-c", carrier_img, "-o", output_img, "-b", number_of_bits]
    cmd2_dc = ["./Steganogra.py", "-m", "decip", "-i", input_img, "-o", output_text,"-b", number_of_bits]

    print("## Task 2 : Cipher long text - 1 bit/byte")
    print("## Cipher operation : ")
    print("## Command : ", end="")
    print(cmd1_c)

    run(["cat", input_text])
    proc = Popen(["eog", carrier_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to run cipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd1_c)
    print(result.stdout)

    input("\n\t--- Press Enter to display output_img. ---\n")

    proc = Popen(["eog", output_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to continue. ---\n")

    print("## Decipher operation : ")
    print("## Command : ", end="")
    print(cmd2_dc)

    input("\n\t--- Press Enter to run decipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd2_dc)
    print(result.stdout)

    print("# Deciphered text : ")
    run(["cat", output_text])

    input("\n\t--- Press Enter to start next task ---\n")

    #### Cipher long text in LSB of pixels (lena.bmp) - 2bits/byte ####

    number_of_bits = "2"
    output_img = "lena_cipher_long2.bmp"

    # Decipher
    input_img = output_img
    output_text = "decipher_text_long2.txt"

    cmd1_c = ["./Steganogra.py", "-m", "cip", "-i", input_text, "-c", carrier_img, "-o", output_img, "-b", number_of_bits]
    cmd2_dc = ["./Steganogra.py", "-m", "decip", "-i", input_img, "-o", output_text,"-b", number_of_bits]

    print("## Task 3 : Cipher long text - 2 bit/byte")
    print("## Cipher operation : ")
    print("## Command : ", end="")
    print(cmd1_c)

    run(["cat", input_text])
    proc = Popen(["eog", carrier_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to run cipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd1_c)
    print(result.stdout)

    input("\n\t--- Press Enter to display output_img. ---\n")

    proc = Popen(["eog", output_img], stdin=None, stdout=None, stderr=None, close_fds=True)

    input("\n\t--- Press Enter to continue. ---\n")

    print("## Decipher operation : ")
    print("## Command : ", end="")
    print(cmd2_dc)

    input("\n\t--- Press Enter to run decipher. ---\n")

    print("## RUN :: ")
    result = run(args=cmd2_dc)
    print(result.stdout)

    print("# Deciphered text : ")
    run(["cat", output_text])

    input("\n\t--- Press Enter to start next task ---\n")