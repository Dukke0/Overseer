
from abc import ABC, abstractmethod

class AbstractAttack(ABC):

    @abstractmethod
    @classmethod
    def attack_name(cls) -> str:
        pass

    @abstractmethod
    @classmethod
    def execute_attack(cls):
        pass