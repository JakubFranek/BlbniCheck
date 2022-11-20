import logging
import os
import sys
import traceback
from datetime import datetime

from PyQt6.QtWidgets import QApplication

from src.models.model import Model
from src.presenters.main_presenter import MainPresenter
from src.views.main_view import MainView


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        if app:
            app.quit()
        return

    stack_summary = traceback.extract_tb(exc_traceback)
    filename, line, dummy, dummy = stack_summary.pop()
    exc_details = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)

    text = f"""<html>The following error has occured:<br/>
        <b>{error}</b><br/><br/>
        It occurred at <b>line {line}</b> of file <b>{filename}</b>.<br/></html>"""

    main_view.display_error(text=text, exc_details=exc_details)


if __name__ == "__main__":

    sys.excepthook = handle_exception

    start_dt = datetime.now()

    logging.basicConfig(
        filename=r"D:\Coding\BlbniCheck\logs\debug_"
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

    logging.info("Executing QApplication")
    app.exec()
