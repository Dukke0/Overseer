
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.utils import target_dump
import subprocess as sb

class BruteForceAttack(AbstractAttack):

    def __init__(self):
        super().__init__()

    def attack_name() -> str:
        return 'Brute Force'

    def execute_attack():
        pass
