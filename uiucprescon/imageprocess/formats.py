import abc

import pykdu_compress

class AbsImageConvert(metaclass=abc.ABCMeta):

    def __init__(self, source_file=None, destination_file=None):
        self._source_file = source_file
        self._destination_file = destination_file


    @property
    def source_file(self):
        return self._source_file

    @source_file.setter
    def source_file(self, value):
        self._source_file = value

    @property
    def destination_file(self):
        return self._destination_file

    @destination_file.setter
    def destination_file(self, value):
        self._destination_file = value

    @abc.abstractmethod
    def convert(self):
        pass


class HathiJp2(AbsImageConvert):
    def convert(self):

        kakadu_args = ["Clevels=5",
                         "Clayers=8","Corder=RLCP",
                         "Cuse_sop=yes",
                         "Cuse_eph=yes",
                         "Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK",
                         "-no_weights",
                         "-slope",
                         "42988",
                         "-jp2_space",
                         "sRGB"]
        pykdu_compress.kdu_compress_cli2(self.source_file, self.destination_file, kakadu_args)

        print("convertin")
