import os
import itertools

from enum import Enum, auto

from .option_file_data import (
    OF_BYTE_LENGTH,
    OF_BLOCK,
    OF_BLOCK_SIZE,
    OF_KEY,
)

from .club import Club

from .utils.common_functions import bytes_to_int, zero_fill_right_shift


class OptionFile:
    of_byte_length = OF_BYTE_LENGTH
    of_block = OF_BLOCK
    of_block_size = OF_BLOCK_SIZE
    of_key = OF_KEY

    def __init__(self, file_location):
        self.file_location = file_location
        self.data = bytearray()
        self.file_name = ""
        self.extension = ""
        self.game_type = None
        self.header_data = bytearray()

        self.read_option_file()

        self.set_clubs()

    def get_game_type(self, file_name):
        """
        Return game type from supplied filename string.
        """
        game_type_map = {
            "BESLES-54913P2K8OPT": GameType.ps2_pes,
        }
        return game_type_map.get(file_name)

    def read_option_file(self):
        """
        Decrypt supplied file and set OF data.
        """
        of_file = open(self.file_location, "rb")
        file_name,extension = os.path.basename(of_file.name).split('.')
        file_size = os.stat(of_file.name).st_size
        self.file_name = file_name
        self.extension = extension
        self.game_type = self.get_game_type(file_name)
        file_contents = bytearray(of_file.read())
        of_file.close()

        if self.extension == "psu":
            self.header_data, self.data = file_contents[:file_size - self.of_byte_length], file_contents[file_size - self.of_byte_length:]
        elif self.extension == "xps":
            self.header_data, self.data = file_contents[:file_size - self.of_byte_length -4], file_contents[file_size - self.of_byte_length-4:-4]
        else:
            self.data = file_contents
        self.decrypt()

        return True

    def save_option_file(self, file_location=None):
        """
        Save OF data to supplied file.
        """
        file_location = self.file_location = file_location or self.file_location

        #self.data[49] = 1
        #self.data[50] = 1
        #self.data[5938] = 1
        #self.data[5939] = 1

        self.encrypt()
        self.checksums()

        of_file = open(file_location, "wb")

        if self.extension == "psu":
            of_file.write(self.header_data)
            of_file.write(self.data)
        elif self.extension == "xps":
            of_file.write(self.header_data)
            of_file.write(self.data)
            of_file.write(0)
            of_file.write(0)
            of_file.write(0)
            of_file.write(0)
        else:
            of_file.write(self.data)
        
        of_file.close()

        self.decrypt()

        return True

    def decrypt(self):
        """
        Decrypt OF.
        """
        for i in range(1, 10):
            k = 0
            a = self.of_block[i]
            while True:
                if a + 4 > self.of_block[i] + self.of_block_size[i]:
                    break

                c = bytes_to_int(self.data, a)
                p = ((c - self.of_key[k]) + 0x7ab3684c) ^ 0x7ab3684c

                self.data[a] = p & 0x000000FF
                self.data[a + 1] = zero_fill_right_shift(p, 8) & 0x000000FF
                self.data[a + 2] = zero_fill_right_shift(p, 16) & 0x000000FF
                self.data[a + 3] = zero_fill_right_shift(p, 24) & 0x000000FF

                k += 1
                if k == 446:
                    k = 0

                a += 4

    def encrypt(self):
        """
        Encrypt OF.
        """
        for i in range(1, 10):
            k = 0
            a = self.of_block[i]
            while True:
                if a + 4 > self.of_block[i] + self.of_block_size[i]:
                    break

                p = bytes_to_int(self.data, a)
                c = self.of_key[k] + ((p ^ 0x7ab3684c) - 0x7ab3684c)

                self.data[a] = c & 0x000000FF
                self.data[a + 1] = zero_fill_right_shift(c, 8) & 0x000000FF
                self.data[a + 2] = zero_fill_right_shift(c, 16) & 0x000000FF
                self.data[a + 3] = zero_fill_right_shift(c, 24) & 0x000000FF

                k += 1
                if k == 446:
                    k = 0

                a += 4

    def checksums(self):
        """
        Set checksums.
        """
        for i in range(0, len(self.of_block)):
            checksum = 0

            for a in range(
                self.of_block[i], self.of_block[i] + self.of_block_size[i], 4
            ):
                checksum += bytes_to_int(self.data, a)

            self.data[self.of_block[i] - 8] = checksum & 0x000000FF
            self.data[self.of_block[i] - 7] = (
                zero_fill_right_shift(checksum, 8) & 0x000000FF
            )
            self.data[self.of_block[i] - 6] = (
                zero_fill_right_shift(checksum, 16) & 0x000000FF
            )
            self.data[self.of_block[i] - 5] = (
                zero_fill_right_shift(checksum, 24) & 0x000000FF
            )

    def set_clubs(self):
        """
        Load all clubs from OF data and add to clubs list.
        """
        self.clubs = []
        for i in range(Club.total):
            club = Club(self, i)
            self.clubs.append(club)


class GameType(Enum):
    ps2_pes = auto()