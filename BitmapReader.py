# BITMAP reader utility


class BitmapReader:

    def __init__(self, byte_bitmap_array):
        self.bitmap_array = byte_bitmap_array
        self.header_dict = self.__extract_header()
        self.dib_dict = self.__extract_dib()

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
        if int(self.dib_dict['compression'], 16) not in [0, 11]:    # https://en.wikipedia.org/wiki/BMP_file_format
            return True
        else:
            return False

    def __extract_header(self):
        """
        Reads file header.
        :return: Dictionary containing the hex string corresponding to every field in bitmap header
        """
        header_dict = dict()
        header_dict['file_format'] = hex(int.from_bytes(self.bitmap_array[0:2], byteorder='little', signed=False))
        header_dict['file_size'] = hex(int.from_bytes(self.bitmap_array[2:6], byteorder='little', signed=False))
        header_dict['reserved_bytes'] = hex(int.from_bytes(self.bitmap_array[6:10], byteorder='little', signed=False))
        header_dict['pixel_array_offset'] = hex(int.from_bytes(self.bitmap_array[10:14], byteorder='little', signed=False))

        return header_dict

    def __extract_dib(self):
        """
        Read DIB header (right after file header).
        WARNING : DIB headers may vary according to the bitmap version (thannnnnnkkssss Microsoft). This implementation
        only works with BITMAPINFOHEADER (and later ?)
        :return: Dictionary containing the hex string corresponding to every field in bitmap dib header
        """
        dib_dict = dict()
        dib_dict['dib_size'] = hex(int.from_bytes(self.bitmap_array[14:18], byteorder='little', signed=False))
        dib_dict['bitmap_width'] = hex(int.from_bytes(self.bitmap_array[18:22], byteorder='little', signed=False))
        dib_dict['bitmap_height'] = hex(int.from_bytes(self.bitmap_array[22:26], byteorder='little', signed=False))
        dib_dict['color_planes'] = hex(int.from_bytes(self.bitmap_array[26:28], byteorder='little', signed=False))
        dib_dict['bits_per_pixel'] = hex(int.from_bytes(self.bitmap_array[28:30], byteorder='little', signed=False))
        dib_dict['compression'] = hex(int.from_bytes(self.bitmap_array[30:34], byteorder='little', signed=False))
        dib_dict['image_size'] = hex(int.from_bytes(self.bitmap_array[34:38], byteorder='little', signed=False))    # can be a dummy 0 if no compression is used.
        # Fields after that are not taken into account for the moment as we shall only need the above data

        return dib_dict

    def get_pixel_array(self):
        """
        :return: PixelArray of the bmp file (found thanks to offset in header)
        """
        pass

    def get_bitmap_array(self):
        return self.bitmap_array


