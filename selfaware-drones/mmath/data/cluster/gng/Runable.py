import abc


class Runable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self) -> None:
        pass
