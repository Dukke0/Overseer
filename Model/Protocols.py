
from abc import ABC, abstractmethod
from Model.Attacks.EvilTwin import EvilTwin
from Model.Attacks.PassCrack import BruteForceAttack, DictionaryAttack
from Model.Attacks.DeauthAttack import DeauthAttack, DeauthAttackPassive
from Model.Attacks.WepAttack import WEPAllInAttack
from Model.Attacks.WpsAttacks import PixieDustAttack, WPSBruteForceAttack

# TODO change abstract protocol 
class AbstractProtocol(ABC):
    
    __attacks_list = list()

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

class WEP(AbstractProtocol):
    __attacks_list = [DeauthAttack, DeauthAttackPassive, WEPAllInAttack, EvilTwin]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

    @classmethod
    def __str__(cls) -> str:
        return "WEP"

class WPA(AbstractProtocol):

    __attacks_list = [DeauthAttack, DeauthAttackPassive, DictionaryAttack, 
                      WPSBruteForceAttack, PixieDustAttack, EvilTwin]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

    @classmethod
    def __str__(cls) -> str:
        return "WPA"

class OPEN(AbstractProtocol):

    __attacks_list = [EvilTwin]

    @classmethod
    def attacks_list(cls) -> list:
        return cls.__attacks_list

    @classmethod
    def __str__(cls) -> str:
        return "OPN"

