import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.models.model import Model
from src.presenters.main_presenter import MainPresenter
from src.views.main_view import MainView

if __name__ == "__main__":
    logging.basicConfig(
        filename=r"D:\Coding\BlbniCheck\logs\debug.log",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
        filemode="w+",
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
