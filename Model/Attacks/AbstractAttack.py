
from abc import ABC, abstractmethod

class AbstractAttack(ABC):

    def __init__(self, target):
        self.target = target

    @abstractmethod
    def attack_name() -> str:
        pass

    @abstractmethod
    def execute_attack():
        pass