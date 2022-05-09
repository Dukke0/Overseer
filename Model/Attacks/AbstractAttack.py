
from abc import ABC, abstractmethod

class AbstractAttack(ABC):

    @classmethod
    @abstractmethod
    def attack_name(cls) -> str:
        pass
    
    @classmethod
    @abstractmethod
    def execute_attack(cls, target=None) -> bool:
        pass