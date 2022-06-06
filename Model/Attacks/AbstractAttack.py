
from abc import ABC, abstractmethod

class AbstractAttack(ABC):
    TIMEOUT = 40
    HANDSHAKE_REQUIRED = False
    
    @classmethod
    @abstractmethod
    def attack_name(cls) -> str:
        pass
    
    @classmethod
    @abstractmethod
    def execute_attack(cls, target=None) -> bool:
        pass

class AttackResultInfo():

    def __init__(self, risk=None, desc=None, attack=None):
        self.__risk = risk
        self.__desc = desc 
        self.attack = attack
    
    
    @property
    def risk(self) -> str:
        return self.__risk

    @risk.setter
    def risk(self, risk: str) -> None:
        self.__risk = risk

    @property
    def desc(self) -> str:
        return self.__desc

    @desc.setter
    def desc(self, desc: str) -> None:
        self.__desc = desc
