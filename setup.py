from setuptools import setup

setup(
    packages=['uiucprescon.imageprocess'],
    namespace_packages=["uiucprescon"],
    install_requires=["pykdu_compress"],
    setup_requires=['pytest-runner'],
    zip_safe=False,
)
