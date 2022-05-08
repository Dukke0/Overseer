
from abc import ABC, abstractmethod
from Model.Attacks.BruteForceAttack import BruteForceAttack
from Model.Attacks.DeauthAttack import DeauthAttack

# TODO change abstract protocol 
class AbstractProtocol(ABC):
    
    __attacks_list = list()

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class WEP(AbstractProtocol):
    
    __attacks_list = list()

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class WPA(AbstractProtocol):

    __attacks_list = [DeauthAttack, BruteForceAttack]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list
