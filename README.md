# Raspberry Pi 7" LCD emulator for `rpi-backlight`

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](ttps://github.com/linusg/rpi-backlight-emulator/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/rpi-backlight-emulator.svg)](https://pypi.org/project/rpi-backlight-emulator/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/linusg/rpi-backlight-emulator.svg)](https://github.com/linusg/rpi-backlight-emulator/issues)

![Demo](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/demo.gif)

## Requirements

Python 3.5+ is required, all necessary packages will be installed automatically (see below).

`rpi-backlight-emulator` uses the `rpi-backlight` v2 API.

## Installation

```
$ pip3 install rpi-backlight-emulator
```

## Usage

Run:

```
$ rpi-backlight-emulator
```

Next, open a Python shell and create a `rpi_backlight.Backlight` instance using the emulator:

```python
>>> from rpi_backlight import Backlight
>>> backlight = Backlight(":emulator:")
>>>
```

Now, continue like you're connected to a real display!

You can make changes to the display using the emulator, they'll be reflected in the Python-API and vice versa.

Enable `Show live screen` to replace the static Raspbian Buster screenshot with a live preview of your monitor.

## Screenshots

![Display off](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_display_off.png)
![Display on](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_display_on.png)
![Brightness low](https://raw.githubusercontent.com/linusg/rpi-backlight-emulator/master/docs/screenshot_brightness_low.png)