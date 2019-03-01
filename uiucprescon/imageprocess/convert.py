from typing import Dict, Union
from . import formats

IMAGE_FORMATS = {
    "hathijp2": formats.HathiJp2()
}


def convert_image(source: str, output_file: str,
                  output_format: Union[str, Dict[str, str]]) -> None:
    """Convert image from one file format into another

    Args:
        source: Source file to convert
        output_file: File name to save new image
        output_format: Desired output format

    """


    if isinstance(output_format, formats.AbsImageConvert):
        converter = output_format
    else:
        converter = IMAGE_FORMATS[output_format]

    converter.source_file = source
    converter.destination_file = output_file
    converter.convert()

