from setuptools import setup

setup(
    packages=['uiucprescon.images'],
    namespace_packages=["uiucprescon"],
    install_requires=["pykdu_compress>=0.1.3b4"],
    setup_requires=['pytest-runner'],
    test_suite="tests",
    tests_require=[
        'pytest',
    ],
    package_data={"uiucprescon.images": ["py.typed"]},
    zip_safe=False,
)
