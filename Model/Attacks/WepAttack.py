from Model.Attacks.AbstractAttack import AbstractAttack


class WEPAllInAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'WEP All-in'

    @classmethod
    def execute_attack(cls, **kwargs):
        pass