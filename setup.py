import ast
import re
from pathlib import Path
from setuptools import setup

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    readme = CURRENT_DIR / "README.md"
    return readme.read_text()


def get_version() -> str:
    rpi_backlight_emulator_py = CURRENT_DIR / "rpi_backlight_emulator" / "__init__.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    match = _version_re.search(rpi_backlight_emulator_py.read_text())
    version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="rpi-backlight-emulator",
    version=get_version(),
    description='Raspberry Pi 7" LCD emulator for rpi-backlight',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Linus Groh",
    license="MIT",
    author_email="mail@linusgroh.de",
    url="https://github.com/linusg/rpi-backlight-emulator",
    download_url="https://pypi.org/project/rpi-backlight-emulator",
    keywords=[
        "raspberry pi",
        "display",
        "touchscreen",
        "brightness",
        "backlight",
        "emulator",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System",
        "Topic :: System :: Emulators",
        "Topic :: System :: Hardware",
        "Topic :: Multimedia",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    packages=["rpi_backlight_emulator"],
    install_requires=["watchdog", "PySide2", "rpi-backlight>=2.0.0"],
    entry_points={
        "console_scripts": ["rpi-backlight-emulator = rpi_backlight_emulator:main"]
    },
)
