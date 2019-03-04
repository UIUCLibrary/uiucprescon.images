from uiucprescon import images


def test_image_formats_loaded():
    assert "Digital Library JPEG 2000" in images.image_formats
    assert "HathiTrust JPEG 2000" in images.image_formats
