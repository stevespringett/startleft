import abc

from otm.otm.entity.otm import Otm


class ProviderParser(metaclass=abc.ABCMeta):
    """
    Formal Interface to parse from an external format to a OTM (Open Threat Model)
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'build_otm') and callable(subclass.build_otm)
                or
                NotImplemented)

    @abc.abstractmethod
    def build_otm(self) -> Otm:
        """Build a OTM from provider source data and mapping data"""
        raise NotImplementedError
