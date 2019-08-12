# Raspberry Pi 7" LCD emulator for [`rpi-backlight`](https://github.com/linusg/rpi-backlight)

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](ttps://github.com/linusg/rpi-backlight-emulator/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/rpi-backlight-emulator.svg)](https://pypi.org/project/rpi-backlight-emulator/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/linusg/rpi-backlight-emulator.svg)](https://github.com/linusg/rpi-backlight-emulator/issues)

![Demo](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/demo.gif)

This is an emulator for the Raspberry Pi 7" LCD to test and develop
[`rpi-backlight`](https://github.com/linusg/rpi-backlight) without having a physical
display connected or even running on the Pi.

## Requirements

Python 3.5+ is required, along with the packages [`PySide2`](https://pypi.org/project/PySide2),
[`watchdog`](https://pypi.org/project/watchdog) and
[`rpi-backlight>=2.0.0`](https://pypi.org/project/rpi-backlight)
(see below).

## Installation

PySide2 wheels for x86/x64 are available on PyPI, so you can simply run:

```
$ pip3 install rpi-backlight-emulator
```

On ARM (e.g. Raspberry Pi) it's more complicated (and only the new Debian/Raspbian Buster
will work, Stretch won't - you'd have to install PySide2 from source):

```
$ sudo apt install python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets
$ pip3 install watchdog rpi-backlight>=2.0.0
$ pip3 install --no-deps rpi-backlight-emulator
```

## Usage

Run:

```
$ rpi-backlight-emulator
```

_Note: on Windows,_
_[you'll need administrator privileges to create symbolic links](https://superuser.com/q/10727/581296),_
_which this program does - so you'll have to execute the above as administrator._

Next, open a Python shell and create a `rpi_backlight.Backlight` instance using the
emulator:

```python
>>> from rpi_backlight import Backlight
>>> backlight = Backlight(":emulator:")
>>>
```

Now, continue like you're connected to a real display!

You can make changes to the display using the emulator, they'll be reflected in the
Python-API and vice versa.

Enable `Show live screen` to replace the static Raspbian Buster screenshot with a live
preview of your monitor.

## Screenshots

![Display off](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_display_off.png)
![Display on](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_display_on.png)
![Brightness low](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_brightness_low.png)

## License

The source code and all other files in this repository are licensed under the MIT
license, so you can easily use it in your own projects. See [`LICENSE`](LICENSE) for
more information.
