
from Model.Attacks.AbstractAttack import AbstractAttack


class EvilTwin(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Evil twin'

    @classmethod
    def execute_attack(cls, target=None) -> bool:
        pass