from abc import ABC, abstractmethod


class ParserABC(ABC):
    """
    Абстрактный класс для парсинга HH
    """

    @abstractmethod
    def get_data(self, keyword): ...

    def _parse(self, data): ...

