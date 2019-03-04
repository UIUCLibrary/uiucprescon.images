import abc

import pykdu_compress  # type: ignore
from typing import Optional


class AbsImageConvert(metaclass=abc.ABCMeta):

    def __init__(self, source_file=None, destination_file=None):
        self._source_file = source_file
        self._destination_file = destination_file

    # name: str = None
    descriptions: Optional[str] = None

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

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.name is None:
            raise TypeError(
                "Can't instantiate abstract class {} with "
                "abstract property name".format(cls.__name__))

    @classmethod
    @property
    def name(cls):
        raise NotImplementedError


class HathiJP2(AbsImageConvert):
    """HathiTrust compatible JPEG2000 files"""

    name = "HathiTrust JPEG 2000"

    def convert(self):

        kakadu_args = ["Clevels=5",
                       "Clayers=8",
                       "Corder=RLCP",
                       "Cuse_sop=yes",
                       "Cuse_eph=yes",
                       "Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK",
                       "-no_weights",
                       "-slope",
                       "42988",
                       "-jp2_space",
                       "sRGB"]
        pykdu_compress.kdu_compress_cli2(self.source_file,
                                         self.destination_file,
                                         kakadu_args)


class DigitalLibraryJP2(AbsImageConvert):
    name = "Digital Library JPEG 2000"

    def convert(self):
        pykdu_compress.kdu_compress_cli2(
            self.source_file, self.destination_file)
