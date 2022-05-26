
from Model.Attacks.AbstractAttack import AbstractAttack


class PmkidAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'PMKID'

    @classmethod
    def execute_attack(cls, target=None) -> bool:
        pass