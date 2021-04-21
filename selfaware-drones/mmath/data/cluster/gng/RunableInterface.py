import abc


class RunableInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self) -> None:
        pass
