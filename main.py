import ctypes
import logging
import os
import sys
import traceback
from datetime import datetime
from types import TracebackType

from PyQt6.QtWidgets import QApplication

from src.models.model import Model
from src.presenters.main_presenter import MainPresenter
from src.views.main_view import MainView


def handle_uncaught_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType,
) -> None:
    # Ignore KeyboardInterrupt (special case)
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    stack_summary = traceback.extract_tb(exc_traceback)
    filename, line, _, _ = stack_summary.pop()
    exc_details_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    exc_details = "".join(exc_details_list)
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)

    text = f"""<html>The following unexpected error has occured:<br/>
        <b>{error}</b><br/><br/>
        It occurred at <b>line {line}</b> of file <b>{filename}</b>.<br/><br/>
        The program will Quit (without saving) after closing this window.</html>"""

    logging.critical(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )

    main_view.display_error(text=text, exc_details=exc_details, critical=True)

    app.exit()


if __name__ == "__main__":

    # The following three lines are needed to make sure task bar icon works on Windows
    if os.name == "nt":
        myappid = "Jakub_Franek.Blbnicheck.v0.1"  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    sys.excepthook = handle_uncaught_exception

    dir_current = os.path.dirname(os.path.realpath(__file__))

    dir_logs = dir_current + r"\logs"
    if not os.path.exists(dir_logs):
        os.makedirs(dir_logs)

    start_dt = datetime.now()
    logging.basicConfig(
        filename=dir_logs
        + r"\debug_"
        + start_dt.strftime("%Y_%m_%d_%Hh%Mm%Ss")
        + ".log",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="""%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s""",
        filemode="w+",
        encoding="utf-8",
    )

    logging.info("Creating QApplication")
    app = QApplication(sys.argv)

    logging.info("Creating MainWindow")
    main_view = MainView()

    logging.info("Creating Model")
    model = Model()

    logging.info("Creating Presenter")
    presenter = MainPresenter(main_view, model)

    """ device_pixel_ratio = app.primaryScreen().devicePixelRatio()
    logical_dpi = app.primaryScreen().logicalDotsPerInchY()
    logging.info(f"{device_pixel_ratio=}")
    logging.info(f"{logical_dpi=}")

    if device_pixel_ratio >= 1.5:
        font = app.font()
        font.setPointSize(8)
        app.setFont(font)
        logging.info("Set QApplication font size to 8")
    else:
        font = app.font()
        font.setPointSize(10)
        app.setFont(font)
        logging.info("Set QApplication font size to 10 ")
    """
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    logging.info("Set QApplication font size to 10 ")

    logging.info("Executing QApplication")
    app.exec()
