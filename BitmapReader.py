# BITMAP reader utility


class BitmapReader:

    def __init__(self, byte_bitmap_array):
        self.bitmap_array = byte_bitmap_array
        self.header_dict = self.__extract_header()

    def get_header(self):
        """
        :return: Header dictionary generated using __extract_header
        """
        return self.header_dict

    def __extract_header(self):
        """
        Reads header file.
        :return: Dictionary containing the hex string corresponding to every field in bitmap header
        """
        header_dict = dict()

        header_dict['file_format'] = hex(int.from_bytes(self.bitmap_array[0:2], byteorder='little', signed=False))
        header_dict['file_size'] = hex(int.from_bytes(self.bitmap_array[2:6], byteorder='little', signed=False))
        header_dict['reserved_bytes'] = hex(int.from_bytes(self.bitmap_array[6:10], byteorder='little', signed=False))
        header_dict['img_offset'] = hex(int.from_bytes(self.bitmap_array[10:14], byteorder='little', signed=False))

        return header_dict

    def get_pixel_array(self):
        """
        :return: PixelArray of the bmp file (found thanks to offset in header)
        """
        pass

    def get_bitmap_array(self):
        return self.bitmap_array
