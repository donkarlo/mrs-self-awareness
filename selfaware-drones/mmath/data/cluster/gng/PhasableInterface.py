import abc
class PhasableInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _runPhases(self):
        pass