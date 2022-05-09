
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class BruteForceAttack(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Brute Force'

    @classmethod
    def execute_attack(cls):
        pass
