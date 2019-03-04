from uiucprescon import imageprocess


def test_image_formats_loaded():
    assert "Digital Library JPEG 2000" in imageprocess.image_formats
    assert "HathiTrust JPEG 2000" in imageprocess.image_formats
