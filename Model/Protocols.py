
from abc import ABC, abstractmethod
from Model.Attacks.PassCrack import BruteForceAttack, DictionaryAttack
from Model.Attacks.DeauthAttack import DeauthAttack
from Model.Attacks.WepAttack import WEPAllInAttack
from Model.Attacks.WpsAttacks import PixieDustAttack, WPSBruteForceAttack

# TODO change abstract protocol 
class AbstractProtocol(ABC):
    
    __attacks_list = list()

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class WEP(AbstractProtocol):
    __attacks_list = [WEPAllInAttack]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class WPA(AbstractProtocol):

    __attacks_list = [DeauthAttack, BruteForceAttack, DictionaryAttack, WPSBruteForceAttack, PixieDustAttack]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class OPEN(AbstractProtocol):

    __attacks_list = list()

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

