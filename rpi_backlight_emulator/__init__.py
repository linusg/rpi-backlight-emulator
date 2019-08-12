import atexit
import os
import signal
import sys
import time
from functools import partial
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Callable

from rpi_backlight import Backlight
from rpi_backlight.utils import FakeBacklightSysfs
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEvent,
    FileModifiedEvent,
    FileDeletedEvent,
    FileSystemEventHandler,
)
from PySide2.QtCore import Qt, QPoint, QRect, QThread, QTimer, Signal
from PySide2.QtGui import QIcon, QImage, QPainter, QPixmap
from PySide2.QtWidgets import (
    QApplication,
    QBoxLayout,
    QCheckBox,
    QDesktopWidget,
    QLabel,
    QMainWindow,
    QSlider,
    QWidget,
)

__author__ = "Linus Groh"
__version__ = "1.2.0"

CURRENT_DIR = Path(__file__).parent
TMP_DIR = Path(gettempdir())
PID_TMP_FILE = TMP_DIR / "rpi-backlight-emulator.pid"
SYSFS_TMP_FILE = TMP_DIR / "rpi-backlight-emulator.sysfs"


def create_tmp_files(backlight_sysfs_path: Path) -> None:
    if PID_TMP_FILE.exists():
        print("PID file {0} exists, aborting".format(PID_TMP_FILE))
        sys.exit()
    PID_TMP_FILE.write_text(str(os.getpid()))
    SYSFS_TMP_FILE.write_text(str(backlight_sysfs_path))
    atexit.register(remove_tmp_files)


def remove_tmp_files() -> None:
    if PID_TMP_FILE.exists():
        PID_TMP_FILE.unlink()
    if SYSFS_TMP_FILE.exists():
        SYSFS_TMP_FILE.unlink()


def get_image_path(filename: str) -> str:
    return str((CURRENT_DIR / "images" / filename).resolve())


def load_display_image(path: str) -> QPixmap:
    image = QPixmap(path)
    return image.scaled(
        image.size().width(),
        image.size().height() * 0.94,
        Qt.AspectRatioMode.IgnoreAspectRatio,
        Qt.SmoothTransformation,
    )


def get_screenshot() -> QPixmap:
    app = QApplication.instance()
    screen = app.screens()[0]
    desḱtop_window = QDesktopWidget().winId()
    return screen.grabWindow(desḱtop_window)


class FileChangeEventHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[FileSystemEvent], None]) -> None:
        self.callback = callback

    def on_any_event(self, event: FileSystemEvent) -> None:
        self.callback(event)


class FileWatcherThread(QThread):
    file_changed = Signal(str)

    def __init__(self, parent: Any, sysfs_directory: Path) -> None:
        super(FileWatcherThread, self).__init__(parent)
        self.sysfs_directory = sysfs_directory
        self.observer = Observer()
        self.running = False

    def interrupt(self) -> None:
        self.observer.stop()
        self.observer.join()
        self.running = False

    def run(self) -> None:
        self.running = True
        self.observer.schedule(
            FileChangeEventHandler(callback=self.handle_file_change),
            str(self.sysfs_directory),
        )
        self.observer.start()

        while self.running:
            time.sleep(1)

    def handle_file_change(self, event: FileSystemEvent) -> None:
        filename = Path(event.src_path).stem
        if filename not in ("bl_power", "brightness"):
            return
        if isinstance(event, FileDeletedEvent):
            print("WARNING: file {0} has been deleted!".format(filename))
            return
        if isinstance(event, FileModifiedEvent):
            self.file_changed.emit(filename)


class MainWindow(QMainWindow):
    def __init__(self, backlight_sysfs_path: Path) -> None:
        QMainWindow.__init__(self)

        self.backlight = Backlight(backlight_sysfs_path)

        self.screenshot = QPixmap(get_image_path("raspbian.png"))
        self.image_display_on = load_display_image(get_image_path("display_on.png"))
        self.image_display_off = load_display_image(get_image_path("display_off.png"))

        widget = QWidget()
        checkbox_layout = QBoxLayout(QBoxLayout.LeftToRight)
        main_layout = QBoxLayout(QBoxLayout.TopToBottom)
        brightness_slider_label = QLabel("Brightness", widget)
        self.live_screen_checkbox = QCheckBox("Show live screen", widget)
        self.live_screen_checkbox.stateChanged.connect(self.update_screen)
        self.power_checkbox = QCheckBox("Power", widget)
        self.power_checkbox.stateChanged.connect(self.write_power_change)
        self.brightness_slider = QSlider(Qt.Horizontal, widget)
        self.brightness_slider.valueChanged.connect(self.write_brightness_change)
        self.brightness_slider.setSingleStep(1)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.screen_image = QLabel()
        checkbox_layout.addWidget(self.power_checkbox)
        checkbox_layout.addWidget(self.live_screen_checkbox)
        main_layout.addLayout(checkbox_layout)
        main_layout.addWidget(brightness_slider_label)
        main_layout.addWidget(self.brightness_slider)
        main_layout.addWidget(self.screen_image)
        widget.setLayout(main_layout)

        self.thread = FileWatcherThread(self, backlight_sysfs_path)
        self.thread.file_changed.connect(self.update_widgets)
        self.thread.start()

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start()

        self.update_widgets("bl_power")
        self.update_widgets("brightness")

        self.setCentralWidget(widget)
        self.setWindowTitle('Raspberry Pi 7" display backlight emulator')
        self.setWindowIcon(QIcon(get_image_path("icon.png")))

    def write_power_change(self):
        on = self.power_checkbox.checkState() == Qt.CheckState.Checked
        self.backlight.power = on

    def write_brightness_change(self):
        value = self.brightness_slider.value()
        self.backlight.brightness = value

    def update_widgets(self, filename: str) -> None:
        if filename == "bl_power":
            self.power_checkbox.setChecked(self.backlight.power)

        if filename == "brightness":
            self.brightness_slider.setValue(self.backlight.brightness)

    def update_screen(self) -> None:
        use_live_screen = (
            self.live_screen_checkbox.checkState() == Qt.CheckState.Checked
        )
        is_powered_on = self.power_checkbox.checkState() == Qt.CheckState.Checked
        image_display = (
            self.image_display_on if is_powered_on else self.image_display_off
        )
        result = QPixmap(image_display.size())
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.drawPixmap(QPoint(0, 0), image_display)

        if is_powered_on:
            screenshot = get_screenshot() if use_live_screen else self.screenshot
            screenshot = screenshot.scaled(
                800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            screenshot = screenshot.copy(QRect(0, 0, 800, 480 * 0.94))
            offset_x = (image_display.size().width() - screenshot.size().width()) / 2
            offset_y = (image_display.size().height() - screenshot.size().height()) / 2
            painter.setOpacity(self.backlight.brightness / 100)
            painter.drawPixmap(QPoint(offset_x, offset_y), screenshot)

        painter.end()
        result = result.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.screen_image.setPixmap(result)

    def closeEvent(self, event) -> None:
        self.thread.interrupt()
        self.thread.quit()
        self.thread.wait()
        self.timer.stop()
        super(MainWindow, self).closeEvent(event)


def main() -> None:
    with FakeBacklightSysfs() as fake_backlight_sysfs:
        create_tmp_files(backlight_sysfs_path=fake_backlight_sysfs.path)
        app = QApplication(sys.argv)
        window = MainWindow(fake_backlight_sysfs.path)
        window.show()
        signal.signal(signal.SIGINT, lambda *_: window.close())
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
