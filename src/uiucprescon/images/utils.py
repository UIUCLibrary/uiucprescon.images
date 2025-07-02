"""Utilities module."""

import inspect
from . import formats
image_formats = dict()  #:


def load_image_formats() -> None:
    """Load image formats supported in the module variable image_formats."""
    for _, subclass in \
            inspect.getmembers(
                formats,
                lambda m: inspect.isclass(m) and not inspect.isabstract(m)):

        if not issubclass(subclass, formats.AbsImageConvert):
            continue

        image_formats[subclass.name] = subclass()


load_image_formats()
