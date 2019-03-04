from typing import Union
from . import formats

import inspect

image_formats = dict()


def load_image_formats():
    for _, subclass in \
            inspect.getmembers(
                formats,
                lambda m: inspect.isclass(m) and not inspect.isabstract(m)):

        if not issubclass(subclass, formats.AbsImageConvert):
            continue

        image_formats[subclass.name] = subclass()


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
        converter = image_formats[output_format]

    converter.source_file = source
    converter.destination_file = output_file
    converter.convert()


load_image_formats()
