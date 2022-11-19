import json
import logging
import traceback

from src.models.model import Model
from src.views.main_view import MainView


class MainPresenter:
    def __init__(self, main_view: MainView, model: Model) -> None:
        self.main_view = main_view
        self.model = model

        self.main_view.show()
