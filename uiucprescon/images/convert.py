from typing import Union
from . import formats
from . import images


def convert_image(source: str, output_file: str,
                  output_format: Union[str, formats.AbsImageConvert]) -> None:
    """Convert image from one file format into another

    Args:
        source: Source file to convert
        output_file: File name to save new image
        output_format: Desired output format

    """

    if isinstance(output_format, formats.AbsImageConvert):
        converter = output_format
    else:
        converter = images.image_formats[output_format]

    converter.source_file = source
    converter.destination_file = output_file
    converter.convert()
