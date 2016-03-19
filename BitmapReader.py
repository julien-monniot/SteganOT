# BITMAP reader utility

class BitmapReader:

    def __init__(self, carrier_file):
        # Open the carrier file :
        try:
            ca_f = open(carrier_file, "rb")
            carrier_bytes = bytearray(ca_f.read())
        except IOError as e:
            print("## ERROR : Carrier file couldn't be openned for reading")
            exit(1)
        ca_f.close()

        self.bitmap_array = carrier_bytes
        self.header_dict = self.__extract_header()
        self.dib_dict = self.__extract_dib()
        self.pixel_array = self.__extract_pixels()

    def get_header(self):
        """
        :return: Header dictionary generated using __extract_header
        """
        return self.header_dict

    def get_dib_header(self):
        """
        :return: Header dictionary generated using __extract_dib
        """
        return self.dib_dict

    def has_compression(self):
        """
        This method checks whether the bitmap image uses some sort of compression or not.
        :return: True if compression is in use, False otherwise
        """
        if self.dib_dict['compression'] not in [0, 11]:    # https://en.wikipedia.org/wiki/BMP_file_format
            return True
        else:
            return False

    def __extract_header(self):
        """
        Reads file header.
        :return: Dictionary containing the hex string corresponding to every field in bitmap header
        """
        header_dict = dict()
        header_dict['file_format'] = int.from_bytes(self.bitmap_array[0:2], byteorder='little', signed=False)
        header_dict['file_size'] = int.from_bytes(self.bitmap_array[2:6], byteorder='little', signed=False)
        header_dict['reserved_bytes'] = int.from_bytes(self.bitmap_array[6:10], byteorder='little', signed=False)
        header_dict['pixel_array_offset'] = int.from_bytes(self.bitmap_array[10:14], byteorder='little', signed=False)

        return header_dict

    def __extract_dib(self):
        """
        Read DIB header (right after file header).git commit (
        WARNING : DIB headers may vary according to the bitmap version (thannnnnnkkssss Microsoft). This implementation
        only works with BITMAPINFOHEADER (and later ?)
        :return: Dictionary containing the hex string corresponding to every field in bitmap dib header
        """
        dib_dict = dict()
        dib_dict['dib_size'] = int.from_bytes(self.bitmap_array[14:18], byteorder='little', signed=False)
        dib_dict['bitmap_width'] = int.from_bytes(self.bitmap_array[18:22], byteorder='little', signed=False)
        dib_dict['bitmap_height'] = int.from_bytes(self.bitmap_array[22:26], byteorder='little', signed=False)
        dib_dict['color_planes'] = int.from_bytes(self.bitmap_array[26:28], byteorder='little', signed=False)
        dib_dict['bits_per_pixel'] = int.from_bytes(self.bitmap_array[28:30], byteorder='little', signed=False)
        dib_dict['compression'] = int.from_bytes(self.bitmap_array[30:34], byteorder='little', signed=False)
        dib_dict['image_size'] = int.from_bytes(self.bitmap_array[34:38], byteorder='little', signed=False)   # can be a dummy 0 if no compression is used.
        # Fields after that are not taken into account for the moment as we shall only need the above data

        return dib_dict

    def __extract_pixels(self):
        """
        Read pixel array from bitmap and place every pixel into a list (so the pixel array is stripped from its
        potential padding)
        :return: list of all the pixels.
        """

        # 1) Compute size of pixel_array : it is equal to (img_width * (pixel_size/8) + padding) * img_height
        img_width = self.dib_dict['bitmap_width']
        img_height = self.dib_dict['bitmap_height']
        pixel_size = self.dib_dict['bits_per_pixel']  # how many bits are needed for 1 pixel in the array (/8 for bytes)
        padding = 4 - (img_width % 4)  # 4-bytes padding
        line_width = (img_width * int(pixel_size/8) + padding)
        #print("Total line width = "+str(line_width))
        pixel_array_size = line_width * img_height
        #print("Image size is : "+str(pixel_array_size))

        # 2) Extract raw pixel array (part of the bytearray, including padding bytes)
        pixel_array_off = self.header_dict['pixel_array_offset']
        raw_pixel_array = self.bitmap_array[pixel_array_off:pixel_array_off + pixel_array_size]
        #print("Raw pixel array starts at "+hex(pixel_array_off)+" and ends at "+hex(pixel_array_off+pixel_array_size))
        #print(raw_pixel_array)

        # 3) Now, extract a list of pixels from the raw pixel array, excluding 4-bytes padding.
        pixel_array = []
        for line_start in range(0, pixel_array_size, line_width):    # loop on every line of the pixel array.
            c_line = raw_pixel_array[line_start:(line_start+line_width)]    # temp of the current line
            # print("# Current line : "+str(c_line))
            # print("# Line len : "+str(len(c_line)))
            for pixel in range(0, (line_width - (line_width-img_width)), int(pixel_size/8)):
                pixel_array.append(c_line[pixel:pixel+int(pixel_size/8)])

        return pixel_array

    def get_pixel_array(self):
        """
        :return: PixelArray of the bmp file, as a list of bytearray. Each bytearray encodes 1 pixel. Padding removed.
        """
        pixel_array = self.pixel_array
        return pixel_array

    def set_pixel_array(self, pixel_array):
        """
        Give a modified pixel array to this methods (with altered bytes in it) and it will rewrite it into the bitmap
        array, including padding.
        :param pixel_array: A list ob bytearrays representing the pixels.
        :return: True is set succed or false if not
        """

        # 1) Check if returned input pixel array has the same size as original pixel array

        img_width = self.dib_dict['bitmap_width']
        img_height = self.dib_dict['bitmap_height']
        pixel_size = self.dib_dict['bits_per_pixel']  # how many bits are needed for 1 pixel in the array (/8 for bytes)
        line_width_no_pad = (img_width * int(pixel_size/8))  # silent error here maybe (Grayscale vs RVB)
        pixel_array_size = line_width_no_pad * img_height

        if not pixel_array_size == len(pixel_array):
            # The given pixel array size doesn't have the right size
            return False

        #print("New pixel array :")
        #[print(hex(pixel_array[i][0])+" ", end="") for i in range(0, len(pixel_array))]
        #print()

        # 2) Add padding to input pixel array, according to img_width * (pixel_size/8)
        if img_width % 4 != 0:
            padding = 4 - (img_width % 4)  # 4-bytes padding
        else:
            padding = 0
        #print("Will add "+str(padding)+" bytes of padding to each line")
        # empty bytearray() that will take the place of the 'raw_byte_array' from __extract_pixel_array
        padded_array = bytearray()

        # Loop on line beginning index for no-padding pixel array.

        #print('Len(pixel_array): '+str(len(pixel_array)))
        #print('Lenght of line (no pad) : '+str(line_width_no_pad))

        for line_start in range(0, len(pixel_array), line_width_no_pad):
            new_line = bytearray()

            #print("Line start : "+str(line_start))
            for i in range(0, line_width_no_pad):
                new_line += pixel_array[line_start+i]

            # append enough byte of padding to the line
            for i in range(0, padding):
                new_line.append(0x00)
            padded_array += new_line


        #print("Padded array :")
        #print(padded_array)

        # 3) Replace old pixel array with new pixel array
        pixel_array_off = self.header_dict['pixel_array_offset']
        # self.bitmap_array[pixel_array_off:pixel_array_off + len(padded_array)] = padded_array
        for i in range(pixel_array_off, pixel_array_off + len(padded_array)):
            self.bitmap_array[i] = padded_array[i-pixel_array_off]
        return True

    def save_bitmap(self, out_filename):
        """
        Save current bitmap_array as a bitmap image file.
        :param out_filename Name of the output file ('.bmp' will be appended by this method)
        :return:
        """
        f = open(out_filename, "wb")
        f.write(self.bitmap_array)

    def get_bitmap_array(self):
        array = self.bitmap_array
        return array


